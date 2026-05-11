# PR3 翻译复核清单

共 227 条（182 中文 + 45 do_not_translate）跨 15 个文件。

`source → target`；DNT = do_not_translate（保留英文）。

占位符 `{name}` / `{}` 保持原样。`occurrences[].context_hint` 给出 AST 父调用。


## `app/src/settings_view/ai_page.rs` (154 条)

- L153 [A7CD2Y] `Let AI suggest the next command to run based on your command history, outputs, and common workflows.` → `让 AI 基于您的命令历史、输出与常用工作流，建议下一条要运行的命令。`
  - ctx: `const:NEXT_COMMAND_DESCRIPTION`
- L154 [RR476T] `Let AI suggest natural language prompts, as inline banners in the input, based on recent commands and their outputs.` → `让 AI 根据近期命令及其输出，在输入区以内联横幅形式建议自然语言提示词。`
  - ctx: `const:PROMPT_SUGGESTIONS_DESCRIPTION`
- L155 [AJF3GF] `Let AI suggest code diffs and queries as inline banners in the blocklist, based on recent commands and their outputs.` → `让 AI 根据近期命令及其输出，在命令块列表中以内联横幅形式建议代码差异与查询。`
  - ctx: `const:SUGGESTED_CODE_BANNERS_DESCRIPTION`
- L157 [7J8V6G] `Let AI suggest natural language autosuggestions, based on recent commands and their outputs.` → `让 AI 根据近期命令及其输出，建议自然语言自动补全。`
  - ctx: `const:NATURAL_LANGUAGE_AUTOSUGGESTIONS`
- L159 [JMGJA6] `Let AI generate a title for your shared block based on the command and output.` → `让 AI 根据命令及其输出为您共享的命令块生成标题。`
  - ctx: `const:SHARED_BLOCK_TITLE_GENERATION_DESCRIPTION`
- L161 [8416YP] `Let AI generate commit messages and pull request titles and descriptions.` → `让 AI 生成提交信息以及 Pull Request 的标题和描述。`
  - ctx: `const:GIT_OPERATIONS_AUTOGEN_DESCRIPTION`
- L182 [GBP0AM] `Active AI` → `主动 AI`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L194 [G244AV] **DNT** `terminal command autodetection in agent input`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L196 [FB3ZPE] **DNT** `natural language detection`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L210 [EZKQSR] **DNT** `agent prompt autodetection in terminal input`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L223 [FCZ1S1] `Next Command` → `下一条命令`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L235 [NRCRBP] **DNT** `prompt suggestions`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L247 [P8HNJD] **DNT** `code suggestions`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L261 [CEJ29B] `Hide agent tips` → `隐藏 Agent 提示`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L261 [9TNZQB] `Show agent tips` → `显示 Agent 提示`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L278 [Z1H3B4] `Show Oz changelog in new agent conversation view` → `在新 Agent 对话视图中显示 Oz 更新日志`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L279 [W0AVGJ] `Hide Oz changelog in new agent conversation view` → `在新 Agent 对话视图中隐藏 Oz 更新日志`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L326 [M6JTRN] **DNT** `natural language autosuggestions`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L339 [AR16MP] **DNT** `shared block title generation`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L352 [0BK6AQ] **DNT** `voice input`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L364 [PVQ3QD] `Show "Use Agent" footer` → `显示“使用 Agent”页脚`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L365 [2K7ANG] `Hide "Use Agent" footer` → `隐藏“使用 Agent”页脚`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L384 [HK5TXT] **DNT** `codebase index`
  - ctx: `ToggleSettingActionPair::add_toggle_setting_action_pairs_as_bindings > macro:vec`
- L612 [Y3R5CX] **DNT** `e.g. ~/code-repos/repo`
  - ctx: `.set_placeholder_text`
- L651 [5DMSQE] `Commands, comma separated` → `命令（用逗号分隔）`
  - ctx: `.set_placeholder_text`
- L673 [QGV2CR] **DNT** `e.g. ls .*`
  - ctx: `.set_placeholder_text`
- L705 [TWNMGF] **DNT** `e.g. rm .*`
  - ctx: `.set_placeholder_text`
- L737 [E4VT8N] `command (supports regex)` → `命令（支持正则）`
  - ctx: `.set_placeholder_text`
- L1340 [E7N7A2] `Add Profile` → `添加配置`
  - ctx: `ActionButton::new`
- L1368 [BQWNS0] `New Tab` → `新建标签页`
  - ctx: `.add_typed_action_view > macro:vec`
- L1372 [9BKEE8] `Split Pane` → `拆分窗格`
  - ctx: `.add_typed_action_view > macro:vec`
- L1812 [BR1WWD] `Read only` → `只读`
  - ctx: `.set_items > macro:vec`
