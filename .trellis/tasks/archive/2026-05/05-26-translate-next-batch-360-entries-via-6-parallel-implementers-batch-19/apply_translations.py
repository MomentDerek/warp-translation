#!/usr/bin/env python3
"""Apply batch-19 merged translations to translations/strings.json.

Batch-19 is a 6-way parallel merge spanning 380 entries (file-pinned).
Sub-batches (per prd.md):

  A: settings_view/code_page + settings/{mod,input,editor,font}                 (61)
  B: crates/ai/aws_credentials + ai/blocklist/{block/status_bar, block, ...}    (61)
  C: terminal/shared_session/* + session_settings + buy_credits_banner + ...    (61)
  D: workspace/view/{cloud_agent_capacity_modal, global_search} + onboarding +  (67)
     workflows + notebooks
  E: themes/default_themes + drive/{export,sharing} + util/external_editor +    (68)
     code/editor/find + workspaces/gql_convert
  F: crates/warp_terminal/model/mode + node_runtime + managed_secrets/hpke +    (62)
     editor/render/model/debug

Each sub-batch output supports the full action taxonomy:
  - translate  -> target=<中文>
  - flag_panic_message               -> target=null, sub=panic_message
  - flag_telemetry_payload           -> target=null, sub=telemetry_payload
  - flag_extractor_false_positive_doc_comment -> target=null, sub=extractor_false_positive_doc_comment
  - flag_test_fixture                -> target=null, sub=test_fixture
  - flag_wgpu_debug_label            -> target=null, sub=wgpu_debug_label
  - flag_protocol_key                -> target=null, sub=protocol_key
  - bilingual_search_terms           -> target=<source>+" "+<chinese>, flag=search_terms_bilingual

Invariants enforced per row (translate path):
  - placeholder set unchanged ({}, {name}, {0}, etc.)
  - strftime code set unchanged (%b, %d, %-I, etc.)
  - leading/trailing whitespace + newline shape preserved
  - brand literals preserved (Warp, Oz, MCP, ...)
  - no ASCII '...' remaining in target
Bilingual path:
  - target starts with "<source> "
  - no punctuation in keyword string
Flag path:
  - target is None

Idempotent: rerunning on an already-translated row is a no-op (no flag
duplication, no status flip).

CWD: anywhere — paths are derived from __file__.
"""

from __future__ import annotations
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STRINGS_PATH = ROOT / "translations" / "strings.json"
TASK_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = TASK_DIR / "outputs"

BATCH_FLAG = "pr-by-file-parallel-batch-19"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
BATCH_LETTERS = ["A", "B", "C", "D", "E", "F"]
EXPECTED_TOTAL = 380

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

BRAND_LITERALS = [
    "Warp Drive",
    "Warp",
    "Oz",
    "MCP",
    "Agent",
    "PTY",
    "REPL",
    "GitHub",
    "Slack",
    "Stripe",
    "Firebase",
    "Fireworks",
    "AWS",
    "OAuth",
    "JWT",
    "Linux",
    "Profile",
    "OpenAI",
    "Anthropic",
    "HPKE",
    "Node.js",
    "tmux",
    "GraphQL",
]

VALID_SUBFLAGS = {
    "panic_message",
    "telemetry_payload",
    "extractor_false_positive_doc_comment",
    "test_fixture",
    "wgpu_debug_label",
    "protocol_key",
}


def placeholders(s: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(s))


def strftime_codes(s: str) -> list[str]:
    return sorted(STRFTIME_RE.findall(s))


