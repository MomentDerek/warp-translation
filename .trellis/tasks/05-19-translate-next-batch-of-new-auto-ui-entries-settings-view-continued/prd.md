# Translate next batch of new auto_ui entries (settings_view continued)

## Goal

继续上一轮 features_page.rs 之后，处理 `status=new` 池中 `auto_ui` 的下一个高价值簇：`app/src/settings_view/teams_page.rs` 的 103 条 auto_ui new entries（Settings → Teams 页面）。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计：`entry_count=6640`, `translated=962`, `fuzzy=30`, `new=5648`。
- `new` 池里 `auto_ui` 剩 1238（上一轮 1352 → 本轮 1238）。
- 候选 top 文件（auto_ui new 计数）：
  | 文件 | new |
  |---|---|
  | teams_page.rs | 97 (出现 103) |
  | appearance_page.rs | 84 |
  | billing_and_usage_page.rs | 66 |
  | code_page.rs | 36 |
  | environments_page.rs | 28 |
- teams_page.rs 内 entries：show_error()/show_success() toast、role/permission/invite UI 文案、team settings labels。
- teams_page.rs 内 `.expect("...")` panic msgs（L151 / L2448 / L2977）**未进入 auto_ui new 池**（已是 uncertain 或 non-extractable），无需 defer 操作。
- 翻译契约（沿用 archive PRD）：placeholder 完整、快捷键修饰符原样、glossary 一致、build + `cargo check -p warp` 通过。

## Assumptions (temporary)

- 单批 103 条，与上一轮 114 接近，控制审校风险。
- 全部 103 条用户可见（show_error/show_success/label/button），无 panic-msg defer。
- glossary 可能新增 team / role 相关条目（Owner / Admin / Member / Invite / SSO / SAML / SCIM 等）。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 103 条 `status: new → translated`，`flags` 含 `pr-settings-teams-batch`，`target` 非空。
- 严格遵守 placeholder/快捷键/glossary 契约。
- `extract --check` exit 0（幂等）。
- 已有 962 条 translated 逐字保留。
- `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
- glossary 必要时增补 team/permission 术语。

## Acceptance Criteria

- [ ] 103 条 entries: `status: new → translated`, `flags` 含 `pr-settings-teams-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 962 条 translated 逐字保留。
- [ ] glossary 一致性：Agent / Warp / Team / Owner / Admin / Member / Invite / SSO / SAML 不混译。
- [ ] placeholder integrity 100%（`{}`, `{name}` 等原样）。
- [ ] `您` register 一致（trellis-check 抓过的边界情况）。
- [ ] `warp-zh-builder` 重建 `build/warp-zh/`。
- [ ] `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Definition of Done

- 翻译沿用既有 tone。
- Journal 记录 stats delta。
- Task archive。

## Out of Scope

- 其余 4410 `uncertain` 条目。
- teams_page.rs 之外的 settings_view 单页（appearance/billing/code 等留下一批）。
- `app/src/remote_server/server_model.rs` 的 23 条 — 与前两轮口径一致 defer。
- Extractor / builder 重构（builder 跳过隐藏目录的问题已是第 2 次踩坑，仍 defer）。

## Decision (locked — Approach A)

**Approach A: 翻译 `app/src/settings_view/teams_page.rs` 全部 103 条 auto_ui new**

锁定理由：单文件第二大簇（features 之后）；主题集中（Teams settings）；批量大小 103 与上一轮 114 接近；glossary 复用率高且必要新增有边界。

**Batch flag**: `pr-settings-teams-batch`（沿 `pr-settings-features-batch` 命名风格）

## Technical Approach

1. 按 `occurrences[].file == app/src/settings_view/teams_page.rs` + `audit.verdict==auto_ui` + `status==new` 过滤选中条目。
2. 必要时增补 glossary（Owner/Admin/Member/Invite/SSO/SAML/SCIM 等团队术语）。
3. 主题/section 分簇翻译；写回 `target`/`status`/`flags`/`history`/`updated_at`。
4. `extract --check` 幂等校验。
5. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
6. Journal + archive。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`（term_count=39 截至上一轮）。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-19-translate-next-batch-of-new-auto-ui-entries/prd.md`。
