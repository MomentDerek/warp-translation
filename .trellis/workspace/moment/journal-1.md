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
