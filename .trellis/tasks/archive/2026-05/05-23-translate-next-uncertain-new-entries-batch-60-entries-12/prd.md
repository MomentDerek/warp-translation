# Translate next uncertain new entries — batch 60 entries 12 (Strategy: first uncertain-pool sweep; 67 high-confidence UI translations across 4 files + 38 extractor-false-positive doc-comment flags across 3 files)

## Goal

第一次从 **uncertain verdict 池**取词（batch-11 已清零 auto_ui-new 热点；剩余 4398 条 `status=new` 全部 `verdict=uncertain`）。本批严格分流——只翻译**显然面向用户**的 UI 标签/Toast/对话文案，对 `lazy_static!`/macro 内部被误抓取的 doc comment 一律标记 `do_not_translate, extractor_false_positive_doc_comment`。

**67 条翻译 + 38 条 do_not_translate 标记 = 105 条 entry 状态翻转**：

| 文件 | 翻译数 | 不翻译数 | 说明 |
|---|---|---|---|
| `app/src/settings_view/features_page.rs` | 11 | 0 | `ToggleSettingActionPair::new(...)` 命令面板标签（`Enable {x}` / `Disable {x}` 显示文案） |
| `app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs` | 21 | 0 | Agent 输入栏：Voice/Plugin/Notifications 按钮与 Toast |
| `app/src/ai/execution_profiles/editor/ui_helpers.rs` | 20 | 0 | 执行 Profile 编辑器：Section 标题、模型描述、权限/MCP 段落 |
| `app/src/terminal/model/secrets.rs` | 15 | 4 | 15 条 `DefaultRegex.name` 机密类型 UI 标签 + 4 条 `regexes` mod 内 doc cmts |
| `app/src/util/bindings.rs` | 0 | 19 | `lazy_static!` 内 doc comment 误抓取 |
| `app/src/experiments/mod.rs` | 0 | 14 | `lazy_static!` 内 doc comment 误抓取 |

继 batch-11 之后，`translated` 2284 → 2389，`new` 4398 → 4293，`fuzzy` 保持 52。`uncertain audit` 仍为 4531（不变，纯计算字段）。

## What I already know

- 当前 `strings.json` 统计（应用前）：`entry_count=6734`, `translated=2284`, `new=4398`, `fuzzy=52`, `uncertain (audit verdict)=4531`。
- glossary 现有 95 条；本批沿用既有术语：`Warp` / `Warp Drive` / `Oz` / `Agent` / `MCP` / `Profile（品牌词，保留）` / `PTY` / `REPL` / `Linux` / `OAuth` / `JWT` / `IPv4` / `IPv6` / `MAC（地址）` / `AWS` / `GitHub` / `Slack` / `Stripe` / `Firebase` / `Fireworks` / `SK（前缀）` / `shell` / `chip → chip（保留英文）` / `token → token（小写常用词不译）` / `Full Terminal Agent`（产品分类名，保留）。无新增 term，`term_count` 保持 95。
- **占位符**（10+ 处）：
  - `{}`（features_page L518 `Enable {} notifications`、agent_input_footer L1914 backtick-wrapped `\`{}\`` voice key、ui_helpers L811 `MCP Server {uuid}` ← 命名占位符）
  - `{uuid}`、`{agent}`、`{now}`、`{log}`（agent_input_footer L2764 log header — 这条不在本批，注意）
- **`Installing Warp plugin...` / `Updating Warp plugin...`**：源用 ASCII `...`，按项目惯例转 `……`。
- **`Voice input is enabled. You can also press and hold the \`{}\` key ... (configure in Settings > AI > Voice)`** (agent_input_footer L1914)：反引号包裹的 `{}` 占位符保留；`Settings > AI > Voice` 是导航路径，保留英文（与 Warp 应用现有设置面板英文键名一致）。
- **`Now using Full Terminal Agent's default model.` (L2263)**：`Full Terminal Agent` 是 Agent 模型分类名（与既有 `Full Terminal Use → 完整终端能力` 同语义系列，但此处是 Agent 类名），保留英文。译「现已使用 Full Terminal Agent 的默认模型。」。
- **`Default profile name cannot be changed.` (ui_helpers L95)**：`Profile` 保留品牌大写。与既有 `Manage profile → 管理 Profile` 一致。
- **`Edit Profile` (ui_helpers L107)**：与既有 `Profile 编辑器` 等用法一致。译「编辑 Profile」。
- **`Computer use` / `Computer use model`**：与既有 `Computer use in Cloud Agents → 云端 Agent 中的计算机使用` 一致 → `计算机使用`。
- **`Ask questions` / `Call web tools`**：执行 Profile 编辑器权限项标题，与既有 `Ask questions: → 提问：` / `Call web tools: → 调用网页工具：`（带冒号的引导文本）对齐 → `提问` / `调用网页工具`（无冒号标题形式）。
- **`Call MCP servers` (既译 `调用 MCP 服务器`)** 不在本批；本批只取 MCP allow/deny 描述：
  - `MCP servers that are allowed to be called by Oz.` → `Oz 允许调用的 MCP 服务器。`
  - `MCP servers that are not allowed to be called by Oz.` → `Oz 不允许调用的 MCP 服务器。`
