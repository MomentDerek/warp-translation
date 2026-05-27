#!/usr/bin/env python3
"""Compose batch-20 candidates: 10 file-pinned batches of ~60 entries each.

Strategy:
  - Read translations/strings.json for status=new entries.
  - Group by primary occurrence file.
  - Sort files by entry count desc; pack into 10 bins targeting ~60 per bin.
  - File is never split across bins.
  - Output candidates/batch-{A..J}.json + composition.md.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent.parent
ROOT = TASK_DIR.parents[2]
STRINGS = ROOT / "translations" / "strings.json"
CAND_DIR = TASK_DIR / "candidates"
RESEARCH_DIR = TASK_DIR / "research"

NUM_BATCHES = 10
TARGET_TOTAL = 600
LETTERS = "ABCDEFGHIJ"

def main() -> None:
    data = json.loads(STRINGS.read_text())
    # group new entries by primary occurrence file
    by_file: dict[str, list[dict]] = defaultdict(list)
    for e in data["entries"]:
        if e["status"] != "new" or not e.get("occurrences"):
            continue
        f = e["occurrences"][0]["file"]
        by_file[f].append(e)

    # sort files by count desc, then path asc
    files_sorted = sorted(by_file.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    # Pack into 10 bins via greedy first-fit-decreasing,
    # always assigning whole files to least-loaded bin until we hit ~600 total.
    bins: list[list[str]] = [[] for _ in range(NUM_BATCHES)]
    bin_counts = [0] * NUM_BATCHES

    selected_total = 0
    for fpath, entries in files_sorted:
        if selected_total >= TARGET_TOTAL:
            break
        # smallest-loaded bin
        bi = min(range(NUM_BATCHES), key=lambda i: bin_counts[i])
        bins[bi].append(fpath)
        bin_counts[bi] += len(entries)
        selected_total += len(entries)

    # If we are too low (single-occurrence files dominate), pull additional small files.
    # The above loop already iterates all files, so selected_total may exceed 600 only modestly.

    # Now reshape: each batch is a list of {entry rows}. Sort files within a batch.
    out_rows: list[list[dict]] = [[] for _ in range(NUM_BATCHES)]
    for bi, file_list in enumerate(bins):
        file_list.sort()
        for fp in file_list:
            for e in by_file[fp]:
                row = {
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
                }
                out_rows[bi].append(row)

    CAND_DIR.mkdir(parents=True, exist_ok=True)
    for bi, rows in enumerate(out_rows):
        letter = LETTERS[bi]
        path = CAND_DIR / f"batch-{letter}.json"
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2))

    # composition.md
    lines: list[str] = ["# batch-20 composition\n"]
    lines.append(f"Total selected: **{sum(len(r) for r in out_rows)}** entries across {NUM_BATCHES} batches.\n")
    lines.append("\n| Batch | files | entries |\n|:---:|---|---:|\n")
    for bi, file_list in enumerate(bins):
        letter = LETTERS[bi]
        n = len(out_rows[bi])
        # truncated file list
        head = ", ".join(file_list[:4])
        if len(file_list) > 4:
            head += f", … (+{len(file_list)-4})"
        lines.append(f"| **{letter}** | {head} | {n} |\n")
    lines.append("\n## Full file-to-batch mapping\n\n")
    for bi, file_list in enumerate(bins):
        letter = LETTERS[bi]
        lines.append(f"### Batch {letter} ({len(out_rows[bi])} entries, {len(file_list)} files)\n\n")
        for fp in file_list:
            n = len(by_file[fp])
            lines.append(f"- `{fp}` — {n}\n")
        lines.append("\n")
    (RESEARCH_DIR / "batch-20-composition.md").write_text("".join(lines))

    print("Built", NUM_BATCHES, "batches:")
    for bi in range(NUM_BATCHES):
        print(f"  {LETTERS[bi]}: {len(out_rows[bi]):4d} entries / {len(bins[bi]):3d} files")
    print(f"Total: {sum(len(r) for r in out_rows)}")

if __name__ == "__main__":
    main()
