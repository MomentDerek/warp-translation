# Translate cli_agent_sessions auto_ui new entries — 31 entries (plugin_manager batch)

## Goal

清扫 `app/src/terminal/cli_agent_sessions/*` 子目录全部 `status=new` + `audit.verdict=auto_ui` 用户可见文案，共 **31 条** 横跨 **6 个文件**（5 个 plugin_manager 子模块 + 1 个 cli_agent_sessions/mod.rs）。继 terminal/view + command_palette 78 条之后，使 auto_ui new 余量从 652 → 621（-31）。

## What I already know

- 当前 `strings.json` 统计：`translated=1589`, `fuzzy=52`, `new=5093`（auto_ui 652 / uncertain 4441）。
- 总热点扫荡顺序：ai/blocklist 94 ✅ → terminal/view + command_palette 78 ✅ → **cli_agent_sessions 31（本批）** → notebooks/editor 23 / server_model.rs 23 / resource_center 22 …
- glossary 现有 89 条；本批所有英文产品名（Warp / Claude Code / Codex / Gemini CLI / OpenCode / jq / Docker / JSON / config.toml）均按既有规则字面保留。需新增 4 个候选 glossary 条目：
  - `plugin` → 插件
  - `extension` → 扩展（Gemini CLI 上下文用，与 plugin 同义但源文本用词不同）
  - `marketplace` → 插件市场（Claude Code plugin marketplace 概念）
  - `notification` → 通知（Codex notifications 上下文）

## Scope by file

### cli_agent_sessions/mod.rs (1)
- L207 `Waiting for your answer` — Agent 等待用户回复时的状态提示

### plugin_manager/claude.rs (10)
- L117 `Plugin update did not take effect` — 插件更新后版本未变化时的错误消息（`PluginInstallError.message`）
- L166 `Install Warp Plugin for Claude Code` — 安装指引弹窗标题
- L167 `Ensure that jq is installed on your machine. Then, run these commands.` — 副标题；`jq` 字面保留
- L170 `Add the Warp plugin marketplace repository` — 步骤 1 描述
- L176 `Install the Warp plugin` — 步骤 2 描述
- L191 `Update Warp Plugin for Claude Code` — 更新指引标题
- L192 `Run the following commands.` — 副标题
- L195 `Remove the existing marketplace (if present)` — 步骤 1 描述
- L201 `Re-add the marketplace` — 步骤 2 描述
- L207 `Install the latest plugin version` — 步骤 3 描述

### plugin_manager/codex.rs (4)
- L34 `Enable Warp Notifications for Codex` — 启用通知指引标题（`Codex` 字面保留）
- L35 长句 `Update Codex to the latest version, then enable in-focus notifications so Warp can display them while you work.` — 副标题
- L38 `Update Codex to the latest version.` — 步骤 1 描述
- L44 `Set the notification condition to "always" in your Codex config. Open or create ~/.codex/config.toml and add:` — 步骤 2；**`"always"` 与 `~/.codex/config.toml` 字面保留**

### plugin_manager/gemini.rs (5)
- L127 `Install Warp Plugin for Gemini CLI` — 标题（`Gemini CLI` 字面保留）
- L128 `Run the following command, then restart Gemini CLI.` — 副标题
- L130 `Install the Warp extension` — 步骤描述（注意：Gemini 用 "extension" 而不是 "plugin"，对应译 "扩展"）
- L140 `Update Warp Plugin for Gemini CLI` — 更新标题
- L143 `Update the Warp extension` — 更新步骤描述

### plugin_manager/mod.rs (4)
- L124 `'{display_cmd}' failed` — 子进程失败错误消息；**`{display_cmd}` 占位符 + 单引号包裹必须保留**
- L131 `failed to run '{display_cmd}'` — 子进程无法启动错误消息；**`{display_cmd}` 占位符 + 单引号包裹必须保留**
- L167 `Auto-install not supported for this agent` — 默认 trait 实现错误
- L176 `Auto-update not supported for this agent` — 默认 trait 实现错误

### plugin_manager/opencode.rs (7)
- L36 `Install Warp Plugin for OpenCode` — 标题（`OpenCode` 字面保留）
- L38 `Add the Warp plugin to your OpenCode configuration, then restart OpenCode.` — 副标题
- L41 长句 `Open or create your opencode.json. This can be in your project root, or the global config path:` — 步骤 1；**`opencode.json` 字面保留**
- L47 `Add "@warp-dot-dev/opencode-warp" to the "plugin" array in the top-level JSON object:` — 步骤 2；**`"@warp-dot-dev/opencode-warp"` 与 `"plugin"` JSON 字面保留，含双引号**
- L59 `Update Warp Plugin for OpenCode` — 更新标题
- L60 长句 `Pin the plugin to the latest version in your opencode.json. OpenCode caches plugins per version spec, so changing the pin forces it to re-fetch on restart.` — 副标题
- L69 `Replace the existing "@warp-dot-dev/opencode-warp" entry in the "plugin" array with the explicit version:` — 步骤；**JSON 字面保留**

## Special literal / placeholder protections

| 锚点 | 规则 |
|---|---|
| `{display_cmd}` (mod.rs L124/L131) | 占位符 + 包围的 ASCII 单引号 `'…'` 完整保留 |
| `~/.codex/config.toml` (codex.rs L44) | 文件路径字面保留 |
| `"always"` (codex.rs L44) | JSON 字符串字面（含双引号）保留 |
| `opencode.json` (opencode.rs L41/L60/L69) | 文件名字面保留 |
| `"@warp-dot-dev/opencode-warp"` (opencode.rs L47/L69) | NPM 包名字面（含双引号）保留 |
| `"plugin"` (opencode.rs L47/L69) | JSON 键字面（含双引号）保留 |
| `jq` (claude.rs L167) | 命令名字面保留 |
| `Warp` / `Claude Code` / `Codex` / `Gemini CLI` / `OpenCode` | 产品名字面保留 |
| `Warp Plugin` / `Warp extension` / `Warp Notifications` | 「Warp 插件」/「Warp 扩展」/「Warp 通知」 |

## Glossary additions

新增 4 条术语（不与既有冲突）：
- `plugin` → 插件
- `extension` → 扩展（注解：与 plugin 同义，按源文本用词分别译）
- `marketplace` → 插件市场（Claude Code 上下文）
- `notification` → 通知

## Acceptance criteria

1. `translations/strings.json` 中所有 31 条 entry 的 `status` 从 `new` → `translated`，`target` 填入中文译文；`audit.verdict=auto_ui` 不变；`flags` 追加 `pr-cli-agent-sessions-plugin-manager-batch`。
2. 全部占位符 `{display_cmd}` 保留；ASCII 单引号 `'…'` 保留；所有品牌字面（Warp/Codex/Claude Code/Gemini CLI/OpenCode/jq）保留；文件路径与 JSON 字面值保留。
3. CJK 邻接半角标点检查通过；无 ASCII `...`（用 `……`）；shell-prompt vs AI-prompt 此批不涉及。
4. `glossary.json` 新增 4 条（plugin/extension/marketplace/notification）；`term_count` 89 → 93。
5. `metadata.stats` 重算：translated 1589→1620，new 5093→5062，auto_ui 余量 652→621。
6. 既有 1589 条 translated 条目 byte-identical 不被触碰。
7. Commit message 形如 `chore(translations): translate 31 cli_agent_sessions plugin_manager auto_ui entries`。
