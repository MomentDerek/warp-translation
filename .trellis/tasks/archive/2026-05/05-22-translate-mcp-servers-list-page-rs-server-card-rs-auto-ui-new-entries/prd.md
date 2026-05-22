# Translate mcp_servers list_page.rs + server_card.rs auto_ui new entries

## Goal

接力 settings_view 翻译序列（teams + referrals → mcp_servers/{list_page, server_card}），转入 MCP servers 子模块：处理 `app/src/settings_view/mcp_servers/list_page.rs` 17 条 + `app/src/settings_view/mcp_servers/server_card.rs` 12 条 = 共 29 条 `status=new` 且 `audit.verdict=auto_ui` 的用户可见文案。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 teams + referrals 收尾）：`translated=1356`, `fuzzy=52`。
- `list_page.rs` 17 条：MCP 列表页（页面 description / 空态 / 搜索 / 自动检测开关 / 分组 header / 来源标签）。
- `server_card.rs` 12 条：单个服务器卡片（运行状态 toast / 工具列表空态 / metadata / 卡片操作按钮）。
- 现 glossary 已有 `mcp / MCP`（推定既有）、Warp / Agent / AI / 您-register。本批需补充：`mcp_server / MCP 服务器`、`tool / 工具`（如未存在）、`config_file / 配置文件`、`gallery / 模板库`。
- 主题分簇：
  - **list_page.rs · 页面引导**：L78 长 description（推荐 MCP 用途）/ L104 空态 / L105 无搜索结果 / L230 搜索框 / L1187 `Learn more.`
  - **list_page.rs · 自动检测开关**：L1146 长描述（auto-detect 全局第三方 AI agent 配置文件）
  - **list_page.rs · 分组 / 来源标签**：L376 `Available to install` / L844 `MCP server updated` toast / L1271 `My MCPs` / L1283/L1284/L1295 `Shared by Warp and ...` 系列 / L1304/L1641 `Detected from ...` / L1775/L1776 `Shared by ...` / L1779 `From another device`
  - **server_card.rs · 运行状态 toast**：L257 `Starting server...` / L317 `Shutting down...`
  - **server_card.rs · 工具与 metadata**：L494 `No tools available` / L623 `Template sync id: {}` / L633 `Gallery Id: {uuid}` / L634 `Gallery Id: None` / L641 `Could not find cloud template`
  - **server_card.rs · 卡片按钮**：L765 `Show logs` / L795 `Share server` / L848 `Edit config` / L864 `Set up` / L912 `Server update available`
- 翻译契约（沿用前批 PRD）：placeholder 完整、全角中文标点、glossary 一致、build + `cargo check -p warp` 通过。
- apply 脚本 stats 位置错位 known issue 仍未修；若 `extract --check` 首轮失败需 canonicalize 一轮。

## Assumptions

- 双文件合并单批 29 条，规模与前批接近（teams+referrals 36 / update_env_form 30）。
- 选择标准：`occurrence.file ∈ {.../mcp_servers/list_page.rs, .../mcp_servers/server_card.rs}` + `audit.verdict==auto_ui` + `status==new`。
- 全部 29 条为用户可见 description / placeholder / button / toast / status / 分组 header / metadata label。
- Glossary 新增预估 2-4 条（MCP 服务器 / 工具 / 配置文件 / 模板库），同时复用 ambient agent / Warp 等。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 29 条 `status: new → translated`，`flags` 含 `pr-settings-mcp-servers-list-card-batch`，`target` 非空。
- 严格遵守 placeholder（`{}`, `{name}`, `{creator}`, `{uuid}` 原样）/快捷键/glossary 契约。
- 全角中文标点（避免半角 `,` `.` `?` `!`，URL/regex/code/file path 字面值除外）。`...` 译为 `……`。
- `MCP` / `Warp` / `Agent` / `ambient agent` 保留原 case。
- L1146 中 `(e.g. ...)` 括号内文件路径示例保留原样。
- `extract --check` exit 0（幂等）。
- 已有 1356 条 translated 逐字保留。
- glossary 必要时增补 mcp_server / tool / config_file / gallery 域术语。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 29 条 entries: `status: new → translated`, `flags` 含 `pr-settings-mcp-servers-list-card-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1356 条 translated 逐字保留。
- [ ] glossary 一致性：Warp / Agent / AI / MCP / MCP 服务器 / 您-register 不混译。
- [ ] placeholder integrity 100%（含 `{name}` / `{creator}` / `{uuid}` named placeholder + 普通 `{}`）。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone（settings 区域偏正式，对用户使用「您」）。
- Journal 记录 stats delta + notable decisions。
- Task archive。

## Out of Scope

- mcp_servers 其他文件：`edit_page.rs` (9) / `installation_modal.rs` (5) / `update_modal.rs` (6) / `destructive_mcp_confirmation_dialog.rs` (7) / `mcp_servers_page.rs` (5)（留下一批 mcp 收尾）。
- 12+ 条 `verdict=uncertain` 条目（uncertain 专项 sweep）。
- 其他 settings_view 单页（execution_profile / agent_assisted_environment_modal / main_page / warpify_page 等留下批）。
- Extractor / builder 重构、translation-contract spec 修订。

## Decision (locked — Approach A)

**Approach A: 双文件合并批 mcp_servers/list_page + server_card 共 29 条 auto_ui new**

锁定理由：mcp_servers 子目录是一个独立功能模块，list_page 与 server_card 是父子结构（列表 + 卡片细节），术语高度共享（MCP 服务器 / 工具 / gallery / 配置）；合并一批可一次性铺设 MCP 域 glossary 词族，为后续 edit_page / installation_modal / update_modal / mcp_servers_page 子批做术语预热。

**Batch flag**: `pr-settings-mcp-servers-list-card-batch`

## Technical Approach

1. 按 `any(occurrence.file ∈ {list_page.rs, server_card.rs})` + `audit.verdict==auto_ui` + `status==new` 过滤，得 29 条。
2. 增补 glossary（mcp_server / tool / config_file / gallery 等），复用既有 MCP / Warp / Agent。
3. 按主题簇翻译，写回 `target` / `status` / `flags` / `updated_at`（沿用上批 history 留空惯例）。
4. apply 脚本沿用上批模板（含全角标点 invariant；URL/file-path/regex/`{}` placeholder 内字面值放行；`...` → `……`）。
5. `extract --check` 幂等校验；如需 canonicalize 跑一轮。
6. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
7. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 源码上下文:
  - `<HOME>/Documents/Codes/warp/app/src/settings_view/mcp_servers/list_page.rs`（L78-1779）
  - `<HOME>/Documents/Codes/warp/app/src/settings_view/mcp_servers/server_card.rs`（L257-912）
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-22-translate-teams-page-rs-referrals-page-rs-auto-ui-new-entries/prd.md`。
- 上轮 apply 脚本：`.trellis/tasks/archive/2026-05/05-22-translate-teams-page-rs-referrals-page-rs-auto-ui-new-entries/apply_translations.py`。
- 候选 entry 清单（29 条）：
  - list_page.rs (17): L78, L104, L105, L230, L376, L844, L1146, L1187, L1271, L1283, L1284, L1295, L1304, L1641, L1775, L1776, L1779
  - server_card.rs (12): L257, L317, L494, L623, L633, L634, L641, L765, L795, L848, L864, L912
