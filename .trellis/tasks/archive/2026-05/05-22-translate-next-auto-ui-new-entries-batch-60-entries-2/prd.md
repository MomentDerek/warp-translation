# Translate next auto_ui new entries — batch 60 entries (settings_view sweep)

## Goal

清扫 `app/src/settings_view/` 下 **4 个热点配置 UI 文件**（execution_profile_view / main_page / mod / agent_assisted_environment_modal）+ warpify_page 1 条收尾，共 **60 条**，主题统一为「设置面板 UI 文案」。

- `app/src/settings_view/execution_profile_view.rs` — 18 条（全部清空 auto_ui-new）
- `app/src/settings_view/main_page.rs` — 14 条（全部清空 auto_ui-new）
- `app/src/settings_view/mod.rs` — 14 条（全部清空 auto_ui-new）
- `app/src/settings_view/agent_assisted_environment_modal.rs` — 13 条（全部清空 auto_ui-new）
- `app/src/settings_view/warpify_page.rs` — 1 条（`Added commands` 收尾凑齐 60）

继 notebooks/editor + remote_server + resource_center 60 条之后，使 auto_ui-new 余量从 561 → 501（-60）；`translated` 1680 → 1740，`new` 5002 → 4942。

## What I already know

- 当前 `strings.json` 统计：`translated=1680`, `fuzzy=52`, `new=5002`（auto_ui 561 / uncertain 4441）。`entry_count=6734`。
- glossary 现有 93 条；本批无新增术语（沿用既有 MCP / Warp Drive / Agent / SSH / allowlist→白名单 / denylist→黑名单 / shell / block→命令块 / settings sync→设置同步 / Warpify / Oz Cloud）。
- 5 个文件的语义分层：
  - `execution_profile_view.rs`：Agent 执行 Profile 编辑器的权限标签（`xxx:` 形式）和 `Permission` 枚举的 `Never ask` / `Ask unless auto-approve` 状态字串。
  - `main_page.rs`：设置主页的更新检测 + Referral + 设置同步 UI（按钮 + 状态指示文本）。
  - `mod.rs`：`SettingsSection` 枚举 → Display 标签 + 块显示开关 + 搜索空状态 + `Enable/Disable {description_suffix}` 模板。
  - `agent_assisted_environment_modal.rs`：Agent 辅助创建环境的「选择已索引仓库」模态对话框。
  - `warpify_page.rs`：Warpify 设置页面的「已添加命令」分区标题。
- 占位符仅出现在 mod.rs 与 modal：`{description_suffix}` / `{path}`。

## Scope by file

### app/src/settings_view/execution_profile_view.rs (18)

Execution Profile 编辑器的权限标签——所有以 `:` 结尾的标签都对应一个右侧权限选择控件。`Ask` 系列状态串与 `Permission` 枚举对齐。

