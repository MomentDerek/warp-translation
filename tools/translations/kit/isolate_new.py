#!/usr/bin/env python3
"""Isolate `status=new` additions, reverting extractor-induced fuzzy/obsolete/
deleted churn so a translation batch (+ its check) sees a clean table.

The daily pipeline runs the extractor first, which produces BOTH new entries and
status flips (translated→fuzzy when upstream source changed, →obsolete / removal
when it disappeared). The shared `translate_batch.mjs` Check phase asserts "the
only entries whose (target,status) changed are the batch ones" — true for the
interactive workflow (where fuzzy/obsolete are handled separately), but the
daily flow's pre-existing fuzzy/obsolete flips trip it as collateral.

This rewrites <table> to: every entry from <before> (the pristine pre-extract
HEAD table) PLUS the `status=new` entries the extractor just added. Net effect —
the only delta vs HEAD is the new additions; fuzzy/obsolete/deleted entries are
restored to their HEAD state (still recorded in the diff artifact for human
resync, and re-detected by the extractor on the next run). The current table's
metadata (including the bumped source_commit) is preserved.

Usage:
  python3 isolate_new.py --before <before.json> --table <strings.json>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True, help="pristine pre-extract table snapshot")
    ap.add_argument("--table", required=True, help="post-extract table to rewrite in place")
    args = ap.parse_args()

    before = json.loads(Path(args.before).read_text())
    after = json.loads(Path(args.table).read_text())

    before_ids = {e["id"] for e in before["entries"]}
    new_entries = [e for e in after["entries"] if e.get("status") == "new"]
    # Pristine HEAD entries + only the brand-new additions. A `new` id is by
    # definition absent from `before`, so this can't duplicate.
    kept = list(before["entries"]) + [e for e in new_entries if e["id"] not in before_ids]

    # Mutate the post-extract object in place so ALL top-level fields are
    # preserved (e.g. `$schema_version`, which the builder's strict parser
    # requires) — only the entry list and entry_count change. Keep the bumped
    # metadata.source_commit from the extract.
    after["entries"] = kept
    if isinstance(after.get("metadata"), dict):
        after["metadata"]["entry_count"] = len(kept)
    Path(args.table).write_text(json.dumps(after, ensure_ascii=False, indent=2) + "\n")

    print(
        f"isolated: kept {len(before['entries'])} HEAD entries + {len(new_entries)} new "
        f"= {len(kept)} total (reverted extractor churn on non-new entries)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
