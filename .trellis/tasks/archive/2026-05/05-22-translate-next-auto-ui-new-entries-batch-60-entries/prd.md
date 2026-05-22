# Translate next auto_ui new entries — batch 60 entries (remote_server + resource_center + notebooks/editor)

## Goal

清扫 auto_ui-new 余量中的 **Top-3 热点文件**，共 **60 条**横跨 **3 个文件**。Strategy 1：把最大单文件直接清空，对中等文件做 deterministic head-cut。

- `app/src/remote_server/server_model.rs` — 23 条（全部清空）
- `app/src/resource_center/sections.rs` — 22 条（全部清空）
- `app/src/notebooks/editor/view.rs` — 15 条（按 id 排序取前 15）

继 cli_agent_sessions plugin_manager 31 条之后，使 auto_ui-new 余量从 621 → 561（-60）；`translated` 1620 → 1680，`new` 5062 → 5002。

## What I already know

- 当前 `strings.json` 统计：`translated=1620`, `fuzzy=52`, `new=5062`（auto_ui 621 / uncertain 4441）。`entry_count=6734`。
- glossary 现有 93 条；本批新增 0 条（无新概念，全部沿用既有术语 plugin/extension/notebook/block/workflow/theme/palette/repository/buffer/diff）。
- 三个文件的语义分层：
  - `server_model.rs`：远程协议错误消息（FileOperationError / DiffOperationError 等），返回给客户端 UI 展示。占位符密集（`{file_id:?}` / `{err}` / `{e}` / `{}` / `{:?}` / `{dir_path}` / `{repo_path}` / `{session_id:?}` 等）。
  - `resource_center/sections.rs`：欢迎面板「Resource Center」的功能引导卡片（标题 + 副标题 + 按钮）。纯英文短句，无占位符。
  - `notebooks/editor/view.rs`：富文本笔记本编辑器的快捷键描述（`EditableBinding::new` 的第二参数）。短句 / 命令式风格，无占位符。

## Scope by file

### app/src/remote_server/server_model.rs (23)

错误回包消息，全部 `FileOperationError.message` / `DiscardFilesError.message` / 类似形态。客户端会直接显示给用户。占位符必须 **数量 + 拼写完全一致**。

