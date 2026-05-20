# Journal - moment (Part 1)

> AI development session journal
> Started: 2026-05-04

---

## 2026-05-06 — PR2 of `05-04-translate-warp-project-to-chinese`

实装 D3（UI 启发式评分）与 D4（翻译表 schema + 增量合并）。

### Files
- 新增 `tools/extractor/src/heuristic.rs`（路径白/黑名单、UI 方法/构造器 + arg-index 门控、反向调用、const 后缀、test 上下文、15 类内容正则、阈值 6/3）
- 新增 `tools/extractor/src/translation.rs`（Table/Entry/Audit/Lock，sha256 short hash，ULID，5 态机，§4 增量合并，3-run obsolete 宽限）
- 扩展 `model.rs`（`parent_call`/`parent_call_arg_index`/`enclosing_const_name`/`in_test`/`struct_field`），同 `Visit` 单趟采集
- `main.rs` 新增 `extract` 子命令（全流程 + `--check`），保留 `raw-extract` 走 PR1 路径
- 工作区新增依赖：`sha2`、`strsim`、`ulid`、`regex`、`once_cell`
- 生成 `translations/strings.json`（38,908 条，含 `audit.score/verdict/reasons[]`），`.lock.json` 走 gitignore

### Verification
- `cargo build` / `cargo clippy --all-targets -- -D warnings` / `cargo test`（12 pass，0 fail）全绿
- 同 source 连跑两次，SHA1 完全相等：`208a0d70…39e` → 幂等达成
- `--check` 在干净表上 exit 0，篡改后 exit 1

### 待用户判断（非 spec 违反，是工程取舍）
1. **doc-comment 噪声**：`///` 被 syn 解析为 `#[doc = "..."]`，约 1,200 条进表（行首多空格、非 UI）。建议在 `visit_macro`/attribute 处过滤 doc 属性内字面量，或对 doc-attribute parent 加惩罚。
2. **单词 CamelCase UI 标签被过滤**："Settings"/"About"/"Help" 这类被 `regex:camel_case` 黑名单 + 阈值切断。需要 PR3 通过 overrides 兜底，或扩展 `UI_METHODS`/`UI_CONSTRUCTORS` 收容 `with_title`、`MenuItemFields::new` 等。
3. spec 字面差异：`metadata.extracted_at` 改名为 `last_changed_at`（仅在实际变化时更新，保证幂等）；`audit` 字段插入 `history` 与 `first_seen_commit` 之间。建议把这两点回写到 `research/translation-table-format.md`。

下一步：PR3（builder + 第一批 LLM 翻译）。



## Session 1: Translate Warp project to Chinese — PR1+PR2+PR3

**Date**: 2026-05-08
**Task**: Translate Warp project to Chinese — PR1+PR2+PR3
**Branch**: `main`

### Summary

End-to-end Chinese translation pipeline for Warp source. Built warp-zh-extractor (syn::Visit + heuristic + 5-state translation table) and warp-zh-builder (surgical byte-range replacement + marker-file safety). 6,327 active table entries, 227 PR3 first-batch translated (45 do_not_translate + 182 Chinese), 32-term glossary. cargo check -p warp passes on build/warp-zh/. 4-angle trellis-check verified builder code, translation quality (100% glossary/placeholder/tone consistency), end-to-end build idempotency, and schema/spec compliance. Captured 4 durable lessons in spec/ (syn doc-attr filtering, canonical-form --check semantic boundary, output-dir marker safety, translation contract checklist).

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `a0ea0ba` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 2: Fix menu bar translation gap (heuristic + second batch)

**Date**: 2026-05-11
**Task**: Fix menu bar translation gap (heuristic + second batch)
**Branch**: `main`

### Summary

