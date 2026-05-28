# Translate mcp_servers remaining files auto_ui new entries

## Goal

mcp_servers 子模块收尾批次：接力 list_page+server_card 批，处理 mcp_servers 余下 5 个文件的 32 条 `status=new` 且 `audit.verdict=auto_ui` 用户可见文案 —— `edit_page.rs` (9) + `update_modal.rs` (6) + `installation_modal.rs` (5) + `destructive_mcp_confirmation_dialog.rs` (7) + `mcp_servers_page.rs` (5)。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 list_page+server_card 收尾）：`translated=1385`, `fuzzy=52`。
- mcp_servers 域 glossary（上批已建）：`mcp_server / MCP 服务器`、`tool / 工具`、`gallery / 模板库`、`template / 模板`，复用 `Warp / Agent / MCP`。
- 5 文件 32 条主题分簇：
  - **edit_page.rs (9) · 编辑表单**：L67 `{\n    "": {\n        "serverUrl": ""\n    }\n}\n`（JSON 模板字面值）/ L147 `Edit Variables` / L194 `Only team admins and the creator of the MCP server can edit the MCP server.` / L318 `Add New MCP Server` / L320 `Edit {name} MCP Server` / L322 `Edit MCP Server` / L544 `This MCP server contains secrets. Visit Settings > Privacy to modify your secret redaction settings.` / L604 `No MCP Server specified.` / L618 `Cannot add multiple MCP servers while editing a single server.`
  - **update_modal.rs (6) · 更新弹窗**：L116 `Update {name}` / L184 `This server has {} updates available, which would you like to proceed with?` / L230 `Update from {publisher_string}` / L237 `Update from {name}` / L238 `Version {new_version}` / L430 `No updates available`
  - **installation_modal.rs (5) · 安装弹窗**：L256 `Install {name}` / L348 `Failed to parse markdown: {e:?}` / L422 `Shared from team` / L448 `Cancel` / L617 `No MCP server selected`
  - **destructive_mcp_confirmation_dialog.rs (7) · 删除确认**：L62 `Delete MCP server?` / L63 `This will uninstall and remove this MCP server from all your devices.` / L64 `Delete MCP` / L68 `Delete shared MCP server?` / L69 `This will not only delete this MCP server for yourself, but also uninstall and remove this MCP server from Warp and across all of ` (拼接段，末尾空格 + team 名) / L74 `Remove shared MCP server from team?` / L75 `This will uninstall and remove this MCP server from Warp and across all of your teammates' devices.`
  - **mcp_servers_page.rs (5) · 顶层 toast/error**：L149 `Successfully logged out of {name} MCP server` / L150 `Successfully logged out of MCP server` / L317 `Finish the current MCP install before opening another install link.` / L332 `Unknown MCP server '{autoinstall_param}'` / L360 `MCP server '{gallery_title}' cannot be installed from this link.`
- 翻译契约（沿用前批 PRD）：placeholder 完整、全角中文标点、glossary 一致、build + `cargo check -p warp` 通过。

## Assumptions

- 单批 32 条，规模与上一批 mcp_servers(29) 接近，与 teams+referrals(36) 相当。
- 选择标准：`occurrence.file ∈ {edit_page.rs, update_modal.rs, installation_modal.rs, destructive_mcp_confirmation_dialog.rs, mcp_servers_page.rs}` + `audit.verdict==auto_ui` + `status==new`。
- L67 JSON 模板字面值：保留原样，**不翻译**（属于用户配置模板）。
- L69 末尾空格保留（与团队名拼接）。
- L348 `{e:?}` Rust Debug 占位符保留。
- glossary 新增预估 0–2 条（多数复用上批 MCP 词族）。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 32 条 `status: new → translated`，`flags` 含 `pr-settings-mcp-servers-remaining-batch`，`target` 非空。
- 严格遵守 placeholder（`{}`, `{name}`, `{publisher_string}`, `{new_version}`, `{autoinstall_param}`, `{gallery_title}`, `{e:?}` 原样）/快捷键/glossary 契约。
- L67 视为模板字面值：`target` 与 `source` 一致（不翻译）。
- L69 末尾尾随空格逐字保留。
- 全角中文标点。`...` → `……`。`>` 路径分隔符（如 `Settings > Privacy`）保留半角并替换为「设置 > 隐私」。
- `extract --check` exit 0（幂等）。
- 已有 1385 条 translated 逐字保留。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 32 条 entries: `status: new → translated`, `flags` 含 `pr-settings-mcp-servers-remaining-batch`, 非空 `target`。
- [ ] L67 JSON 模板 target == source（保留原样）。
- [ ] L69 末尾空格保留。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1385 条 translated 逐字保留。
- [ ] glossary 一致性：Warp / Agent / MCP / MCP 服务器 / 您-register 不混译。
- [ ] placeholder integrity 100%。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone（settings 区域偏正式，对用户使用「您」）。
- Journal 记录 stats delta + notable decisions。
- Task archive。

## Out of Scope

- mcp_servers 其他 `verdict=uncertain` 条目（约 12+ 条，留 uncertain 专项 sweep）。
- 其他 settings_view 单页（execution_profile / agent_assisted_environment_modal / main_page / warpify_page 等）。

## Decision (locked — Approach A)

**Approach A: mcp_servers 子目录收尾批 32 条 auto_ui new**

锁定理由：续完 mcp_servers 子目录，让该模块所有 auto_ui 条目一次清空，glossary 词族在同一时间窗口内固化，避免后续散批回头修订。

**Batch flag**: `pr-settings-mcp-servers-remaining-batch`

## Technical Approach

1. 按 `any(occurrence.file ∈ {5 文件})` + `audit.verdict==auto_ui` + `status==new` 过滤，得 32 条。
2. glossary 检查复用（mcp_server / tool / gallery / template 已存在），按需小幅增补。
3. 按主题簇翻译，写回 `target` / `status` / `flags` / `updated_at`。
4. 特殊处理：
   - L67：`TRANSLATIONS[id] = source` 原样保留（JSON 模板）。
   - L69：拼接段末尾空格不丢。
   - L348：`{e:?}` Rust Debug 占位符原样。
   - L544：`Settings > Privacy` → `「设置」>「隐私」`（保留 `>`）。
5. apply 脚本沿用上批模板（全角标点 invariant + history 留空惯例 + 占位符内放行）。
6. `extract --check` 幂等校验。
7. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
8. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 源码上下文（5 文件）:
  - `../warp/app/src/settings_view/mcp_servers/edit_page.rs`
  - `../warp/app/src/settings_view/mcp_servers/update_modal.rs`
  - `../warp/app/src/settings_view/mcp_servers/installation_modal.rs`
  - `../warp/app/src/settings_view/mcp_servers/destructive_mcp_confirmation_dialog.rs`
  - `../warp/app/src/settings_view/mcp_servers_page.rs`
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-22-translate-mcp-servers-list-page-rs-server-card-rs-auto-ui-new-entries/prd.md`。
- 上轮 apply 脚本: `.trellis/tasks/archive/2026-05/05-22-translate-mcp-servers-list-page-rs-server-card-rs-auto-ui-new-entries/apply_translations.py`。
- 候选 entry 行号清单（32）：
  - edit_page.rs: L67, L147, L194, L318, L320, L322, L544, L604, L618
  - update_modal.rs: L116, L184, L230, L237, L238, L430
  - installation_modal.rs: L256, L348, L422, L448, L617
  - destructive_mcp_confirmation_dialog.rs: L62, L63, L64, L68, L69, L74, L75
  - mcp_servers_page.rs: L149, L150, L317, L332, L360