| ID | Line | Source | Translation rule |
|---|---|---|---|
| `01KQXQV129DAJB5Q49MYY4X8GB` | 757 | `ClientMessage had no message variant set` | 「ClientMessage 未设置 message 字段」— `ClientMessage` / `message` 字面保留（protobuf 字段名） |
| `01KQXQV12BF9FECWH1XTQQ5BPG` | 1880 | `Failed to initiate write: {err}` | 「无法发起写入：{err}」 |
| `01KQXQV12BHFZYBXX5W0GJP0DP` | 1923 | `Failed to initiate delete: {err}` | 「无法发起删除：{err}」 |
| `01KQXQV12BQP6G2BBEFSRA56HC` | 1823 | `Failed to load directory: {e}` | 「加载目录失败：{e}」 |
| `01KQXQV12BVFFD5SD28B1XJMC9` | 1613 | `Failed to execute command: {e}` | 「执行命令失败：{e}」 |
| `01KQXQV12C4T5XHVWBR2ESEB42` | 1789 | `Invalid repo_path: {e}` | 「repo_path 无效：{e}」— `repo_path` 字面保留 |
| `01KQXQV12CA5B7QDR41HHVQR6V` | 1799 | `Invalid dir_path: {e}` | 「dir_path 无效：{e}」— `dir_path` 字面保留 |
| `01KQXQV12CTA3S9V5A9ES6N7EK` | 1652 | `Invalid path: {e}` | 「路径无效：{e}」 |
| `01KQXQV12CW9E4YAFTASHY256M` | 2757 | `File not found or could not be read` | 「文件不存在或无法读取」 |
| `01KQXQV12DECSP36TKA66KT9AH` | 1551 | `No executor for session {session_id:?}` | 「会话 {session_id:?} 没有可用的执行器」 |
| `01KQXQV12J2KY0M1BQK79RDN0F` | 1809 | `dir_path {dir_path} is not a descendant of repo_path {repo_path}` | 「dir_path {dir_path} 不是 repo_path {repo_path} 的子目录」— 两个占位符 + 两处字段名字面保留 |
| `01KRNVK98997K44JR1Z3H83ED4` | 397 | `Buffer loaded but content or sync clock unavailable for file {file_id:?}` | 「缓冲区已加载，但文件 {file_id:?} 的内容或同步时钟不可用」 |
| `01KRNVK98KDYFZBYEYHTVJ39W2` | 2073 | `Buffer loaded but has no file content` | 「缓冲区已加载，但没有文件内容」 |
| `01KRNVK98W263ZRDHJQQ3C8GMF` | 2088 | `Buffer loaded but has no sync clock` | 「缓冲区已加载，但没有同步时钟」 |
| `01KRNVK997ZCG12YNVVJAVAV8V` | 2161 | `Buffer not open: {}` | 「缓冲区未打开：{}」— 位置占位符 `{}` 保留 |
| `01KRNVK9PV3EFC2BY8AWTVB8ZS` | 531 | `Failed to load buffer: {error}` | 「加载缓冲区失败：{error}」 |
| `01KRNVK9RVGJCMWXCKA9AX1QF8` | 2241 | `Failed to resolve conflict: {err}` | 「解决冲突失败：{err}」 |
| `01KRNVK9SNGTX3DXHED6NZX9J7` | 2186 | `Failed to save: {err}` | 「保存失败：{err}」 |
| `01KRNVK9Z55GBBCT0MKGE5TP0F` | 2553 | `Missing mode in DiscardFiles` | 「DiscardFiles 缺少 mode 字段」— `DiscardFiles` / `mode` 字面保留（protobuf 命名） |
| `01KRNVK9ZA1Z3EG7ACKFPWB66E` | 2275 | `Missing mode in GetDiffState` | 「GetDiffState 缺少 mode 字段」— 同上 |
| `01KRNVKA05R5MKM5BVFK1Q0CB2` | 2570 | `No active diff state model for repo={} mode={:?}` | 「未找到活动的 diff 状态模型：repo={} mode={:?}」— `{}` 与 `{:?}` 两个位置占位符保留；`repo=` / `mode=` 等号语法保留 |
| `01KRNVKA1HF3TBAJQAS2DC7Q28` | 2582 | `No files specified in DiscardFilesRequest` | 「DiscardFilesRequest 未指定任何文件」 |
| `01KRNVKA2S0991RPRNGWKV57PX` | 2604 | `No valid files after path validation` | 「路径验证后没有有效的文件」 |

### app/src/resource_center/sections.rs (22)

欢迎面板的 Getting Started + Maximize Warp + Advanced Setup 三个 section 的功能卡片文案。所有都是用户首屏看到的引导文字。

Getting Started 区（标题 + 副标题成对出现）：
| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12AYDMTHHJYCXQS4NVW` | 20 | `Create your first block` | 「创建您的第一个命令块」 |
| `01KQXQV12FEKZW144XGZTSZRSW` | 21 | `Run a command to see your command and output grouped.` | 「运行一条命令，您将看到该命令与其输出被组合到一起。」 |
| `01KQXQV12DYNZC1700Z5HXRY4J` | 26 | `Navigate blocks` | 「浏览命令块」 |
| `01KQXQV129C9DHQBSS8G6W9WFE` | 27 | `Click to select a block and navigate with arrow keys.` | 「点击以选中命令块，并使用方向键在其间移动。」 |
| `01KQXQV12GQRBNSDGSF40G94DV` | 32 | `Take an action on block` | 「对命令块执行操作」 |
| `01KQXQV12FQ1TGWJ35D74PW83N` | 33 | `Right click on a block to copy/paste, share, more.` | 「右键点击命令块即可复制 / 粘贴、分享等更多操作。」 |
| `01KQXQV12E7BC8QYENFND3438D` | 38 | `Open command palette` | 「打开命令面板」 |
| `01KQXQV128AQBVB4Z0H24227M7` | 39 | `Access all of Warp via the keyboard.` | 「通过键盘访问 Warp 的所有功能。」 |
| `01KQXQV12F09EWC1HQ8SG8T46Z` | 44 | `Set your theme` | 「设置您的主题」 |
| `01KQXQV12D9YR6VNBPNZ1ENMEQ` | 45 | `Make Warp your own by choosing a theme.` | 「通过选择主题，让 Warp 成为您专属的工具。」 |

Maximize Warp 区：
| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12C5527GXQXM6RWZ370` | 92 | `Find and run previously executed commands, workflows, and more.` | 「查找并运行此前执行过的命令、工作流等。」 |
| `01KQXQV12GBD6TCYS0YR2JFNEZ` | 106 | `Split panes` | 「拆分面板」 |
| `01KQXQV12D7WYHZCAWQ367TMYG` | 115 | `Launch configuration` | 「启动配置」 |
| `01KQXQV12FBJ2SEVRYK7FC54CA` | 116 | `Save your current configuration of windows, tabs, and panes.` | 「保存您当前的窗口、标签页与面板配置。」 |

