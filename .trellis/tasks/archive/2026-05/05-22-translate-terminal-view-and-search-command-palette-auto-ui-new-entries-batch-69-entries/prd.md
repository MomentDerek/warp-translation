# Translate terminal/view + search/command_palette auto_ui new entries — 78 entries (combined sweep)

## Goal

一次清扫 `app/src/terminal/view/*` 与 `app/src/search/command_palette/*` 两个最大剩余热点的全部 `status=new` + `audit.verdict=auto_ui` 用户可见文案，共 **78 条** 横跨 **34 个文件**。继 ai/blocklist 子目录清零之后，使 auto_ui new 余量从 730 → 652（-78）。

## What I already know

- 当前 `strings.json` 统计：`translated=1511`, `fuzzy=52`, `new=5171`（auto_ui 730 / uncertain 4441）。
- 总热点扫荡顺序：ai/blocklist 94 ✅ → terminal/view + command_palette 78（本批）→ cli_agent_sessions 31 / notebooks/editor 23 …
- 实际过滤 78 条（之前 hotspot 列表把深路径如 `terminal/view/inline_banner/*` 也归入 `terminal/view` 桶，所以 37+32=69 是 4 段截断值的虚低数；准确是 78）。
- glossary 现状（83 条）：相关已有 `session→会话` / `prompt→提示词` / `fork→派生` / `drive→Warp Drive` / `notebook→笔记本` / `workflow→工作流` / `lsp→LSP` / `tab→标签页` / `pane→窗格` / `agent→Agent` / `mcp_server→MCP 服务器` / `harness→Agent 执行环境`。
- **关键 collision**：现有 `prompt → 提示词` 是 AI prompt 语境。本批 L240 `Shell prompt (PS1)` 与 L329 `Warp prompt` 用的是 **shell 提示符** 语义（不是 AI prompt），必须按上下文译为「提示符」。需新增 `shell_prompt` 词条与 `prompt` 区分。

## Scope by subdirectory

### command_palette (37 条 / 14 文件)
- **conversations/data_source.rs (3)**：L30/31/32 三个 section header（Active/Other/Past conversations）
- **conversations/search_item.rs (7)**：L69 `New conversation` / L90 `Fork current conversation` / L417 `Conversation: {}` / L422 `Fork current conversation ({title})` / L431/435/437 `Press enter to ...` 三连
- **files/search_item.rs (7)**：Directory/File: {} / Press Enter to ... / Create {}…（U+2026） / Create file: {} / Press Enter to create {} in the current directory
- **launch_config/search_item.rs (2)**：L73 `Selected {}.` / L77 launch configuration
- **navigation/render.rs (6)**：L107 `Current` / L357 `Completed over 1 hour ago` / L358/359 复数对偶 `Completed {mins} minute(s) ago` / L360 `No timestamp found` / L377 `Empty Session`
- **new_session/new_session_option.rs (3)**：L84 `Create New Tab: {}` / L86 `Create New Window: {}` / L89 `Split Pane {direction}: {}`
- **new_session/search_item.rs (1)**：L82 `Press enter to launch this session.`
- **repos/repo_search_item.rs (1)**：L139 `Repo: {}`
- **separator_search_item.rs (1)**：L69 `Section: {}`
- **view.rs (3)**：L60（**特殊：注释文本而非 UI 文案**，前导空格 + ASCII content）/ L289 `Search for a command` / L846 `Cannot switch conversations while agent is monitoring a command.`
- **warp_drive/env_var_collection_search_item.rs (1)**：L166 `Environment Variables: {}`
- **warp_drive/notebook_search_item.rs (1)**：L144 `Notebook: {}`
- **warp_drive/workflow_search_item.rs (1)**：L151 `Workflow: {}`

