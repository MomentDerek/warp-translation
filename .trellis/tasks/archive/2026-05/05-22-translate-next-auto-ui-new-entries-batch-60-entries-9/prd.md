# Translate next auto_ui new entries — batch 60 entries 9 (Strategy: long-tail hot-spot sweep — onboarding/workflow argument editor + resource_center/changelog + Warp Drive page + launch modals + skill resolve + commit dialog + global search + many 2-entry leaves)

## Goal

清扫 **29 个 auto_ui-new 热点文件** 共 **60 条**，29 个文件全部清零。本批为「长尾扫荡」批次：余量分布从大到小（最大 3）转入小叶节点，单文件 2 条占多数。覆盖：onboarding（agent_slide 3）+ workflow argument editor（3）+ resource_center（view 3 + changelog 2）+ Warp Drive page（2）+ launch modal oz_launch（2）+ env_vars/transfer/delete environment 三个 settings 模态（2/2/2）+ settings_page 通用 tooltip（2）+ 命令搜索/Warp AI（2）+ undo_close（2）+ skill resolve（2 panic-like）+ ui_components 两组 panic（dialog 2 + red_notification_dot 2）+ install_tmux（2）+ git commit dialog（2）+ warpify success block（2）+ notebooks editor find_bar（2）+ uri new-tab toast（2）+ terminal block_filter（2）+ launch_configs save_modal（2）+ settings import view（2）+ code review comment list（2）+ global search toggles（2）+ accept-autosuggestion keybinding（2）+ drive sort（2）+ directory_color_add_picker（2）+ theme_deletion_body（1）。

跨文件外溢清零（副作用扫到的 SHARED 条目）：
- `app/src/settings_view/features_page.rs` 同步清零 2 条（与 accept_autosuggestion 共享 `Accept Autosuggestion` / `Change keybinding`）。
- `app/src/settings_view/billing_and_usage_page.rs` 同步清零 2 条（与 drive/mod 共享 `A to Z` / `Z to A`）。
- `app/src/workflows/workflow_view.rs` 同步清零 1 条（与 env_var_collection 共享 `Add a title`）。
- `app/src/workspace/view.rs` 同步清零 1 条（与 resource_center/view 共享 `Warp Essentials`）。
- `app/src/notebooks/editor/view.rs` 同步清零 2 条（与 notebooks/editor/find_bar 共享 `Focus next match` / `Focus previous match`）。

