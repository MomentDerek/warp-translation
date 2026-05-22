# Translate next auto_ui new entries — batch 60 entries (settings + onboarding sweep)

## Goal

清扫 **6 个 auto_ui-new 热点文件**（warpify_page / show_blocks_view / platform_page / create_api_key_modal / welcome_banner / wasm_nux_dialog）+ notebooks/editor/view.rs 5 条收尾 + ai_assistant/mod.rs 1 条品牌名收尾，共 **60 条**。主题统一为「设置面板 + Warpify/SSH + API key 管理 + HoA 引导横幅 + WASM NUX 对话框」。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/settings_view/warpify_page.rs` | 11 | Warpify/SSH 配置 + 黑白名单标签（全部清空） |
| `app/src/settings_view/show_blocks_view.rs` | 9 | 共享命令块管理（chrono 格式串 + 取消分享对话框） |
| `app/src/settings_view/platform_page.rs` | 9 | API key 列表页（创建/列/状态） |
| `app/src/settings_view/platform/create_api_key_modal.rs` | 9 | 创建 API key 模态对话框 |
| `app/src/workspace/hoa_onboarding/welcome_banner.rs` | 8 | HoA 引导横幅（垂直标签、Agent 收件箱、原生代码评审） |
| `app/src/wasm_nux_dialog.rs` | 8 | Web→桌面端 NUX 对话框 |
| `app/src/notebooks/editor/view.rs` | 5 | 笔记本编辑器 Toggle 系列收尾（残留 auto_ui） |
| `app/src/ai_assistant/mod.rs` | 1 | `Warp AI` 品牌名（凑齐 60） |

继 batch-1 (notebooks/editor + remote_server + resource_center) 与 batch-2 (settings_view sweep) 之后，auto_ui-new 余量 501 → 441（-60）；`translated` 1740 → 1800，`new` 4942 → 4882。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=1740`, `fuzzy=52`, `new=4942`（auto_ui 501 / uncertain 4441）。
- glossary 现有 93 条；本批无新增术语：沿用 `MCP` / `SSH` / `Warp` / `Warp Drive` / `Agent` / `API` / `Git` / `Oz Cloud` / `shell` / `block→命令块` / `allowlist→白名单` / `denylist→黑名单` / `Warpify`（产品动词，字面保留）/ `Warpification`（字面保留）/ `worktree`（字面保留）/ `tmux`（字面保留）/ `bash`/`zsh`/`fish`（字面保留）。
- 7 个文件 + 1 凑数的语义分层：
  - `warpify_page.rs`：SSH/tmux warpify 子页面 — 描述 + 标题 + 主机/命令黑白名单。
  - `show_blocks_view.rs`：设置中「共享的命令块」列表 — chrono 格式串 + 取消分享确认对话框 + 列表加载/空状态。
  - `platform_page.rs`：API key 平台总览页 — 创建按钮 + 列标题 + 空状态。
  - `create_api_key_modal.rs`：创建 API key 模态对话框 — 标题 + 状态文本 + 错误提示 + 复制密钥提示。
  - `welcome_banner.rs`：HoA（Home of Agents）入门引导横幅 — 三大特性介绍（垂直标签 / 标签页配置 / Agent 收件箱 / 原生代码评审）。
  - `wasm_nux_dialog.rs`：WASM 版本「在 Web 还是桌面端打开」NUX 对话框。
  - `notebooks/editor/view.rs`：笔记本富文本编辑器的 toggle 工具栏标签。
  - `ai_assistant/mod.rs`：`Warp AI` 品牌名一条凑齐 60。
- 占位符：`{}` （show_blocks: `Executed on: {}`）、`{object_kind}`（wasm_nux_dialog）。

## Scope by file

