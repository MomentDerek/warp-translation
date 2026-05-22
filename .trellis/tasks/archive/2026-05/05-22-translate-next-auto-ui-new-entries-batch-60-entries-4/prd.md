# Translate next auto_ui new entries — batch 60 entries 4 (workspace + quit-warning + AI panel)

## Goal

清扫 **5 个 auto_ui-new 热点文件** 并附 1 条 workspace/view/left_panel.rs 凑数收尾，共 **60 条**。主题统一为「workspace 主视图 + 退出/关闭警告对话框 + AI 助手面板 + 登录表单 + 窗格分组键位」。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/workspace/view.rs` | 17 | 自动更新菜单 / 标签配置入口 / 重新登录横幅 / Tools panel 工具提示 / 云端任务接力 |
| `app/src/quit_warning/mod.rs` | 16 | 退出/关闭确认对话框（标题 + 进程提示 + 范围后缀拼接） |
| `app/src/ai_assistant/panel.rs` | 10 | AI 助手面板（占位符 + 零状态示例 prompt + 工具提示 + 键位标签） |
| `app/src/auth/auth_view_body.rs` | 8 | 登录表单（同意条款碎片 + 跳过登录碎片 + 浏览器未启动提示） |
| `app/src/pane_group/mod.rs` | 8 | 窗格分组键位（切换/调整分隔条上下左右） |
| `app/src/workspace/view/left_panel.rs` | 1 | 左侧面板关闭按钮工具提示（凑齐 60，清零该文件） |

继 batch-3（settings + onboarding sweep）之后，auto_ui-new 余量 441 → 381（-60）；`translated` 1800 → 1860，`new` 4882 → 4822。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=1800`, `fuzzy=52`, `new=4882`（auto_ui 441 / uncertain 4441）。
- glossary 现有 93 条；本批无新增术语：沿用 `Warp` / `Warp AI` / `Warp Agent` / `Warp Drive` / `MCP` / `API` / `Git` / `Agent` / `block→命令块` / `pane→窗格` / `tab→标签页` / `worktree`（字面保留）。
- 6 个文件 + 1 凑数的语义分层：
  - `workspace/view.rs`：主工作区视图常量串 — 横幅 / 更新菜单 / 用户菜单 / 工具提示。
  - `quit_warning/mod.rs`：退出/关闭警告对话框 — 含 3 条「范围后缀」(scope_suffix)，源以前置空格 + 句末英文句点拼接到上文。
  - `ai_assistant/panel.rs`：AI 助手面板 — 含 2 条以前置空格开头的 placeholder 文本 + 4 条零状态示例 prompt。
  - `auth/auth_view_body.rs`：登录入口表单 — 6 条以「尾随空格」结尾的链接前缀碎片。
  - `pane_group/mod.rs`：窗格分组键位 — 8 条 `Switch panes …` / `Resize pane > Move divider …`。
  - `workspace/view/left_panel.rs`：左侧面板关闭按钮 tooltip 凑数。
- 占位符：`{version}`（workspace/view L6736）、`{}`（多条 `format!` 模板）、`{scope_suffix}`（quit_warning L327/337，命名占位符）。

## Scope by file