- L1998 [C37GT5] `Allow in specific directories` → `在指定目录中允许`
  - ctx: `.map`
- L2161 [477FNH] `Select coding agent` → `选择编码 Agent`
  - ctx: `.set_menu_header_text_override`
- L3170 [CJWSWP] `Toolbar layout` → `工具栏布局`
  - ctx: `.span`
- L3253 [978PXK] **DNT** `oz warp agent global ai a.i. active next command prompt code diffs suggestion suggested suggestions agent mode natural language detection input hint api keys bring your own byo google anthropic openai`
- L3277 [XR34JA] `Warp Agent` → `Warp Agent`
  - ctx: `Text::new_inline`
- L3290 [JYSAR9] `Your organization disallows AI when the active pane contains content from a remote session` → `当当前窗格包含远程会话内容时，您所在组织禁止使用 AI`
  - ctx: `Text::new`
- L3311 [6Q5YEX] `To use AI features, please create an account.` → `要使用 AI 功能，请创建账户。`
  - ctx: `Text::new_inline`
- L3408 [YV6JKM] `Restricted due to billing issue` → `因账单问题受限`
- L3412 [0EXDQN] **DNT** `{used}/{limit}`
  - ctx: `macro:format`
- L3532 [Z25MS7] **DNT** `a.i. ai usage limit plan`
- L3543 [H7J2QJ] **DNT** `%b %d`
  - ctx: `.format`
- L3565 [MHHM1W] `Resets {formatted_next_refresh_time}` → `于 {formatted_next_refresh_time} 重置`
  - ctx: `.paragraph > macro:format`
- L3582 [20F3F6] `This is the {} limit of AI credits for your account.` → `这是您账户的 {} AI 额度上限。`
  - ctx: `macro:format`
- L3607 [EV119R] ` to get more AI usage.` → `以获得更多 AI 用量。`
  - ctx: `macro:vec`
- L3613 [4PS8BG] ` for more AI usage.` → `以获得更多 AI 用量。`
  - ctx: `macro:vec`
- L3770 [63DQXJ] `Prompt Suggestions` → `提示词建议`
  - ctx: `render_ai_setting_toggle`
- L3797 [FSC1F2] `Suggested Code Banners` → `建议代码横幅`
  - ctx: `render_ai_setting_toggle`
- L3825 [CEKPTH] `Natural Language Autosuggestions` → `自然语言自动补全`
  - ctx: `render_ai_setting_toggle`
- L3851 [AMYMKA] `Shared Block Title Generation` → `共享命令块标题生成`
  - ctx: `render_ai_setting_toggle`
- L3877 [Q13SHF] `Commit & Pull Request Generation` → `Commit 与 Pull Request 生成`
  - ctx: `render_ai_setting_toggle`
- L3898 [C7EBZY] **DNT** `active ai a.i. next command prompt suggestions code diffs suggested banners passive unit tests commit pull request pr git code review autogen generate`
- L3990 [M4AZEE] **DNT** `ai a.i. agent autonomy profiles allowlist denylist autoexecute permissions models llms planning mcp server`
- L3992 [GJJGS9] **DNT** `ai a.i. agent autonomy profiles allowlist denylist autoexecute permissions models llms planning`
- L4026 [KN1JCV] `Set the boundaries for how your Agent operates. Choose what it can access, how much autonomy it has, and when it must ask for your approval. You can also fine-tune behavior around natural language input, codebase awareness, and more.` → `为 Agent 的运作方式设置边界。选择它可以访问什么、拥有多少自主权，以及何时必须征求您的审批。您还可以微调自然语言输入、代码库感知等方面的行为。`
  - ctx: `render_ai_setting_description`
- L4073 [QDQRFA] `Profiles let you define how your Agent operates — from the actions it can take and when it needs approval, to the models it uses for tasks like coding and planning. You can also scope them to individual projects.` → `配置让您定义 Agent 的运作方式 —— 从它可以执行的操作、何时需要审批，到它在编码和规划等任务中使用的模型。您还可以将其限定到单个项目。`
  - ctx: `render_ai_setting_description`
- L4171 [F9SA9A] `Context window (tokens)` → `上下文窗口（tokens）`
  - ctx: `render_body_item_label`
- L4183 [KF4E8B] **DNT** `{min}`
  - ctx: `.span > macro:format`
- L4193 [ND1801] **DNT** `{max}`
  - ctx: `.span > macro:format`
- L4382 [AHP77W] `Some of your permissions are managed by your workspace.` → `您的部分权限由所属工作区管理。`
  - ctx: `render_settings_info_banner`
- L4533 [SV2351] `Regular expressions to match commands that the Warp Agent should always ask permission to execute.` → `用于匹配 Warp Agent 在执行前总是询问权限的命令的正则表达式。`
  - ctx: `render_ai_list`
