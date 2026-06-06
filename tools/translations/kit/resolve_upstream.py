#!/usr/bin/env python3
"""Resolve the latest upstream warpdotdev/warp release tag for a channel and
decide whether the localization repo is behind it.

The repo's "what was last translated/built" pin is authoritative in
`translations/strings.json` -> metadata.source_commit (a commit SHA, committed
to git). Upstream publishes git tags of the form
    v0.YYYY.MM.DD.HH.MM.{dev|preview|stable}_NN
both as tags and as GitHub releases. This script:

  1. Lists upstream tags (via `gh api`, falling back to `git ls-remote`).
  2. Picks the highest version-sorted tag whose channel matches (default: dev).
  3. Resolves that tag -> commit SHA.
  4. Compares the SHA to the repo's current pin.
  5. Emits GitHub Actions outputs (and a human summary) describing whether a
     sync/translate/release run is needed.

Usage:
  python3 resolve_upstream.py [--channel dev] [--strings <path>] \
      [--repo warpdotdev/warp] [--force] [--github-output <path>]

Outputs written to $GITHUB_OUTPUT (or --github-output), one per line:
  should_run=true|false      whether the upstream tag is newer than our pin (or --force)
  upstream_tag=<tag>         e.g. v0.2026.06.06.09.03.dev_00
  upstream_sha=<full sha>    commit the tag points at
  current_pin=<full sha>     our metadata.source_commit
  current_tag=<tag-or-empty> best-effort tag name for the current pin (if resolvable)
  channel=<channel>

Resolution order for tag listing (first that succeeds wins):
  - `gh api repos/<repo>/tags --paginate`  (uses GH_TOKEN / GITHUB_TOKEN if set)
  - `git ls-remote --tags --refs https://github.com/<repo>.git`
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
REPO_ROOT = KIT_DIR.parents[2]  # tools/translations/kit -> repo root
DEFAULT_STRINGS = REPO_ROOT / "translations" / "strings.json"

# v0.2026.06.06.09.03.dev_00  ->  version key + channel + build number
TAG_RE = re.compile(
    r"^v0\.(?P<date>\d{4}\.\d{2}\.\d{2}\.\d{2}\.\d{2})\.(?P<channel>dev|preview|stable)_(?P<n>\d+)$"
)


def _run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def parse_tag(tag: str):
    """Return a sortable key (date-tuple, n) for a recognized tag, else None."""
    m = TAG_RE.match(tag)
    if not m:
        return None
    date_key = tuple(int(x) for x in m["date"].split("."))
    return (date_key, int(m["n"]), m["channel"])


def list_tags_gh(repo: str) -> dict[str, str] | None:
    """tag name -> commit sha via `gh api`. None if gh is unavailable/fails."""
    rc, out, err = _run(
        ["gh", "api", f"repos/{repo}/tags", "--paginate",
         "--jq", ".[] | [.name, .commit.sha] | @tsv"]
    )
    if rc != 0 or not out.strip():
        print(f"::debug::gh api tag listing failed (rc={rc}): {err.strip()}", file=sys.stderr)
        return None
    tags: dict[str, str] = {}
    for line in out.splitlines():
        name, _, sha = line.partition("\t")
        if name and sha:
            tags[name.strip()] = sha.strip()
    return tags


def list_tags_lsremote(repo: str) -> dict[str, str] | None:
    """tag name -> commit sha via `git ls-remote`. Note: ls-remote gives the
    tag OBJECT sha for annotated tags, not the commit; we deref with ^{}."""
    rc, out, err = _run(
        ["git", "ls-remote", "--tags", "--refs",
         f"https://github.com/{repo}.git"]
    )
    if rc != 0 or not out.strip():
        print(f"::debug::git ls-remote failed (rc={rc}): {err.strip()}", file=sys.stderr)
        return None
    tags: dict[str, str] = {}
    for line in out.splitlines():
        sha, _, ref = line.partition("\t")
        if not ref.startswith("refs/tags/"):
            continue
        name = ref[len("refs/tags/"):]
        tags[name] = sha.strip()
    return tags


def pick_latest(tags: dict[str, str], channel: str) -> tuple[str, str] | None:
    """Highest version-sorted tag matching the channel. Returns (tag, sha)."""
    candidates = []
    for name in tags:
        key = parse_tag(name)
        if key and key[2] == channel:
            candidates.append((key[:2], name))
    if not candidates:
        return None
    candidates.sort()
    best = candidates[-1][1]
    return best, tags[best]


def current_pin(strings_path: Path) -> str:
    data = json.loads(strings_path.read_text())
    return data.get("metadata", {}).get("source_commit", "")


def tag_for_sha(tags: dict[str, str], sha: str) -> str:
    for name, s in tags.items():
        if s == sha and parse_tag(name):
            return name
    return ""


def emit(outputs: dict[str, str], github_output: str | None) -> None:
    lines = [f"{k}={v}" for k, v in outputs.items()]
    block = "\n".join(lines) + "\n"
    target = github_output or os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(block)
    # Always echo to stdout for local runs / logs.
    print(block, end="")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="dev", choices=["dev", "preview", "stable"])
    ap.add_argument("--repo", default="warpdotdev/warp")
    ap.add_argument("--strings", default=str(DEFAULT_STRINGS))
    ap.add_argument("--force", action="store_true",
                    help="force should_run=true even if already current")
    ap.add_argument("--github-output", default=None,
                    help="path to write key=value outputs (default: $GITHUB_OUTPUT)")
    args = ap.parse_args()

    tags = list_tags_gh(args.repo)
    if tags is None:
        tags = list_tags_lsremote(args.repo)
    if not tags:
        print("::error::could not list upstream tags (gh api and git ls-remote both failed)",
              file=sys.stderr)
        return 2

    latest = pick_latest(tags, args.channel)
    if latest is None:
        print(f"::error::no upstream tag found for channel '{args.channel}'", file=sys.stderr)
        return 3
    upstream_tag, upstream_sha = latest

    pin = current_pin(Path(args.strings).resolve())
    cur_tag = tag_for_sha(tags, pin)

    should_run = args.force or (upstream_sha != pin)

    emit(
        {
            "should_run": "true" if should_run else "false",
            "upstream_tag": upstream_tag,
            "upstream_sha": upstream_sha,
            "current_pin": pin,
            "current_tag": cur_tag,
            "channel": args.channel,
        },
        args.github_output,
    )

    # Human summary on stderr so it never pollutes the key=value stdout contract.
    msg = (
        f"channel={args.channel}  latest upstream={upstream_tag} ({upstream_sha[:12]})  "
        f"current pin={pin[:12]}{f' ({cur_tag})' if cur_tag else ''}  "
        f"=> should_run={should_run}"
    )
    print(msg, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