### app/src/workspace/view.rs (17)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV128X02B566DEG5G692P` | 625 | `Access your tab configs here.` | `在此访问您的标签页配置。` |
| `01KQXQV12AEXSNW2MXMYTA1W0A` | 6736 | `Current version is {version}` | `当前版本为 {version}`（命名占位符保留） |
| `01KQXQV12CCQ7M2ENMDZYBB463` | 6743 | `Install update ({})` | `安装更新（{}）`（占位符保留；英文括号→全角） |
| `01KQXQV12CXTS869VN5NFC0BE6` | 8586 | `Invite a friend` | `邀请好友` |
| `01KQXQV12DJK6HZMSEXMZX05RT` | 6382 | `New tab config` | `新建标签页配置` |
| `01KQXQV12DQ7CE410CG9EK27PV` | 6375 | `New worktree config` | `新建 worktree 配置`（`worktree` 字面保留） |
| `01KQXQV12ERYY4NW1GVXPZC2P0` | 19747 | `Please sign in again to restore access to cloud-based features.` | `请重新登录以恢复对云端功能的访问。` |
| `01KQXQV12G09JYFD9W5TBDH2B9` | 611 | `Some Warp features may not work as expected without updating immediately, but Warp is unable to perform the update.` | `部分 Warp 功能在未立即更新时可能无法按预期工作，但 Warp 无法执行此次更新。` |
| `01KQXQV12HBVS7DATJMHYT07FE` | 6748 | `Updating to ({})` | `正在更新至（{}）` |
| `01KQXQV12HDNQAXWM6MY7J3WMX` | 17991 | `Tools panel` | `工具面板` |
| `01KQXQV12HVC242QKJ7511HJ0C` | 582 | `Update Warp` | `更新 Warp` |
| `01KQXQV12HW07YW7RJC7Z3K76N` | 8489 | `Update and relaunch Warp` | `更新并重启 Warp` |
| `01KQXQV12HZ6N0JD4ZQAKM3EMJ` | 8523 | `What's new` | `新功能` |
| `01KQXQV12J0MFA5NBATN92M6VB` | 19746 | `Your login has expired.` | `您的登录已过期。` |
| `01KQXQV12J6TT5MZQ6A82DHSHT` | 609 | `Your app is out of date and some features may not work as expected. Please update immediately.` | `应用已过期，部分功能可能无法按预期工作。请立即更新。` |
| `01KQXQV12JYMEDV8JZZAC7PXJ3` | 19837 | `Your app is out of date and needs to update.` | `应用已过期，需要更新。` |
| `01KS2GEQ04DAXQX46KH3M3FDVZ` | 685 | `Continue this local Warp Agent task in the cloud from the current conversation state.` | `从当前会话状态在云端继续此本地 Warp Agent 任务。` |

### app/src/quit_warning/mod.rs (16)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1214YS0CEYDTVSRMY0K` | 298 | ` in this pane.` （前置 ASCII 空格 + 句末英文句点） | ` （位于此窗格）。` （保留前置空格；英文句点→全角句号） |
| `01KQXQV1218WA166R3H2J2GQR2` | 296 | ` in this tab.` | ` （位于此标签页）。` |
| `01KQXQV1219N114H9S3RBQGXTD` | 297 | ` in this window.` | ` （位于此窗口）。` |
| `01KQXQV12925HR740VRWK5AJ78` | 434 | `Close pane?` | `关闭窗格？` |
| `01KQXQV129AK83JY7SDE5M8D0H` | 436 | `Close tabs?` | `关闭标签页？` |
| `01KQXQV129B2PS6DRWYKVRTH41` | 437 | `Close window?` | `关闭窗口？` |
| `01KQXQV129X5H48ERD6BQ7FTWD` | 435 | `Close tab?` | `关闭标签页？` |
| `01KQXQV12BENEB9F66SD21PTEN` | 415 | `Don't Save` | `不保存` |
| `01KQXQV12BQA1F5QJRWM4RK3NN` | 335 | `Do you want to save the changes you made to {}? Your changes will be discarded if you don't save them.` | `是否保存对 {} 所做的更改？如不保存，您的更改将被丢弃。` |
| `01KQXQV12EMNR98FHHNCHEY8Y4` | 438 | `Quit Warp?` | `退出 Warp？` |
| `01KQXQV12FJQ0ZK9J5HHG6S6WJ` | 439 | `Save changes?` | `保存更改？` |
| `01KQXQV12J0PQZVBFH3DQ2722R` | 327 | `You are sharing {} {}{scope_suffix}` | `您正在分享 {} {}{scope_suffix}`（3 个占位符全部保留；后缀附加 `（位于此...）。`） |
| `01KQXQV12J7KY0GS918HEK548F` | 403 | `Yes, close` | `是，关闭` |
| `01KQXQV12JC2PRPCA2759RC9R8` | 337 | `You have unsaved file changes{scope_suffix}` | `您有未保存的文件更改{scope_suffix}` |
| `01KQXQV12JEGPQCCRDJFP56J6F` | 304 | `You have {} {} running` | `您有 {} 个 {} 正在运行` |
| `01KQXQV12JR7NCZBTWYP95A19R` | 404 | `Yes, quit` | `是，退出` |