- **`Regular expressions to match commands ... can be automatically executed by Oz.` / `... that Oz should always ask permission to execute.`**：与既有 `Regular expressions to match commands that the Warp Agent should always ask permission to execute. → 用于匹配 Warp Agent 在执行前总是询问权限的命令的正则表达式。` 同结构。译「用于匹配可由 Oz 自动执行的命令的正则表达式。」/「用于匹配 Oz 在执行前总是询问权限的命令的正则表达式。」。
- **`Plan auto-sync` / `The plans this agent creates will be automatically added and synced to Warp Drive.`**：`Warp Drive` 保留品牌。译「计划自动同步」/「此 Agent 创建的计划将自动添加并同步到 Warp Drive。」。
- **`The base model's working memory — how many tokens of your conversation ...` (L322)**：长描述。`tokens` 小写常用词不译。译保留破折号（`——`）。`tokens` 在中文里保留小写英文（与既有 `Context window (tokens) → 上下文窗口（tokens）` 一致用法）。
- **`The model used when the agent operates inside interactive terminal applications like database shells, debuggers, REPLs, or dev servers—reading live output and writing commands to the PTY.` (L275)**：`shell`/`REPL`/`PTY` 保留英文。译保留破折号（`——`）。
- **`This model serves as the primary engine ... conversation summarization.` (L264)**：base model 描述长文。`Warp` 保留。
- **secrets.rs 机密类型 UI 标签（15）**：来自 `terminal/model/secrets.rs::regexes::DEFAULT_REGEXES_WITH_NAMES`，在 `settings_view/privacy_page.rs` 中显示为机密脱敏正则名称（用户可见列表）。处理原则：
  - 协议/技术缩写保留英文（`IPv4`、`IPv6`、`MAC`、`AWS`、`OAuth`、`JWT`、`SK`）。
  - 品牌名保留英文（`GitHub`、`Slack`、`Stripe`、`Firebase`、`Fireworks`）。
  - 通用名词译中文（`Address` → `地址`、`Token` → `令牌`、`Key` → `密钥`、`API Key` → `API 密钥`）。
  - `Auth Domain` → `认证域名`、`Access ID` → `访问 ID`。
  - `Server-to-Server` / `User-to-Server` 直译为「服务器对服务器」/「用户对服务器」（机密上下文中描述 token 颁发主体方向）。
  - `Personal Access Token` → `个人访问令牌`、`Classic` → `经典`、`Fine-Grained` → `细粒度`、`Generic` → `通用`。
- **agent_input_footer 21 条**：均为 plugin 安装/更新 toast、voice input 状态文案、`Dismiss`/`Enable notifications`/`Update Warp plugin` 按钮。
  - `Dismiss` → `关闭`（与既有 toast `Dismiss` 风格通用动作；既有 `Auto dismiss Rich Input ...` 中 `dismiss` 译「关闭」）。
  - `Rich Input` → `富文本输入`（与既有 `Auto dismiss Rich Input after prompt submission → 提交提示词后自动关闭富文本输入` 一致）。
  - `Could not automatically install plugin. Please click the chip again ...` → `chip` 保留英文（与 batch-11 `prompt context chip → 提示词上下文 chip` 一致）。
  - `Failed to start voice input (you may need to enable Microphone access)` → 「启动语音输入失败（您可能需要启用麦克风访问权限）」。
- **features_page.rs 11 条**：均为 `ToggleSettingActionPair::new("<lowercase label>", ...)` 第一参数，作为 `Enable {label}`/`Disable {label}` 命令面板动作标签显示，与 batch-11 之前已译 L313/L355/L387/L451 等同体系。沿用既有 lowercase → 中文规整用语模式：
  - `linux selection clipboard` → `Linux 选择剪贴板`（既有 `Honor linux selection clipboard → 遵循 Linux 选择剪贴板`，本条短形式）。`Linux` 首字母大写规范化。
  - `audible terminal bell` → `终端响铃`（与既有 `Use Audible Bell → 启用响铃` 一致）。
  - `copy on select within the terminal` → `终端内选中即复制`（与既有 `Copy on select → 选中即复制` 一致）。
  - `syntax highlighting` → `语法高亮`、`error underlining` → `错误下划线`、`scroll reporting` → `滚动上报`、`command corrections` → `命令纠错`、`completions while typing` → `输入时自动打开补全`、`autosuggestion keybinding hint` → `自动建议快捷键提示`、`autocomplete quotes, parentheses, and brackets` → `自动补全引号、圆括号和方括号`（与既有 `Autocomplete quotes, parentheses, and brackets → 自动补全引号、圆括号和方括号` 一致大小写差异不分译）、`restore windows, tabs, and panes on startup` → `启动时恢复窗口、标签页和窗格`（与既有 `Restore windows, tabs, and panes on startup` 译文一致）。