- L4568 [Q8V550] `Regular expressions to match commands that can be automatically executed by the Warp Agent.` → `用于匹配可由 Warp Agent 自动执行的命令的正则表达式。`
  - ctx: `render_ai_list`
- L4648 [9J0V7J] `Show model picker in prompt` → `在提示词中显示模型选择器`
  - ctx: `.span`
- L4670 [FX9WZB] `This model serves as the primary engine behind the Warp Agent. It powers most interactions and invokes other models for tasks like planning or code generation when necessary. Warp may automatically switch to alternate models based on model availability or for auxiliary tasks such as conversation summarization.` → `此模型作为 Warp Agent 的主要引擎，驱动大部分交互，并在必要时调用其他模型完成规划或代码生成等任务。Warp 可能会基于模型可用性或在对话总结等辅助任务时自动切换到备用模型。`
  - ctx: `Some`
- L4690 [EKQK0T] `Codebase Context` → `代码库上下文`
  - ctx: `render_ai_setting_toggle`
- L4701 [0HBJ0D] `Allow the Warp Agent to generate an outline of your codebase that can be used for context. No code is ever stored on our servers. ` → `允许 Warp Agent 生成您代码库的大纲，作为上下文使用。代码不会存储在我们的服务器上。`
  - ctx: `macro:vec`
- L4774 [B32DMG] `You haven't added any MCP servers yet. Once you do, you'll be able to control how much autonomy the Warp Agent has when interacting with them. ` → `您还没有添加任何 MCP 服务器。添加之后，您将能够控制 Warp Agent 在与之交互时拥有的自主程度。`
  - ctx: `macro:vec`
- L4777 [XEZYFR] `Add a server` → `添加服务器`
  - ctx: `macro:vec`
- L4780 [C3545W] ` or ` → ` 或 `
  - ctx: `macro:vec`
- L4782 [VY8JVD] `learn more about MCPs.` → `了解更多 MCP 信息。`
  - ctx: `macro:vec`
- L4855 [XH4NN8] `Allow the Warp Agent to call these MCP servers.` → `允许 Warp Agent 调用这些 MCP 服务器。`
  - ctx: `.render_mcp_list`
- L4872 [TENGS5] `The Warp Agent will always ask for permission before calling any MCP servers on this list.` → `Warp Agent 在调用此列表中的任何 MCP 服务器之前，总是会请求权限。`
  - ctx: `.render_mcp_list`
- L4968 [6NSNQP] **DNT** `oz agent ai input natural language detection autodetection prompt terminal command commands history shell executed execution`
- L4999 [94Y3TR] `Show input hint text` → `显示输入提示文本`
  - ctx: `render_ai_setting_toggle`
- L5029 [9XA8T1] `Include agent-executed commands in history` → `在历史记录中包含 Agent 执行过的命令`
  - ctx: `render_ai_setting_toggle`
- L5078 [A590X6] `Encountered an incorrect detection? ` → `检测结果不正确？`
  - ctx: `LazyLock::new > const:AUTODETECTION_DESCRIPTION_FRAGMENTS > macro:vec`
- L5080 [TNME8G] `Let us know` → `告诉我们`
  - ctx: `LazyLock::new > const:AUTODETECTION_DESCRIPTION_FRAGMENTS > macro:vec`
- L5088 [NXFS6B] `Autodetect agent prompts in terminal input` → `在终端输入中自动检测 Agent 提示词`
  - ctx: `render_ai_setting_toggle`
- L5097 [RGSXTM] `Autodetect terminal commands in agent input` → `在 Agent 输入中自动检测终端命令`
  - ctx: `render_ai_setting_toggle`
- L5133 [0Z9RH5] `Enabling natural language detection will detect when natural language is written in the terminal input, and then automatically switch to Agent Mode for AI queries.` → `启用自然语言检测后，当终端输入中写入自然语言时会自动检测到，并切换到 Agent 模式进行 AI 查询。`
  - ctx: `LazyLock::new > const:NATURAL_LANGUAGE_DETECTION_DESCRIPTION_FRAGMENTS > macro:vec`
- L5136 [Z3A4PR] ` Encountered an incorrect input detection? ` → ` 检测结果不正确？`
  - ctx: `LazyLock::new > const:NATURAL_LANGUAGE_DETECTION_DESCRIPTION_FRAGMENTS > macro:vec`
- L5147 [VRWAZG] `Natural language detection` → `自然语言检测`
  - ctx: `render_ai_setting_toggle`
- L5181 [K4NP43] `Natural language denylist` → `自然语言黑名单`
  - ctx: `render_ai_setting_label`
- L5187 [EKNXEB] `Commands listed here will never trigger natural language detection.` → `此处列出的命令永远不会触发自然语言检测。`
  - ctx: `render_ai_setting_description`