### app/src/ai_assistant/panel.rs (10)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV10N8SEYP4AK21K7JH87` | 84 | ` Ask a question...` （前置空格 + ASCII `...`） | ` 提问……` （保留前置空格；ASCII `...`→`……`） |
| `01KQXQV11RY5TZDZC609BR8PZZ` | 85 | ` Type a response or click one above...` | ` 输入回复或点击上方任一选项……` |
| `01KQXQV129PBQSABCH6PCP0D15` | 154 | `Close Warp AI` | `关闭 Warp AI` |
| `01KQXQV12AV1ZXW9WG7SC66JH1` | 791 | `Copy transcript to clipboard` | `复制对话记录到剪贴板` |
| `01KQXQV12C1N3119STH7GVT0M0` | 161 | `Focus Terminal Input From Warp AI` | `从 Warp AI 聚焦到终端输入` |
| `01KQXQV12C89VWPZMG13WCNF6V` | 81 | `How do I find all files containing specific text?` | `如何查找包含特定文本的所有文件？` |
| `01KQXQV12CNPXDTB8AGHBBKNTD` | 80 | `How do I undo the most recent commits in git?` | `如何撤销 Git 中最近的提交？` |
| `01KQXQV12EZWW21FZF0C6S6BMB` | 168 | `Restart Warp AI` | `重启 Warp AI` |
| `01KQXQV12FW7Q2QGQDNC215Q23` | 78 | `Shift + ctrl + space a block or text selection to ask Warp AI.` | `选中命令块或文本后按 Shift + ctrl + space 即可向 Warp AI 提问。` |
| `01KQXQV12JS3KGSTC6VKT00EKY` | 79 | `Write a script to connect to an AWS EC2 instance.` | `编写一个连接 AWS EC2 实例的脚本。` |

### app/src/auth/auth_view_body.rs (8)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1290B2BXXHGAW9NJ3BT` | 335 | `By continuing, you agree to Warp's ` （尾随空格） | `继续即表示您同意 Warp 的 ` （保留尾随空格；后接 `Terms of Service` 链接） |
| `01KQXQV1292TSY727D48NX2B0X` | 493 | `Already have an account? ` （尾随空格） | `已有账户？ ` （保留尾随空格；后接 `Sign in` 链接；中文问号 + 空格紧贴英文链接） |
| `01KQXQV129D8BRAV7D4JNGAGDR` | 52 | `Auth Token` | `认证令牌` |
| `01KQXQV12B4F2C86ZTHRCA527D` | 521 | `Don't want to sign in right now? ` （尾随空格） | `暂时不想登录？ ` |
| `01KQXQV12CY05JA1GFN0TRPNY9` | 776 | `If your browser hasn't launched, ` （尾随空格） | `如果浏览器未启动， ` （保留尾随空格；中文逗号 + ASCII 空格紧贴 `copy the URL` 链接） |
| `01KQXQV12ETVKKPMD9RWW4GEQ7` | 363 | `Privacy Settings` | `隐私设置` |
| `01KQXQV12J5C5PW6HDC6PXGMB0` | 566 | `are only available to logged-in users. ` （尾随空格） | `仅对已登录用户开放。 ` |
| `01KQXQV12JEED5P4BERYQ53CQ4` | 802 | `and open the page manually.` | `并手动打开页面。` |