### terminal/view (41 条 / 20 文件)
- **ambient_agent/block/entry.rs (1)**：L35 `New cloud agent` ← 「新建云端 Agent」
- **ambient_agent/host_selector.rs (1)**：L42 `Execution host` ← 新词「执行主机」
- **ambient_agent/model_selector.rs (2)**：L62 `Choose agent model` / L64 `No results`
- **block_banner/warpify.rs (1)**：L163 `Do not show again`
- **block_onboarding/onboarding_drive_sharing_block.rs (3)**：L54 `Sharing in Warp Drive` / L56 长句（含 `Warp` / `web` / `- ` 拼接连字符）/ L57 长句（**含 curly apostrophe `'` U+2019，原样保留**）
- **block_onboarding/onboarding_prompt_block.rs (5)**：L240 `Shell prompt (PS1)` ← shell-prompt 语义 / L241 `No existing prompt.` / L242 `Look incorrect? ` ← **末尾尾随空格保留** / L243 `Let us know.` ← L242 + L243 是拼接对 / L329 `Warp prompt` ← shell-prompt 语义
- **init_environment/mod.rs (2)**：L21 / L22 长句 onboarding（含 `environment` / `cloud agent` / 命令重新运行指引）
- **init_project/lsp_server_selector.rs (2)**：L133 长句 / L166 `Skip for now`
- **init_project/mod.rs (4)**：L41 长句 / L42 长句 / L520 `Re-generate AGENTS.md file` ← **AGENTS.md 字面保留** / L680 `View index status`
- **inline_banner/agent_mode_setup.rs (1)**：L20 截断长句
- **inline_banner/alias_expansion.rs (1)**：L94 `Warp can auto-expand aliases.`
- **inline_banner/anonymous_user_ai_sign_up.rs (1)**：L23 `Sign Up`
- **inline_banner/aws_bedrock_login.rs (1)**：L77 `Use AWS Bedrock?` ← **AWS Bedrock 字面保留**
- **inline_banner/aws_cli_not_installed.rs (1)**：L80 `AWS CLI Not Installed` ← **AWS CLI 字面保留**
- **inline_banner/shell_process_terminated.rs (2)**：L18 `Shell process exited prematurely!` / L37 `Shell process exited`
- **inline_banner/vim_mode.rs (1)**：L49 `Enable Warp's Vim keybindings?` ← **Vim 字面保留**
- **pane_impl.rs (2)**：L685 `Stop sharing session` / L833 `Show details`
- **shared_session/conversation_ended_tombstone_view.rs (2)**：L218 `Fork this conversation locally` / L239 `Open this conversation in the Warp desktop app`
- **shared_session/view_impl.rs (3)**：L1866 `Share session...` (ASCII 三点 → ……) / L1885 `Copy session sharing link` / L1999 `Request edit access`
- **shell_terminated_banner.rs (1)**：L18 `File issue` ← 动词短语「提交问题」
- **ssh_file_upload.rs (1)**：L419 `Clear upload`
- **use_agent_footer/mod.rs (2)**：L1101 `Ask the Warp agent to assist` / L1115 `Ask the Warp agent to resume`
- **use_agent_footer/warpify_footer.rs (1)**：L39 `Enable Warp shell integration in this session`

## Special literal / placeholder protections

| 锚点 | 规则 |
|---|---|
| L60 view.rs | **疑似 Rust 注释文本**（前导空格 + 完整段落 `Set of hardcoded action names that we want to show in the command palette zero state ...`）。需保留前导空格 + 整体可读；按上下文判定是否就是 UI 文案，若是普通注释字符串则按字面译并保留前导空格。**实施时实际打开源码 view.rs:60 确认**。 |
| L417/L139/L144/L151/L166/L166/L100/L102 etc | `{}` 匿名占位符原样、位置正确 |
| L422 / L431 / L437 | `{title}` / `{}` / `{}` 命名占位符原样 |
| L84/L86/L89 | `Create New Tab: {}` / `Split Pane {direction}: {}` 多占位符 |
| L358/L359 | `{mins}` 命名占位符原样；译法注意单复数中文一般不区分（皆「{mins} 分钟前」） |
| L164 | `Create {}…` 末尾 U+2026 原样 |
| L1866 | `Share session...` ASCII 三点 → `……` |
| L242 | `Look incorrect? ` 末尾尾随**半角空格**保留（与 L243 拼接） |
| L57 | curly apostrophe `'` (U+2019) 在 `You'll` 原样保留 |
| L56 | 长句含 ` - ` 拼接连字符（半角空格 + 连字符 + 半角空格），保留；末尾省略号 ASCII `...` → `……` |
| L520 | `AGENTS.md` 文件名字面保留（不译） |
| L77 (aws_bedrock) | `AWS Bedrock` 字面保留 |
| L80 (aws_cli) | `AWS CLI` 字面保留 |
| L49 | `Vim` 字面保留（与 keybindings 拼接：「Vim 键位映射」） |
| L329 / L240 | `Warp prompt` / `Shell prompt` → 「Warp 提示符」/「Shell 提示符（PS1）」（区分既有 `prompt → 提示词`） |