- L5218 [87WY59] **DNT** `oz agent mcp server servers model context protocol file-based file based project claude .mcp.json .claude/.mcp.json .codex config.toml .codex/config.toml`
- L5244 [2S522T] `Add MCP servers to extend the Warp Agent's capabilities. MCP servers expose data sources or tools to agents through a standardized interface, essentially acting like plugins. ` → `添加 MCP 服务器以扩展 Warp Agent 的能力。MCP 服务器通过标准化接口向 Agent 暴露数据源或工具，本质上类似插件。`
  - ctx: `macro:vec`
- L5277 [XR578G] `Auto-spawn servers from third-party agents` → `从第三方 Agent 自动启动服务器`
  - ctx: `render_ai_setting_toggle`
- L5291 [YQDA0A] `Automatically detect and spawn MCP servers from globally-scoped third-party AI agent configuration files (e.g. in your home directory). Servers detected inside a repository are never spawned automatically and must be enabled individually from the MCP settings page. ` → `从全局范围的第三方 AI Agent 配置文件（例如位于您的主目录）中自动检测并启动 MCP 服务器。在仓库中检测到的服务器永远不会自动启动，必须在 MCP 设置页面中逐项启用。`
  - ctx: `LazyLock::new > const:FILE_BASED_MCP_DESCRIPTION_FRAGMENTS > macro:vec`
- L5294 [PE6RNM] `See supported providers.` → `查看支持的提供商。`
  - ctx: `LazyLock::new > const:FILE_BASED_MCP_DESCRIPTION_FRAGMENTS > macro:vec`
- L5328 [ZPC7PB] `Manage MCP servers` → `管理 MCP 服务器`
  - ctx: `render_full_pane_width_ai_button`
- L5376 [NJWSA3] `Rules help the Warp Agent follow your conventions, whether for codebases or specific workflows. ` → `规则帮助 Warp Agent 遵循您的约定，无论是针对代码库还是特定工作流。`
  - ctx: `macro:vec`
- L5416 [DEFVTM] `Suggested Rules` → `建议规则`
  - ctx: `render_ai_setting_toggle`
- L5426 [C2CMTE] `Let AI suggest rules to save based on your interactions.` → `让 AI 根据您的交互建议要保存的规则。`
  - ctx: `render_ai_setting_description`
- L5444 [CNZZRB] `Warp Drive as agent context` → `将 Warp Drive 作为 Agent 上下文`
  - ctx: `render_ai_setting_toggle`
- L5454 [SKA168] `The Warp Agent can leverage your Warp Drive Contents to tailor responses to your personal and team developer workflows and environments. This includes any Workflows, Notebooks, and Environment Variables.` → `Warp Agent 可以利用您的 Warp Drive 内容，使响应贴合您个人和团队的开发者工作流与环境。这包括任意工作流、笔记本与环境变量。`
  - ctx: `render_ai_setting_description`
- L5470 [R0ASE1] **DNT** `agent oz ai a.i. knowledge fact memory memories rules warp drive context workflows notebooks environment variables`
- L5544 [2NEPCC] `Voice input allows you to control Warp by speaking directly to your terminal (powered by ` → `语音输入让您可以直接对终端说话来控制 Warp（由 `
  - ctx: `macro:vec`
- L5546 [KKZ2NE] **DNT** `Wispr Flow`
  - ctx: `macro:vec`
- L5576 [ZFEN42] `Key for Activating Voice Input` → `激活语音输入的按键`
  - ctx: `render_dropdown_item`
- L5577 [T3A0ZF] `Press and hold to activate.` → `按住激活。`
  - ctx: `Some`
- L5598 [QQ3YYA] **DNT** `voice agent oz ai a.i. speech input natural language talk english`
- L5663 [ZQVDY7] **DNT** `other oz updates zero state empty changelog new conversation agent what's new use agent footer toolbar layout chip chips rearrange re-arrange thinking expanded reasoning collapse never show hide conversation history`
- L5691 [77B30K] `Show Oz changelog in new conversation view` → `在新对话视图中显示 Oz 更新日志`
  - ctx: `render_ai_setting_toggle`
- L5709 [1DT65P] `Shows hint to use the "Full Terminal Use"-enabled agent in long running commands.` → `提示在长时间运行的命令中使用启用了“完整终端使用”的 Agent。`
  - ctx: `render_ai_setting_description`
- L5725 [66DWAM] `Show conversation history in tools panel` → `在工具面板中显示对话历史`
  - ctx: `render_ai_setting_toggle`
- L5736 [KCPECR] `Agent thinking display` → `Agent 思考过程显示`
  - ctx: `render_dropdown_item`
