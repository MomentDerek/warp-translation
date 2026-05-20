# Translate next batch of new auto_ui entries (settings_view appearance_page)

## Goal

继续上一轮 `teams_page.rs` 之后，处理 `status=new` 池中 `auto_ui` 的下一个高价值簇：`app/src/settings_view/appearance_page.rs` 的 auto_ui new entries（Settings → Appearance 页面）。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计：`entry_count=6640`, `translated=1065`, `fuzzy=30`, `new=5545`。
- `auto_ui` new 池剩 1135（上一轮 1238 → 本轮 1135）。
- 候选 top 文件（auto_ui new 计数）：
  | 文件 | new |
  |---|---|
  | appearance_page.rs | 84（首占）/ 89（任意 occurrence） |
  | billing_and_usage_page.rs | 64 |
  | code_page.rs | 37 |
  | privacy_page.rs | 32 |
  | environments_page.rs | 30 |
- appearance_page.rs 主题：theme / font / cursor / tab bar / window chrome / app icon / opacity 等外观与字体类设置 label & helper text。
- 翻译契约（沿用 archive PRD）：placeholder 完整、快捷键修饰符原样、glossary 一致、build + `cargo check -p warp` 通过。

## Assumptions (temporary)

- 单批 84 条（按首占口径选择），与上一轮 103 接近，控制审校风险。
- 选择标准与上一轮一致：`occurrences[0].file == app/src/settings_view/appearance_page.rs` + `audit.verdict==auto_ui` + `status==new`。
- 全部 84 条用户可见（label / helper / option / button），无 panic-msg defer。
- glossary 可能新增 appearance 相关条目（Theme / Light / Dark / Cursor / Tab bar / Window / Opacity / Blur / Padding 等）。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 84 条 `status: new → translated`，`flags` 含 `pr-settings-appearance-batch`，`target` 非空。
- 严格遵守 placeholder/快捷键/glossary 契约。
- `extract --check` exit 0（幂等）。
- 已有 1065 条 translated 逐字保留。
- `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
- glossary 必要时增补 appearance 术语。

## Acceptance Criteria

- [ ] 84 条 entries: `status: new → translated`, `flags` 含 `pr-settings-appearance-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1065 条 translated 逐字保留。
- [ ] glossary 一致性：Agent / Warp / Theme / Light / Dark / Cursor / Tab / Window / Padding / Opacity 不混译。
- [ ] placeholder integrity 100%（`{}`, `{name}` 等原样）。
- [ ] `您` register 一致（trellis-check 抓过的边界情况）。
- [ ] `warp-zh-builder` 重建 `build/warp-zh/`。
- [ ] `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Definition of Done

- 翻译沿用既有 tone。
- Journal 记录 stats delta。
- Task archive。

## Out of Scope

- 其余 `uncertain` 条目。
- appearance_page.rs 之外的 settings_view 单页（billing/code/privacy/environments 留下一批）。
- `app/src/remote_server/server_model.rs` 的 23 条 — 与既有口径一致 defer。
- Extractor / builder 重构（builder 跳过隐藏目录的问题已独立任务）。

## Decision (locked — Approach A)

**Approach A: 翻译 `app/src/settings_view/appearance_page.rs` 全部 84 条 auto_ui new（首占口径）**

锁定理由：settings_view 系列中 features / teams 之后单文件最大簇；主题集中（Appearance settings）；批量大小 84 与上一轮 103 接近；glossary 复用率高且必要新增有边界。

**Batch flag**: `pr-settings-appearance-batch`（沿 `pr-settings-teams-batch` 命名风格）

## Technical Approach

1. 按 `occurrences[0].file == app/src/settings_view/appearance_page.rs` + `audit.verdict==auto_ui` + `status==new` 过滤选中条目。
2. 必要时增补 glossary（Theme/Light/Dark/Cursor/Tab bar/Window/Padding/Opacity/Blur 等外观术语）。
3. 主题/section 分簇翻译；写回 `target`/`status`/`flags`/`history`/`updated_at`。
4. `extract --check` 幂等校验。
5. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
6. Journal + archive。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`（term_count=43 截至上一轮）。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-19-translate-next-batch-of-new-auto-ui-entries-settings-view-continued/prd.md`。
