# Batch-19 Composition

- **Date**: 2026-05-26
- **Source pool**: `translations/strings.json` (canonical), `status="new"` only — 2283 entries
- **Target**: ~360 entries across 6 sub-batches, file-pinned, ~60 per batch (acceptable 55–70)

## Selection logic

1. Loaded the **canonical** `translations/strings.json` `entries[]`; filtered to `status == "new"` (2283 entries, 691 distinct primary files).
   - Note: `tools/translations/strings.json` is a fresh-extraction snapshot containing **all** strings as `new` and is **not** the canonical merge target — using it would over-include already-translated entries. The canonical file is `translations/strings.json` (counts: `new=2283`, `translated=4399`, `fuzzy=52`), matching the batch-18 PRD `Counts after apply` target.
2. Grouped each entry by **primary occurrence file** (`occurrences[0].file`).
3. Built a "burned files" set of 68 files from batch-15..18 PRDs. **All burned files have zero residue** in the canonical pool, so no burned file needed re-inclusion.
4. The fresh pool is **fragmented**: top file is 17 entries, then 14, 14, 13, 12, … So each sub-batch contains 4–7 small files clustered by flavor (cohesive flavor between files within a batch).
5. Each candidate file is fully consumed in batch-19 — no intra- or inter-batch file splits. Remaining new entries (~1903 after batch-19) roll into batch-20+.
6. Each entry sorted by `(file ASC, line ASC)`.

## File → batch mapping

### Batch A — Settings / settings-view cluster (61)
- `app/src/settings_view/code_page.rs` (14)
- `app/src/settings/mod.rs` (14)
- `app/src/settings/input.rs` (12)
- `app/src/settings/editor.rs` (11)
- `app/src/settings/font.rs` (10)

### Batch B — AI / Agent inline-action & utilities (61)
- `crates/ai/src/aws_credentials.rs` (10) — may overlap with previously-burned `app/src/ai/aws_credentials.rs` semantically, but is a separate crate file
- `app/src/ai/blocklist/block/status_bar.rs` (9)
- `app/src/ai/blocklist/inline_action/ask_user_question_view.rs` (9)
- `app/src/ai/blocklist/block.rs` (9)
- `app/src/ai/blocklist/inline_action/requested_command.rs` (8)
- `app/src/ai/blocklist/action_model/execute/start_agent.rs` (8)
- `app/src/ai/blocklist/inline_action/search_codebase.rs` (8)

### Batch C — Terminal subsystems (61)
- `app/src/terminal/shared_session/sharer/network.rs` (10)
- `app/src/terminal/session_settings.rs` (10)
- `app/src/terminal/buy_credits_banner.rs` (9)
- `app/src/terminal/view/ambient_agent/loading_screen.rs` (8)
- `app/src/terminal/model/early_output.rs` (8)
- `app/src/terminal/model/tmux/parser.rs` (8)
- `app/src/terminal/shared_session/share_modal/body.rs` (8)

### Batch D — Onboarding + workflows + notebooks + workspace modals (67)
- `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs` (13)
- `crates/onboarding/src/slides/agent_slide.rs` (10)
- `crates/onboarding/src/slides/free_user_no_ai_slide.rs` (9)
- `app/src/workflows/workflow_view.rs` (9)
- `app/src/notebooks/file/mod.rs` (9)
- `app/src/workspace/view/global_search/view.rs` (9)
- `crates/onboarding/src/lib.rs` (8)

### Batch E — Drive / sharing + code editor utilities + themes (68)
- `app/src/themes/default_themes.rs` (13)
- `app/src/drive/export.rs` (11)
- `app/src/drive/sharing/dialog/mod.rs` (11)
- `app/src/util/file/external_editor/mod.rs` (11)
- `app/src/code/editor/find/view.rs` (11)
- `app/src/workspaces/gql_convert.rs` (11)

### Batch F — Foundational crates: terminal mode, node runtime, managed-secrets, editor debug (62)
- `crates/warp_terminal/src/model/mode.rs` (17)
- `crates/node_runtime/src/lib.rs` (17)
- `crates/managed_secrets/src/envelope/hpke_impl.rs` (14)
- `crates/editor/src/render/model/debug.rs` (14)

## Summary table

| Batch | Files | Entries | Flavor |
|:---:|:---:|:---:|---|
| A | 5 | 61 | UI Settings (code page + settings model + input/editor/font) |
| B | 7 | 61 | AI block-list / inline-action / agent execution |
| C | 7 | 61 | Terminal: shared session, session settings, tmux, ambient agent |
| D | 7 | 67 | Onboarding slides + workflows + notebooks + workspace modals |
| E | 6 | 68 | Drive export/sharing + editor find + themes + workspace gql |
| F | 4 | 62 | Foundational crates (warp_terminal, node_runtime, managed_secrets, editor debug) |
| **Total** | **36** | **380** | |

## Implementer hints (per-batch caveats)

- **B (`crates/ai/src/aws_credentials.rs`)**: This is a separate file from `app/src/ai/aws_credentials.rs` (burned in batch-17). Check sink: AWS credential errors usually surface to UI on auth setup, but some are pure telemetry. Trace each.
- **C (`terminal/model/early_output.rs`, `tmux/parser.rs`)**: Model-layer parsers often contain `panic!`/`unreachable!`/debug log strings — apply §10 (`flag_panic_message`) or §11 (`flag_telemetry_payload`) liberally where the literal never reaches a UI element.
- **D (`crates/onboarding/*`)**: Onboarding slide text is end-user UI — translate plainly.
- **E (`themes/default_themes.rs`)**: Theme **names** are brand-like proper nouns (e.g. "Dracula", "Solarized") — check whether each string is a UI label vs. a theme identifier. Display labels translate; internal identifiers/keys do not (`flag_protocol_key` if used as a serialization key).
- **F (`crates/node_runtime/src/lib.rs`)**: Node runtime crate — likely mix of panic messages, tracing labels, and a few user-visible "install Node.js" prompts. Trace sink per entry.
- **F (`crates/managed_secrets/src/envelope/hpke_impl.rs`)**: HPKE crypto envelope — almost certainly all panic / error / tracing strings, no user-facing UI. Default-bias toward `flag_panic_message` / `flag_telemetry_payload`.
- **F (`crates/editor/src/render/model/debug.rs`)**: Filename literally `debug.rs` — strong signal these are debug/tracing strings → `flag_telemetry_payload` is the likely outcome for most entries.
- **F (`crates/warp_terminal/src/model/mode.rs`)**: Terminal mode model — may include mode names exposed to UI (e.g. "Normal", "Insert"). Mix of UI and internal identifiers.

## Expected post-apply counts

- `status=new`: 2283 → **1903** (-380)
- `status=translated`: 4399 → **4779** (+380)
- `fuzzy`: 52 (unchanged)
- New entries with `pr-by-file-parallel-batch-19` flag: 380