- L5737 [B1HP3P] `Controls how reasoning/thinking traces are displayed.` → `控制推理/思考过程的显示方式。`
  - ctx: `Some`
- L5757 [XRHABB] `Preferred layout when opening existing agent conversations` → `打开已有 Agent 对话时的首选布局`
  - ctx: `render_dropdown_item`
- L5793 [NHV6SG] **DNT** `third party cli coding agent claude codex gemini toolbar footer layout chip chips rearrange re-arrange bar command regex auto show rich input dismiss`
- L5808 [6EQD4D] `Show coding agent toolbar` → `显示编码 Agent 工具栏`
  - ctx: `render_ai_setting_toggle`
- L5819 [0ZA09G] `Show a toolbar with quick actions when running coding agents like ` → `在运行编码 Agent 时显示带快捷操作的工具栏，例如 `
  - ctx: `macro:vec`
- L5824 [7GEQ66] `, or ` → `，或 `
  - ctx: `macro:vec`
- L5844 [WXKZF6] `Third party CLI agents` → `第三方 CLI Agent`
  - ctx: `build_sub_header`
- L5869 [2QXVWX] `Auto show/hide Rich Input based on agent status` → `根据 Agent 状态自动显示/隐藏富文本输入`
  - ctx: `render_body_item_label`
- L5876 [Y2CSJ9] `Requires the Warp plugin for your coding agent` → `需要为您的编码 Agent 安装 Warp 插件`
  - ctx: `Some > field:tooltip_override_text`
- L5903 [GJKY1V] `Auto open Rich Input when a coding agent session starts` → `编码 Agent 会话开始时自动打开富文本输入`
  - ctx: `render_ai_setting_toggle`
- L5915 [QAEWF7] `Auto dismiss Rich Input after prompt submission` → `提交提示词后自动关闭富文本输入`
  - ctx: `render_ai_setting_toggle`
- L5931 [MVB4YF] `Commands that enable the toolbar` → `启用工具栏的命令`
  - ctx: `.span`
- L6023 [XZ3JDM] `Add regex patterns to show the coding agent toolbar for matching commands.` → `添加正则表达式，以便对匹配的命令显示编码 Agent 工具栏。`
  - ctx: `.paragraph`
- L6099 [4DMBGS] **DNT** `agent attribution commit pull request co-author author credit oz warp`
- L6150 [AQQHRX] `Enable agent attribution` → `启用 Agent 署名`
  - ctx: `render_body_item_label`
- L6167 [57MS9X] `Agent Attribution` → `Agent 署名`
  - ctx: `build_sub_header`
- L6175 [KDVB9X] `Oz can add attribution to commit messages and pull requests it creates` → `Oz 可以为它创建的提交信息和 Pull Request 添加署名`
  - ctx: `render_ai_setting_description`
- L6197 [3MG35Z] **DNT** `oz cloud agent computer use orchestration multi-agent`
- L6254 [HZ7T39] `Computer use in Cloud Agents` → `云端 Agent 中的计算机使用`
  - ctx: `render_body_item_label`
- L6279 [FC22ZA] `Enable computer use in cloud agent conversations started from the Warp app.` → `在 Warp 应用启动的云端 Agent 对话中启用计算机使用。`
  - ctx: `render_ai_setting_description`
- L6296 [MB89DH] `Enable multi-agent orchestration, allowing the agent to spawn and coordinate parallel sub-agents.` → `启用多 Agent 编排，允许 Agent 派生并协调并行的子 Agent。`
  - ctx: `render_ai_setting_description`
- L6400 [2SF5MR] **DNT** `sk-...`
  - ctx: `macro:create_api_key_editor`
- L6405 [ERC05J] **DNT** `sk-ant-...`
  - ctx: `macro:create_api_key_editor`
- L6411 [7VHX9H] **DNT** `AIzaSy...`
  - ctx: `macro:create_api_key_editor`
- L6439 [DG24PK] `Use your own API keys from model providers for the Warp Agent to use. API keys are stored locally and never synced to the cloud. Using auto models or models from providers you have not provided API keys for will consume Warp credits.` → `使用您自己的模型提供商 API 密钥，供 Warp Agent 使用。API 密钥仅本地存储，从不同步到云端。使用自动选择的模型，或您未提供 API 密钥的提供商的模型时，会消耗 Warp 额度。`
  - ctx: `render_ai_setting_description`
- L6488 [HQNYTD] `OpenAI API Key` → `OpenAI API 密钥`
  - ctx: `render_api_key_input`
- L6495 [E2VKDS] `Anthropic API Key` → `Anthropic API 密钥`
  - ctx: `render_api_key_input`
- L6502 [W8RQXC] `Google API Key` → `Google API 密钥`
  - ctx: `render_api_key_input`
