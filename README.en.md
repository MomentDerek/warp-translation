# warp_translation

> 📖 **中文版 / Chinese version**: [README.md](README.md)

Chinese localization of the [Warp](https://github.com/warpdotdev/Warp) terminal — **without modifying upstream**.

A pure overlay: extract every Rust string literal from `../warp`, store translations in this repo's `translations/strings.json`, then build a localized source copy that you can `cargo build` like normal. Upstream stays untouched.

```
upstream Warp (../warp, read-only)
        │
        ▼ extract
warp-zh-extractor ──► translations/strings.json   (single source of truth)
                                  │
                                  ▼ build
                       warp-zh-builder ──► build/warp-zh/   (compilable Chinese source)
```

Missing or stale entries automatically fall back to English, so the build always succeeds. Incremental: only new/changed strings need retranslation when upstream moves.

**Status** (table snapshot, aligned with upstream `v0.2026.06.05.09.22.dev_00`): 6,908 entries — all translated, 0 fuzzy, 0 obsolete.

## Quick start

```bash
# 0. Clone this repo and put Warp next to it
git clone https://github.com/warpdotdev/Warp.git ../warp

# 1. Re-extract from upstream (idempotent; only new/changed entries flip status)
cd tools && cargo run -p warp-zh-extractor -- extract \
    --source ../../warp \
    --table ../translations/strings.json \
    --lock ../translations/.lock.json

# 2. Build the localized source tree
cd tools && cargo run -p warp-zh-builder -- build \
    --source ../../warp \
    --table ../translations/strings.json \
    --out ../build/warp-zh \
    --report ../reports/build.json

# 3. Compile the localized Warp
cd build/warp-zh && MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp
```

That's it. The localized binary lives in `build/warp-zh/target/`.

## Running the action-built artifacts on Mac

Don't want to compile locally? Grab the installer GitHub Actions already built.

### Get the `.dmg`

- **A tagged release (recommended)**: the repo's [Releases](../../releases) page — every tag auto-publishes a release with the macOS `WarpOss-arm64.dmg` (plus the Linux deb/rpm/AppImage).
- **Any build**: go to [Actions](../../actions) → pick a *Build Chinese Warp* run → **Artifacts** at the bottom → download `warp-zh-installer-macos-latest` (unzips to the `.dmg`).

> The artifact is **Apple Silicon (arm64)** only; Intel Macs aren't covered — build from source via "Quick start" above instead.

### Install and get past Gatekeeper

The `.dmg` is built with `script/bundle --nosign`, so it is **unsigned / un-notarized**. macOS Gatekeeper blocks it on first launch ("cannot be opened because the developer cannot be verified"). To run it:

```bash
# 1. Double-click WarpOss-arm64.dmg to mount it, drag WarpOss.app to Applications
# 2. Clear the quarantine attribute (either one):

#  a) one-shot from the CLI:
xattr -dr com.apple.quarantine /Applications/WarpOss.app

#  b) or in Finder: right-click WarpOss.app → Open → click "Open" again in the dialog
```

It launches normally afterward. `WarpOss.app` is Warp's self-contained OSS build (`oss` channel, bundle id `dev.warp.WarpOss`); it coexists with the official signed Warp without conflict.

## Repository layout

| Path | Purpose |
|---|---|
| `tools/extractor/` | `warp-zh-extractor` — scans `.rs` files, applies UI-string heuristics, merges into the translation table |
| `tools/builder/` | `warp-zh-builder` — copies the source tree and substitutes translated literals; produces a buildable Chinese Warp |
| `tools/translations/kit/` | `build_batch.py`, `apply_batch.py` — Python helpers for batch translation |
| `translations/strings.json` | The translation table (single source of truth) |
| `translations/glossary.json` | Term decisions (~32 terms) and translation philosophy |
| `.claude/workflows/` | [Claude Code](https://claude.com/claude-code) Workflow scripts for parallel batch translation and upstream sync |
| `.trellis/` | Task journal & spec — the [Trellis](https://github.com/) workflow used to develop this project. Reference material only; not required for running the tools |
| `build/warp-zh/` | Output of `warp-zh-builder` (gitignored) |
| `reports/` | Extract/build diagnostics (gitignored) |

## The five workflows

### A. Re-extract from upstream

Re-run after `../warp` changes. Idempotent: HEAD-stable input → byte-identical `strings.json`.

```bash
cd tools
cargo run -p warp-zh-extractor -- extract \
    --source ../../warp \
    --table ../translations/strings.json \
    --lock ../translations/.lock.json
```

What it does: walks every `.rs` file in `../warp` with `syn`, applies UI-string heuristics (path-allow/deny lists, UI method/constructor recognition, content regexes, sentence-structure features), assigns a `score`/`verdict` to each literal, and incrementally merges into `strings.json`. Existing translations are preserved; upstream text changes flip an entry to `fuzzy`; vanished entries flip to `obsolete` (hard-removed after 3 missing extractions).

**Check mode** (CI / pre-commit):

```bash
cargo run -p warp-zh-extractor -- extract --source ../../warp \
    --table ../translations/strings.json --check
```

Non-zero exit if `strings.json` isn't in canonical form (sort order / stats / field order).

**Raw mode** (debugging — dumps every literal pre-heuristic):

```bash
cargo run -p warp-zh-extractor -- raw-extract \
    --source ../../warp --out ../reports/raw-extract.json
```

### B. Build the localized source

```bash
cd tools
cargo run -p warp-zh-builder -- build \
    --source ../../warp \
    --table ../translations/strings.json \
    --out ../build/warp-zh \
    --report ../reports/build.json
```

Mirrors the source tree (skipping `target/`, `.git/`, `node_modules/`, etc.), re-parses each `.rs` with `syn`, and substitutes literals whose `target` is non-empty and `status ∈ {translated, approved, fuzzy}`. Replacements apply in reverse byte order to preserve offsets; quote style auto-selects `"..."` vs `r#"..."#` based on content. Untranslated literals stay English — the build always compiles.

**Compile verification** (macOS):

```bash
cd build/warp-zh
MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp
```

`-p warp` is the app crate (see `app/Cargo.toml`). The `MACOSX_DEPLOYMENT_TARGET` requirement comes from Warp's own `app/build.rs`, not from this project.

### C. Translate single entries

Two helper subcommands on `warp-zh-builder` for incremental translation:

```bash
# List status=new entries for one or more files
cargo run -p warp-zh-builder -- list-batch \
    --table ../translations/strings.json \
    --filter app/src/app_menus.rs \
    --status new > /tmp/candidates.json

# Write a batch
# input: { "flag": "<your-flag>",
#          "translations": {
#            "<id>": { "target": "中文" },
#            "<id>": { "target": null, "do_not_translate": true }
#          } }
cargo run -p warp-zh-builder -- apply-batch \
    --table ../translations/strings.json \
    --input /tmp/batch.json \
    --now 2026-05-08T00:00:00Z
```

`apply-batch` writes the targets, flips status to `translated`, attaches the flag, and re-canonicalizes the table.

### D. Parallel batch translation (advanced — requires Claude Code)

For larger batches (~75–600 entries), there's a Claude Code Workflow that fans out N sub-agents in parallel:

```
1. build candidates → tools/translations/kit/build_batch.py
2. translate        → .claude/workflows/translate_batch.mjs   (N implementer sub-agents)
3. apply            → tools/translations/kit/apply_batch.py   (hard-fails on invariant violations)
4. check            → trellis-check sub-agent
```

Full end-to-end steps: see [`tools/translations/kit/RUNBOOK.md`](tools/translations/kit/RUNBOOK.md).
File/API reference: see [`tools/translations/kit/README.md`](tools/translations/kit/README.md).

This flow depends on Claude Code's `Workflow` tool plus the `trellis-implement` / `trellis-check` sub-agents shipped under `.claude/agents/`. Without Claude Code, use workflow C (manual `apply-batch`) instead — the table format and invariants are identical.

### E. Upstream sync (when upstream Warp moves)

A Claude Code Workflow that fast-forwards `../warp`, re-extracts, diffs `strings.json` before vs after, classifies changes per source-area, and writes a Markdown report:

```js
Workflow({
  scriptPath: ".claude/workflows/sync-upstream-translations.ts",
  args: {
    repoRoot: "<absolute path to this repo>",
    srcRepo:  "<absolute path to upstream warp clone>",
  }
})
```

Output: `reports/sync-translation-changes.{json,md}`. The report lists per-source-area what's new / fuzzy / obsolete / deleted and recommends a next batch.

Read-only on `../warp` (fast-forward only — never force, never merge non-ff). The merge step aborts if upstream diverged.

## Translation policy

Per-entry decision flow when translating (first hit wins):

1. **Doc-comment false positives** (`/// …` fragments) — flag `extractor_false_positive_doc_comment`, no target.
2. **`.expect()` / `panic!` / `unreachable!`** messages — flag `panic_message`, no target.
3. **Telemetry / logging-only** literals (`tracing::*`, log files — not UI) — flag `telemetry_payload`, no target.
4. **`fn search_terms()`** keywords — bilingual append: `target = "<source> <中文>"` (preserves English search, adds Chinese).
5. **wgpu debug labels / test fixtures / protocol keys** (serde/YAML field names, feature/model identifiers) — matching sub-flag, no target.
6. **Regular UI text** — translate to Chinese per the contract.

Sub-flag whitelist (exactly one per flagged entry): `panic_message`, `telemetry_payload`, `extractor_false_positive_doc_comment`, `test_fixture`, `wgpu_debug_label`, `protocol_key`.

Translation invariants enforced by `apply_batch.py`:

- placeholders (`{}`, `{name}`, `{0}`) and strftime codes (`%b`, `%d`, …) preserved exactly
- leading/trailing whitespace + newline shape preserved
- brand literals preserved verbatim (Warp, MCP, AI, OAuth, GitHub, …)
- Chinese punctuation full-width (`，。；！？`); ASCII `...` rejected (must be `……`)
- bilingual targets start with `"<source> "` (one ASCII space, no punctuation)

Full contract: [`.trellis/spec/guides/translation-contract.md`](.trellis/spec/guides/translation-contract.md).

## Toolchain

`tools/rust-toolchain.toml` pins Rust 1.92.0, matching `../warp`. Mismatched toolchains will cause `cargo check` of `build/warp-zh/` to recompile heavy deps under a different rustc.

## Design documents

- [Translation table format](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/research/translation-table-format.md)
- [`syn` string extraction](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/research/syn-string-extraction.md)
- [UI string heuristics](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/research/ui-string-heuristics.md)
- [Original PRD](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/prd.md)

## License

MIT — see [`LICENSE`](LICENSE).

Note that the build output `build/warp-zh/` is a derivative work of upstream Warp (AGPLv3 + MIT) and remains subject to upstream's licenses. The MIT license here covers only this repository's original tooling and translation data.