### app/src/pane_group/mod.rs (8)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E5NBF8QGVAVWFA1H0` | 440 | `Resize pane > Move divider up` | `调整窗格大小 > 向上移动分隔条` |
| `01KQXQV12EJRJKTMXRVW3QNTG3` | 449 | `Resize pane > Move divider down` | `调整窗格大小 > 向下移动分隔条` |
| `01KQXQV12EPRHFYEY7H5KRBW9Y` | 422 | `Resize pane > Move divider left` | `调整窗格大小 > 向左移动分隔条` |
| `01KQXQV12EW9MTGTB8A4MKFMZJ` | 431 | `Resize pane > Move divider right` | `调整窗格大小 > 向右移动分隔条` |
| `01KQXQV12G799CZN2BB2CV0JF3` | 389 | `Switch panes right` | `切换到右侧窗格` |
| `01KQXQV12G8Z673T24F40VTWC1` | 398 | `Switch panes up` | `切换到上方窗格` |
| `01KQXQV12GADARX32XQW4452RY` | 407 | `Switch panes down` | `切换到下方窗格` |
| `01KQXQV12GV9FBN6S4FC692C5R` | 380 | `Switch panes left` | `切换到左侧窗格` |

### app/src/workspace/view/left_panel.rs (1, workspace family pad)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12937TNH3NRP95VRDQ9` | 797 | `Close panel` | `关闭面板` |

## Decisions / Anomalies

- **scope_suffix 拼接链 (quit_warning)**：源串运行时拼接为 `"You have 2 processes running" + " in 2 windows" + " in this tab."`。我们能控制的只是表内三条最外层后缀（`" in this tab."` / `" in this window."` / `" in this pane."`）与首段模板 `"You have {} {} running"`。中间动态英文片段 (`" in 2 windows"`) 不在翻译表内、运行时仍为英文，因此最终中文显示会是「您有 2 个 processes 正在运行 in 2 windows （位于此标签页）。」——存在混合，可接受。后续 uncertain 批可补全 `pluralize` 词形。
- **前置空格保留 (quit_warning 3 条 / panel.rs 2 条 / auth_view_body.rs 5 条)**：源串以 ASCII 空格起始或结尾，作为拼接 glue。译文必须严格保留单方向：源有→译有；源无→译无。`check_invariants` 强制此规则。
- **`{scope_suffix}` 命名占位符 (quit_warning L327/337)**：与 `{}` 不同，必须保留命名形式且数量一致。占位符校验按 `re.findall(r"\{[^{}]*\}")` 精确匹配。
- **`Warp Agent` 品牌串 (workspace/view L685)**：与 `Warp AI` 同等地位，字面保留双词组合。
- **`worktree` 字面保留**：与 batch-3 一致策略；新建项语境下读作「新建 worktree 配置」。
- **`Shift + ctrl + space` 键名 (panel.rs L78)**：源串中 `ctrl` 小写、`Shift` 首字母大写，是平台键标准写法。译文按字面保留，前置「选中命令块或文本后按 …」。
- **`AWS EC2` 品牌名 (panel.rs L79)**：字面保留，不译成「亚马逊云服务弹性计算」类。
- **`git` → `Git` (panel.rs L80)**：源中 `git` 小写指 git 命令行；译文用 `Git` 大写品牌名（与 batch-3 / glossary 一致）。
- **括号风格 (workspace/view L6743/6748, quit_warning suffix)**：源使用 ASCII `()`，译文统一用全角 `（）`；中文段落中括号包裹版本号视觉更协调。
- **Tools panel / Tools panel tooltip 区分 (workspace/view L17991)**：源串作为 fallback tooltip（具体子视图打开时显示具体名，否则显示 `"Tools panel"`）；译为「工具面板」。
- **凑数项 `Close panel` (left_panel.rs)**：从「文件剩余 1 条」候选池中选择 workspace 主题相邻者，清零 `workspace/view/left_panel.rs` 的 auto_ui-new 计数。

## Glossary delta

无新增。沿用既有 93 条术语。`term_count` 保持 93。