## Glossary additions (新增预估 6 条)

1. `shell_prompt`: en=`shell prompt`, zh=`提示符`, notes=`Shell PS1 提示符；与既有 'prompt → 提示词'（AI prompt 语境）区分。'Shell prompt (PS1)' → 'Shell 提示符（PS1）'；'Warp prompt' → 'Warp 提示符'；'No existing prompt' (shell 上下文) → '无现有提示符'。`, do_not_translate=false
2. `execution_host`: en=`execution host`, zh=`执行主机`, notes=`ambient agent 的运行主机选择。'Execution host' → '执行主机'；'Choose execution host' → '选择执行主机'。`, do_not_translate=false
3. `alias`: en=`alias`, zh=`别名`, notes=`Shell alias 命令别名。'auto-expand aliases' → '自动展开别名'。`, do_not_translate=false
4. `vim`: en=`Vim`, zh=`Vim`, notes=`编辑器品牌名。保留英文。`Vim keybindings` → `Vim 键位映射`。`, do_not_translate=true
5. `aws`: en=`AWS`, zh=`AWS`, notes=`Amazon Web Services 品牌缩写。保留英文。配套：'AWS Bedrock' / 'AWS CLI' 全字面保留。`, do_not_translate=true
6. `agents_md`: en=`AGENTS.md`, zh=`AGENTS.md`, notes=`项目 Agent 配置文件名。文件名字面保留。'Re-generate AGENTS.md file' → '重新生成 AGENTS.md 文件'。`, do_not_translate=true

## Locked tricky translations