| 文件 | 数量 | 说明 |
|---|---|---|
| `crates/onboarding/src/slides/agent_slide.rs` | 3 | 浏览器认证回退栏 inline span（含 leading/trailing 空格）+ 套餐激活 toast |
| `app/src/workflows/workflow_view/argument_editor.rs` | 3 | 工作流参数编辑器（占位符 / 工具提示 / 描述长文） |
| `app/src/resource_center/view.rs` | 3 | 资源中心顶级标题（Keyboard Shortcuts / Warp Essentials）+ 1 个 `.expect` panic |
| `app/src/settings_view/directory_color_add_picker.rs` | 2 | 目录颜色添加选择器（footer label / 列表头） |
| `app/src/editor/accept_autosuggestion_keybinding_view.rs` | 2 | 自动建议快捷键提示（Accept Autosuggestion / Change keybinding） |
| `app/src/drive/mod.rs` | 2 | 排序方向（A to Z / Z to A，与 billing_and_usage_page 共享） |
| `app/src/workspace/view/launch_modal/oz_launch.rs` | 2 | OpenWarp 启动模态（云端同步会话 checkbox + 描述长文） |
| `app/src/env_vars/view/env_var_collection.rs` | 2 | 环境变量集合（教育文 / 标题占位符） |
| `app/src/settings_view/transfer_ownership_confirmation_modal.rs` | 2 | 转让团队所有权确认（长描述 + 按钮） |
| `app/src/settings_view/delete_environment_confirmation_dialog.rs` | 2 | 移除环境确认（标题 + 长描述） |
| `app/src/settings_view/settings_page.rs` | 2 | 设置页通用 tooltip（点击查看文档 / 不同步提示） |
| `app/src/search/command_search/warp_ai.rs` | 2 | 命令搜索 Warp AI 入口（询问 / 翻译为 shell 命令） |
| `app/src/settings_view/features/undo_close.rs` | 2 | 撤销关闭会话设置（启用 toggle / 宽限期标签） |
| `app/src/ai/skills/resolve_skill_spec.rs` | 2 | skill spec 解析错误（`git clone` 失败 / 目标目录非 git 仓库） |
| `app/src/ui_components/dialog.rs` | 2 | 2 条 `.expect` panic（FamilyId set / Font size set） |
| `app/src/terminal/ssh/install_tmux.rs` | 2 | SSH 安装 tmux 选项（使用包管理器 / 安装到 ~/.warp） |
| `app/src/code_review/git_dialog/commit.rs` | 2 | 提交对话框（生成中占位符 / 输入占位符） |
| `app/src/terminal/warpify/success_block.rs` | 2 | Warpify 成功命令块（说明文 + 自动 Warpify 提示） |
| `app/src/notebooks/editor/find_bar.rs` | 2 | 笔记本查找栏（上一个 / 下一个匹配项） |
| `app/src/uri/mod.rs` | 2 | URI 新标签页 toast（标题 + 描述） |
| `app/src/terminal/block_filter.rs` | 2 | 命令块过滤工具提示（反转 / 上下文行） |
| `app/src/launch_configs/save_modal.rs` | 2 | 启动配置保存模态（标题 + Open YAML） |
| `app/src/settings/import/view.rs` | 2 | 设置导入视图（选择提示 + 加载文案） |
| `app/src/ui_components/red_notification_dot.rs` | 2 | 2 条 `.expect` panic（RedNotificationDot 缺 width/height） |
| `app/src/resource_center/section_views/changelog_section.rs` | 2 | 更新日志分区（错误文 + 阅读全部） |
| `app/src/code_review/comment_list_view.rs` | 2 | 评论列表（发送给 Agent / 在 GitHub 中查看） |
| `app/src/settings_view/warp_drive_page.rs` | 2 | Warp Drive 设置页（未登录提示 + 总览长描述） |
| `app/src/workspace/view/global_search/view.rs` | 2 | 全局搜索（切换大小写敏感 / 切换正则表达式） |
| `app/src/themes/theme_deletion_body.rs` | 1 | 主题删除模态（Delete theme） |