Diagnosed and fixed the menu bar translation gap in build/warp-zh: B-class top-level menus (File/View/Window/Help/Drive/Blocks/Agent/Tabs) + D-class menu items (Switch tab/Activate pane/Clear command editor/Left Panel:X/etc) were filtered by heuristic or never captured. Trace research showed D-class literals live in EditableBinding::new[1] / FixedBinding::custom[2] / BindingDescription::new[0] across workspace/terminal/editor source files. Added 7 (call_path, arg_index) entries to UI_CONSTRUCTORS plus 10 unit tests including arg-index-rejection coverage. Re-extracted (6327 to 6391 entries, +64 menu strings); translated 506 entries with flags=[pr-menu-batch] (503 Chinese + 3 do_not_translate); 227 prior pr3_first_batch entries preserved verbatim. Quality check: 44/44 tests green, glossary 100% consistency, placeholder 100% integrity, cargo check -p warp passes in 2m 52s on the new build, builder idempotent. Updated spec rust-syn-extraction.md with the UI constructor whitelist strategy. Out of scope: C-class macOS system menu (Cut/Copy/Paste/Undo/Redo/Select All) needs Info.plist + zh-Hans.lproj route, independent task.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `032569e` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete

---

## 2026-05-15 — sync-upstream-b9ec4f39

### Context

- `../warp` fast-forward 到 `b9ec4f39`（旧锚 `25652d73`，357 commits）
- `extract --check` 当前失败 → 翻译表必须重跑

### Action

- 跑 `cargo run -p warp-zh-extractor --release -- extract`
- Approach A：纯表同步，不翻新条目、不重 build

### Result（metadata.stats 前 → 后）

| 字段 | 25652d73 | b9ec4f39 | Δ |
|---|---|---|---|
| entry_count | 6391 | 6670 | +279 |
| translated | 735 | 728 | -7 |
| new | 5655 | 5878 | +223 |
| fuzzy | 1 | 34 | +33 |
| obsolete | 0 | 30 | +30 |
| uncertain | 4357 | 4509 | +152 |

merge log：`added=279 changed=33 unchanged=6328 obsoleted=30 hard_deleted=0`

### 回退分析

translated 减 7 条全部为合理原因：
- 4 条 → fuzzy：原文小改动（`git branch`/`tab→pane`/`up one line→down one page`/`Oz→Orchestration`）
- 2 条 → obsolete：上游删除（`Add new MCP server`、AI page API key 长句）
- 1 条边界差异

### Followups（下个 task）

- 复核 4 条 fuzzy（小修翻译即可，glossary 已就位）
- 评估新增 279 条里能直接翻译消化的部分（Cloud Agent / Custom endpoints / Billing 等）
- 1 条 `syn::parse_file` 失败（extractor WARN，count=1）— 不影响 sync 幂等，但下次扩展功能时可顺手查源


## Session 3: Sync translation table to upstream b9ec4f39

**Date**: 2026-05-15
**Task**: Sync translation table to upstream b9ec4f39
**Branch**: `main`

### Summary

Re-ran extractor against upstream warp master (25652d73..b9ec4f39, 357 commits). Net merge: added=279, changed=33, unchanged=6328, obsoleted=30. Translated 735->728 (7 affected: 4 fuzzy from real source edits like 'Copy git branch'->'Copy branch', 'tab'->'pane', 'Oz'->'Orchestration'; 2 obsoleted due to upstream deletion; 1 boundary diff). extract --check idempotent. No code changes, no spec updates required. Followups deferred: review 4 fuzzy with existing translations, plan translation of 279 new entries by feature area (Cloud Agent, Custom inference endpoints, Billing & Usage).

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `05f6f0d` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 4: Refresh 4 fuzzy translations after upstream sync

**Date**: 2026-05-18
**Task**: Refresh 4 fuzzy translations after upstream sync
**Branch**: `main`

### Summary

Followup to 05-15 sync. The 4 previously-translated entries that went fuzzy after upstream changes are now refreshed: 'Copy git branch'->'Copy branch' (drop git), 'Rename ... tab'->'... pane' (重命名当前窗格 per glossary), 'Scroll ... up one line'->'... down one page' (paired with sibling translated entry pattern), and '[Debug] Reset Oz Launch Modal State'->'[Debug] Reset Orchestration Launch Modal State' (Oz internal codename renamed to public concept Orchestration->编排, follows existing multi-agent orchestration->多 Agent 编排 glossary usage). stats: translated 728->732, fuzzy 34->30. extract --check idempotent. No code changes.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `95ec339` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 5: Translate next batch of new entries after upstream sync