- **38 条 `do_not_translate, extractor_false_positive_doc_comment`**：全部为 `lazy_static!` 内 `pub static ref XXX:` 之前的 `///` doc comment 行。Extractor 抓取后被 LLM verdict 评为 `uncertain`，但本质上不会显示给最终用户。沿用 batch-7/-8/-9/-10 `extractor_false_positive_doc_comment` 处置惯例：`target=null + status=translated + flags=[batch_flag, do_not_translate, extractor_false_positive_doc_comment]`。
  - `app/src/util/bindings.rs` 19 条（L143-214，跨 5 个 `pub static ref` 的 doc cmt 段）。
  - `app/src/experiments/mod.rs` 14 条（L47-80，跨 5 个 `static ref` 的 doc cmt 段）。
  - `app/src/terminal/model/secrets.rs` 4 条（L31-43，模块/字段 doc cmts）。
- **本批未触及的内容**：
  - `features_page.rs` 的 `search_terms()` lowercase keyword bundles（如 `wayland x11 window system compositor`、`gpu graphics backend vulkan dx12 directx12 opengl driver` 等）—— 翻译策略尚未确定（应翻译为中文搜索关键词，还是保留英文以保证 fallback？），延后到下批讨论。
  - `features_page.rs` 内 `.expect("XXX failed to serialize")` 系列（10+ 条）—— 内部诊断 panic，按既有 panic 惯例可翻译，但本批先专注 UI 高确定度路径。
  - `features_page.rs` 的 `width: {:?}, height: {:?}`、`{}s` 等 telemetry payload format strings —— 应标记 `do_not_translate, telemetry_payload`，延后专批处理。
  - 大量 settings/schemars `description:` —— 是否翻译有待协议讨论。
  - `editor/view/model/mod.rs` ~22 条 panic strings —— 集中一批 panic 翻译更划算。
  - `terminal/view/action.rs` 全部 telemetry log labels —— 应整批 `do_not_translate`。

## Scope by file

### app/src/settings_view/features_page.rs (11)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12JWZN15AZVXMV98ZN6` | 136 | `copy on select within the terminal` | `终端内选中即复制` |
| `01KQXQV12J1VD2NJ5FTSRG4N31` | 144 | `linux selection clipboard` | `Linux 选择剪贴板` |
| `01KQXQV12JDMCCM6JD4N3063S2` | 157 | `autocomplete quotes, parentheses, and brackets` | `自动补全引号、圆括号和方括号` |
| `01KQXQV12JCJCGRFCNSXXXGQHX` | 170 | `restore windows, tabs, and panes on startup` | `启动时恢复窗口、标签页和窗格` |
| `01KQXQV12JEEGWNXSDD9MFY426` | 204 | `scroll reporting` | `滚动上报` |
| `01KQXQV12J34WMS5YR03JX442F` | 217 | `completions while typing` | `输入时自动打开补全` |
| `01KQXQV12JMYYRH4TCN11RW83Y` | 230 | `command corrections` | `命令纠错` |
| `01KQXQV12J2CTVE0DB6RQJBM7H` | 243 | `error underlining` | `错误下划线` |
| `01KQXQV12J76CQKJ9DVRG25VZ9` | 256 | `syntax highlighting` | `语法高亮` |
| `01KQXQV12JXNXJPH5Y4DZME8F4` | 269 | `audible terminal bell` | `终端响铃` |
| `01KQXQV12J9W3W9MKVWX3XJVTB` | 290 | `autosuggestion keybinding hint` | `自动建议快捷键提示` |