| ID 锚点 | source | target |
|---|---|---|
| L30 | Active pane conversations | 当前窗格的会话 |
| L31 | Other active conversations | 其他活跃会话 |
| L32 | Past conversations | 历史会话 |
| L69 | New conversation | 新建会话 |
| L90 | Fork current conversation | 派生当前会话 |
| L417 | Conversation: {} | 会话：{} |
| L422 | Fork current conversation ({title}) | 派生当前会话（{title}） |
| L431 | Press enter to navigate to conversation "{}". | 按 Enter 跳转到会话 "{}"。 |
| L435 | Press enter to fork the current conversation into a new conversation. | 按 Enter 将当前会话派生为新会话。 |
| L437 | Press enter to create a new conversation. | 按 Enter 创建新会话。 |
| L100 | Directory: {} | 目录：{} |
| L102 | File: {} | 文件：{} |
| L108 | Press Enter to navigate to this directory | 按 Enter 跳转到此目录 |
| L110 | Press Enter to open this file | 按 Enter 打开此文件 |
| L164 | Create {}… | 创建 {}… |
| L198 | Create file: {} | 创建文件：{} |
| L203 | Press Enter to create {} in the current directory | 按 Enter 在当前目录中创建 {} |
| L73 (launch_config) | Selected {}. | 已选中 {}。 |
| L77 (launch_config) | Press enter to use this launch configuration. | 按 Enter 使用此启动配置。 |
| L107 (navigation) | Current | 当前 |
| L357 | Completed over 1 hour ago | 完成于 1 小时前 |
| L358 | Completed {mins} minute ago | 完成于 {mins} 分钟前 |
| L359 | Completed {mins} minutes ago | 完成于 {mins} 分钟前 |
| L360 | No timestamp found | 未找到时间戳 |
| L377 | Empty Session | 空会话 |
| L84 | Create New Tab: {} | 新建标签页：{} |
| L86 | Create New Window: {} | 新建窗口：{} |
| L89 | Split Pane {direction}: {} | 拆分窗格 {direction}：{} |
| L82 | Press enter to launch this session. | 按 Enter 启动此会话。 |
| L139 | Repo: {} | 仓库：{} |
| L69 (sep) | Section: {} | 区段：{} |
| L60 (view.rs) | (注释文本，实施时确认；保留前导空格) | 按上下文译，保留前导空格 |
| L289 | Search for a command | 搜索命令 |
| L846 | Cannot switch conversations while agent is monitoring a command. | Agent 正在监控命令时无法切换会话。 |
| L166 (env_var) | Environment Variables: {} | 环境变量：{} |
| L144 | Notebook: {} | 笔记本：{} |
| L151 | Workflow: {} | 工作流：{} |
| L35 (ambient) | New cloud agent | 新建云端 Agent |
| L42 (host_selector) | Execution host | 执行主机 |
| L62 (model_selector) | Choose agent model | 选择 Agent 模型 |
| L64 | No results | 无结果 |
| L163 (warpify) | Do not show again | 不再显示 |
| L54 | Sharing in Warp Drive | 在 Warp Drive 中分享 |
| L240 | Shell prompt (PS1) | Shell 提示符（PS1） |
| L241 | No existing prompt. | 无现有提示符。 |
| L242 | Look incorrect?  | 看起来不对吗？ (末尾保留半角空格) |
| L243 | Let us know. | 请告诉我们。 |
| L329 | Warp prompt | Warp 提示符 |
| L166 (lsp) | Skip for now | 暂时跳过 |
| L520 | Re-generate AGENTS.md file | 重新生成 AGENTS.md 文件 |
| L680 | View index status | 查看索引状态 |
| L94 (alias) | Warp can auto-expand aliases. | Warp 可以自动展开别名。 |
| L23 | Sign Up | 注册 |
| L77 (bedrock) | Use AWS Bedrock? | 使用 AWS Bedrock？ |
| L80 | AWS CLI Not Installed | AWS CLI 未安装 |
| L18 (shell_term) | Shell process exited prematurely! | Shell 进程意外退出！ |
| L37 (shell_term) | Shell process exited | Shell 进程已退出 |
| L49 | Enable Warp's Vim keybindings? | 启用 Warp 的 Vim 键位映射？ |
| L685 | Stop sharing session | 停止分享会话 |
| L833 | Show details | 显示详情 |
| L218 | Fork this conversation locally | 在本地派生此会话 |
| L239 | Open this conversation in the Warp desktop app | 在 Warp 桌面应用中打开此会话 |
| L1866 | Share session... | 分享会话…… |
| L1885 | Copy session sharing link | 复制会话分享链接 |
| L1999 | Request edit access | 请求编辑权限 |
| L18 (shell_term_banner) | File issue | 提交问题 |
| L419 | Clear upload | 清除上传 |
| L1101 | Ask the Warp agent to assist | 请 Warp Agent 协助 |
| L1115 | Ask the Warp agent to resume | 请 Warp Agent 继续 |
| L39 (warpify) | Enable Warp shell integration in this session | 在此会话中启用 Warp shell 集成 |

长句（L21/L22 init_env、L41/L42 init_project、L20 agent_mode_setup、L56 onboarding_drive_sharing、L57、L133 lsp_selector）由 implementer 按 tone 翻译，遵守：
- 全角标点；
- 已知品牌字面保留（Warp / Agent / AWS / Vim / AGENTS.md / cloud agent 译「云端 Agent」）；
- L56 ` - ` 拼接连字符保留；
- L57 curly apostrophe `'` (U+2019) 在 `You'll` 处原样保留；
- L41/L42 段落用「您」register；
- L240/L329 区分 shell prompt → 提示符 vs AI prompt → 提示词；
- ASCII `...` → `……`，U+2026 `…` 原样。

## Requirements

- 78 条 entries: `status: new → translated`，`flags` 含 `pr-terminal-view-command-palette-batch`，`target` 非空。
- placeholder integrity 100%（`{}` / `{title}` / `{mins}` / `{direction}` 计数、命名一致）。
- 拼接片段尾随空格 / `'`（U+2019）/ `…`（U+2026）字面保留。
- 全角中文标点，shell-prompt vs AI-prompt 语义区分。
- AGENTS.md / AWS Bedrock / AWS CLI / Vim / Warp 字面保留。
- `extract --check` exit 0。
- 1511 条已有 translated 逐字保留。
- glossary +6 条（按上 §Glossary additions；如某条已存在改为复用，记录决策到 journal）。
- `warp-zh-builder` 重建成功。
- `cargo check -p warp` 通过。

## Acceptance Criteria

