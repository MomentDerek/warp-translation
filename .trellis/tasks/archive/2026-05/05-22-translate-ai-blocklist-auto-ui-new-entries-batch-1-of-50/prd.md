# Translate ai/blocklist auto_ui new entries — batch 1 (Agent control cluster, 51 entries)

## Goal

启动 `app/src/ai/blocklist` 子目录的翻译推进。本批次（共 51 条 `status=new` 且 `audit.verdict=auto_ui` 用户可见文案）聚焦 **Agent 输入栏 + 内联 Agent 控制面板** 集群：`agent_input_footer/*` (20) + `inline_agent_view_header.rs` (6) + `orchestration_pill_bar.rs` (2) + `zero_state_block.rs` (2) + `block/view_impl/{common.rs,orchestration.rs}` (5) + `inline_action/{requested_command.rs,orchestration_controls.rs}` (16)。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 mcp_servers 收尾后）：`translated=1417`, `fuzzy=52`, `new=5265`。
- `ai/blocklist` 子目录共 94 条 `auto_ui new`（最大热点）。本批切走 51 条，剩 43 条留下批。
- 已有 glossary 覆盖核心词族：`agent → Agent`（产品名保留）、`block → 命令块`、`pane → 窗格`、`tab → 标签页`、`command → 命令`、`model → 模型`、`MCP → MCP`、`API → API`、`API key → API 密钥`、`Agent Mode → Agent 模式`、`ambient agent`（保留英文）、`mcp_server → MCP 服务器`。
- 文件 + 行号分簇：
  - **agent_input_footer/mod.rs (19) · Agent 输入栏工具条 tooltip + 状态**：L129 `Enable terminal command autodetection` / L130 `Disable terminal command autodetection` / L132 `Turn off auto-approve all agent actions` / L133 `Auto-approve all agent actions for this task` / L135 `Start remote control` / L136 `Log in to use /remote-control` / L305 `Voice input` / L341 `Attach file` / L369 `Hand off to cloud (or type &)` / L380 `File explorer` / L382 `Open file explorer` / L397 `Open Rich Input` / L412 `Open coding agent settings` / L424 `Install the Warp plugin to enable rich agent notifications within Warp` / L437 `View instructions to install the Warp plugin` / L451 `A new version of the Warp plugin is available` / L463 `View instructions to update the Warp plugin` / L603 `Context window usage` / L1285 `No plugin manager available`
  - **agent_input_footer/environment_selector.rs (1)**：L210 `Choose an environment`
  - **agent_view/inline_agent_view_header.rs (6) · Agent 状态标签**：L24 `Prompt agent to interact with` / L25 `Agent is waiting on instructions` / L26 `Agent is waiting for command to exit` / L27 `Agent needs your permission to continue` / L28 `Agent is in control` / L29 `User is in control`
  - **agent_view/orchestration_pill_bar.rs (2)**：L443 `Open in new pane` / L448 `Open in new tab`
  - **agent_view/zero_state_block.rs (2)**：L409 `New Oz cloud agent conversation` / L425 `New Oz agent conversation`
  - **block/view_impl/common.rs (4)**：L127 `Agent waiting for instructions...` / L130 `I'm sorry, I couldn't complete that request.` / L971 `Ask the agent to check this command now, skipping its timer.` / L3131 `Edit API Keys`
  - **block/view_impl/orchestration.rs (1)**：L48 `Generating title...`
  - **inline_action/requested_command.rs (12) · Agent run command 提示集**：L85 `Generating command...` / L86 `OK if I run this command and read the output?` / L87 `OK if I call this MCP tool?` / L88 `Agent is monitoring command...` / L89 `Agent needs your input to continue` / L90 `User is in control.` / L91 `Paused agent. User is in control.` / L92 `User in control` / L93 `Agent ran into an issue. Take over control.` / L94 `Viewing command detail` / L95 `Viewing MCP tool call detail` / L161 `Edit requested command`
  - **inline_action/orchestration_controls.rs (4)**：L70 `Default model` / L74 `Skip (advanced)` / L77 `New API key…` / L1866 `Agent harness`