- L6518 [2BR8EA] `Contact sales` → `联系销售`
  - ctx: `macro:vec`
- L6520 [SW2ZR5] ` to enable bringing your own API keys on your Enterprise plan.` → `以在企业版套餐中启用使用您自己的 API 密钥。`
  - ctx: `macro:vec`
- L6530 [7X661N] `Upgrade to the Build plan` → `升级到 Build 套餐`
  - ctx: `macro:vec`
- L6533 [JSN71Q] ` to use your own API keys.` → `以使用您自己的 API 密钥。`
  - ctx: `macro:vec`
- L6537 [CNJ0AN] `Ask your team's admin to upgrade to the Build plan to use your own API keys.` → `请您团队的管理员升级到 Build 套餐，以便使用您自己的 API 密钥。`
  - ctx: `macro:vec`
- L6577 [M09XEY] `Warp credit fallback` → `Warp 额度回退`
  - ctx: `render_ai_setting_toggle`
- L6587 [G5W2XD] `When enabled, agent requests may be routed to one of Warp's provided models in the event of an error. Warp will prioritize using your API keys over your Warp credits.` → `启用后，Agent 请求在出错时可能被路由到 Warp 提供的某个模型。Warp 会优先使用您的 API 密钥而非您的 Warp 额度。`
  - ctx: `render_ai_setting_description`
- L6603 [NFS2SC] **DNT** `api keys bring your own byo openai anthropic google claude gemini gpt`
- L6621 [B3M1GJ] `API Keys` → `API 密钥`
  - ctx: `build_sub_header`
- L6678 [KMA9TZ] **DNT** `aws login`
  - ctx: `.set_placeholder_text`
- L6859 [50HK7Z] `Warp loads and sends local AWS CLI credentials for Bedrock-supported models. This setting is managed by your organization.` → `Warp 会加载并发送本地 AWS CLI 凭据，用于受 Bedrock 支持的模型。此设置由您所在组织管理。`
- L6861 [2M0N4M] `Warp loads and sends local AWS CLI credentials for Bedrock-supported models.` → `Warp 会加载并发送本地 AWS CLI 凭据，用于受 Bedrock 支持的模型。`
- L6868 [BFTV2N] `Use AWS Bedrock credentials` → `使用 AWS Bedrock 凭据`
  - ctx: `render_ai_setting_toggle`
- L7000 [V4K81K] `Login Command` → `登录命令`
  - ctx: `render_input`
- L7007 [JWM1MS] `AWS Profile` → `AWS 配置`
  - ctx: `render_input`
- L7016 [Q2TWQC] `Automatically run login command` → `自动运行登录命令`
  - ctx: `render_ai_setting_toggle`
- L7025 [18AJ54] `When enabled, the login command will run automatically when AWS Bedrock credentials expire.` → `启用后，AWS Bedrock 凭据过期时会自动运行登录命令。`
  - ctx: `render_ai_setting_description`
- L7044 [9GCXDD] **DNT** `aws bedrock amazon credentials login profile`
- L7068 [VQVNVY] **DNT** `AWS Bedrock`
  - ctx: `build_sub_header`

## `app/src/app_menus.rs` (42 条)

- L42 [F4TY24] `Enable Shell Debug Mode (-x) for New Sessions` → `为新会话启用 Shell 调试模式 (-x)`
  - ctx: `const:ENABLE_SHELL_DEBUG_MODE_MENU_ITEM_NAME`
- L44 [X2FEDB] `Disable Shell Debug Mode (-x) for New Sessions` → `为新会话禁用 Shell 调试模式 (-x)`
  - ctx: `const:DISABLE_SHELL_DEBUG_MODE_MENU_ITEM_NAME`
- L45 [2YWXYW] `Enable In-band Generators for New Sessions` → `为新会话启用带内生成器`
  - ctx: `const:ENABLE_IN_BAND_GENERATORS_MENU_ITEM_NAME`
- L47 [MVP7RT] `Disable in-band generators for new sessions` → `为新会话禁用带内生成器`
  - ctx: `const:DISABLE_IN_BAND_GENERATORS_MENU_ITEM_NAME`
- L48 [TN4RTV] `Enable PTY Recording Mode (warp.pty.recording)` → `启用 PTY 录制模式（warp.pty.recording）`
  - ctx: `const:ENABLE_PTY_RECORDING`
- L49 [VD0W19] `Disable PTY Recording Mode (warp.pty.recording)` → `禁用 PTY 录制模式（warp.pty.recording）`
  - ctx: `const:DISABLE_PTY_RECORDING`
- L50 [Z25V97] `Show Initialization Block` → `显示初始化命令块`
  - ctx: `const:SHOW_BOOTSTRAP_BLOCK_MENU_ITEM_NAME`