**Date**: 2026-05-18
**Task**: Translate next batch of new entries after upstream sync
**Branch**: `main`

### Summary

Followup to 05-15 sync. Translated 116 auto_ui-verdict UI strings from the b9ec4f39 delta across 7 themes: Custom endpoints/BYOK (26), misc UI (42), billing & credits (16), remote codebase (15), cloud handoff (9), orchestration (6), agent harness (2). Excluded 27 crates/remote_server log strings + 16 app/src/remote_server/server_model.rs technical buffer errors. Stats translated 732 -> 848 (+116). Glossary 32 -> 39: credit/auto-reload/handoff/harness/BYOK/endpoint/orchestration (codifies Oz -> 编排 from 05-18 fuzzy refresh). Verification: extract --check exit 0, 116/116 placeholder integrity, trellis-check sampled 25 entries across all themes (PASS on glossary/tone/punct/canonical-form/build-spot-check). warp-zh-builder rebuilt against b9ec4f39 (4995 copied / 202 modified / 1371 replaced); cargo check -p warp PASS in 3m 25s with CARGO_NET_GIT_FETCH_WITH_CLI=true. Followup: builder skips hidden dirs; had to manually cp -r ../warp/.cargo build/warp-zh/.cargo because upstream now requires MACOSX_DEPLOYMENT_TARGET from .cargo/config.toml — worth a builder fix or spec note. 150 uncertain-verdict + 16 server_model.rs auto_ui still status=new for next batch.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `1adb63b` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 6: Translate features_page.rs batch (114 auto_ui entries)

**Date**: 2026-05-19
**Task**: Translate features_page.rs batch (114 auto_ui entries)
**Branch**: `main`

### Summary