## Assumptions

- 本批 51 条，规模与上一批 mcp_servers 收尾 (32) 接近，与最大批 36 略大。50 上下的批量节奏在过往任务中验证可控。
- 选择标准：`occurrence.file ∈ {9 文件}` + `audit.verdict==auto_ui` + `status==new`。详细 ID/source/file/line 已固化为 `candidates.json`。
- 特殊字面值保护：
  - L369 `Hand off to cloud (or type &)` —— `&` 是 Rich Input 的 mode-switch 字符，逐字保留（不替换为全角）。
  - L136 `Log in to use /remote-control` —— `/remote-control` 是斜杠命令名，保留半角小写。
  - L409 / L425 `Oz cloud agent conversation` / `Oz agent conversation` —— `Oz` 是 Warp 内部代号（cloud-agent 系列）；按 glossary 保守策略保留 `Oz`，与 `Agent` 并列：`新建 Oz 云端 Agent 会话` / `新建 Oz Agent 会话`。
  - L3131 `Edit API Keys` —— `API` 大写保留，glossary `API key → API 密钥`，按上下文译为「编辑 API 密钥」。
  - L77 `New API key…` —— 末尾省略号已是 `…` U+2026，保留。
  - 所有 `...`（三个 ASCII 点）→ `……`（U+2026 × 2）。
- glossary 增补预估 0–2 条（多数复用既有词族）。候选新增：
  - `take over control` → 「接管控制权」（统一 L93 / 其他后续批次）。
  - `in control` 短语：`Agent is in control` → 「Agent 正在控制」/ `User is in control` → 「您在控制」（统一 L28/L29/L90/L92）。
  - `Rich Input` → 「富文本输入」（L397）。

## Open Questions (blocking)

- (none — scope locked, glossary 词族已成熟)

## Requirements

- 选中 51 条 entries: `status: new → translated`，`flags` 含 `pr-ai-blocklist-agent-control-batch`，`target` 非空。
- 严格遵守 placeholder（无名称占位符；保留 `{}` 若有）/快捷键/glossary 契约。
- L369 `&` 字面保留半角；L136 `/remote-control` 字面保留；`Oz` 字面保留；`API` 大写保留。
- 全角中文标点。`...` → `……`。`?` → `？`、`,` → `，`、`.` → `。`、`!` → `！`。`-` 在 `At Limit -` 类拼接段保留。
- `extract --check` exit 0（幂等）。
- 已有 1417 条 translated 逐字保留，glossary 现有 81 条不破坏。
- 控制权语义在本批内自洽：`in control` / `Take over control` / `take control of` 译法统一。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 51 条 entries: `status: new → translated`, `flags` 含 `pr-ai-blocklist-agent-control-batch`, 非空 `target`。
- [ ] L369 `&` 半角保留；L136 `/remote-control` 字面保留。
- [ ] `Oz` 代号原样保留（L409 / L425）。
- [ ] 控制权语义在 L28/L29/L90/L91/L92/L93 之间自洽（推荐：Agent 在控制 / 您在控制 / 接管控制权）。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1417 条 translated 逐字保留。
- [ ] glossary 一致性：Agent / MCP / API / 命令块 / 窗格 / 标签页 / 模型 不混译。
- [ ] placeholder integrity 100%（本批无名称占位符，但 `{}` 若误删需检测）。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone：Agent 交互文案对用户使用「您」，状态标签简洁（不加多余主语）。
- glossary 按需新增 `take over control` / `in control` / `Rich Input` 三个候选条目。
- Journal 记录 stats delta + Agent 控制权语义决定 + 后续批次余量（ai/blocklist 剩 43 条）。
- Task archive。

## Out of Scope