### app/src/settings_view/warpify_page.rs (11)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12A0QVMZPECAQ5KQ4FR` | 813 | `Denylisted hosts` | `黑名单主机` |
| `01KQXQV12A63Z0AP7X3R8F8C9A` | 86 | `Controls the installation behavior for Warp's SSH extension when a remote host doesn't have it installed.` | `控制远程主机未安装 Warp SSH 扩展时的安装行为。` |
| `01KQXQV12AKPEZ2XAK7MY3X8Y2` | 617 | `Denylisted commands` | `黑名单命令` |
| `01KQXQV12APT990HJ9QC8TSAJ2` | 540 | `Configure whether Warp attempts to "Warpify" … certain shells. ` (有尾随空格) | `配置 Warp 是否尝试对某些 shell 进行 "Warpify"（添加对命令块、输入模式等的支持）。 ` （保留尾随空格） |
| `01KQXQV12C2BKYKX1Z2KHTF51B` | 725 | `Install SSH extension` | `安装 SSH 扩展` |
| `01KQXQV12FKG10XFG7TN8AZCEA` | 65 | `SSH session detection for Warpification` | `SSH 会话的 Warpification 检测` |
| `01KQXQV12GHQXP2CB4RB5XDN8Y` | 83 | `The tmux ssh wrapper works in many situations where the default one does not, but may require you to hit a button to warpify. Takes effect in new tabs.` | `tmux ssh 包装器在许多默认包装器无法工作的场景下仍可正常运行，但可能需要您点击按钮才能完成 warpify。新标签页生效。` |
| `01KQXQV12GPXCC8BFSN5DNSYP0` | 182 | `Subshells supported: bash, zsh, and fish.` | `支持的子 shell：bash、zsh 和 fish。` |
| `01KQXQV12H6RHXQGZDMWBHXNS7` | 193 | `Warpify your interactive SSH sessions.` | `为交互式 SSH 会话启用 Warpify。` |
| `01KQXQV12H7ZGBDP07J8QHQNT6` | 760 | `Use Tmux Warpification` | `使用 Tmux Warpification` |
| `01KQXQV12HPG683H3RK81F2KX9` | 690 | `Warpify SSH Sessions` | `Warpify SSH 会话` |

### app/src/settings_view/show_blocks_view.rs (9)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1286B8Q8WPKVHHMYT6Y` | 251 | `%a, %b %-d %Y at %-I:%M %p`（chrono 格式串） | `%Y 年 %-m 月 %-d 日 %-I:%M %p`（弃用 `%a`/`%b` 英文区域 token，改为数值中文日期；保留 12h 制 `%-I:%M %p`） |
| `01KQXQV129WZVNVZKD9KE2CJ5F` | 42 | `Are you sure you want to unshare this block?\n\nIt will no longer be accessible by link and will be permanently deleted from Warp servers.` | `确定要取消分享此命令块吗？\n\n它将无法再通过链接访问，并将从 Warp 服务器永久删除。` |
| `01KQXQV129ZR47KG5XC6Z3CWYD` | 556 | `Block was successfully unshared.` | `命令块已成功取消分享。` |
| `01KQXQV12AXS3W4P5NJDXJRKKS` | 171 | `Deleting...` | `正在删除……`（ASCII `...` → U+2026 双字符） |
| `01KQXQV12BSK3WHYKZTCH1Y04P` | 248 | `Executed on: {}` | `执行于：{}`（占位符保留） |
| `01KQXQV12CQXYBJ0Z8DZ2NF4N9` | 313 | `Getting blocks...` | `正在获取命令块……` |
| `01KQXQV12HA4JDYS5TZQC7S564` | 716 | `Unshare` | `取消分享` |
| `01KQXQV12HF6EY8HPTWBH2BABV` | 663 | `Unshare block` | `取消分享命令块` |
| `01KQXQV12J87DHB67B5PA6GNNG` | 309 | `You don't have any shared blocks yet.` | `您还没有任何已分享的命令块。` |

### app/src/settings_view/platform_page.rs (9)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV128B5TXF8V5RR2QJ5CT` | 502 | `+ Create API Key` | `+ 创建 API 密钥` |
| `01KQXQV128PGXE7SYFTK2NTTQ6` | 306 | `API key deleted` | `API 密钥已删除` |
| `01KQXQV12A931HZTN58F1HF6QD` | 814 | `Create a key to manage external access to Warp` | `创建密钥以管理对 Warp 的外部访问` |
| `01KQXQV12AFMXXE6YRZ9A36X5H` | 454 | `Create and manage API keys to allow other Oz cloud agents to access your Warp account.\nFor more information, visit the ` （有尾随空格） | `创建和管理 API 密钥，允许其他 Oz Cloud Agent 访问您的 Warp 账户。\n如需了解更多信息，请访问 ` （保留尾随空格；`Oz cloud` 大写化为 `Oz Cloud` 与既定品牌写法一致） |
| `01KQXQV12BSZSP23M2F6NDM421` | 568 | `Expires at` | `过期时间` |
| `01KQXQV12DBEXNTRFATG0RS7B5` | 178 | `New API key` | `新建 API 密钥` |
| `01KQXQV12DRZJXRKSJ9N11Q436` | 565 | `Last used` | `上次使用` |
| `01KQXQV12DV31TTWCAZA4K7PTV` | 800 | `No API Keys` | `暂无 API 密钥` |
| `01KQXQV12F1GYA968XRC8SSJ9B` | 255 | `Save your key` | `保存您的密钥` |