| ID | Line | Source | Translation rule |
|---|---|---|---|
| `01KQXQV1294SJYA4BHZEK96BJE` | 301 | `Ask questions:` | 「提问：」 |
| `01KQXQV1299SQKF7F5JK05STFE` | 163 | `Base model:` | 「基础模型：」 |
| `01KQXQV12923JXHA3EHXY1FPAA` | 355 | `Call web tools:` | 「调用网页工具：」 |
| `01KQXQV129E1CXPXZ83DXWENJZ` | 311 | `Call MCP servers:` | 「调用 MCP 服务器：」— `MCP` 字面保留 |
| `01KQXQV129GND90HDFJ080ZV5Y` | L739 | `Ask unless auto-approve` | 「除非自动批准否则询问」（沿用 auto-approve→自动批准） |
| `01KQXQV129MX3NZBYP0BN10EG3` | 211 | `Apply code diffs:` | 「应用代码 diff：」— `diff` 字面（一致性，glossary 无 diff→差异） |
| `01KQXQV129QKG9E377RQ7JVPZF` | 366 | `Auto-sync plans to Warp Drive:` | 「自动同步计划至 Warp Drive：」— `Warp Drive` 字面保留 |
| `01KQXQV12A6BPC67G5VQ2TGX4A` | 764 | `Directory allowlist:` | 「目录白名单：」（与已有「目录白名单」一致） |
| `01KQXQV12ACFJB9KY0H8QPBS31` | 778 | `Command allowlist:` | 「命令白名单：」 |
| `01KQXQV12AH4B2RZDK5VAB5F2C` | 182 | `Computer use:` | 「计算机使用：」（与已有 Computer use→计算机使用 一致） |
| `01KQXQV12AYYXW0288A2ABKN1B` | 792 | `Command denylist:` | 「命令黑名单：」 |
| `01KQXQV12B1VV84DZS932QNY2C` | 240 | `Execute commands:` | 「执行命令：」 |
| `01KQXQV12CR7TV3FD4TN32X1CD` | 279 | `Interact with running commands:` | 「与运行中的命令交互：」 |
| `01KQXQV12CTVMHTJV38EQ13SQ3` | 172 | `Full terminal use:` | 「完整终端使用：」 |
| `01KQXQV12D4FX1WTJW2HSGGSWJ` | L737 | `Never ask` | 「从不询问」 |
| `01KQXQV12D6VR3M1DVNSBPRDC1` | 807 | `MCP allowlist:` | 「MCP 白名单：」 |
| `01KQXQV12DC7DAFTPT804R1KJE` | 823 | `MCP denylist:` | 「MCP 黑名单：」 |
| `01KQXQV12EVAARTTG38JKYVMZZ` | 220 | `Read files:` | 「读取文件：」 |

### app/src/settings_view/main_page.rs (14)

设置主页的 Referral CTA + 设置同步 toggle + 更新管理器 UI（状态文本 / 按钮 / 错误消息）。

| ID | Line | Source | Translation rule |
|---|---|---|---|
| `01KQXQV12BKV2WVXPZQ7HMWWYT` | 59 | `Earn rewards by sharing Warp with friends & colleagues` | 「与亲朋好友及同事分享 Warp 即可获得奖励」— `Warp` 字面 |
| `01KQXQV12JRNY42E1Q850ZF289` | 93 | `settings sync` | 「设置同步」— 小写为 `description_suffix`，组装为 `Enable settings sync` / `Disable settings sync` |
| `01KQXQV12GHVXM3NSB5GEFJ248` | 153 | `Toggle Settings Sync` | 「切换设置同步」— LoginGatedFeature 显示名 |
| `01KQXQV12EPA026PJKS4BSYBM5` | 790 | `Refer a friend` | 「推荐朋友」（沿用 Referrals→推荐） |
| `01KQXQV12F6NEKWMWV40AFA3CW` | 706 | `Settings sync` | 「设置同步」 |
| `01KQXQV12H8018GM5Z90XKZHCQ` | 840 | `Up to date` | 「已是最新版本」 |
| `01KQXQV12J1CBQFWWKX9WF7EBH` | 850 | `checking for update...` | 「正在检查更新……」— `...` → `……`（U+2026 双字符） |
| `01KQXQV12JZ7MW66KDEAJC29ZQ` | 857 | `downloading update...` | 「正在下载更新……」 |
| `01KQXQV12HM1K9BVGK0X0JPYZ2` | 864 | `Update available` | 「有可用更新」 |
| `01KQXQV12E833RN1JM1M1S4RVX` | 868 | `Relaunch Warp` | 「重新启动 Warp」— `Warp` 字面 |
| `01KQXQV12CSMMN5ZFGS6MR947R` | 881 | `Installed update` | 「已安装更新」 |
| `01KQXQV128PFQ5AFK0FESE8YFG` | 891 | `A new version of Warp is available but can't be installed` | 「Warp 有新版本可用，但无法完成安装」 |
| `01KQXQV12HV8X3WGHXS07HE802` | 895 | `Update Warp manually` | 「手动更新 Warp」 |
| `01KQXQV128PXP78HN1KFKG6GSY` | 902 | `A new version of Warp is installed but can't be launched.` | 「Warp 新版本已安装，但无法启动。」 |