### app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs (21)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FX5BN5WV9YA9YDXWJ` | 395 | `Rich Input` | `富文本输入` |
| `01KQXQV12BH2FXHVKE75ZVAY10` | 421 | `Enable notifications` | `启用通知` |
| `01KQXQV12DVPN5GW70YEKC8QJ6` | 435 | `Notifications setup instructions` | `通知设置说明` |
| `01KQXQV12H51MCY67D9JT6V25N` | 449 | `Update Warp plugin` | `更新 Warp 插件` |
| `01KQXQV12EYAPK3KHWGPCF2TRB` | 461 | `Plugin update instructions` | `插件更新说明` |
| `01KQXQV12BHBPBMQKRZ93H2FZ5` | 478 | `Dismiss` | `关闭` |
| `01KQXQV12B4FC1PF06E59A1K0D` | 518 | `Enable {} notifications` | `启用 {} 通知` |
| `01KQXQV12CHRHKTX69F601RDVP` | 554 | `Hide Rich Input` | `隐藏富文本输入` |
| `01KQXQV12F5GWREY5TS3ZHBQGN` | 1340 | `See logs for details` | `查看日志了解详情` |
| `01KQXQV12H96ZBKZ3720R7S9QZ` | 1367 | `Warp plugin installed. Please restart the session to activate.` | `Warp 插件已安装。请重启会话以激活。` |
| `01KQXQV12CV9JNMNGWMS5W1PAP` | 1369 | `Installing Warp plugin...` | `正在安装 Warp 插件……` |
| `01KQXQV12B9613WM7JYZ6PXQ7B` | 1370 | `Failed to install Warp plugin` | `Warp 插件安装失败` |
| `01KQXQV12HHGP6YRDPW7TF4WF0` | 1384 | `Warp plugin updated. Please restart the session to activate.` | `Warp 插件已更新。请重启会话以激活。` |
| `01KQXQV12HS0GJ3QC23VZRF8Q6` | 1386 | `Updating Warp plugin...` | `正在更新 Warp 插件……` |
| `01KQXQV12BF4R2FQ7W0WF8SH65` | 1387 | `Failed to update Warp plugin` | `Warp 插件更新失败` |
| `01KQXQV12A87P6BP6ZB8VM2EGN` | 1190 | `Could not automatically install plugin. Please click the chip again for manual installation steps.` | `无法自动安装插件。请再次点击 chip 查看手动安装步骤。` |
| `01KQXQV12HGSCZCEHQRD0NSZ28` | 1740 | `Voice input limit reached` | `语音输入额度已达上限` |
| `01KQXQV12B7QV42G3JNSA1TF93` | 1860 | `Failed to transcribe voice input` | `转写语音输入失败` |
| `01KQXQV12BYCC1XY73G9DMEQPB` | 1901 | `Failed to start voice input (you may need to enable Microphone access)` | `启动语音输入失败（您可能需要启用麦克风访问权限）` |
| `01KQXQV12H7E8T0ZSB5V9KQ2DN` | 1914 | `Voice input is enabled. You can also press and hold the \`{}\` key to activate voice input (configure in Settings > AI > Voice)` | `语音输入已启用。您也可以按住 \`{}\` 键来激活语音输入（在 Settings > AI > Voice 中配置）` |
| `01KQXQV12D9CF1JKM42A91VF9B` | 2263 | `Now using Full Terminal Agent's default model.` | `现已使用 Full Terminal Agent 的默认模型。` |

