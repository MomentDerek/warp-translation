# PRD — fix builder skipping `.cargo/` hidden dir

## Problem
`tools/extractor/src/walk.rs::is_ignored_dir` lists `.cargo` alongside truly
generated/throw-away dirs (`target`, `node_modules`, `build`, `dist`,
`.git`). Builder's `collect_all_files` (`tools/builder/src/lib.rs:208`)
shares that predicate via `walkdir::filter_entry`, so when we mirror the
Warp source tree into `build/warp-zh/`, the entire `.cargo/` directory is
silently dropped. In Warp's repo, `.cargo/config.toml` carries
target/registry configuration that the translated copy needs to build the
same way as upstream. The current `build/warp-zh/.cargo/config.toml` only
exists because of a prior manual copy — a fresh build would lose it.

## Goal
The builder must mirror `.cargo/` (and any other hidden Cargo config dir)
into the output tree verbatim. The extractor should keep ignoring truly
generated dirs but should not skip user-authored hidden config dirs like
`.cargo`.

## Scope (MVP)
1. Remove `.cargo` from `is_ignored_dir` in
   `tools/extractor/src/walk.rs`. Keep `target`, `.git`, `node_modules`,
   `build`, `dist` — those are reproducible/generated and should still be
   skipped.
2. Add a unit test asserting `.cargo` is NOT ignored and the other entries
   still are.
3. Add a builder integration test (or extend an existing one in
   `tools/builder/tests/`) that creates a fake source tree with
   `.cargo/config.toml` and asserts the file appears in the output.

## Non-goals
- No generic "include all hidden dirs" rule — we still drop `.git`.
- No config flag for the ignore list. Hard-coded is fine for MVP.
- No change to how `.rs` files are translated.

## Acceptance
- `cargo test -p warp-zh-extractor` passes, including new `.cargo` case.
- `cargo test -p warp-zh-builder` passes, including new `.cargo` mirroring
  case.
- Running `warp-zh-builder build --source ../../warp` produces
  `build/warp-zh/.cargo/config.toml` identical to
  `warp/.cargo/config.toml`.