继 batch-8 之后，auto_ui-new 余量 141 → 81（-60 主清扫；SHARED 副作用条目同时翻转为 translated 但与主条目共享同一 entry，因此 registry 净降仍为 60）；`translated` 2100 → 2160，`new` 4582 → 4522。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=2100`, `new=4582`, `fuzzy=52`。
- glossary 现有 95 条；本批沿用既有术语：`Warp` / `Warp Drive` / `Warp AI` / `Agent` / `MCP` / `GitHub` / `keybinding → 快捷键` / `theme → 主题` / `workflow → 工作流` / `notebook → 笔记本` / `prompt → 提示词` / `model → 模型` / `shell → shell（保留英文）` / `secret → 机密信息` / `changelog → 更新日志` / `autosuggestion → 自动建议` / `session → 会话`。无新增术语，`term_count` 保持 95。
- **占位符**：4 条含位置/命名占位符 —
  - `{e}`（resolve_skill_spec L191，命名）
  - `{}`（resolve_skill_spec L168 / transfer_ownership L57 / delete_environment L88，位置）
  - `{package_manager}`（install_tmux L260，命名）
  均保留字面占位符，原位置/语序可按中文表达自然调整（已有同类先例：`'Failed to load directory: {e}' → '加载目录失败：{e}'`）。无 strftime。
- **`.expect` 内部诊断 panic 串（5 条）**：
  - `Should have a valid page`（resource_center/view L204）
  - `FamilyId set` / `Font size set`（ui_components/dialog L108-109）
  - `RedNotificationDot requires width` / `RedNotificationDot requires height`（ui_components/red_notification_dot L17-18）
  这些 panic 在崩溃时才显示。沿用 batch-7/8 panic 翻译惯例：Rust 标识符（`FamilyId`、`RedNotificationDot`）保留英文，叙述部分译中文；`width`/`height` 作为代码字段名也保留英文。
- **`Generating commit message…` (commit.rs L76)**：源已使用 unicode 省略号 `…`（U+2026），译文直接复用即可，**不**需要 `...` → `……` 转换。
- **`Looking for settings to import...` (settings/import/view L974)**：源使用 ASCII `...`，按项目惯例转为 `……`。
- **`+ Add directory…` (directory_color_add_picker L29)**：源已使用 unicode `…`，保留。
- **`' and open the page manually. '` / `' to paste your token from the browser.'` (agent_slide)**：与链接 chip 拼接的 inline span，**含 leading/trailing 空格**。翻译必须严格保留空格方向，否则与链接挤在一起。已对照既有翻译 `'and open the page manually.' → '并手动打开页面。'`（同义短句），加上首尾空格。
- **`Generating commit message…` 上下文**：`code_review/git_dialog/commit.rs` 中 `GENERATING_PLACEHOLDER_TEXT`，加载占位符。译「正在生成提交信息…」（保留源中 unicode 省略号）。

## Scope by file

### crates/onboarding/src/slides/agent_slide.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV11XYQABRZQ4D93W92AZ` | 1219 | `' and open the page manually. '` | `' 并手动打开页面。 '` |
| `01KQXQV127FAV6VBFE25X67P3D` | 1227 | `' to paste your token from the browser.'` | `' 以粘贴来自浏览器的令牌。'` |
| `01KQXQV12ECK18X04M2X5MC9BB` | 1273 | `Plan successfully activated. All premium models are available.` | `套餐已成功激活。所有高级模型均已可用。` |

### app/src/workflows/workflow_view/argument_editor.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129RJ5FHZPPG57RF85F` | 591 | `Add a workflow argument` | `添加工作流参数` |
| `01KQXQV12CBYYERR41832VYPF2` | 605 | `Fill out the arguments in this workflow and copy it to run in your terminal session` | `填写此工作流中的参数并复制到您的终端会话中运行` |
| `01KQXQV12HPPKKV7W1GPMNF4CY` | 48 | `Value (optional)` | `值（可选）` |

### app/src/resource_center/view.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DPG4EWFR6WW4792X1` | 334 | `Keyboard Shortcuts` | `键盘快捷键` |
| `01KQXQV12F7V39Q83KS16MNGQX` | 204 | `Should have a valid page` | `应有一个有效的页面` |
| `01KQXQV12H13BSTEQ1T1NG3TY0` | 339 | `Warp Essentials` | `Warp 入门精要` |

### app/src/settings_view/directory_color_add_picker.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV128795HD9Y1RTAPYN8W` | 29 | `+ Add directory…` | `+ 添加目录…` |
| `01KQXQV1295KZN6K5N88K92TE0` | 30 | `Add directory color` | `添加目录颜色` |

### app/src/editor/accept_autosuggestion_keybinding_view.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1288YA2VRN0K94DMEEB` | 225 | `Accept Autosuggestion` | `接受自动建议` |
| `01KQXQV1291DG3EMESBRVPB372` | 348 | `Change keybinding` | `修改快捷键` |

### app/src/drive/mod.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV128MYXRDJ77F0NETEDA` | 355 | `A to Z` | `A 到 Z` |
| `01KQXQV12JEX64PJSW1S7ZZPTB` | 356 | `Z to A` | `Z 到 A` |