Translated 114 auto_ui new entries in app/src/settings_view/features_page.rs (Settings > Features). Excluded 4 internal .expect() panic-msg lines (L1491/1500/1509/3082, same defer pattern as last round's server_model.rs). Stats: translated 848 -> 962 (+114), new 5762 -> 5648. Glossary unchanged (39 terms). extract --check idempotent both before and after trellis-check fixes (3 issues caught: 2 missing trailing spaces before inline link spans + 1 您/你 register violation). warp-zh-builder rebuilt; cargo check -p warp PASS in 3m00s. Builder still skips hidden dirs - had to cp .cargo/config.toml again.

### Main Changes

### Main Changes

- `translations/strings.json`：114 条 features_page.rs auto_ui new → translated；新增 batch flag `pr-settings-features-batch`；stats: translated 848 → 962（+114），new 5762 → 5648。
- `.trellis/tasks/05-19-translate-next-batch-of-new-auto-ui-entries/apply_translations.py`：114 条源→译表 + 4 行 panic-msg 排除（L1491/1500/1509/3082 的 `.expect("...")`）。
- Glossary 不变（39 条已覆盖本批所有术语：Agent / Warp / SSH / Vim / Wayland / GPU / pane / block / 命令块 / 窗格 等）。

### Themes covered (Settings → Features 单页)

| 簇 | 条数 |
|---|---|
| Modifier keys (Left/Right Option/Alt) | 4 |
| Toggle-pair labels (Warp SSH wrapper / quit warning / alias expansion / Vim 等) | 18 |
| Block / pin 布局 (Active Screen / Pin to top/bottom/left/right / Width%/Height%) | 8 |
| Tab placement & 标签页 | 3 |
| Notifications (desktop / agent / sound / toast) | 7 |
| Hotkey & startup behavior (Global hotkey / Start at login / Restore windows) | 12 |
| Block 限制 (max rows / mouse-wheel interval) | 5 |
| Shell defaults (default shell / working directory / confirm close) | 3 |
| Completions / autosuggestions (含 6 条 `{}` 占位符) | 16 |
| Vim (3) + 终端输入上下文菜单 (6) | 9 |
| Mouse/scroll/focus reporting + bell | 4 |
| Selection / copy / new tab placement | 6 |
| Linux clipboard | 2 |
| GPU / Wayland (含 `\n\nRestart Warp...` 前导换行 + `Current backend: {}`) | 8 |
| 其它 categories / wrapper headers | 9 |
| **Total** | **114** |

### Lessons / 边界情况

- **Trailing-space matters before inline link span**：L4290 `"Window positions won't be restored on Wayland. "` 和 L5371 `"Not supported on Wayland. "` 都以一个空格结尾，因为后面会拼接 `See docs.` 链接 span。trellis-check 抓到了第一遍漏掉的空格——译文必须保留 source 末尾空格。后续翻译时凡见末尾带空格的 source 都要原样保留。
- **`您` vs `你` register**：trellis-check 抓到 L5016 用了 `你的关注`，修为 `您的关注`。已在 spec 里有规则（line 85），但仍可能在长句里漏过——审校时应专门 grep `你` 字符。
- **Panic / assert defer 口径**：features_page.rs 内 4 条 `.expect("X failed to serialize")` + 1 条 `.expect("Pin position should exist...")` 与上一轮 server_model.rs 同口径排除，保持 status=new。
- **Builder 副作用**：`warp-zh-builder` 重建时会重新 copy 上游目录，但跳过隐藏目录——`.cargo/config.toml` 每次重建后需手动 `cp -r ../warp/.cargo build/warp-zh/.cargo`。已是第 2 次踩同一坑，值得后续做 builder 修复。

### Verification

- `extract --check` exit 0（两次幂等校验，含 trellis-check 修正后的第二次）。
- `warp-zh-builder` 重建 `build/warp-zh/`：copied=4994 / modified=203 / replaced=1493 / kept_english=7798 / parse_failed=1（上游既存 1 个 parse failure，与本批无关）。
- `cargo check -p warp` 两次 PASS（首次 3m01s、修正后 3m00s）。
- Placeholder integrity 100%（`{max_rows}` / `{}` × 5 / leading `\n\n` / 末尾空格 × 2 全部 verbatim）。
- Glossary spot-check：Agent / Warp / Vim / SSH / Wayland 0 mix；`您` 100% consistency（trellis-check 修正后）。

### Next Steps

- 剩余 1238 条 auto_ui new（settings_view 占 586）、4410 条 uncertain new、4 条 features_page 内部 panic msg。
- 下一轮自然候选：`teams_page.rs`(97) / `appearance_page.rs`(84) / `billing_and_usage_page.rs`(66) 任一单页，或同样规模的 mcp_servers/code/environments 组合。


### Git Commits

(No commits - planning session)

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 7: Translate teams_page.rs batch (103 auto_ui entries)

**Date**: 2026-05-19
**Task**: Translate teams_page.rs batch (103 auto_ui entries)
**Branch**: `main`

### Summary

Translated 103 auto_ui new entries in `app/src/settings_view/teams_page.rs` (Settings → Teams). Glossary +4 terms (admin / invite / plan / discoverable) → term_count 39→43. Stats: translated 962→1065 (+103), new 5648→5545. trellis-check caught 1 issue: `'Please '` trailing-space dropped on prefix half of sentence-link composition (L136 + L137 + L138 chain — same pattern as last batch's L4290 Wayland). Fixed to `'请 '`. extract --check idempotent (after first canonicalization pass). warp-zh-builder rebuilt; cargo check -p warp PASS in 3m10s.

### Main Changes

- `translations/strings.json`：103 条 teams_page.rs auto_ui new → translated；batch flag `pr-settings-teams-batch`；stats: translated 962→1065（+103），new 5648→5545。
- `translations/glossary.json`：+4 条术语（admin / invite / plan / discoverable），term_count 39→43。
- `.trellis/tasks/05-19-translate-next-batch-of-new-auto-ui-entries-settings-view-continued/apply_translations.py`：103 条源→译表 + 4 条 glossary 增补。
- Teams 页面术语锁定：`admin`→管理员、`team admin`→团队管理员、`invite`→邀请、`invite link`→邀请链接、`plan`→套餐（订阅层级）、`Lightspeed/Turbo/Build plan`→Lightspeed/Turbo/Build 套餐、`team ownership`→团队所有权、`discoverable/discoverability`→可发现/可发现性。

### Themes covered (Settings → Teams 单页)

| 簇 | 条数 |
|---|---|
| Team CRUD (create/delete/rename/leave/transfer ownership) | 14 |
| Roles (admin/member/promote/demote/remove) | 6 |
| Invite by email (placeholders / instructions / send / cancel / delete) | 12 |
| Invite by link (toggle / reset / domain restrictions) | 14 |
| Domain restrictions (add/remove/invalid/instructions) | 7 |
| Team discoverability | 5 |
| Plan & billing (Free/Build/Lightspeed/Turbo/usage limits/Stripe portal) | 13 |
| Delinquent / limit-hit copy (4 个角色 × 多模板) | 10 |
| Toast / show_error 文案（成功/失败状态） | 17 |
| 其它（offline / placeholder / sub-headers） | 5 |
| **Total** | **103** |

### Lessons / 边界情况

- **Sentence-link composition trailing space**（再次踩坑，第 3 次）：L136 `'Please '` + L137 `'update your payment information'`（link） + L138 `' to restore access.'`（leading-space suffix）拼接成完整句。前缀的尾部空格译文也必须保留：`'请 '`。规律：**只要 source 末尾有空格，译文末尾也保留空格**，无论中文语感是否需要。trellis-check 已两次抓到此类——值得在 spec 里加 explicit rule。
- **history 字段不可乱写**：本批首次尝试在 `history[]` 中追加 `{at, action, batch, note}` 失败，extractor 报 `missing field source`——history entry struct 期望含 `source` 字段。之前所有 batch 都用 `"history": []`，本批沿用空数组，flag 才是审计入口。**应在 spec 里固化：批次内不写 history，仅靠 flag tracking**。
- **canonicalize 二步法**：Python 直接 `json.dump` 的格式与 extractor canonical form 不完全一致，必须先跑一次 `extract`（不带 --check）让 extractor 重写为 canonical，再跑 `extract --check` 才会通过。两步流程已稳定。
- **Builder 隐藏目录 bug 第 3 次**：`.cargo/config.toml` 又被跳过；又手动 cp。**真该修一下 builder 了**——不能再 defer，下一轮加 task 修。
- **Glossary 新增节奏**：本批一次性加 4 条（admin/invite/plan/discoverable），teams 页面术语密度高、未来 settings 页可大量复用，值得集中入库。

### Verification

- `extract --check` exit 0（先 canonicalize 再 --check 两次幂等）。
- `warp-zh-builder` 重建：copied=4992 / modified=205 / replaced=1611 / kept_english=7680 / parse_failed=1（上游既存 1 个 parse failure 与本批无关）。
- `cargo check -p warp` PASS（首次 3m03s、trellis-check 修正后 3m10s）。
- trellis-check 自动校验：103 条 placeholder integrity 100%（`{domain}`/`{prorated_message}`/`{monthly_cost:.0}`/`{yearly_cost:.0}`/`{}` 全部 verbatim）、`你` 0 处、半角点号 0 处误用、leading/trailing space 100% 保留（含修正后的 L136 `'请 '`）。
- Glossary 一致性 spot-check：admin/管理员、Warp/Agent 不混译、Lightspeed/Turbo/Build 套餐名保留英文。

### Next Steps

- 剩余 1135 条 auto_ui new（settings_view 占 ~480）、4410 条 uncertain new、4 条 features_page 内部 panic msg。
- 下一轮自然候选：`appearance_page.rs`(84) / `billing_and_usage_page.rs`(66) / `code_page.rs`(36) 任一单页。
- **待修**：tools/builder/ 跳过隐藏目录的 bug（`.cargo/` 每次都要手动 cp）——下一轮第一件事。

### Git Commits

(No commits - implementation only; commit on user approval)

### Testing

- [OK] extract --check idempotent
- [OK] cargo check -p warp PASS (3m10s)
- [OK] trellis-check 0 issues (after 1 fix)

### Status

[OK] **Completed**

### Next Steps

- Await user approval to commit + archive.


## Session 7: Translate teams_page.rs batch (103 auto_ui entries)

**Date**: 2026-05-19
**Task**: Translate teams_page.rs batch (103 auto_ui entries)
**Branch**: `main`

### Summary

Translated 103 auto_ui new entries in app/src/settings_view/teams_page.rs (Settings → Teams). Glossary +4 terms (admin/invite/plan/discoverable) → 43. Stats: translated 962→1065, new 5648→5545. trellis-check caught 1 trailing-space drop on sentence-link prefix ('Please ' → '请 '), 3rd time hitting this pattern. extract --check idempotent; cargo check -p warp PASS in 3m10s.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `2257b5c` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete

---

## Session 8: Fix builder skipping .cargo hidden dir

**Date**: 2026-05-19
**Task**: fix-builder-skipping-cargo-hidden-dir
**Branch**: `main`

### Summary

`tools/extractor/src/walk.rs::is_ignored_dir` listed `.cargo` alongside truly generated dirs (`target`, `.git`, `node_modules`, `build`, `dist`). Builder reuses this predicate via `collect_all_files`, so `.cargo/config.toml` got silently dropped from `build/warp-zh/`, losing registry / target build config the translated copy needs to compile. Removed `.cargo` from the ignore list and added regression tests at both layers.

### Main Changes

- `tools/extractor/src/walk.rs`: drop `.cargo` from `is_ignored_dir`; add 3 unit tests (ignored dirs, `.cargo` regression case, normal dirs).
- `tools/builder/tests/build_safety.rs`: extend `build_succeeds_and_drops_marker` to write `.cargo/config.toml` into the fake source and assert it is mirrored verbatim.

### Testing

- `cargo test -p warp-zh-extractor` — 26 passed (3 new walk:: tests)
- `cargo test -p warp-zh-builder` — 21 passed (4 build_safety + 10 edge_cases + 7 lib)
- `cargo clippy --all-targets -- -D warnings` — clean
- `rustfmt --check` on touched files — clean

### Status

[OK] **Completed**

### Next Steps

- None - task complete

---

## Session 9: Translate next batch of new auto_ui entries (settings_view appearance_page)

**Date**: 2026-05-19
**Task**: translate-next-batch-of-new-auto-ui-entries-settings-view-appearance-page
**Branch**: `main`

### Summary

继续 features → teams 序列的第三批：`app/src/settings_view/appearance_page.rs` 84 条 auto_ui new 中翻译 83 条（L4341 `.expect("Cursor does not exist")` 为 panic msg，按 translation-contract defer 不译；建议日后调整 extractor heuristic 把 `.expect(...)` 排出 auto_ui pool）。新增 5 个 glossary 术语（cursor / font / opacity / blur / padding），术语数 43 → 48。

### Stats Delta

| metric | before | after | delta |
|---|---|---|---|
| translated | 1065 | 1148 | +83 |
| new | 5545 | 5462 | -83 |
| auto_ui new | 1135 | ~1052 | -83 |
| glossary terms | 43 | 48 | +5 |

### Main Changes

- `translations/strings.json`: 83 条 entries `new → translated`, 全部标 `pr-settings-appearance-batch`。
- `translations/glossary.json`: +5 terms（cursor 光标 / font 字体 / opacity 不透明度 / blur 模糊 / padding 内边距）。
- 翻译范围：cursor / font / tab bar / vertical tabs / opacity / blur / theme sync / app icon / DPI / padding / zoom 等 Appearance 设置 label & helper text。
- Glossary lock：`tab → 标签页` 全文应用（`tab bar → 标签页栏`、`tab indicators → 标签页指示器` 等）；`Warp` 保留英文（`Warp mode`）；`Classic` 作为输入模式名保留英文；`Reverse` 描述性，译为「反向」；`Oz` 保留英文。

### Testing

- `extract --check` exit 0（幂等）。
- `warp-zh-builder` 重建：copied=4992 modified=206 replaced=1700。
- `cargo check -p warp` 在 `build/warp-zh/` 通过（3m13s）。
- Spot check：placeholder integrity 100%、无「你」混用、glossary 一致性（tab/Agent）clean。

### Deferred

- L4341 「Cursor does not exist」— `.expect()` panic msg，按 translation-contract 不应进入 auto_ui pool；当前 status 保持 `new`，留待 extractor heuristic 修正。

### Status

[OK] **Completed**

### Next Steps

- 下一批候选 top files（auto_ui new）：billing_and_usage_page.rs (64)、code_page.rs (37)、privacy_page.rs (32)、environments_page.rs (30)。