### app/src/ai/execution_profiles/editor/ui_helpers.rs (20)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12APA1KYZRT9HMA3M02` | 95 | `Default profile name cannot be changed.` | `默认 Profile 名称无法修改。` |
| `01KQXQV12BV5A1E6AX2PTHD6HP` | 107 | `Edit Profile` | `编辑 Profile` |
| `01KQXQV12GFEE5XT1NFPBYR6MK` | 264 | `This model serves as the primary engine behind the agent. It powers most interactions and invokes other models for tasks like planning or code generation when necessary. Warp may automatically switch to alternate models based on model availability or for auxiliary tasks such as conversation summarization.` | `此模型作为 Agent 背后的主引擎。它支持大多数交互，并在需要时调用其他模型来完成规划或代码生成等任务。Warp 可能会根据模型可用性，或为对话摘要等辅助任务自动切换到备用模型。` |
| `01KQXQV12CR8WKF4SRQ6AJY5VX` | 274 | `Full terminal use model` | `完整终端能力模型` |
| `01KQXQV12G8AQBFGKEY9A91DKH` | 275 | `The model used when the agent operates inside interactive terminal applications like database shells, debuggers, REPLs, or dev servers—reading live output and writing commands to the PTY.` | `Agent 在数据库 shell、调试器、REPL 或开发服务器等交互式终端应用中运行时所使用的模型——读取实时输出并向 PTY 写入命令。` |
| `01KQXQV12A5FSER1N5MRP6XJGE` | 282 | `Computer use model` | `计算机使用模型` |
| `01KQXQV12G822RT3ZDK0TWGYJR` | 283 | `The model used when the agent takes control of your computer to interact with graphical applications through mouse movements, clicks, and keyboard input.` | `Agent 通过鼠标移动、点击和键盘输入接管您的计算机以操作图形化应用时所使用的模型。` |
| `01KQXQV12AH02DR5MWRPG706AE` | 313 | `Context window` | `上下文窗口` |
| `01KQXQV12GF1W2TVQ4R6MFSGMQ` | 322 | `The base model's working memory — how many tokens of your conversation, code, and documents it can consider at once. Larger windows enable longer conversations and more coherent responses over bigger codebases, at the cost of higher latency and compute usage.` | `基础模型的工作记忆——它可同时考虑的对话、代码与文档的 token 数量。窗口越大，越能支持更长的对话以及在更大代码库上更连贯的响应，代价是更高的延迟与计算开销。` |
| `01KQXQV12A2NT4N6DD5G82SDPG` | 534 | `Computer use` | `计算机使用` |
| `01KQXQV129RDMZC21M63CAGKCW` | 547 | `Ask questions` | `提问` |
| `01KQXQV12EJZJ85TGD43DYDYPF` | 732 | `Regular expressions to match commands that can be automatically executed by Oz.` | `用于匹配可由 Oz 自动执行的命令的正则表达式。` |
| `01KQXQV12E0G3EP5FPY0AFFDKW` | 798 | `Regular expressions to match commands that Oz should always ask permission to execute.` | `用于匹配 Oz 在执行前总是询问权限的命令的正则表达式。` |
| `01KQXQV12D1G1H3CZ5Z1Q8BRM2` | 811 | `MCP Server {uuid}` | `MCP 服务器 {uuid}` |
| `01KQXQV12DWT6CF5E8D4MJY2V2` | 826 | `MCP servers that are allowed to be called by Oz.` | `Oz 允许调用的 MCP 服务器。` |
| `01KQXQV12DB4PCF4N84QBTNJ14` | 852 | `MCP servers that are not allowed to be called by Oz.` | `Oz 不允许调用的 MCP 服务器。` |
| `01KQXQV12E138QCRQ5MB9YK82R` | 886 | `Plan auto-sync` | `计划自动同步` |
| `01KQXQV12GB7PBAG3ESTFBZ6MN` | 894 | `The plans this agent creates will be automatically added and synced to Warp Drive.` | `此 Agent 创建的计划将自动添加并同步到 Warp Drive。` |
| `01KQXQV12936790QJE18S5NT3V` | 960 | `Call web tools` | `调用网页工具` |
| `01KQXQV12G1Y865VV0M359GB8J` | 968 | `The agent may use web search when helpful for completing tasks.` | `Agent 可在有助于完成任务时使用网页搜索。` |

### app/src/terminal/model/secrets.rs (15 translated)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12C69WBW49RJ8JSD5Q9` | 537 | `IPv4 Address` | `IPv4 地址` |
| `01KQXQV12CF3FKC4N9E5VCVY8V` | 541 | `IPv6 Address` | `IPv6 地址` |
| `01KQXQV12E5NTEPW2JBFG5D765` | 545 | `Phone Number` | `电话号码` |
| `01KQXQV12D97R2ZRTTXNT170YV` | 549 | `MAC Address` | `MAC 地址` |
| `01KQXQV128P4TWH95VBS9521FE` | 557 | `AWS Access ID` | `AWS 访问 ID` |
| `01KQXQV12GG0WQ98Y9ANQQFE99` | 561 | `Slack App Token` | `Slack 应用令牌` |
| `01KQXQV12C74W327ZMWRCBG40R` | 565 | `GitHub Classic Personal Access Token` | `GitHub 经典个人访问令牌` |
| `01KQXQV12C85QY0YDJJ7Z1XBNR` | 569 | `GitHub Fine-Grained Personal Access Token` | `GitHub 细粒度个人访问令牌` |
| `01KQXQV12CEFGTB6M2R0E15XT5` | 573 | `GitHub OAuth Access Token` | `GitHub OAuth 访问令牌` |
| `01KQXQV12CGK53GZGYZ2GRXMWR` | 577 | `GitHub User-to-Server Token` | `GitHub 用户对服务器令牌` |
| `01KQXQV12CA4A18X36TKACP25K` | 581 | `GitHub Server-to-Server Token` | `GitHub 服务器对服务器令牌` |
| `01KQXQV12G1B95JANM219ESM36` | 585 | `Stripe Key` | `Stripe 密钥` |
| `01KQXQV12CXP9EMM8RJ9VQZ1KK` | 589 | `Firebase Auth Domain` | `Firebase 认证域名` |
| `01KQXQV12CADVG525BZM47C2CB` | 605 | `Generic SK API Key` | `通用 SK API 密钥` |
| `01KQXQV12CX0CPDAZRY2H2JWWG` | 609 | `Fireworks API Key` | `Fireworks API 密钥` |