### app/src/settings_view/mod.rs (14)

`SettingsSection` Display 标签 + Workspace 块显示开关 + 设置搜索空状态 + `Enable/Disable {description_suffix}` 模板。

| ID | Line | Source | Translation rule |
|---|---|---|---|
| `01KQXQV12DR7QS44JSSM5P20XX` | 272 | `Keyboard shortcuts` | 「键盘快捷键」 |
| `01KQXQV12FJN1QQ78F5PZ9MF7X` | 273 | `Shared blocks` | 「共享命令块」（沿用 block→命令块） |
| `01KQXQV12DP2QY1C1NEDH0F18D` | 278 | `MCP servers` | 「MCP 服务器」 |
| `01KQXQV12CJ738FSDJX95KQGTR` | 281 | `Indexing and projects` | 「索引与项目」 |
| `01KQXQV12E293FNJGNZ32F0CGR` | 284 | `Oz Cloud API Keys` | 「Oz Cloud API 密钥」— `Oz Cloud` 与 `API` 字面保留（Oz Cloud 是 Warp 企业产品名） |
| `01KQXQV12F5NDPA97S8WW9V9RT` | 442 | `Same_Line_Prompt_Enabled` | 「Same_Line_Prompt_Enabled」— **特征标志标识符**（`pub const SAME_LINE_PROMPT: &str = "Same_Line_Prompt_Enabled"`），不译，保留原文 |
| `01KQXQV12CJSMSASBC8SG41W76` | 554 | `Hide initialization block` | 「隐藏初始化命令块」（沿用 initialization block→初始化命令块） |
| `01KQXQV12GX4TCE2XTY78X1N6P` | 567 | `Show in-band command blocks` | 「显示带内命令块」（沿用 in-band→带内） |
| `01KQXQV12C9V5VEQP0S9QAES32` | 568 | `Hide in-band command blocks` | 「隐藏带内命令块」 |
| `01KQXQV12BR15VM7NRA5GR7DQV` | 706 | `Enable {description_suffix}` | 「启用 {description_suffix}」— 占位符保留 |
| `01KQXQV12AYE4MHP2ZZNQ323DG` | 707 | `Disable {description_suffix}` | 「禁用 {description_suffix}」 |
| `01KQXQV129XYDGWMD5FS8MK60R` | 1243 | `Cloud platform` | 「云端平台」 |
| `01KQXQV12DP37CKVX2AY8V0846` | 2280 | `No settings match your search.` | 「没有匹配您搜索条件的设置。」 |
| `01KQXQV12JQCP6BMWT8JPAX1V5` | 2288 | `You may want to try using different keywords or checking for any possible typos.` | 「您可以尝试使用其他关键词，或检查是否存在拼写错误。」 |

### app/src/settings_view/agent_assisted_environment_modal.rs (13)

Agent 辅助创建环境模态对话框——「选择本地已索引仓库」分区文案。