### app/src/settings_view/platform/create_api_key_modal.rs (9)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12A7WJDDVFQNCHRPE9B` | 648 | `Create key` | `创建密钥` |
| `01KQXQV12AA5HFSP8A2E90ZSGD` | 646 | `Creating…`（源已 U+2026） | `正在创建…`（保留 U+2026） |
| `01KQXQV12BHEPA72MWPXQ4EZDX` | 548 | `Done` | `完成` |
| `01KQXQV12BQK83WR2B1AJD0SRQ` | 399 | `Failed to create API key. Please try again.` | `创建 API 密钥失败。请重试。` |
| `01KQXQV12F1SPQHXKS9BDFSJDR` | 838 | `Secret key copied.` | `密钥已复制。` |
| `01KQXQV12GGBV8HR8JK1TEB6K8` | 475 | `This secret key is shown only once. Copy and store it securely.` | `此密钥仅显示一次，请复制并妥善保存。` |
| `01KQXQV12GQ6TKPBD7Y8394RZR` | 47 | `This API key is tied to your user and can make requests against your Warp account.` | `此 API 密钥与您的用户绑定，可用于向您的 Warp 账户发起请求。` |
| `01KQXQV12HBD36ZG3TH3S4ET0Z` | 368 | `Unable to create a team API key because there is no current team.` | `无法创建团队 API 密钥，因为当前没有团队。` |
| `01KQXQV12HCFDFAD1QAWBH4FAH` | 161 | `Warp API Key` | `Warp API 密钥` |

### app/src/workspace/hoa_onboarding/welcome_banner.rs (8)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129316WW0W2VTSS8E39` | 41 | `Agent inbox` | `Agent 收件箱` |
| `01KQXQV12D2H8V771GZP5RVX1Y` | 42 | `Notifications when any agent needs your attention, also accessible in a central inbox` | `任何 Agent 需要您关注时发出的通知，也可在统一收件箱中查看` |
| `01KQXQV12DFES18YEDDS5XWPCA` | 46 | `Native code review` | `原生代码评审` |
| `01KQXQV12FCBVERKF8DT3A7RJ0` | 47 | `Send inline comments from Warp's code review directly to Claude Code, Codex, or OpenCode` | `将 Warp 代码评审中的行内评论直接发送至 Claude Code、Codex 或 OpenCode` |
| `01KQXQV12FMDZ005X1VVFCWT5Q` | 32 | `Rich tab titles and metadata like git branch, worktree, and PR. Fully customizable.` | `丰富的标签页标题与元数据，例如 Git 分支、worktree 和 PR。完全可自定义。` |
| `01KQXQV12GNPS9HA9T01RTJP76` | 36 | `Tab configs` | `标签页配置` |
| `01KQXQV12GQQV67RVC3ACEAQWT` | 37 | `Tab-level schema to set your directory, startup commands, theme, and worktree with one click` | `标签页级别的模板，一键设定您的目录、启动命令、主题和 worktree` |
| `01KQXQV12H8XXMJ1F989V4CKW5` | 31 | `Vertical tabs` | `垂直标签页` |