- L51 [TYKWKT] `Hide Initialization Block` → `隐藏初始化命令块`
  - ctx: `const:HIDE_BOOTSTRAP_BLOCK_MENU_ITEM_NAME`
- L52 [6Z0ZSE] `Show In-band Command Blocks` → `显示带内命令块`
  - ctx: `const:SHOW_IN_BAND_COMMAND_BLOCKS_MENU_ITEM_NAME`
- L53 [36E4RY] `Hide In-band Command Blocks` → `隐藏带内命令块`
  - ctx: `const:HIDE_IN_BAND_COMMAND_BLOCKS_MENU_ITEM_NAME`
- L54 [9DSHE9] `Show Warpified SSH Blocks` → `显示 Warp 化 SSH 命令块`
  - ctx: `const:SHOW_SSH_COMMAND_BLOCKS_MENU_ITEM_NAME`
- L55 [F7T28R] `Hide Warpified SSH Blocks` → `隐藏 Warp 化 SSH 命令块`
  - ctx: `const:HIDE_SSH_COMMAND_BLOCKS_MENU_ITEM_NAME`
- L57 [E8JS5G] `Export Default Settings as CSV to home dir` → `将默认设置导出为 CSV 到主目录`
  - ctx: `const:EXPORT_DEFAULT_SETTINGS_CSV_MENU_ITEM_NAME`
- L83 [XDMGTR] `New Window` → `新建窗口`
  - ctx: `Menu::new`
- L104 [BNX16F] **DNT** `<NO DESCRIPTION>`
  - ctx: `.unwrap_or_else`
- L169 [A3CVTW] `Preferences` → `偏好设置`
  - ctx: `CustomMenuItem::new_with_submenu`
- L190 [41XFAC] `Privacy Policy...` → `隐私政策…`
  - ctx: `link_menu_item`
- L197 [JBCYVX] `Debug` → `调试`
  - ctx: `CustomMenuItem::new_with_submenu`
- L211 [FSX3XR] `Set Warp as Default Terminal` → `将 Warp 设为默认终端`
  - ctx: `CustomMenuItem::new`
- L231 [FVJDEF] `Log out` → `登出`
  - ctx: `CustomMenuItem::new`
- L255 [QTYHTR] `Open Recent` → `打开最近`
  - ctx: `CustomMenuItem::new_with_submenu`
- L302 [AEMGTA] `Use Warp's Prompt` → `使用 Warp 的提示符`
  - ctx: `macro:vec`
- L315 [A2NZ16] `Copy on Select within the Terminal` → `在终端中选择时即复制`
  - ctx: `macro:vec`
- L341 [FHQW5M] `Synchronize Inputs` → `同步输入`
  - ctx: `CustomMenuItem::new_with_submenu`
- L393 [JC9552] `Toggle Mouse Reporting` → `切换鼠标报告`
  - ctx: `macro:vec`
- L410 [X5GPRR] `Toggle Scroll Reporting` → `切换滚动报告`
  - ctx: `macro:vec`
- L425 [59KRGW] `Toggle Focus Reporting` → `切换焦点报告`
  - ctx: `macro:vec`
- L451 [CP5C11] `Compact Mode` → `紧凑模式`
  - ctx: `CustomMenuItem::new`
- L849 [SPFW68] `Manually Toggle Network Status` → `手动切换网络状态`
  - ctx: `CustomMenuItem::new`
- L865 [G5MYEH] **DNT** `Failed to create settings csv file`
  - ctx: `.expect`
- L869 [ND190J] **DNT** `Failed to write header record`
  - ctx: `.expect`
- L874 [8V99A7] **DNT** `Failed to write settings record`
  - ctx: `.expect`
- L883 [3ERAN6] `Create anonymous user` → `创建匿名用户`
  - ctx: `CustomMenuItem::new`
- L910 [RYTJD6] `Send Feedback...` → `发送反馈…`
  - ctx: `CustomMenuItem::new`
- L927 [QJCFH6] `Warp Documentation...` → `Warp 文档…`
  - ctx: `Menu::new > macro:vec`
- L928 [AKMQAN] `GitHub Issues...` → `GitHub Issues…`
  - ctx: `Menu::new > macro:vec`
- L929 [BHGP7J] `Warp Slack Community...` → `Warp Slack 社区…`
  - ctx: `Menu::new > macro:vec`
- L963 [1MK0B9] `Save New...` → `另存为新…`
  - ctx: `CustomMenuItem::new`
- L984 [BMJJJ4] `New Terminal Tab` → `新建终端标签页`
  - ctx: `macro:vec`
- L1009 [8EWNDB] `New Agent Tab` → `新建 Agent 标签页`
  - ctx: `macro:vec`
- L1045 [GT3K5X] `Reopen closed session` → `重新打开已关闭的会话`
  - ctx: `CustomMenuItem::new`