- ai/blocklist 剩余 43 条 auto_ui new（block.rs / requested_command 其他、prompt_alert.rs、codebase_index_speedbump_banner.rs、code_diff_view.rs 等）—— 留下批。
- ai/blocklist 子目录的 `verdict=uncertain` 条目（约 200+，需人工审）。

## Decision (locked — Approach A)

**Approach A: Agent 输入/控制语义簇 51 条 auto_ui new**

锁定理由：
1. 集中翻译 Agent 控制权语义（`in control` / `take over control` / `waiting on instructions` / `needs your permission`），词族在同一时间窗口内统一固化，避免散批回头修订。
2. agent_input_footer/mod.rs 19 条 + requested_command.rs 12 条是两个最高密度叶节点，一次清空能显著减少 ai/blocklist 残余。
3. `Oz` 代号、`/remote-control` 斜杠命令、`&` Rich Input 字符等特殊字面值集中在本批，便于一次性建立惯例。

**Batch flag**: `pr-ai-blocklist-agent-control-batch`

## Technical Approach

1. 读取 `candidates.json` 锁定 51 条 entry id。
2. glossary 检查：先看 `take over control` / `in control` / `Rich Input` 是否已存在；若否，先增补再翻译以保证一致性。
3. 按 9 文件分簇翻译，写回 `target` / `status=translated` / `flags 追加 pr-ai-blocklist-agent-control-batch` / `updated_at`。
4. 特殊处理：
   - L369 `Hand off to cloud (or type &)` → `移交至云端（或键入 &）`（`&` 字面保留半角，括号全角）。
   - L136 `Log in to use /remote-control` → `登录以使用 /remote-control`。
   - L409 / L425：`Oz` 保留，`新建 Oz 云端 Agent 会话` / `新建 Oz Agent 会话`。
   - L3131 `Edit API Keys` → `编辑 API 密钥`。
   - L28 `Agent is in control` → `Agent 正在控制`；L29 `User is in control` → `您正在控制`（保持现在进行时一致）。
   - L92 `User in control` （状态标签简短形式）→ `您正在控制`（与 L29 合一）或 `用户控制中`，由实施时按上下文确认。
   - L93 `Agent ran into an issue. Take over control.` → `Agent 遇到问题。请接管控制权。`
   - L91 `Paused agent. User is in control.` → `已暂停 Agent。您正在控制。`
   - L86 `OK if I run this command and read the output?` → `允许我运行此命令并读取输出吗？`
   - L87 `OK if I call this MCP tool?` → `允许我调用此 MCP 工具吗？`
   - L127 `Agent waiting for instructions...` → `Agent 正在等待指令……`
   - L48 `Generating title...` → `正在生成标题……`
   - L85 `Generating command...` → `正在生成命令……`
   - L88 `Agent is monitoring command...` → `Agent 正在监控命令……`
   - L130 `I'm sorry, I couldn't complete that request.` → `抱歉，我无法完成该请求。`
5. apply 脚本沿用上批模板（全角标点 invariant + history 留空惯例 + 占位符内放行 + glossary 同步）。
6. `extract --check` 幂等校验。
7. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
8. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- Candidates (固化): `.trellis/tasks/05-22-translate-ai-blocklist-auto-ui-new-entries-batch-1-of-50/candidates.json`（51 条）。
- 源码上下文（9 文件）:
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/agent_view/agent_input_footer/environment_selector.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/agent_view/inline_agent_view_header.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/agent_view/orchestration_pill_bar.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/agent_view/zero_state_block.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/block/view_impl/common.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/block/view_impl/orchestration.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/inline_action/requested_command.rs`
  - `<HOME>/Documents/Codes/warp/app/src/ai/blocklist/inline_action/orchestration_controls.rs`
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-22-translate-mcp-servers-remaining-files-auto-ui-new-entries-edit-update-installation-destructive-page/prd.md`。
- 上轮 apply 脚本: `.trellis/tasks/archive/2026-05/05-22-translate-mcp-servers-remaining-files-auto-ui-new-entries-edit-update-installation-destructive-page/apply_translations.py`。