## do_not_translate entries (38) — `extractor_false_positive_doc_comment`

### app/src/util/bindings.rs (19) — `lazy_static!` 内 doc comments

| ID | Line | Source | Flag | Reason |
|---|---|---|---|---|
| `01KQXQV112PE61M4406QEDR3F5` | 143 | ` Maps for converting from custom tags back to the action enum` | extractor_false_positive_doc_comment | `///` 注释解释 `CUSTOM_TAG_TO_ACTION` 用途 |
| `01KQXQV11PW8CN4GF9QQKY0K6Q` | 144 | ` This layer of indirection is necessary because the UI framework can't` | extractor_false_positive_doc_comment | 同上下文 |
| `01KQXQV11YYSP9B5YJ3838RWXT` | 146 | ` as plain isizes.  Within Warp though we want to deal with them as the enum type.` | extractor_false_positive_doc_comment | 同上下文 |
| `01KQXQV116QDKJRVDWADZT3EA8` | 151 | ` Regex that matches whether the the normalized form of a [`Keystroke`] matches a control` | extractor_false_positive_doc_comment | `CONTROL_CHARACTER_KEY_REGEX` 注释 |
| `01KQXQV11YP1R6K6V7FJ2MFVRE` | 152 | ` character. ASCII control characters constitute the first 31 values of ASCII characters.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11Q4H5DP2W5QDXBVMRB` | 153 | ` Though they have their own ASCII codepoints, they are typed into the keyboard using` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11WP69TH8GTST7PHFT4` | 154 | ` \`ctrl-XX\`, see <https://en.wikipedia.org/wiki/Caret_notation>.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV10NHR482QB0QBHMF8HP` | 156 | ` As an example, the ETX character (represented as \`^C\` in caret notation) is sent to` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV1250MS0AWHQCJHGDZTW` | 157 | ` the PTY when the user presses \`ctrl-c\`.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11JS8PYQD59EQK5KB9Y` | 160 | ` The full list of these control characters (and their corresponding name) are documented` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11YJ36F8QATCX5ZA9C7` | 161 | ` below:` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11QQFYEZ6Z85VR7PVA9` | 197 | ` Though caret notation uses uppercase letters (\`^C\` instead of \`^c\`), we validate using` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11W30R9JKTJHNXWED4P` | 199 | ` \`ctrl-[A-Z]\`. See [\`Keystroke::parse\`].` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11DHGFPJJYBMFV4X1A9` | 202 | ` Set of actions on Mac that should be considered valid bindings even though they aren't PTY` | extractor_false_positive_doc_comment | `MAC_PTY_NON_COMPLIANT_ACTIONS` 注释 |
| `01KQXQV126QRFKQ8H0R35GP99M` | 205 | ` this allowlist to special case these legacy actions for the purposes of binding validation.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11DWEVPW9B29C7DK37S` | 208 | ` Set of actions on Windows that should be considered valid bindings even though they aren't` | extractor_false_positive_doc_comment | `WINDOWS_PTY_NON_COMPLIANT_KEYSTROKES` 注释 |
| `01KQXQV1151REV1B3JEZT4EVA1` | 209 | ` PTY compliant. Windows users expect pasting to work using both \`ctrl-v\` and \`ctrl-shift-v\`,` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV1250N3W9XXJB3Y23K7P` | 210 | ` so we allowlist the terminal paste action for the purposes of binding validation.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11DM39176D6C9BXVRD1` | 213 | ` Set of keystrokes that should be considered valid bindings on all platforms even though` | extractor_false_positive_doc_comment | `PTY_NON_COMPLIANT_KEYSTROKES` 注释 |
| `01KQXQV1260VRQHHZEXH8FF2HR` | 214 | ` they aren't PTY compliant.` | extractor_false_positive_doc_comment | 同上 |

### app/src/experiments/mod.rs (14) — `lazy_static!` 内 doc comments