def check_translate_invariants(src: str, tgt: str, eid: str) -> list[str]:
    problems: list[str] = []
    src_ph = placeholders(src)
    tgt_ph = placeholders(tgt)
    if src_ph != tgt_ph:
        problems.append(f"placeholders differ: src={src_ph} vs tgt={tgt_ph}")

    src_strf = strftime_codes(src)
    tgt_strf = strftime_codes(tgt)
    if src_strf != tgt_strf:
        problems.append(f"strftime differs: src={src_strf} vs tgt={tgt_strf}")

    if src.startswith(" ") != tgt.startswith(" "):
        problems.append("leading whitespace mismatch")
    if src.endswith(" ") != tgt.endswith(" "):
        problems.append("trailing whitespace mismatch")
    if src.startswith("\n") != tgt.startswith("\n"):
        problems.append("leading newline mismatch")
    if src.endswith("\n") != tgt.endswith("\n"):
        problems.append("trailing newline mismatch")
    if src.count("\n") != tgt.count("\n"):
        problems.append(
            f"newline count differs: src={src.count(chr(10))} tgt={tgt.count(chr(10))}"
        )

    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")

    if "..." in tgt:
        problems.append("ASCII '...' still in target (should be '……')")

    return problems


def check_bilingual_invariants(src: str, tgt: str, eid: str) -> list[str]:
    problems: list[str] = []
    if not tgt.startswith(src + " "):
        problems.append("bilingual target does not start with '<source> '")
    bad_punct = [c for c in tgt if c in ",.，。；;！!？?"]
    if bad_punct:
        problems.append(f"bilingual target contains punctuation: {set(bad_punct)}")
    return problems


def load_outputs() -> tuple[dict, dict, set, dict]:
    translations: dict[str, str | None] = {}
    subflags: dict[str, list[str]] = {}
    bilingual_ids: set[str] = set()
    per_batch_counts: dict[str, dict[str, int]] = {}

    seen_ids: set[str] = set()
    for letter in BATCH_LETTERS:
        path = OUTPUTS_DIR / f"batch-{letter}-output.json"
        out = json.loads(path.read_text())
        ids = list(out["translations"].keys())
        clash = set(ids) & seen_ids
        if clash:
            raise SystemExit(f"batch-{letter}: duplicate ids across batches: {clash}")
        seen_ids.update(ids)

        translations.update(out["translations"])
        for k, v in out["do_not_translate_subflags"].items():
            if not v or len(v) != 1 or v[0] not in VALID_SUBFLAGS:
                raise SystemExit(
                    f"batch-{letter}: invalid sub-flag for {k}: {v}; "
                    f"must be one of {sorted(VALID_SUBFLAGS)}"
                )
            subflags[k] = list(v)
        bilingual_ids.update(out["bilingual_search_terms_ids"])

        null_ct = sum(1 for v in out["translations"].values() if v is None)
        per_batch_counts[letter] = {
            "total": len(ids),
            "null": null_ct,
            "translated": len(ids) - null_ct,
            "flagged": len(out["do_not_translate_subflags"]),
            "bilingual": len(out["bilingual_search_terms_ids"]),
        }

    null_ids = {k for k, v in translations.items() if v is None}
    if null_ids != set(subflags.keys()):
        only_null = null_ids - set(subflags.keys())
        only_flag = set(subflags.keys()) - null_ids
        raise SystemExit(
            f"null_ids vs subflag_ids mismatch: only_null={only_null}, only_flag={only_flag}"
        )
    for bid in bilingual_ids:
        if translations.get(bid) is None:
            raise SystemExit(f"bilingual id {bid} has null target")
        if bid in subflags:
            raise SystemExit(f"bilingual id {bid} also in subflags")

    return translations, subflags, bilingual_ids, per_batch_counts