- L1060 [BYQ7CZ] `Launch Configurations` → `启动配置`
  - ctx: `CustomMenuItem::new_with_submenu`

## `app/src/ai/execution_profiles/editor/ui_helpers.rs` (13 条)

- L71 [15HX6R] `This option is enforced by your organization's settings and cannot be customized.` → `此选项由您所在组织的设置强制启用，无法自定义。`
  - ctx: `const:WORKSPACE_OVERRIDE_TOOLTIP_MESSAGE`
- L263 [3CZYYC] `Base model` → `基础模型`
  - ctx: `render_filterable_dropdown_row`
- L449 [F0B0SS] `Apply code diffs` → `应用代码差异`
  - ctx: `render_permission_row`
- L460 [Y2TSMV] `Read files` → `读取文件`
  - ctx: `render_permission_row`
- L484 [CJ9XE7] `Execute commands` → `执行命令`
  - ctx: `render_permission_row`
- L521 [PRYKHY] `Interact with running commands` → `与运行中的命令交互`
  - ctx: `render_permission_row`
- L559 [VATQM7] `Call MCP servers` → `调用 MCP 服务器`
  - ctx: `render_permission_row`
- L706 [PST9NN] `Directory allowlist` → `目录白名单`
  - ctx: `render_list_section`
- L707 [BH4SJP] `Give the agent file access to certain directories.` → `授予 Agent 对特定目录的文件访问权限。`
  - ctx: `render_list_section`
- L731 [0DR5DC] `Command allowlist` → `命令白名单`
  - ctx: `render_list_section`
- L797 [GKDRS7] `Command denylist` → `命令黑名单`
  - ctx: `create_section_header`
- L825 [1X5WM7] `MCP allowlist` → `MCP 白名单`
  - ctx: `render_list_section`
- L851 [BWH1R9] `MCP denylist` → `MCP 黑名单`
  - ctx: `render_list_section`

## `app/src/ai/execution_profiles/editor/mod.rs` (4 条)

- L279 [G2EGXN] `Agent decides` → `由 Agent 决定`
  - ctx: `.set_items > macro:vec`
- L291 [DFNM2V] `Always ask` → `总是询问`
  - ctx: `.set_items > macro:vec`
- L375 [R9PCYC] `Ask on first write` → `首次写入时询问`
  - ctx: `.set_items > macro:vec`
- L472 [CXZX40] `Select MCP servers` → `选择 MCP 服务器`
  - ctx: `.set_menu_header_to_static`

## `app/src/settings_view/about_page.rs` (3 条)

- L57 [K51ZP8] **DNT** `about warp version`
- L75 [Q79HB8] **DNT** `v#.##.###`
  - ctx: `.unwrap_or`
- L121 [JX4A6D] **DNT** `Copyright 2026 Warp`
  - ctx: `.span`

## `app/src/ai/blocklist/prompt/prompt_alert.rs` (2 条)

- L41 [BFV41D] `Compare plans` → `比较套餐`
  - ctx: `const:COMPARE_PLANS_TEXT`
- L42 [T06GN0] `Contact support` → `联系支持`
  - ctx: `const:CONTACT_SUPPORT_TEXT`

## `app/src/ai/blocklist/block/cli.rs` (1 条)

- L1821 [XYCKAF] `Always allow` → `总是允许`
  - ctx: `.span`

## `app/src/drive/index.rs` (1 条)

- L4128 [PNVB03] `MCP Servers` → `MCP 服务器`

## `app/src/ai/blocklist/block/status_bar.rs` (1 条)

- L1016 [3WW0YS] `Learn more` → `了解更多`
  - ctx: `FormattedTextFragment::hyperlink`

## `app/src/ai/blocklist/block.rs` (1 条)

- L1101 [21RFGY] `Manage rules` → `管理规则`
  - ctx: `ActionButton::new`

## `app/src/auth/auth_view_body.rs` (1 条)

- L481 [AK09HR] `Sign up` → `注册`
  - ctx: `.with_centered_text_label`

## `app/src/search/command_search/view.rs` (1 条)

- L984 [7D1213] `Upgrade AI Usage` → `升级 AI 用量`
  - ctx: `.attempt_login_gated_feature`

## `app/src/ai/blocklist/agent_view/agent_input_footer/toolbar_item.rs` (1 条)

- L115 [79T098] `Voice Input` → `语音输入`

## `app/src/ai/mcp/templatable_manager/native.rs` (1 条)

- L150 [G4Y7CZ] `Unknown reason` → `未知原因`
  - ctx: `macro:format`

## `app/src/ai/blocklist/summarization_cancel_dialog.rs` (1 条)

- L128 [PB4SQN] **DNT** `Valid keystroke`
  - ctx: `.expect`