### app/src/workspace/view/launch_modal/oz_launch.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GV6SR8S1NSFWT8YSS` | 174 | `Sync conversations to cloud` | `将会话同步至云端` |
| `01KQXQV1292KS1XH52EB2393Q6` | 175 | `Agent conversations stored in the cloud can be shared with anyone with one click, and allow conversations to be continued across devices and on logout.` | `存储在云端的 Agent 会话只需一键即可与任何人分享，并支持跨设备和登出后继续对话。` |

### app/src/env_vars/view/env_var_collection.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1295MKB31WX5JNVZ5C7` | 83 | `Add secret or command. Warp never stores external secrets` | `添加机密信息或命令。Warp 永远不会存储外部机密信息` |
| `01KQXQV129R3KK8TA76DV1HG52` | 94 | `Add a title` | `添加标题` |

### app/src/settings_view/transfer_ownership_confirmation_modal.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1298ZJXC3JE4NZXW0PK` | 57 | `Are you sure you want to transfer team ownership to {}? You will no longer be the owner and will not be able to take any administrative actions for this team.` | `确定要将团队所有权转让给 {} 吗？您将不再是所有者，也无法对此团队执行任何管理操作。` |
| `01KQXQV12HTQWVMTYHVED4NWHV` | 91 | `Transfer` | `转让` |

### app/src/settings_view/delete_environment_confirmation_dialog.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1299G1QQQ11ZRE8X732` | 88 | `Are you sure you want to remove the {} environment?` | `确定要移除环境 {} 吗？` |
| `01KQXQV12ADE5CCXQ3WSMRBX12` | 93 | `Delete environment?` | `删除环境？` |

### app/src/settings_view/settings_page.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129SB4G1381FMC8ACFK` | 557 | `Click to learn more in docs` | `点击在文档中了解更多` |
| `01KQXQV12GF6T8MGNDT00TPD4J` | 615 | `This setting is not synced to your other devices` | `此设置不会同步至您的其他设备` |

### app/src/search/command_search/warp_ai.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129XQE3T9X77F1P0RAB` | 39 | `Ask Warp AI for command suggestions` | `向 Warp AI 询问命令建议` |
| `01KQXQV12HSQSG7ZM7CZQYNVPG` | 40 | `Translate into shell command using Warp AI` | `使用 Warp AI 翻译为 shell 命令` |

### app/src/settings_view/features/undo_close.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12B65N8GJEVNKWZMXAK` | 181 | `Enable reopening of closed sessions` | `启用重新打开已关闭的会话` |
| `01KQXQV12CFV16K20FE5Z88JHQ` | 140 | `Grace period (seconds)` | `宽限期（秒）` |

### app/src/ai/skills/resolve_skill_spec.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BH5BB2KGD84P8GR4M` | 191 | `Failed to execute git clone: {e}` | `执行 git clone 失败：{e}` |
| `01KQXQV12GD1ZQ6D9JNH5WSSC2` | 168 | `Target directory {} already exists but is not a git repository` | `目标目录 {} 已存在但不是 git 仓库` |

### app/src/ui_components/dialog.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BWHCWANGH2SAEYS91` | 108 | `FamilyId set` | `FamilyId 已设置` |
| `01KQXQV12C94X07P38ED0YA7XK` | 109 | `Font size set` | `字号已设置` |

### app/src/terminal/ssh/install_tmux.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12C1DM1C6G5D67JQ7Z8` | 260 | `Install with {package_manager}` | `使用 {package_manager} 安装` |
| `01KQXQV12CJ05PK5XPRR99CFWF` | 264 | `Install to ~/.warp` | `安装到 ~/.warp` |

### app/src/code_review/git_dialog/commit.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12C2428FHA0E5YSA32P` | 76 | `Generating commit message…` | `正在生成提交信息…` |
| `01KQXQV12H72EA4W15E9AC28RC` | 80 | `Type a commit message` | `输入提交信息` |