| ID | Line | Source | Flag | Reason |
|---|---|---|---|---|
| `01KQXQV110PT4A9Q1FPVTXB9QV` | 47 | ` In-memory map that caches users' group assignments so we don't have to calculate` | extractor_false_positive_doc_comment | `GROUP_ASSIGNMENTS` 注释 |
| `01KQXQV122KRH5AM1FXJW29M50` | 48 | ` it from their anonymous id each time. Also keeps track of experiment overrides.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV111Y0GFP4W1Z8832485` | 49 | ` Key is the name of the experiment, and the value is the variant name.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV110RNKMCM7T04DTWCPY` | 54 | ` In-memory map that stores the user's local overrides. This map differs from` | extractor_false_positive_doc_comment | `USER_OVERRIDES` 注释 |
| `01KQXQV10XS3KTD9PM4G1KVRXC` | 55 | ` GROUP_ASSIGNMENTS as it uses owned strings to store the overrides read from` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV122098HK8Z6M6JDHVCS` | 57 | ` keys are experiment names and the values are the variant names.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV10M4QSCSA3PF97K7BPQ` | 60 | ` All of the layers currently enabled in the application. A layer must be added` | extractor_false_positive_doc_comment | `LAYERS` 注释 |
| `01KQXQV121BX7B585MFZGS5MWZ` | 63 | ` in users never being assigned to the experiment in non-local builds.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV10V8KKC8PS04GS8YFY7` | 65 | ` EMPTY_LAYER is not included here, since we will never add experiments to it,` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV11X2JTFAGHD7HZ8RFBG` | 66 | ` and so users can never be assigned to experiments in EMPTY_LAYER.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV112PZAFQ8KVKCNX2JH6` | 74 | ` Mapping of experiments to their respective layers. The mappings are built up` | extractor_false_positive_doc_comment | `EXPERIMENT_LAYER_MAPPINGS` 注释 |
| `01KQXQV120M51MVYJB9JJBESTG` | 75 | ` during bootstrap. The keys are experiment names.` | extractor_false_positive_doc_comment | 同上 |
| `01KQXQV10KXCW3VT178EQXQVF7` | 78 | ` A no-op layer. This layer is only used if an error state occurs where there is` | extractor_false_positive_doc_comment | `EMPTY_LAYER` 注释 |
| `01KQXQV1275TT0NHFQ6D7ARBB7` | 80 | ` user will never be assigned to the experiment.` | extractor_false_positive_doc_comment | 同上 |

### app/src/terminal/model/secrets.rs (4) — module/struct doc comments

| ID | Line | Source | Flag | Reason |
|---|---|---|---|---|
| `01KQXQV11RG4FZ4KPTDDGRK28W` | 31 | ` Used for secret redaction in the Grid.` | extractor_false_positive_doc_comment | struct field doc cmt |
| `01KQXQV11199NJE5M1HQ8XKK3E` | 32 | ` Initially empty - will be populated with user-defined regexes when safe mode is enabled.` | extractor_false_positive_doc_comment | struct field doc cmt |
| `01KQXQV11RVV6ZZ3NCAASDSQSG` | 37 | ` Used for secret redaction in simple text strings (e.g.: rich content blocks).` | extractor_false_positive_doc_comment | struct field doc cmt |
| `01KQXQV11QFWT1WSY1K81E4GVJ` | 43 | ` Tracks counts to infer which regex patterns correspond to which secret levels` | extractor_false_positive_doc_comment | struct field doc cmt |

## Decisions / Anomalies