- [ ] 78 条 `new → translated`，flag 一致。
- [ ] L242 末尾半角空格保留；L57 `'` U+2019 保留；L164/L77(launch)/L1866 末尾省略号风格正确。
- [ ] L240/L329 译为「提示符」，L29x（如有）AI prompt 保留「提示词」（本批无 AI prompt 实例）。
- [ ] L520 `AGENTS.md` 字面；L77 `AWS Bedrock` 字面；L80 `AWS CLI` 字面；L49 `Vim` 字面。
- [ ] L60 view.rs 注释文本前导空格保留（如确认为注释/doc string）。
- [ ] glossary +6 候选条目，已存在的复用并记录。
- [ ] `extract --check` exit 0；1511 条逐字保留。
- [ ] `warp-zh-builder` + `cargo check -p warp` 双绿。
- [ ] 子目录归零验证：`terminal/view` + `command_palette` 下 auto_ui new = 0。

## Definition of Done

- Tone：onboarding 长句使用「您」；按钮/动作短句无主语；状态/error 客观陈述。
- glossary 落地：`shell_prompt / execution_host / alias / vim / aws / agents_md`，已存在的复用并在 journal 记录。
- Journal 记录 stats delta + 子目录清零 + shell-prompt 语义分叉决策。
- Task 由 main loop commit + archive（与 batch 1/2 流程一致）。

## Out of Scope

- 两子目录的 `verdict=uncertain` 条目（需人工审）。
- 下一热点（cli_agent_sessions 31 / remote_server/server_model.rs 23 / notebooks/editor 23 / resource_center/sections.rs 22 / crates/warpui/src/rendering 22 / settings_view/billing_and_usage 21）—— 留下批。

## Decision (locked — Approach A)

**Approach A: terminal/view + command_palette 双子目录合并扫荡 78 条**

锁定理由：
1. 用户明确「一次做完」，规模 78 在可控范围（之前 51 单批已验证）。
2. 两子目录共享术语词族（session/conversation/fork/tab/window/pane/agent），合并批一次固化避免回头修订。
3. shell-prompt vs AI-prompt 语义分叉只发生在 terminal/view，与 command_palette 同时处理可让 glossary 调整一次到位。
4. AWS/Vim/AGENTS.md 等品牌字面保护规则集中。

**Batch flag**: `pr-terminal-view-command-palette-batch`

## Technical Approach

1. 读取 `candidates.json` 锁定 78 条 entry id。
2. glossary 增补：先检查 `shell_prompt / execution_host / alias / vim / aws / agents_md` 是否存在；不存在按 §Glossary additions 加入。
3. 翻译 + 写回（按上表 locked tricky translations 直接落，长句由 implementer 按 tone 翻）。
4. apply 脚本沿用 batch 2 模板（`apply_translations.py`），新增断言：
   - placeholder integrity：`{}` count, `{title}` / `{mins}` / `{direction}` 名称匹配
   - L242 target 末尾为半角空格
   - L57 target 含 U+2019 (`'`)
   - L1866 / L56 target 含 `……` (U+2026 ×2)
   - L164 / L77(launch_config) target 末尾为 `…` (U+2026 单个)
   - L520 target 含 `AGENTS.md`；L77 (bedrock) 含 `AWS Bedrock`；L80 含 `AWS CLI`；L49 含 `Vim`
   - L60 target 首字符为半角空格（若源以空格开头）
5. `extract --check`、`warp-zh-builder`、`cargo check -p warp`。
6. 子目录归零验证。
7. Journal。
8. Stop, no commit/archive（main loop 完成）。

## Technical Notes

- Candidates (固化): `.trellis/tasks/05-22-translate-terminal-view-and-search-command-palette-auto-ui-new-entries-batch-69-entries/candidates.json`（78 条）。
- 源码上下文：见 candidates.json `file` 字段（34 文件）。
- 上轮 (batch 2) PRD: `.trellis/tasks/archive/2026-05/05-22-translate-ai-blocklist-remaining-43-auto-ui-new-entries-batch-2-of-2-sweep/prd.md`。
- 上轮 apply 脚本: `.trellis/tasks/archive/2026-05/05-22-translate-ai-blocklist-remaining-43-auto-ui-new-entries-batch-2-of-2-sweep/apply_translations.py`。
- L60 view.rs 上下文需 implementer 实际打开 `<HOME>/Documents/Codes/warp/app/src/search/command_palette/view.rs:60` 验证是否注释 / doc string / runtime UI 文案。