| ID | Line | Source | Translation rule |
|---|---|---|---|
| `01KQXQV129FY142Y3RKVV23R2D` | 104 | `Add repo` | 「添加仓库」 |
| `01KQXQV12FZ8DGXSKV3901AR9M` | 336 | `Selected repos` | 「已选仓库」 |
| `01KQXQV12D4MQ8KC17WSW1MHEA` | 341 | `No repos selected yet` | 「尚未选择任何仓库」 |
| `01KQXQV1297SK5MV3Z7CNFJ0QT` | 417 | `Available indexed repos` | 「可用的已索引仓库」 |
| `01KQXQV12DBR65M54B5Y2DHCK1` | 437 | `Loading locally indexed repos…` | 「正在加载本地已索引的仓库……」— U+2026 已存在于源，原样保留 |
| `01KQXQV12D40VG9SQ0RYSF6YDA` | 439 | `No locally indexed repos found yet. Index a repo, then try again.` | 「尚未找到本地已索引的仓库。请先索引一个仓库后再试。」 |
| `01KQXQV12DX2EG8CTZW4T0H7EP` | 442 | `Local repo selection is unavailable in this build.` | 「当前构建版本不支持本地仓库选择。」 |
| `01KQXQV129PA1ANEG2JBCT6T84` | 512 | `All locally indexed repos are already selected.` | 「所有本地已索引的仓库均已被选中。」 |
| `01KQXQV12FN53SNC6M29ZJ6F6R` | 555 | `Selected folder is not a Git repository: {path}` | 「所选文件夹不是 Git 仓库：{path}」— `{path}` 占位符保留，`Git` 字面 |
| `01KQXQV12DQZE9GVM3T9S3ZRF7` | 599 | `No directory selected` | 「未选择任何目录」 |
| `01KQXQV12F3HS6GQP4F8MFWBHM` | 617 | `Select locally indexed repos to provide context for the environment creation agent.` | 「选择本地已索引的仓库，为环境创建 Agent 提供上下文。」 |
| `01KQXQV12FBFFMWXRJZ3T43KAB` | 619 | `Select repos to provide context for the environment creation agent.` | 「选择仓库，为环境创建 Agent 提供上下文。」 |
| `01KQXQV12FXMRX59C2MTR1NAR6` | 643 | `Select repos for your environment` | 「为您的环境选择仓库」 |

### app/src/settings_view/warpify_page.rs (1)

| ID | Line | Source | Translation rule |
|---|---|---|---|
| `01KQXQV1292BJYESSV75ZAXMDP` | 605 | `Added commands` | 「已添加的命令」 |

## Decisions / Anomalies

- **`Same_Line_Prompt_Enabled` (L442 mod.rs)**: 实质上是 `pub const SAME_LINE_PROMPT: &str = "..."` 的内部 feature flag 标识符，不应进入 auto_ui。但既已分类，按「保留原文不译」处理：`target = "Same_Line_Prompt_Enabled"`。占位符不变，全 ASCII，符合 invariants。
- **`Ask unless auto-approve` / `Never ask` (L737-L739)**: 与 `Permission::AskUserQuestionPermission` 枚举的 `Never` / `AskExceptInAutoApprove` 状态对齐。延续 `auto-approve→自动批准` 用法。
- **`settings sync` (L93) 与 `Settings sync` (L706)**: 同义不同大小写。L93 是 `description_suffix`，将组合到 `Enable {suffix}` / `Disable {suffix}` 模板中（→「启用设置同步」/「禁用设置同步」）。统一译为「设置同步」。
- **`Oz Cloud API Keys`**: `Oz Cloud` 是 Warp 内部企业产品名（`WarpIcon::OzCloud`），字面保留；`API Keys` → 「API 密钥」。
- **`...` 处理**: `checking for update...` / `downloading update...` 中的 ASCII `...` → `……` (U+2026 双字符)，与既有约定一致。`Loading locally indexed repos…` 源已是 U+2026，原样保留。
- **占位符**: `{description_suffix}` (mod.rs ×2) 与 `{path}` (modal ×1) 严格保留拼写与位置。
- **`Warpify` (warpify_page L605 上下文)**: 本批次只译 1 条（`Added commands`），不涉及 Warpify 本身翻译，未来批次处理。

## Glossary delta

无新增。沿用既有 93 条术语：MCP / SSH / Warp / Warp Drive / Agent / API / Git / shell / allowlist→白名单 / denylist→黑名单 / block→命令块 / workflow→工作流 / settings sync→设置同步 / Oz Cloud（已作为产品名保留）等。

`term_count` 保持 93。