- **首次切入 uncertain 池**：之前 11 个批次集中清扫 `verdict=auto_ui`。本批是 uncertain 池首次扫描。策略——按文件聚簇审视，确认 100% user-facing 才翻译，混杂的 macro/`lazy_static!` 内 doc 注释立即标 `do_not_translate, extractor_false_positive_doc_comment`。
- **`features_page.rs` 11 条**：均位于 L130-300 区间的 `ToggleSettingActionPair::new(<lowercase label>, ...)` 列表。第一参数作为 `Enable {label}` 或 `Disable {label}` 模板的 `{label}` 槽位显示在命令面板（参 batch-11 `Profile`/`Manage profile` 等品牌词用法）。100% UI 路径已通过 `mod.rs::SettingActionPairDescriptions::{enable, disable}` 验证。
- **`features_page.rs` 未触及的 `search_terms()` 长 keyword bundles**：本文件 L4000-L7300 内大量 `fn search_terms(&self) -> &str { "wayland x11 window system compositor" }` 风格条目，长 lowercase 关键词串。**翻译策略未定**——若翻译为中文，可让中文用户搜索；若保留英文，则在中文 UI 下设置搜索完全失效。本批跳过，留待下一批专门讨论。
- **`features_page.rs` 内 `.expect("failed to serialize XXX")` 系列**：约 10 条，CamelCase Rust 标识符紧跟 panic 串（如 `failed to serialize ShowAutosuggestionIgnoreButton`）。沿用 batch-7/-11 panic 翻译惯例可译，但本批聚焦 UI 高确定度路径，跳过。
- **`features_page.rs` 内 `width: {:?}, height: {:?}` / `{}s` / `1 million` / `10 million`**：均为 `TelemetryEvent::FeaturesPageAction.value` payload format strings 或调试常量，不对外显示。应标记 `do_not_translate, telemetry_payload`/`debug_only`，集中专批处理。
- **`agent_input_footer/mod.rs` 21 条**：均为 voice input/Warp plugin install-update toast/通知/按钮文案。100% UI，无需歧义判断。`chip` 保留英文与 batch-11 `提示词上下文 chip` 用法一致。
- **`agent_input_footer/mod.rs` 未触及的 `Warp plugin installation — {agent:?}\n{now}\n\n{log}` (L2764)**：是 `fs::write(&log_path, contents)` 写入到磁盘日志文件的内容头。仅供开发者排错查看，非 UI 渲染路径。应标 `do_not_translate, log_file_content`，但本批已超 60，留待后批。
- **`ui_helpers.rs` 20 条**：全部为 `render_section_label` / `Text::new_inline` / `create_section_header` 等 UI 渲染函数的直接字符串实参。100% Profile 编辑器 UI。长描述（L264/L275/L283/L322）的「——」破折号沿用中文全角破折号统一风格。
- **`ui_helpers.rs` 长描述中的 `token` 处理**：`how many tokens of your conversation, code, and documents` 中 `tokens` 是 LLM 上下文窗口单位，与既有 `Context window (tokens) → 上下文窗口（tokens）` 一致——`token` 保留小写英文（专业词汇，中文 LLM 用户也广泛使用「token」）。
- **`secrets.rs` 15 条机密类型名**：`DEFAULT_REGEXES_WITH_NAMES` 数组的 `.name` 字段，通过 `RegexDisplayInfo::name(&self)` 在 `settings_view/privacy_page.rs` 中渲染为机密脱敏正则名称（用户在 Privacy 设置页面可见）。处理原则：协议/技术缩写（`IPv4` / `IPv6` / `MAC` / `AWS` / `OAuth` / `JWT` / `SK`）保留英文；品牌名（`GitHub` / `Slack` / `Stripe` / `Firebase` / `Fireworks`）保留英文；通用名词译中文（`Address → 地址`、`Token → 令牌`、`Key → 密钥`、`API Key → API 密钥`、`Domain → 域名`、`Access ID → 访问 ID`）。
- **`secrets.rs` 未触及条目**：`Google API Key` / `JWT` / `OpenAI API Key` / `Anthropic API Key` / `Warp API Key`（均在同一数组）—— 这些条目 ID 未出现在当前 `status=new` 池中（可能已是 `translated` 或 `fuzzy` 状态，或被去重）。下批可统一审视。
- **`do_not_translate, extractor_false_positive_doc_comment` 38 条**：完全沿用 batch-7/-8/-9/-10 既定处置（首见于 batch 早期）。`extractor` 在扫描 `lazy_static!`/`macro_rules!` 等宏体内的 token 流时，会把 `///` 文档注释也作为字面量提取并产生 entry；这类 entry **绝不**会渲染给用户（编译后即丢弃）。统一处置：`target=null, status=translated, flags=[batch_flag, do_not_translate, extractor_false_positive_doc_comment]`。
- **本批 panic 翻译 0 条**：与 batch-11 不同（其中含 2 条 `.expect` panic）。本批专注 UI 与 doc-comment 分流，panic 翻译集中下批处理。

## Glossary delta

无新增术语。`term_count` 保持 95。

新增 *用法*（沿用既有词条不新增 term）：
- `Linux` → `Linux`（首字母大写规范化，与既有 `Honor linux selection clipboard` 中 lowercase 形式相比，UI 标签场景一致大写）
- `Full Terminal Agent` → `Full Terminal Agent`（产品分类名，保留英文）
- `Rich Input` → `富文本输入`（与既有 `Auto dismiss Rich Input ...` 一致）
- `Warp plugin` → `Warp 插件`
- `Plan auto-sync` → `计划自动同步`
- `IPv4 Address` → `IPv4 地址`、`IPv6 Address` → `IPv6 地址`、`MAC Address` → `MAC 地址`
- `Personal Access Token` → `个人访问令牌`
- `Server-to-Server Token` → `服务器对服务器令牌`、`User-to-Server Token` → `用户对服务器令牌`
- `Classic` (token) → `经典`、`Fine-Grained` → `细粒度`、`Generic` → `通用`
- `Auth Domain` → `认证域名`、`Access ID` → `访问 ID`
- `chip` → `chip`（保留英文，与 batch-11 用法一致）
- `token` → `token`（小写英文，与 `Context window (tokens) → 上下文窗口（tokens）` 一致）

新增 *do_not_translate* 用法：
- `extractor_false_positive_doc_comment` flag 在 `app/src/util/bindings.rs`、`app/src/experiments/mod.rs`、`app/src/terminal/model/secrets.rs` 三文件首次大规模使用（38 条），全部为 `lazy_static!` / `mod regexes { ... }` 内的 `///` doc comment 误抓取。