Advanced Setup 区（ContentItem 卡片：title + description + button_label）：
| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H1S0VX0CY165JVDT2` | 63 | `Use your custom prompt` | 「使用您的自定义 shell 提示符」 |
| `01KQXQV12FC0G2W2V0A4JSCKAA` | 64 | `Set up Warp to honor your PS1 setting` | 「配置 Warp 以遵循您的 PS1 设置」— `PS1` 字面保留（环境变量名） |
| `01KQXQV12HBZR54842AX1BC34B` | 66 | `View documentation` | 「查看文档」 |
| `01KQXQV12C69RNQ1RF2T3C009E` | 69 | `Integrate Warp with your IDE` | 「将 Warp 与您的 IDE 集成」— `IDE` 字面保留 |
| `01KQXQV12AD39WNKYHDNA75HES` | 70 | `Configure Warp to launch from your most used development tools` | 「配置 Warp 让您能从最常用的开发工具中启动它」 |
| `01KQXQV12CFTDDZ6H67VE9H5W4` | 75 | `How Warp uses Warp` | 「Warp 团队如何使用 Warp」 |
| `01KQXQV12D4DR0N4J8RHAHPWPC` | 76 | `Learn how Warp's engineering team uses their favorite features` | 「了解 Warp 工程团队如何使用他们最爱的功能」 |
| `01KQXQV12E6QS51BKQ7CHX23MK` | 78 | `Read article` | 「阅读文章」 |

### app/src/notebooks/editor/view.rs (15)