### app/src/terminal/warpify/success_block.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FJSPACWM6PN6XVY6C` | 119 | `Run the following to automatically Warpify in the future:` | `运行以下命令以在将来自动 Warpify：` |
| `01KQXQV12C7ZP4DJKD092N2BMS` | 121 | `In remote subshells, Warp runs commands in the background to power completions, syntax highlighting, and other features.` | `在远程子 shell 中，Warp 会在后台运行命令以支持补全、语法高亮等功能。` |

### app/src/notebooks/editor/find_bar.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CPTH0YSQ9TV20P6CK` | 558 | `Focus next match` | `聚焦下一个匹配项` |
| `01KQXQV12C8HR63KT0AM6VXK1R` | 559 | `Focus previous match` | `聚焦上一个匹配项` |

### app/src/uri/mod.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12D9B7ARH10MWBAFRJ0` | 1089 | `New tab created` | `已创建新标签页` |
| `01KQXQV12CE79C0FF9EBHBV2XB` | 1090 | `Go to Warp to see your new tab.` | `前往 Warp 查看您的新标签页。` |

### app/src/terminal/block_filter.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FATG2W881N8J0379R` | 52 | `Show context lines around matches` | `在匹配项周围显示上下文行` |
| `01KQXQV12CTM18YDM0DXJMC9PX` | 55 | `Invert filter` | `反转过滤器` |

### app/src/launch_configs/save_modal.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FVKV9WA97AT280CJJ` | 40 | `Save Configuration` | `保存配置` |
| `01KQXQV12D7H1Y8CPAF9F62SB4` | 41 | `Open YAML File` | `打开 YAML 文件` |

### app/src/settings/import/view.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FJKN2DMQ7R7KYPG83` | 973 | `Select a settings profile to import:` | `选择要导入的设置配置：` |
| `01KQXQV12DSPRFAWTM2H6Z5H9S` | 974 | `Looking for settings to import...` | `正在查找可导入的设置……` |

### app/src/ui_components/red_notification_dot.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E7832S4J9DYTBY9PC` | 17 | `RedNotificationDot requires width` | `RedNotificationDot 需要 width` |
| `01KQXQV12EEMQ80P7ZD85AASHA` | 18 | `RedNotificationDot requires height` | `RedNotificationDot 需要 height` |

### app/src/resource_center/section_views/changelog_section.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HYC0AGWGXV96BBN8D` | 32 | `Unable to fetch the latest changelog.` | `无法获取最新的更新日志。` |
| `01KQXQV12EJQSQ2XDV81N2W8QQ` | 368 | `Read all changelogs` | `阅读全部更新日志` |

### app/src/code_review/comment_list_view.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FVG8M9S7WJ93FAC2F` | 955 | `Send to Agent` | `发送给 Agent` |
| `01KQXQV12H137VMVYJ5V0PDK0J` | 1084 | `View in GitHub` | `在 GitHub 中查看` |

### app/src/settings_view/warp_drive_page.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GV98JWH1XJ5GJDN3W` | 142 | `To use Warp Drive, please create an account.` | `要使用 Warp Drive，请创建账户。` |
| `01KQXQV12HWY53Z9CPN3A6NJSF` | 251 | `Warp Drive is a workspace in your terminal where you can save Workflows, Notebooks, Prompts, and Environment Variables for personal use or to share with a team.` | `Warp Drive 是您终端中的工作区，可用于保存工作流、笔记本、提示词与环境变量，供个人使用或与团队共享。` |

### app/src/workspace/view/global_search/view.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GKJ8CCZ0GHTHPDFFV` | 668 | `Toggle Case Sensitivity` | `切换大小写敏感` |
| `01KQXQV12GT9XNKF39ZES7R2CT` | 678 | `Toggle Regex` | `切换正则表达式` |

### app/src/themes/theme_deletion_body.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12ADK90JYEGZ1CD1FG1` | 31 | `Delete theme` | `删除主题` |

## Decisions / Anomalies