### app/src/wasm_nux_dialog.rs (8)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129S50CY44D1SF9J90C` | 227 | `Always open {object_kind} on the web?` | `始终在网页上打开 {object_kind}？` |
| `01KQXQV12BSSMZ1EW4SM59JDKD` | 168 | `Download Warp Desktop?` | `下载 Warp 桌面端？` |
| `01KQXQV12CTXF3JNFJA2CBAMFQ` | 158 | `Future links will automatically open on desktop.` | `未来打开链接时将自动在桌面端打开。` |
| `01KQXQV12ENPCYVT3Y24N6EYWX` | 157 | `Open in Warp Desktop?` | `在 Warp 桌面端打开？` |
| `01KQXQV12HAE5T5F4JCCSWXNX5` | 176 | `Warp is the intelligent terminal with AI and your dev team's knowledge built-in.` | `Warp 是一款智能终端，内置 AI 与您的开发团队知识。` |
| `01KQXQV12HFJB5FT6QJ682MR2A` | 223 | `Warp links` | `Warp 链接` |
| `01KQXQV12HMZ6GYMTEZ3Y15VSM` | 221 | `Warp Drive objects` | `Warp Drive 对象` |
| `01KQXQV12JH0ZE1CWNDRGYS0H9` | 228 | `You can change this at any time in settings.` | `您可以随时在设置中更改此项。` |

### app/src/notebooks/editor/view.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H1V42P6CGWAFDK4EA` | 696 | `Toggle strikethrough styling` | `切换删除线样式` |
| `01KQXQV12HNPJGADJ4023478BH` | 685 | `Toggle inline code styling` | `切换行内代码样式` |
| `01KQXQV12HV3QY5TDYC45QR7RT` | 734 | `Toggle regular expression search` | `切换正则表达式搜索` |
| `01KQXQV12HVG1TESJQBG7E6AHP` | 383 | `Toggle rich-text debug mode` | `切换富文本调试模式` |
| `01KQXQV12HXY3S33XH8N05X2X6` | 703 | `Toggle underline styling` | `切换下划线样式` |

### app/src/ai_assistant/mod.rs (1, brand pad)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H80E93FRQ5RK6JVYY` | 37 | `Warp AI` | `Warp AI`（品牌名字面保留） |

## Decisions / Anomalies

- **chrono 格式串 (`%a, %b %-d %Y at %-I:%M %p` → `%Y 年 %-m 月 %-d 日 %-I:%M %p`)**：源串包含 `%b`（英文月名缩写 `Jan`/`Feb`）与 `%a`（英文星期缩写 `Mon`），这些在中文场景下无意义；改为数值年/月/日格式更自然。`%-I:%M %p` 保留 12h 制（`%p` 输出 `AM`/`PM`），与英文版本时态信息一致。chrono 对未转义的非 `%` 字符按字面输出，因此中文「年」「月」「日」会原样保留。
- **尾随空格保留 (warpify_page L540, platform_page L454)**：源串以空格结尾因为后接 `Learn more` 链接片段；译文必须保留尾随空格，否则中文+英文链接之间会粘连。`check_invariants` 强制单向（源有 → 译有；源无 → 译无）。
- **`Warpify` / `Warpification` / `warpify`**：均为 Warp 自创产品动词/名词，字面保留三种大小写形式。Glossary 已收录。
- **`Oz Cloud` 大写规范化**：源串在 L454 写作 `Oz cloud agents`（小写 `cloud`），但本仓库既有翻译统一使用 `Oz Cloud` 大写形式（与 `WarpIcon::OzCloud` 一致），译文统一为 `Oz Cloud Agent`。
- **U+2026 一致性**：`Creating…` 源已使用 U+2026 单字符，译文 `正在创建…` 保留同一字符。其他 ASCII `...` 严格转为 `……`（U+2026 双字符）。
- **`{object_kind}` 占位符**：运行时插入 `Warp Drive objects` / `shared sessions` / `Warp links` 之一。`shared sessions`（id `01KQXQV12JAAX9GKJS0SFE2S5P`）仍为 `uncertain`，本批未译；混合显示在所难免，待后续 uncertain 批处理。
- **`block→命令块`** 一致性：`Block was successfully unshared.` / `Getting blocks...` / `Unshare block` / `shared blocks` 全部使用「命令块」译法。
- **`Warp AI` 凑数项**：从「文件剩余 1 条」候选池中选择最简单的品牌名收尾，清零 `app/src/ai_assistant/mod.rs` 的 auto_ui-new 计数。

## Glossary delta

无新增。沿用既有 93 条术语。`term_count` 保持 93。
