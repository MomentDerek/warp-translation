# Translate next batch of new auto_ui entries

## Goal

继续上一轮（05-18 b9ec4f39 sync 后的 116 条）之后，处理 `status=new` 池中剩余的 **1352 条 `auto_ui`-verdict** 条目里下一个高价值簇，保持 `extract --check` 幂等、build 与 `cargo check` 通过。

## What I already know

- 当前 `translations/strings.json` 统计：`entry_count=6670`, `translated=848`, `fuzzy=30`, `obsolete=30`, `new=5762`。
- `new` 池里 `auto_ui` 共 1352，`uncertain` 共 4410。
- `auto_ui` 的 top-level 分布：`app/`=1300, `crates/`=52（其中 `app/src/settings_view/` 占 704）。
- `settings_view` 内部 auto_ui 分布（前几位）：
  | 文件 | auto_ui new |
  |---|---|
  | features_page.rs | 118 |
  | teams_page.rs | 97 |
  | appearance_page.rs | 84 |
  | billing_and_usage_page.rs | 66 |
  | mcp_servers/* | 59 |
  | code_page.rs | 36 |
  | environments_page.rs | 28 |
  | privacy_page.rs | 27 |
  | update_environment_form.rs | 25 |
- 非 settings_view 的 auto_ui top 文件（每个 8–23 条）：`remote_server/server_model.rs`（23 — 上一轮已 defer，技术 buffer/diff error）、`resource_center/sections.rs`(22)、`notebooks/editor/view.rs`(20)、`ai/blocklist/agent_view/...`(18)、`quit_warning/mod.rs`(16)、`workspace/view.rs`(16) 等。
- 上一轮（05-18）批次大小：116 条（7 个主题簇），约 1 个 PR / 1 个 task。glossary `term_count` 已从 32 → 39。
- 翻译契约（来自 archive PRD）：placeholder 完整、快捷键修饰符原样、glossary 一致、build + `cargo check -p warp` 通过。

## Assumptions (temporary)

- 优先翻译 settings_view 系列（占整池 52%，UX 可见度最高，每个 page 自带主题边界，glossary 复用率高）。
- 单批仍按 ~100–150 条目标，与上一轮节奏一致；避免一次性吞 700+ 引入审校风险。
- 非 settings 的零散 UI（quit_warning、resource_center、ai/blocklist、workspace 等）放到后续批次，因为它们主题分散、需要逐文件读上下文。

## Open Questions (blocking)

- (none — scope locked, see Decision)

## Requirements (evolving)

- 选中条目 `status: new → translated`，`flags` 含本轮 batch tag，`target` 非空且符合 placeholder/快捷键/glossary 契约。
- `extract --check` exit 0（幂等）。
- 已有 848 条 translated 逐字保留。
- `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
- glossary 仅在新主题强制要求时增补（如新出现的 settings 概念）。

## Acceptance Criteria (final)

- [ ] 114 条 entries: `status: new → translated`, `flags` 含 `pr-settings-features-batch`, 非空 `target`。
- [ ] 4 条 `.expect()` panic 条目保持 `status=new`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 848 条 translated 逐字保留（diff 仅新增 114 条变更 + 4 条 audit-only 不变）。
- [ ] glossary 一致性 spot-check：Agent / 命令块 / 窗格 / 编排 / 积分 / Warp / GPU / Wayland 等不混译；快捷键修饰符（⌘/⌥/⇧/⌃/Ctrl/Tab）原样保留。
- [ ] placeholder integrity 100%（`{max_rows}`, `{}`, 占位符全部原样）。
- [ ] `warp-zh-builder` 重建 `build/warp-zh/`。
- [ ] `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Definition of Done

- 翻译沿用既有 tone（命令式简洁，settings 标签语态）。
- Journal 记录 stats delta。
- Task archive。

## Out of Scope (explicit)

- 4410 `uncertain` 条目（多为带 placeholder 的 log/error）— 留到 uncertain 轮。
- `app/src/remote_server/server_model.rs` 的 23 条技术 buffer/diff error — 与上一轮口径一致，defer。
- Extractor / builder 重构。

## Decision (locked — Approach A)

**Approach A: 仅翻译 `app/src/settings_view/features_page.rs` 的 118 条 auto_ui new**

锁定理由：单文件最大簇（主题集中 = Settings → Features 各 toggle/label）；批量大小与上一轮 116 接近；context 切换最少；glossary 复用率最高。

**Final selection: 114 条** — 排除 4 条内部 `.expect()` panic 消息（非用户可见，与上轮 server_model.rs 一致口径）：
| Line | Source | 排除原因 |
|---|---|---|
| 1491 | `MouseReportingEnabled failed to serialize` | `.expect(...)` panic msg |
| 1500 | `ScrollReportingEnabled failed to serialize` | `.expect(...)` panic msg |
| 1509 | `FocusReportingEnabled failed to serialize` | `.expect(...)` panic msg |
| 3082 | `Pin position should exist in default size percentages` | `.expect(...)` panic msg |

剩余 4 条仍保持 `status=new`，留待 uncertain 轮或 defer。

**Batch flag**: `pr-settings-features-batch`（沿 `pr-menu-batch` / `pr-post-sync-batch` 命名风格）

## Technical Approach

1. （若选 settings 页）按文件 + verdict 过滤选中条目。
2. 必要时增补 glossary（settings 专属术语）。
3. 主题/section 分簇翻译；写回 `target`/`status`/`flags`/`history`/`updated_at`。
4. `extract --check` 幂等校验。
5. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
6. Journal + archive。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`（term_count=39）。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 上轮 PRD 参考: `.trellis/tasks/archive/2026-05/05-18-translate-next-batch-of-new-entries-after-upstream-sync/prd.md`。
- 上轮 fuzzy 处理: `.trellis/tasks/archive/2026-05/05-18-refresh-fuzzy-translations/prd.md`。