- **`Value (optional)` (argument_editor L48)**：与既有翻译 `'Default value (optional)' → '默认值（可选）'` 保持一致，译「值（可选）」。
- **`Warp Essentials` (resource_center/view L339)**：资源中心中的「入门必读」分组。译「Warp 入门精要」（保留 Warp 品牌；与同文件其他术语风格对齐）。
- **`Keyboard Shortcuts` (resource_center/view L334)**：与既有 `'Open Settings: Keyboard Shortcuts' → '打开设置：快捷键'` 略有不同 — 这里是页面标题，更完整地译「键盘快捷键」以与「Keyboard Shortcuts」原文对应；既有「快捷键」翻译用于 keybinding 通用术语，两者并存不矛盾。
- **`Should have a valid page` (resource_center/view L204, `.expect`)**：内部 panic 不变式描述。沿用 batch-7 panic 翻译惯例，译「应有一个有效的页面」。
- **`A to Z` / `Z to A` (drive/mod L355-356)**：排序方向。译「A 到 Z」/「Z 到 A」（保留字母原文，使用中文「到」连接）。
- **`Accept Autosuggestion` / `Change keybinding`**：与既有 `'Accept autosuggestion' → '接受自动建议'` 完全对齐（即便首字母大小写差异，中文译文相同）。`Change keybinding` 译「修改快捷键」沿用 keybinding glossary。
- **`+ Add directory…` (directory_color_add_picker L29)**：源已使用 unicode 省略号 `…`，保留。译「+ 添加目录…」。
- **`Add a title` (env_var_collection L94, SHARED with workflow_view)**：通用占位符。译「添加标题」。
- **`Are you sure you want to transfer team ownership to {}?` (transfer_ownership L57)**：`{}` 是位置占位符（用户/团队名），保留原位。译「确定要将团队所有权转让给 {} 吗？...」。
- **`Are you sure you want to remove the {} environment?` (delete_environment L88)**：`{}` 是环境名。中文调整为「确定要移除环境 {} 吗？」（中文「环境 X」语序更自然）。
- **`Click to learn more in docs` (settings_page L557)**：设置项 tooltip 默认值。译「点击在文档中了解更多」。
- **`This setting is not synced to your other devices` (settings_page L615)**：本地设置 tooltip。译「此设置不会同步至您的其他设备」。
- **`Ask Warp AI for command suggestions` / `Translate into shell command using Warp AI` (warp_ai L39-40)**：命令搜索面板的 Warp AI 入口。`Warp AI` 保留品牌；`shell command` 译「shell 命令」（沿用既有 `'Generate shell commands with natural language.' → '使用自然语言生成 shell 命令。'`）。
- **`Grace period (seconds)` (undo_close L140)**：会话关闭后允许撤销的宽限秒数。译「宽限期（秒）」。
- **`Failed to execute git clone: {e}` (resolve_skill_spec L191)**：`git clone` 是命令字面量，保留英文；`{e}` 是命名占位符（错误对象）。译「执行 git clone 失败：{e}」。
- **`Target directory {} already exists but is not a git repository` (resolve_skill_spec L168)**：`{}` 是路径，保留原位。`git repository` 译「git 仓库」（保留 git 英文）。
- **`FamilyId set` / `Font size set` (dialog L108-109, `.expect`)**：`Option.expect()` 的字段名 unwrap panic 提示。`FamilyId` 是 Rust 字段标识符，保留英文；译「FamilyId 已设置」/「字号已设置」（叙述部分译中文，提示 unwrap 失败时该值「本应已被设置」）。
- **`Install with {package_manager}` (install_tmux L260)**：`{package_manager}` 是命名占位符（如 `apt`/`brew`），保留原位。译「使用 {package_manager} 安装」。
- **`Install to ~/.warp` (install_tmux L264)**：`~/.warp` 是路径字面量，保留原文。译「安装到 ~/.warp」。
- **`Generating commit message…` (commit L76)**：源含 unicode `…`，**直接复用**，不需要 `...` → `……` 转换。译「正在生成提交信息…」。
- **`Type a commit message` (commit L80)**：提交对话框 fallback 占位符。译「输入提交信息」（与既有 `commit message → 提交信息` 一致）。
- **`Run the following to automatically Warpify in the future:` (success_block L119)**：`Warpify` 是 Warp 品牌动词（让远程 shell 启用 Warp 特性），保留英文。译「运行以下命令以在将来自动 Warpify：」。
- **`In remote subshells, ...` (success_block L121)**：`subshell` 译「子 shell」（保留 shell 英文，沿用既有 shell 命名）。译「在远程子 shell 中，Warp 会在后台运行命令以支持补全、语法高亮等功能。」。
- **`Focus next/previous match` (find_bar L558-559)**：笔记本查找栏快捷按钮。译「聚焦上一个/下一个匹配项」（中文按动词在前的搭配）。
- **`Go to Warp to see your new tab.` (uri L1090)**：URI 创建标签后的系统通知描述。译「前往 Warp 查看您的新标签页。」。
- **`Open YAML File` (save_modal L41)**：`YAML` 文件格式名，保留英文。译「打开 YAML 文件」。
- **`Looking for settings to import...` (settings/import/view L974)**：源使用 ASCII `...`，按项目惯例转为 `……`。译「正在查找可导入的设置……」。
- **`RedNotificationDot requires width/height` (red_notification_dot L17-18, `.expect`)**：内部 panic。`RedNotificationDot` 是 Rust 组件标识符，`width`/`height` 是样式字段名，均保留英文；叙述部分译「RedNotificationDot 需要 width/height」。
- **`Unable to fetch the latest changelog.` (changelog_section L32)**：`changelog` glossary 译「更新日志」。
- **`Read all changelogs` (changelog_section L368)**：跳转链接锚文本。译「阅读全部更新日志」。
- **`Send to Agent` (comment_list_view L955)**：将评论作为上下文发给 Agent。译「发送给 Agent」（保留 Agent）。
- **`View in GitHub` (comment_list_view L1084)**：菜单项。译「在 GitHub 中查看」（保留 GitHub）。
- **`To use Warp Drive, please create an account.` (warp_drive_page L142)**：与既有 `'To use AI features, please create an account.' → '要使用 AI 功能，请创建账户。'` 句型对齐。译「要使用 Warp Drive，请创建账户。」。
- **`Warp Drive is a workspace in your terminal where you can save Workflows, Notebooks, Prompts, and Environment Variables ...` (warp_drive_page L251)**：与既有 Warp Drive 描述风格对齐。`Workflows/Notebooks/Prompts/Environment Variables` 均使用 glossary 中文译名（工作流/笔记本/提示词/环境变量）。
- **`Toggle Case Sensitivity` / `Toggle Regex` (global_search L668, L678)**：与既有 `'Toggle case-sensitive search' → '切换大小写敏感搜索'` 风格对齐，此处更简洁（全局搜索图标 tooltip）。译「切换大小写敏感」/「切换正则表达式」。
- **`Delete theme` (theme_deletion_body L31)**：单条主题删除模态标题。译「删除主题」。
- **agent_slide 三条文案（onboarding）**：前两条是与链接拼接的 inline span，源含 leading/trailing 空格 — 译文严格保留空格方向；与现存翻译 `'and open the page manually.' → '并手动打开页面。'` 一致，加首尾空格。第三条（plan activated toast）译「套餐已成功激活。所有高级模型均已可用。」。
- **`Sync conversations to cloud` / 描述 (oz_launch L174-175)**：OpenWarp 启动模态中的 checkbox label + description。`Agent conversations` 译「Agent 会话」（沿用既有 `Agent conversations are only stored locally on your machine, ...' → 'Agent 会话仅存储在您本机，...'`）。

## Glossary delta

无新增术语。`term_count` 保持 95。
