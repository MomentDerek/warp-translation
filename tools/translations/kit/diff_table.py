#!/usr/bin/env python3
"""Diff a translation table before vs after an extractor run.

Compares two strings.json snapshots by entry id + status and classifies what
changed into new / fuzzy / obsolete / deleted — the same logic the
`.claude/workflows/sync-upstream-translations.ts` workflow uses inline, lifted
here so the daily GitHub Actions pipeline (and local simulation) can run it
without a Claude session.

Usage:
  python3 diff_table.py <before.json> <after.json> [--report <out.json>] \
      [--github-output <path>]

Emits to stdout a compact JSON summary {counts, byFile, samples}, writes the
full machine report to --report (if given), and writes GitHub Actions outputs
new_count / fuzzy_count / obsolete_count / deleted_count to $GITHUB_OUTPUT (or
--github-output).
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
from pathlib import Path


def srcfile(e: dict) -> str:
    occ = e.get("occurrences") or []
    return occ[0]["file"] if occ else "(no-occurrence)"


def short(s: str | None, n: int = 120) -> str:
    s = (s or "").replace("\n", "\\n")
    return s if len(s) <= n else s[:n] + " ..."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--report", default=None, help="write full machine report JSON here")
    ap.add_argument("--github-output", default=None, help="default: $GITHUB_OUTPUT")
    args = ap.parse_args()

    before = json.loads(Path(args.before).read_text())
    after = json.loads(Path(args.after).read_text())
    b = {e["id"]: e for e in before.get("entries", [])}
    a = {e["id"]: e for e in after.get("entries", [])}

    records: dict[str, list] = {"new": [], "fuzzy": [], "obsolete": [], "deleted": []}
    for i in a:
        if i not in b:
            e = a[i]
            records["new"].append(
                {"id": i, "file": srcfile(e), "source": e.get("source"), "status": e.get("status")}
            )
    for i in b:
        if i not in a:
            e = b[i]
            records["deleted"].append(
                {"id": i, "file": srcfile(e), "source": e.get("source"), "status": e.get("status")}
            )
    for i in set(a) & set(b):
        eb, ea = b[i], a[i]
        if eb.get("status") != ea.get("status"):
            if ea.get("status") == "fuzzy":
                records["fuzzy"].append(
                    {"id": i, "file": srcfile(ea), "source": ea.get("source"),
                     "old_source": eb.get("source")}
                )
            elif ea.get("status") == "obsolete":
                records["obsolete"].append(
                    {"id": i, "file": srcfile(ea), "source": ea.get("source")}
                )

    byfile = collections.defaultdict(lambda: {"new": 0, "fuzzy": 0, "obsolete": 0})
    for k in ("new", "fuzzy", "obsolete"):
        for r in records[k]:
            byfile[r["file"]][k] += 1
    byFile = [{"file": f, **c} for f, c in sorted(byfile.items())]
    counts = {k: len(v) for k, v in records.items()}

    if args.report:
        report = {
            "counts": counts,
            "byFile": byFile,
            "records": records,
            "source_commit_before": before.get("metadata", {}).get("source_commit"),
            "source_commit_after": after.get("metadata", {}).get("source_commit"),
        }
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2))

    samples = []
    for k in ("new", "fuzzy", "obsolete"):
        for r in records[k][:10]:
            samples.append({"id": r["id"], "change": k, "file": r["file"], "source": short(r["source"])})

    print(json.dumps({"counts": counts, "byFile": byFile, "samples": samples[:30]}, ensure_ascii=False))

    target = args.github_output or os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as fh:
            for k, v in counts.items():
                fh.write(f"{k}_count={v}\n")
            fh.write(f"changed_total={sum(counts.values())}\n")

    print(
        f"diff: new={counts['new']} fuzzy={counts['fuzzy']} "
        f"obsolete={counts['obsolete']} deleted={counts['deleted']}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