富文本笔记本编辑器的 `EditableBinding::new(id, label, action)` 中的 `label`（用户在 keybinding 设置中看到的命令名）。按 id 字典序取前 15。

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12A0WG966STTN65H689` | 397 | `Copy rich-text selection` | 「复制富文本选区」 |
| `01KQXQV12A5XA7FJ64WPF08B1C` | 678 | `Create or edit link` | 「创建或编辑链接」 |
| `01KQXQV12A60QRZBM4PJ6R944N` | 318 | `De-select shell commands` | 「取消选中 shell 命令」 |
| `01KQXQV12AEZCGXD6QRZFFD7TH` | 390 | `Copy rich-text buffer` | 「复制富文本缓冲区」 |
| `01KQXQV12C789ZKVKADRXWRXX4` | 714 | `Find in Notebook` | 「在笔记本中查找」 |
| `01KQXQV12DCAAJRSGTF6T5H1SM` | 471 | `Move to start of paragraph` | 「移动到段落开头」 |
| `01KQXQV12DG2RN2PFB2YSQ6863` | 404 | `Log editor state` | 「记录编辑器状态」 |
| `01KQXQV12DT9W8CE5Q0HZMWB2R` | 487 | `Move to end of paragraph` | 「移动到段落末尾」 |
| `01KQXQV12F35W520BV3FM2GC4X` | 336 | `Select previous command` | 「选择上一条命令」 |
| `01KQXQV12F3MRGTVVZBNN0D1E0` | 325 | `Select shell command at cursor` | 「选中光标处的 shell 命令」 |
| `01KQXQV12F4ESNNSR3Q11FFY56` | 560 | `Select to end of paragraph` | 「选择到段落末尾」 |
| `01KQXQV12FESMXGE27Z0PP9MW8` | 350 | `Run selected commands` | 「运行选中的命令」 |
| `01KQXQV12FMNKGH61P4C7PNP4F` | 553 | `Select to start of paragraph` | 「选择到段落开头」 |
| `01KQXQV12FQD38ZXZBGXWKRJBJ` | 343 | `Select next command` | 「选择下一条命令」 |
| `01KQXQV12G5EEWMBRBRAWJSGKR` | 740 | `Toggle case-sensitive search` | 「切换大小写敏感搜索」 |

## Special literal / placeholder protections

| 锚点 | 规则 |
|---|---|
| `{err}` / `{e}` / `{error}` (server_model L531/L1613/L1652/...) | 命名占位符必须原样保留（拼写 + 大括号） |
| `{file_id:?}` / `{session_id:?}` (server_model L397/L1551) | 命名 + `:?` debug 格式说明符必须保留 |
| `{dir_path}` / `{repo_path}` (server_model L1809) | 命名占位符保留；译文中字段名 `dir_path` / `repo_path` 亦字面保留（这两个 token 同时是字段名 + 占位符内容） |
| `{}` / `{:?}` (server_model L2161/L2570) | 位置占位符保留；`repo=` / `mode=` 等号语法保留 |
| `ClientMessage` / `message` / `DiscardFiles` / `DiscardFilesRequest` / `GetDiffState` / `mode` (server_model 多处) | protobuf 协议字段 / 消息类型名，全部字面保留 |
| `repo_path` / `dir_path` (server_model 多处) | 协议字段名字面保留 |
| `Warp` / `IDE` / `PS1` (resource_center) | 品牌名 / 通用缩写 / 环境变量名字面保留 |
| `shell` (notebooks/editor L325/L318) | shell 一词字面保留（小写）—— 是 Warp 多处使用的固定写法（"shell command" → "shell 命令"） |

## Glossary additions / verifications

本批 **不新增** glossary 条目。涉及的关键术语全部已存在并按既有 target 翻译：

- `block` → 命令块（resource_center 多处）
- `command_palette` → 命令面板（resource_center L38）
- `command` → 命令（多处）
- `theme` → 主题（resource_center L44/45）
- `workflow` → 工作流（resource_center L92）
- `pane` → 面板（resource_center L106/116）
- `tab` → 标签页（resource_center L116）
- `notebook` → 笔记本（notebooks/editor L714）
- `shell_prompt` → shell 提示符（resource_center L63）
- `keybinding` → 按键绑定（notebooks/editor 整体场景）

protobuf 字段名 / Rust 标识符（`repo_path`, `dir_path`, `mode`, `ClientMessage`, `DiscardFiles*`, `GetDiffState`, `PS1`, `IDE`）按既有 do_not_translate 惯例保留，不需进入 glossary。

## Acceptance criteria

1. `translations/strings.json` 中所选 60 条 entry 的 `status` 从 `new` → `translated`，`target` 填入中文译文；`audit.verdict=auto_ui` 不变；`flags` 追加 `pr-remote-server-resource-center-notebooks-editor-batch`。
2. 全部命名占位符 `{err}`/`{e}`/`{error}`/`{file_id:?}`/`{session_id:?}`/`{dir_path}`/`{repo_path}` 保留；位置占位符 `{}` / `{:?}` 数量与顺序完全一致。
3. 所有 protobuf 协议字段 / 类型名（`ClientMessage`/`message`/`DiscardFiles`/`DiscardFilesRequest`/`GetDiffState`/`mode`/`repo_path`/`dir_path`）字面保留；`Warp`/`IDE`/`PS1` 字面保留；`shell` 小写保留。
4. CJK 邻接半角标点检查通过；无 ASCII `...`（如需省略号用 U+2026 `……`）；无 lowercase standalone `agent`。
5. `metadata.stats` 重算：translated 1620→1680，new 5062→5002，auto_ui-new 余量 621→561。
6. 既有 1620 条 translated 条目 byte-identical 不被触碰。
7. `glossary.json` term_count 保持 93（本批无增量）。
8. 4 阶段验证全部通过：apply_translations.py → extract --check（幂等）→ builder build → cargo check -p warp。
9. Commit message 形如 `chore(translations): translate 60 remote_server + resource_center + notebooks/editor auto_ui entries`（仅暂存，不 commit）。
