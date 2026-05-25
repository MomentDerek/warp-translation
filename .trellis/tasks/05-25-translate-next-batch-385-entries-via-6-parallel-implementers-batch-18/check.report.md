# Batch-18 Check Report

**Verdict: PASS — proceed to commit**

385 entries merged across 6 sub-batches (A/B/C/D/E/F). All invariants verified.

## Counts (expected vs actual)

| Metric | Expected | Actual | Status |
|---|---:|---:|:---:|
| metadata.stats.new | 2283 | 2283 | PASS |
| metadata.stats.translated | 4399 | 4399 | PASS |
| metadata.stats.fuzzy | 52 | 52 | PASS |
| Entries with flag `pr-by-file-parallel-batch-18` | 385 | 385 | PASS |
| b18 with status=translated | 385 | 385 | PASS |
| b18 updated 2026-05-25 | 385 | 385 | PASS |
| Translated (target≠null, non-bilingual) | 184 | 184 | PASS |
| Bilingual | 8 | 8 | PASS |
| Flagged (target=null, do_not_translate) | 193 | 193 | PASS |
| Non-b18 translated (collateral isolation) | 4014 | 4014 | PASS |

`4014 + 385 = 4399` confirms no pre-existing `translated` entry was touched.

## Sub-flag breakdown (expected vs actual)

| Sub-flag | Expected | Actual | Status |
|---|---:|---:|:---:|
| extractor_false_positive_doc_comment | 48 | 48 | PASS |
| panic_message | 20 | 20 | PASS |
| protocol_key | 41 | 41 | PASS |
| telemetry_payload | 54 | 54 | PASS |
| test_fixture | 30 | 30 | PASS |
| wgpu_debug_label | 0 | 0 | (none this batch) |
| **Total flagged** | **193** | **193** | PASS |

## Invariant checks (385 entries)

- Null-target entries all carry `do_not_translate` and exactly one sub-flag: **PASS** (0 violations)
- Placeholder set (`{...}`) identical between source and target: **PASS** (0 violations)
- strftime codes (`%X`) identical: **PASS** (0 violations)
- Leading/trailing whitespace preserved: **PASS** (0 violations)
- Newline count preserved: **PASS** (0 violations)
- ASCII `...` absent in translated targets (must be `……`): **PASS** (0 violations)
- Brand literals (Warp, Oz, MCP, GitHub, Linux, Wayland, etc.) preserved: **PASS** (0 violations)
- Half-width `, . ! ? ;` before Chinese char: **PASS** (0 violations)

## Bilingual entries (8 total — all in `app/src/settings_view/{teams_page,privacy_page}.rs`)

| ID suffix | File | OK |
|---|---|:---:|
| 7QC8VN40 | privacy_page.rs | PASS |
| 7SNX4KCC | privacy_page.rs | PASS |
| VH3R40N5 | privacy_page.rs | PASS |
| Q01ZA6QY | privacy_page.rs | PASS |
| 6S9TE4W5 | privacy_page.rs | PASS |
| 1CPTNDS2 | teams_page.rs | PASS |
| PY48CZXP | privacy_page.rs | PASS |
| 0DX7875N | privacy_page.rs | PASS |

All have `target = <exact source> + " " + <Chinese keywords>`, no forbidden punctuation.

## Spot-checks (10 random translated entries across sub-batches)

| ID suffix | File | Source → Target | Notes |
|---|---|---|---|
| W3M63TH2 | settings_view/teams_page.rs:4056 | `{} teammates` → `{} 位队友` | glossary applied (teammate→队友), placeholder preserved |
| SGWEJ29F | terminal/warpify/settings.rs:33 | `Commands that should not trigger the subshell warpification prompt.` → `不应触发子 shell warpify 提示的命令。` | full-width period, brand preserved |
| 8G0MYP6B | settings_view/teams_page.rs:4054 | `1 teammate` → `1 位队友` | consistent with plural |
| 8466WFC1 | terminal/input/slash_commands/mod.rs:638 | `File not found: {}` → `找不到文件：{}` | full-width colon, placeholder kept |
| ZRE2CPYT | terminal/shared_session/viewer/network.rs:1091 | `Invalid conversation. Please try again.` → `对话无效。请重试。` | natural Chinese register |
| H8A3KZC0 | terminal/shared_session/viewer/network.rs:1017 | `Failed to connect. Please try again later.` → `连接失败。请稍后重试。` | UI register |
| ND34DMP2 | workspace/mod.rs:159 | `Crash the app (for testing sentry-native)` → `崩溃应用（用于测试 sentry-native）` | dev tooling, full-width parens, brand kept |
| 02HZ8HDP | ai/conversation_details_panel.rs:643 | `Continue locally` → `在本地继续` | concise UI |
| QNG4AQHS | ai/blocklist/inline_action/run_agents_card_view.rs:1523 | `Failed to start orchestration: {error}` → `启动协调失败：{error}` | "Orchestrate→协调" glossary, placeholder kept |
| 9976D2FM | workflows/categories.rs:171 | `Showing all workflows` → `正在显示所有工作流` | progressive aspect |

All spot-checks reasonable; glossary applied consistently; placeholders preserved; full-width punctuation; correct register.

## Spot-checks (flagged entries — sub-flag sanity)

- **panic_message** `01PH4WS0` (`warp_util/path.rs:27` "Shell escape regex should be valid"): `.expect(...)` panic message — correctly flagged.
- **protocol_key** `2J9JF7TK` (`font_fallback.rs:91` "Noto Sans Symbols"): external font family name in `ExternalFontFamily { name: ... }` — correctly flagged as external identifier.
- **protocol_key** `K2ZFSJ8P` (`wgpu/resources.rs:499` "Intel(R) UHD Graphics 620"): GPU adapter identifier string — correctly flagged.
- **extractor_false_positive_doc_comment** `977A7TGF` (`static_commands/mod.rs:8` " Specifies the requirements..."): doc-comment leak via `scan_macro_tokens` — known false-positive class.
- **test_fixture** `MGAR1G1R` (`warpui/examples/table-sample/root_view.rs:1177`): example app demo string — correctly flagged.
- **telemetry_payload** `6C7FYG76` (`wayland/session.rs:38` "Failed to create Screencast proxy: {e}"): tracing/log sink — correctly flagged.

## Issues found and fixed

None. No self-fixes required.

## Recommendation

**Proceed to commit.** All 385 batch-18 entries pass every checked invariant; no collateral changes to pre-existing translated entries; sub-flag breakdown matches the apply log exactly; spot-checks confirm translation quality and policy compliance.
