#!/usr/bin/env python3
"""Generic apply step for the parallel-translation workflow.

Merges per-batch implementer outputs into translations/strings.json. Batch
letters and expected total are DISCOVERED, not hardcoded:
  - letters  : from <task-dir>/outputs/batch-*-output.json
  - expected : sum of entry counts in <task-dir>/candidates/manifest.json
               (falls back to summing candidates/batch-*.json if no manifest)

Action taxonomy (per output row):
  - translate                -> target=<中文>
  - flag_<sub>               -> target=null, sub in VALID_SUBFLAGS
  - bilingual_search_terms   -> target="<source> <中文>", flag search_terms_bilingual

Writes <task-dir>/outputs/apply_summary.json with before/after counts, deltas,
and per-action breakdown — consumed by the check step so it needs no hardcoded
absolute numbers.

Usage:
  python3 apply_batch.py --task-dir <dir> --batch-flag pr-by-file-parallel-batch-21
                         [--strings <path>]

Idempotent: rerunning on already-translated rows is a no-op.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
REPO_ROOT = KIT_DIR.parents[2]
DEFAULT_STRINGS = REPO_ROOT / "translations" / "strings.json"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

BRAND_LITERALS = [
    "Warp Drive", "Warp", "Oz", "MCP", "Agent", "PTY", "REPL", "GitHub",
    "Slack", "Stripe", "Firebase", "Fireworks", "AWS", "OAuth", "JWT",
    "Linux", "Profile", "OpenAI", "Anthropic", "HPKE", "Node.js", "tmux",
    "GraphQL",
]
VALID_SUBFLAGS = {
    "panic_message", "telemetry_payload", "extractor_false_positive_doc_comment",
    "test_fixture", "wgpu_debug_label", "protocol_key",
}


def placeholders(s: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(s))


def strftime_codes(s: str) -> list[str]:
    return sorted(STRFTIME_RE.findall(s))


def check_translate_invariants(src: str, tgt: str) -> list[str]:
    problems: list[str] = []
    if placeholders(src) != placeholders(tgt):
        problems.append(f"placeholders differ: {placeholders(src)} vs {placeholders(tgt)}")
    if strftime_codes(src) != strftime_codes(tgt):
        problems.append(f"strftime differs: {strftime_codes(src)} vs {strftime_codes(tgt)}")
    if src.startswith(" ") != tgt.startswith(" "):
        problems.append("leading whitespace mismatch")
    if src.endswith(" ") != tgt.endswith(" "):
        problems.append("trailing whitespace mismatch")
    if src.startswith("\n") != tgt.startswith("\n"):
        problems.append("leading newline mismatch")
    if src.endswith("\n") != tgt.endswith("\n"):
        problems.append("trailing newline mismatch")
    if src.count("\n") != tgt.count("\n"):
        problems.append(f"newline count differs: {src.count(chr(10))} vs {tgt.count(chr(10))}")
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")
    if "..." in tgt:
        problems.append("ASCII '...' still in target (should be '……')")
    return problems


def check_bilingual_invariants(src: str, tgt: str) -> list[str]:
    problems: list[str] = []
    if not tgt.startswith(src + " "):
        problems.append("bilingual target does not start with '<source> '")
        return problems
    # Only the appended Chinese keywords must be punctuation-free; the source
    # prefix may legitimately carry punctuation (e.g. search_terms "a.i.").
    appended = tgt[len(src) + 1:]
    bad = [c for c in appended if c in ",.，。；;！!？?"]
    if bad:
        problems.append(f"bilingual appended keywords contain punctuation: {set(bad)}")
    return problems


def discover_letters(outputs_dir: Path) -> list[str]:
    letters = []
    for p in sorted(outputs_dir.glob("batch-*-output.json")):
        # batch-A-output.json -> A
        letters.append(p.name[len("batch-"):-len("-output.json")])
    if not letters:
        raise SystemExit(f"no batch-*-output.json found in {outputs_dir}")
    return letters


def expected_total(task_dir: Path) -> int:
    manifest = task_dir / "candidates" / "manifest.json"
    if manifest.exists():
        return json.loads(manifest.read_text())["total"]
    total = 0
    for p in sorted((task_dir / "candidates").glob("batch-*.json")):
        if p.name == "manifest.json":
            continue
        total += len(json.loads(p.read_text()))
    return total


def load_outputs(outputs_dir: Path, letters: list[str]):
    translations: dict[str, str | None] = {}
    subflags: dict[str, list[str]] = {}
    bilingual_ids: set[str] = set()
    per_batch: dict[str, dict] = {}
    seen: set[str] = set()
    for letter in letters:
        out = json.loads((outputs_dir / f"batch-{letter}-output.json").read_text())
        ids = list(out["translations"].keys())
        clash = set(ids) & seen
        if clash:
            raise SystemExit(f"batch-{letter}: duplicate ids across batches: {clash}")
        seen.update(ids)
        translations.update(out["translations"])
        for k, v in out["do_not_translate_subflags"].items():
            if not v or len(v) != 1 or v[0] not in VALID_SUBFLAGS:
                raise SystemExit(f"batch-{letter}: invalid sub-flag for {k}: {v}")
            subflags[k] = list(v)
        bilingual_ids.update(out["bilingual_search_terms_ids"])
        null_ct = sum(1 for x in out["translations"].values() if x is None)
        per_batch[letter] = {
            "total": len(ids), "null": null_ct, "translated": len(ids) - null_ct,
            "flagged": len(out["do_not_translate_subflags"]),
            "bilingual": len(out["bilingual_search_terms_ids"]),
        }
    null_ids = {k for k, v in translations.items() if v is None}
    if null_ids != set(subflags.keys()):
        raise SystemExit(
            f"null_ids vs subflag_ids mismatch: "
            f"only_null={null_ids - set(subflags)}, only_flag={set(subflags) - null_ids}"
        )
    for bid in bilingual_ids:
        if translations.get(bid) is None:
            raise SystemExit(f"bilingual id {bid} has null target")
        if bid in subflags:
            raise SystemExit(f"bilingual id {bid} also in subflags")
    return translations, subflags, bilingual_ids, per_batch


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-dir", required=True)
    ap.add_argument("--batch-flag", required=True)
    ap.add_argument("--strings", default=str(DEFAULT_STRINGS))
    args = ap.parse_args()

    task_dir = Path(args.task_dir).resolve()
    strings_path = Path(args.strings).resolve()
    outputs_dir = task_dir / "outputs"
    batch_flag = args.batch_flag

    letters = discover_letters(outputs_dir)
    exp_total = expected_total(task_dir)
    translations, subflags, bilingual_ids, per_batch = load_outputs(outputs_dir, letters)

    if len(translations) != exp_total:
        raise SystemExit(f"expected {exp_total} merged entries, got {len(translations)}")

    print(f"batch-flag: {batch_flag}")
    print(f"Loaded {len(translations)} entries from {len(letters)} sub-batches ({','.join(letters)}):")
    for letter, ct in per_batch.items():
        print(f"  batch-{letter}: {ct}")

    data = json.loads(strings_path.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}
    missing = [eid for eid in translations if eid not in by_id]
    if missing:
        print(f"missing ids in strings.json: {missing}", file=sys.stderr)
        return 1

    pre = Counter(e["status"] for e in entries)
    pre_snapshot = {
        e["id"]: (e.get("target"), e["status"])
        for e in entries if e["status"] == "translated"
    }

    errors: list[str] = []
    applied = already = 0
    by_action: Counter = Counter()

    for eid, tgt in translations.items():
        entry = by_id[eid]
        is_flagged = eid in subflags
        is_bilingual = eid in bilingual_ids
        action = (f"flag_{subflags[eid][0]}" if is_flagged
                  else "bilingual_search_terms" if is_bilingual else "translate")

        if entry["status"] == "translated" and entry.get("target") == tgt:
            already += 1
            flags = entry.get("flags") or []
            needed = [batch_flag]
            if is_flagged:
                needed += ["do_not_translate"] + subflags[eid]
            elif is_bilingual:
                needed += ["search_terms_bilingual"]
            changed = False
            for f in needed:
                if f not in flags:
                    flags.append(f); changed = True
            if changed:
                entry["flags"] = flags; entry["updated_at"] = NOW
            continue

        if entry["status"] != "new":
            errors.append(f"{eid}: status not 'new' (got {entry['status']!r})")
            continue

        src = entry["source"]
        if is_flagged:
            if tgt is not None:
                errors.append(f"{eid}: flagged entry must have null target, got {tgt!r}")
                continue
            entry["target"] = None
            entry["status"] = "translated"
            flags = entry.get("flags") or []
            for f in (batch_flag, "do_not_translate", *subflags[eid]):
                if f not in flags:
                    flags.append(f)
            entry["flags"] = flags; entry["updated_at"] = NOW
            applied += 1; by_action[action] += 1
            continue

        if tgt is None:
            errors.append(f"{eid}: non-flag entry has null target")
            continue

        probs = (check_bilingual_invariants(src, tgt) if is_bilingual
                 else check_translate_invariants(src, tgt))
        if probs:
            kind = "bilingual" if is_bilingual else "translate"
            errors.append(f"{eid} ({kind}): {probs}\n  src={src!r}\n  tgt={tgt!r}")
            continue

        entry["target"] = tgt
        entry["status"] = "translated"
        flags = entry.get("flags") or []
        if batch_flag not in flags:
            flags.append(batch_flag)
        if is_bilingual and "search_terms_bilingual" not in flags:
            flags.append("search_terms_bilingual")
        entry["flags"] = flags; entry["updated_at"] = NOW
        applied += 1; by_action[action] += 1

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    for eid, (prev_t, prev_s) in pre_snapshot.items():
        if eid in translations:
            continue
        e = by_id[eid]
        if e.get("target") != prev_t or e["status"] != prev_s:
            print(f"ERROR: unrelated translated entry mutated: {eid}", file=sys.stderr)
            return 1

    post = Counter(e["status"] for e in entries)
    md = data.setdefault("metadata", {})
    stats = md.setdefault("stats", {})
    for k in ("new", "translated", "fuzzy", "approved", "obsolete"):
        stats[k] = post.get(k, 0)
    md["entry_count"] = len(entries)
    md["last_changed_at"] = NOW
    strings_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    summary = {
        "batch_flag": batch_flag,
        "letters": letters,
        "expected_total": exp_total,
        "applied": applied,
        "already": already,
        "per_action": dict(by_action),
        "before": {k: pre.get(k, 0) for k in ("new", "translated", "fuzzy")},
        "after": {k: post.get(k, 0) for k in ("new", "translated", "fuzzy")},
        "delta": {k: post.get(k, 0) - pre.get(k, 0) for k in ("new", "translated", "fuzzy")},
        "batch_flag_count": sum(1 for e in entries if batch_flag in (e.get("flags") or [])),
        "entry_count": len(entries),
        "applied_at": NOW,
    }
    (outputs_dir / "apply_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print(f"\napplied={applied}  already={already}  total_input={exp_total}")
    print("per-action breakdown:")
    for k, v in sorted(by_action.items()):
        print(f"  {k}: {v}")
    print()
    for k in ("translated", "new", "fuzzy"):
        print(f"{k}: {pre.get(k,0)} -> {post.get(k,0)}  (Δ {post.get(k,0)-pre.get(k,0):+d})")
    print(f"entry_count: {len(entries)}")
    print(f"summary: {outputs_dir / 'apply_summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
