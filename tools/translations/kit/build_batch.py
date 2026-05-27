#!/usr/bin/env python3
"""Generic batch candidate builder for the parallel-translation workflow.

Packs `status=new` entries into N file-pinned bins (~target/N each), never
splitting a file across bins. Writes:
  <task-dir>/candidates/batch-{A..}.json   (one file per bin)
  <task-dir>/candidates/manifest.json      (machine-readable bin summary)
  <task-dir>/research/composition.md        (human-readable file->bin map)

Usage:
  python3 build_batch.py --task-dir <abs-or-rel task dir> \
      --num-batches 8 --target-total 600 [--strings <path>] [--status new]

Defaults:
  --strings  : <repo-root>/translations/strings.json  (repo-root = 3 levels up
               from this file: tools/translations/kit -> repo root)
  --status   : new

This script is batch-number agnostic. The batch flag (e.g.
`pr-by-file-parallel-batch-21`) is applied later by apply_batch.py, not here.
"""
from __future__ import annotations
import argparse
import json
import string
from collections import defaultdict
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
REPO_ROOT = KIT_DIR.parents[2]  # tools/translations/kit -> repo root
DEFAULT_STRINGS = REPO_ROOT / "translations" / "strings.json"

# A..Z then AA, AB, ... (supports >26 bins if ever needed)
def bin_label(i: int) -> str:
    if i < 26:
        return string.ascii_uppercase[i]
    return string.ascii_uppercase[i // 26 - 1] + string.ascii_uppercase[i % 26]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-dir", required=True)
    ap.add_argument("--num-batches", type=int, default=8)
    ap.add_argument("--target-total", type=int, default=600)
    ap.add_argument("--strings", default=str(DEFAULT_STRINGS))
    ap.add_argument("--status", default="new")
    args = ap.parse_args()

    task_dir = Path(args.task_dir).resolve()
    strings_path = Path(args.strings).resolve()
    cand_dir = task_dir / "candidates"
    research_dir = task_dir / "research"
    cand_dir.mkdir(parents=True, exist_ok=True)
    research_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(strings_path.read_text())
    by_file: dict[str, list[dict]] = defaultdict(list)
    for e in data["entries"]:
        if e["status"] != args.status or not e.get("occurrences"):
            continue
        by_file[e["occurrences"][0]["file"]].append(e)

    files_sorted = sorted(by_file.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    n = args.num_batches
    bins: list[list[str]] = [[] for _ in range(n)]
    bin_counts = [0] * n
    selected_total = 0
    for fpath, entries in files_sorted:
        if selected_total >= args.target_total:
            break
        bi = min(range(n), key=lambda i: bin_counts[i])
        bins[bi].append(fpath)
        bin_counts[bi] += len(entries)
        selected_total += len(entries)

    out_rows: list[list[dict]] = [[] for _ in range(n)]
    for bi, file_list in enumerate(bins):
        file_list.sort()
        for fp in file_list:
            for e in by_file[fp]:
                out_rows[bi].append({
                    "id": e["id"],
                    "source": e["source"],
                    "file": e["occurrences"][0]["file"],
                    "line": e["occurrences"][0]["line"],
                    "occurrences_kind": e["occurrences"][0].get("kind"),
                    "source_hash": e.get("source_hash"),
                    "audit_verdict": e.get("audit", {}).get("verdict"),
                    "occurrences_count": len(e["occurrences"]),
                    "occurrences_all": [
                        {"file": o["file"], "line": o["line"], "kind": o.get("kind")}
                        for o in e["occurrences"]
                    ],
                })

    manifest_batches = []
    for bi in range(n):
        letter = bin_label(bi)
        (cand_dir / f"batch-{letter}.json").write_text(
            json.dumps(out_rows[bi], ensure_ascii=False, indent=2)
        )
        manifest_batches.append({
            "letter": letter,
            "count": len(out_rows[bi]),
            "files": [{"path": fp, "count": len(by_file[fp])} for fp in bins[bi]],
        })

    total = sum(len(r) for r in out_rows)
    manifest = {
        "num_batches": n,
        "target_total": args.target_total,
        "total": total,
        "status_filter": args.status,
        "strings_path": str(strings_path),
        "batches": manifest_batches,
    }
    (cand_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    # composition.md
    lines = ["# batch composition\n\n",
             f"Total selected: **{total}** entries across {n} batches "
             f"(target {args.target_total}, status={args.status}).\n\n",
             "| Batch | files | entries |\n|:---:|---|---:|\n"]
    for b in manifest_batches:
        head = ", ".join(f["path"] for f in b["files"][:4])
        if len(b["files"]) > 4:
            head += f", … (+{len(b['files'])-4})"
        lines.append(f"| **{b['letter']}** | {head} | {b['count']} |\n")
    lines.append("\n## Full file-to-batch mapping\n\n")
    for b in manifest_batches:
        lines.append(f"### Batch {b['letter']} ({b['count']} entries, {len(b['files'])} files)\n\n")
        for f in b["files"]:
            lines.append(f"- `{f['path']}` — {f['count']}\n")
        lines.append("\n")
    (research_dir / "composition.md").write_text("".join(lines))

    print(f"Built {n} batches (total {total}, target {args.target_total}):")
    for b in manifest_batches:
        print(f"  {b['letter']}: {b['count']:4d} entries / {len(b['files']):3d} files")
    print(f"\nmanifest: {cand_dir / 'manifest.json'}")
    print(f"composition: {research_dir / 'composition.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