def main() -> int:
    translations, subflags, bilingual_ids, per_batch_counts = load_outputs()
    if len(translations) != EXPECTED_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_TOTAL} merged entries, got {len(translations)}"
        )

    print(f"Loaded {len(translations)} entries from {len(BATCH_LETTERS)} sub-batches:")
    for letter, ct in per_batch_counts.items():
        print(f"  batch-{letter}: {ct}")

    with STRINGS_PATH.open() as f:
        data = json.load(f)

    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}
    missing = [eid for eid in translations if eid not in by_id]
    if missing:
        print(f"missing ids in strings.json: {missing}", file=sys.stderr)
        return 1

    pre_translated = sum(1 for e in entries if e["status"] == "translated")
    pre_new = sum(1 for e in entries if e["status"] == "new")
    pre_fuzzy = sum(1 for e in entries if e["status"] == "fuzzy")
    pre_snapshot = {
        e["id"]: (e.get("target"), e["status"])
        for e in entries
        if e["status"] == "translated"
    }

    errors: list[str] = []
    applied = 0
    already = 0
    counts_by_action: Counter = Counter()

    for eid, tgt in translations.items():
        entry = by_id[eid]
        is_flagged = eid in subflags
        is_bilingual = eid in bilingual_ids

        if is_flagged:
            sub = subflags[eid][0]
            action = f"flag_{sub}"
        elif is_bilingual:
            action = "bilingual_search_terms"
        else:
            action = "translate"

        if entry["status"] == "translated" and entry.get("target") == tgt:
            already += 1
            flags = entry.get("flags") or []
            needed = [BATCH_FLAG]
            if is_flagged:
                needed += ["do_not_translate"] + subflags[eid]
            elif is_bilingual:
                needed += ["search_terms_bilingual"]
            mutated_flags = False
            for f in needed:
                if f not in flags:
                    flags.append(f)
                    mutated_flags = True
            if mutated_flags:
                entry["flags"] = flags
                entry["updated_at"] = NOW
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
            for flag in (BATCH_FLAG, "do_not_translate", *subflags[eid]):
                if flag not in flags:
                    flags.append(flag)
            entry["flags"] = flags
            entry["updated_at"] = NOW
            applied += 1
            counts_by_action[action] += 1
            continue

        if tgt is None:
            errors.append(f"{eid}: non-flag entry has null target")
            continue

        if is_bilingual:
            probs = check_bilingual_invariants(src, tgt, eid)
            if probs:
                errors.append(f"{eid} (bilingual): {probs}\n  src={src!r}\n  tgt={tgt!r}")
                continue
        else:
            probs = check_translate_invariants(src, tgt, eid)
            if probs:
                errors.append(f"{eid} (translate): {probs}\n  src={src!r}\n  tgt={tgt!r}")
                continue

        entry["target"] = tgt
        entry["status"] = "translated"
        flags = entry.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        if is_bilingual and "search_terms_bilingual" not in flags:
            flags.append("search_terms_bilingual")
        entry["flags"] = flags
        entry["updated_at"] = NOW
        applied += 1
        counts_by_action[action] += 1

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    for eid, (prev_target, prev_status) in pre_snapshot.items():
        e = by_id[eid]
        if eid in translations:
            continue
        if e.get("target") != prev_target or e["status"] != prev_status:
            print(f"ERROR: unrelated translated entry mutated: {eid}", file=sys.stderr)
            return 1

    status_counter = Counter(e["status"] for e in entries)
    md = data.setdefault("metadata", {})
    stats = md.setdefault("stats", {})
    stats["new"] = status_counter.get("new", 0)
    stats["translated"] = status_counter.get("translated", 0)
    stats["fuzzy"] = status_counter.get("fuzzy", 0)
    stats["approved"] = status_counter.get("approved", 0)
    stats["obsolete"] = status_counter.get("obsolete", 0)
    md["entry_count"] = len(entries)
    md["last_changed_at"] = NOW

    STRINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    post_translated = status_counter.get("translated", 0)
    post_new = status_counter.get("new", 0)
    post_fuzzy = status_counter.get("fuzzy", 0)

    print()
    print(f"applied={applied}  already={already}  total_input={EXPECTED_TOTAL}")
    print("per-action breakdown:")
    for k, v in sorted(counts_by_action.items()):
        print(f"  {k}: {v}")
    print()
    print(f"translated: {pre_translated} -> {post_translated}  (Δ {post_translated - pre_translated:+d})")
    print(f"new:        {pre_new} -> {post_new}  (Δ {post_new - pre_new:+d})")
    print(f"fuzzy:      {pre_fuzzy} -> {post_fuzzy}  (Δ {post_fuzzy - pre_fuzzy:+d})")
    print(f"entry_count: {len(entries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
