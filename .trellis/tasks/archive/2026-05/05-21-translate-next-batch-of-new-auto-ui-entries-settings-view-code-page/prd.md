# Translate next batch of new auto_ui entries (settings_view code_page)

## Goal

继续 `billing_and_usage_page.rs` 之后，处理 `status=new` 池中 `auto_ui` 的下一个高价值簇：`app/src/settings_view/code_page.rs` 的 auto_ui new entries（Settings → Code 页面，含 codebase indexing / code review / project explorer 等子区）。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计：`entry_count=6785`, `translated=1189`, `fuzzy=52`, `new=5493`，`obsolete=51`（含 sync fdd74928 后的 145 新条目）。
- `auto_ui` 池：`translated=1131`, `new=1052`, `fuzzy=20`, `obsolete=27`。
- 候选 top 文件（auto_ui new 首占口径）：
  | 文件 | auto_ui new |
  |---|---|
  | code_page.rs | 39 |
  | privacy_page.rs | ~31 |
  | environments_page.rs | ~26 |
  | update_environment_form.rs | ~38 |
  | teams_page.rs | ~22 |
- `code_page.rs` 当前 `status=new` 共 53 条（auto_ui 39 + uncertain 14），本批仅做 auto_ui 39 条。
- 主题：Codebase indexing（available / not available / too large / checking）、Code Editor and Review、Auto open code review panel、Project explorer / file tree、Global file search、AI features gate 等。
- 翻译契约（沿用 archive PRD）：placeholder 完整、快捷键修饰符原样、glossary 一致、build + `cargo check -p warp` 通过。

## Assumptions (temporary)

- 单批 39 条，规模适中（上轮 62、再上轮 83），审校风险可控。
- 选择标准与上一轮一致：`occurrences[0].file == app/src/settings_view/code_page.rs` + `audit.verdict==auto_ui` + `status==new`。
- 全部 39 条用户可见（label / helper / option / button / status text），无 panic-msg defer。
- glossary 可能新增 code-area 术语（Codebase indexing / Code Editor / Code Review / Project Explorer / File Tree 等）；多数已存在沿用。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 39 条 `status: new → translated`，`flags` 含 `pr-settings-code-batch`，`target` 非空。
- 严格遵守 placeholder/快捷键/glossary 契约。
- `extract --check` exit 0（幂等）。
- 已有 1189 条 translated 逐字保留。
- `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
- glossary 必要时增补 code-area 术语。

## Acceptance Criteria

- [ ] 39 条 entries: `status: new → translated`, `flags` 含 `pr-settings-code-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1189 条 translated 逐字保留。
- [ ] glossary 一致性：Agent / Warp / Codebase / Code Review / Project Explorer 不混译。
- [ ] placeholder integrity 100%（`{}`, `{name}`, `{0}` 等原样）。
- [ ] `您` register 一致。
- [ ] `warp-zh-builder` 重建 `build/warp-zh/`。
- [ ] `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Definition of Done

- 翻译沿用既有 tone。
- Journal 记录 stats delta。
- Task archive。

## Out of Scope

- `code_page.rs` 内 14 条 `uncertain` 条目（留作后续判例 / glossary 决议）。
- 其他 settings_view 单页（privacy / environments / update_environment_form / teams 留下一批）。
- Extractor / builder 重构。

## Decision (locked — Approach A)

**Approach A: 翻译 `app/src/settings_view/code_page.rs` 全部 39 条 auto_ui new（首占口径）**

锁定理由：settings_view 序列接力 — appearance → billing 之后 code 是单文件主题最聚焦簇；批量 39 控制风险；glossary 复用率高。

**Batch flag**: `pr-settings-code-batch`（沿 `pr-settings-billing-batch` / `pr-settings-appearance-batch` 命名风格）

## Technical Approach

1. 按 `occurrences[0].file == app/src/settings_view/code_page.rs` + `audit.verdict==auto_ui` + `status==new` 过滤选中条目。
2. 必要时增补 glossary（Codebase indexing / Project explorer / File tree 等）。
3. 主题/section 分簇翻译；写回 `target`/`status`/`flags`/`history`/`updated_at`。
4. `extract --check` 幂等校验。
5. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
6. Journal + archive。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-20-translate-next-batch-of-new-auto-ui-entries-settings-view-billing-and-usage-page/prd.md`。
