# Translate next auto_ui new entries — batch 60 entries 6 (Strategy: drive/auth/workspace + warpui crate + billing/settings sweep)

## Goal

清扫 **20 个 auto_ui-new 热点文件** 共 **60 条**。覆盖：drive 子树（清空回收站 / 命名对话框 / 共享对话框 / 抢编辑权）+ workspace 二次确认对话框集群（关闭会话 / 倒带 / 删除对话）+ 会话列表视图 + auth 子树（登录页隐私 / SSO 关联 / 多用户覆盖警告）+ billing_and_usage（团队合计 / 成员行）+ 隐私正则添加模态 + working_directory 设置 + notebooks 文件视图 + warpui crate 渲染层（wgpu 调试标签 + macOS 标准菜单项）。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/auth/auth_override_warning_body.rs` | 3 | 新登录覆盖警告（描述 + 导出/导入提示） |
| `app/src/auth/login_slide.rs` | 3 | 登录页隐私链接前导 + 浏览器未启动提示尾部 |
| `app/src/auth/needs_sso_link_view.rs` | 3 | SSO 关联视图（按钮 + 标题 + 提示） |
| `app/src/cloud_object/grab_edit_access_modal.rs` | 3 | 抢编辑权对话框（CTA + 警告 + 标签） |
| `app/src/drive/cloud_object_naming_dialog.rs` | 3 | Drive 对象命名占位符（notebook / folder / collection） |
| `app/src/drive/empty_trash_confirmation_dialog.rs` | 3 | 清空回收站确认（标题 + 不可撤销 + 确认按钮） |
| `app/src/drive/sharing/dialog/mod.rs` | 4 | Drive 共享对话框（无访问 / 谁有访问 / 只邀请成员 / 链接成员） |
| `app/src/notebooks/file/mod.rs` | 3 | notebook 文件视图（聚焦终端输入 / 重载 / 刷新） |
| `app/src/settings_view/billing_and_usage/billing_cycle_usage_rows.rs` | 3 | 用量行（其他成员 / 服务账号提示 / 您的用量） |
| `app/src/settings_view/billing_and_usage/billing_cycle_usage_team_totals.rs` | 3 | 团队合计（整体用量 / 本地代理用量 / 限额行） |
| `app/src/settings_view/features/working_directory.rs` | 3 | 工作目录设置（新建窗口 / 拆分窗格 / 目录路径占位符） |
| `app/src/settings_view/privacy/add_regex_modal.rs` | 3 | 添加正则模态（名称可选 / 正则模式 / 无效正则） |
| `app/src/workspace/close_session_confirmation_dialog.rs` | 3 | 关闭共享会话二次确认 |
| `app/src/workspace/delete_conversation_confirmation_dialog.rs` | 3 | 删除对话二次确认 |
| `app/src/workspace/rewind_confirmation_dialog.rs` | 3 | 倒带二次确认（含 shell-edits 不受影响提示） |
| `app/src/workspace/view/conversation_list/view.rs` | 3 | 对话列表（查看全部 / Fork 至窗格 / Fork 至标签页） |
| `crates/warpui/src/platform/mac/menus.rs` | 3 | macOS 标准菜单项（Show All / Bring All to Front）+ 1 条 doc-comment 假阳性 |
| `crates/warpui/src/rendering/wgpu/renderer.rs` | 3 | wgpu 调试标签（Command encoder / Frame capture buffer / encoder） |
| `crates/warpui/src/rendering/wgpu/resources/quad.rs` | 2 | wgpu 调试标签（Quad Index/Vertex Buffer） |
| `crates/warpui/src/rendering/wgpu/resources/uniforms.rs` | 3 | wgpu 调试标签（Bind Group Layout / buffer / Bind Group） |

20 个文件中：**18 个**完整清零至 auto_ui-new=0；**2 个文件**因含跨文件复用条目（`Don't show again.` / `New tab`）残留 1 条，将随后续 batch 一并清扫：
- `app/src/workspace/close_session_confirmation_dialog.rs` 残 1 条 (`Don't show again.` 还出现在 `terminal/shared_session/role_change_modal/sharer_grant_body.rs` 和 `workspace/native_modal.rs`)
- `app/src/settings_view/features/working_directory.rs` 残 1 条 (`New tab` 还出现在 `pane_group/pane/welcome_view.rs` × 2 和 `tab_configs/session_config.rs`)

继 batch-5 之后，auto_ui-new 余量 321 → 261（-60）；`translated` 1920 → 1980，`new` 4762 → 4702。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=1920`, `new=4762`, `fuzzy=52`（auto_ui 321 / uncertain 4441）。
- glossary 现有 93 条；本批沿用既有术语（`Warp` / `Warp Drive` / `Markdown` / `SSO` / `Git` / `MCP` / `notebook→Notebook` / `folder→文件夹` / `collection→集合` / `pane→窗格` / `tab→标签页` / `block→命令块` / `agent→Agent` / `credit` / `shell` / `fork→派生` 等）。**新增 1 条**：`rewind → 倒带 (UI 动词，回退到先前状态)`。`term_count` 93 → 94。
- **占位符**：仅 `Delete '{}'?` 和 `Limit: {}` 各含一个 `{}` 位置占位符；其他无占位符；无 strftime。
- **wgpu 调试标签（8 条，crates/warpui/src/rendering/wgpu/*）**：均为 `wgpu::*Descriptor { label: Some("...") }` 形式，仅在 GPU 调试器（RenderDoc / wgpu validation）中显示，**非用户可见 UI**。处置：`target=null` + `status=translated` + `flags=[..., do_not_translate, wgpu_debug_label]`（沿用 IDENTITY_IDS 范式但用专属 flag 区分）。
- **mac/menus.rs L31 doc-comment 假阳性**：源 `' A mac-menu-specific map of key names to special characters used for the keyboard shortcuts'` 是 `///` doc 注释，被 `scan_macro_tokens` 误捕。处置：`target=null` + `flags=[..., do_not_translate, extractor_false_positive_doc_comment]`。
- **mac 标准菜单项（L198/L201）**：`Show All` / `Bring All to Front` 是 macOS Window/Application 菜单标准项，用户可见，须翻译。沿用 macOS 中文本地化惯例：`Show All → 显示全部`、`Bring All to Front → 全部窗口前置`。

## Scope by file

### app/src/auth/auth_override_warning_body.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DYHB1JYEZY64PBG3W` | 31 | `It looks like you logged into a Warp account through a web browser. If you continue, any personal Warp drive objects and preferences from this anonymous session with be permanently deleted.` | `检测到您已通过浏览器登录 Warp 账户。如果继续，此匿名会话中的所有个人 Warp Drive 对象和偏好设置都将被永久删除。` |
| `01KQXQV12BX5F2BHDM3YY4148Z` | 36 | `Export your data` | `导出您的数据` |
| `01KQXQV127223FBVARD86DQQMT` | 37 | ` to import later.` | ` 以便后续导入。`（前置空格保留以维持链接片段渲染间隔；句末英文句号 → 全角中文句号） |

### app/src/auth/login_slide.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CY723VVKF8RS22MPG` | 469 | `If you'd like to opt out of analytics, you can adjust your ` | `如需选择退出数据分析，您可以调整您的 `（尾部空格保留以维持链接片段渲染间隔） |
| `01KQXQV11XDPA63Q5CES42MENF` | 711 | ` and open` | ` 并手动打开`（前置空格保留；将 `manually` 提前以贴合中文「手动打开...」语序） |
| `01KQXQV12JKQ2308RBVNNW8D46` | 720 | `the page manually.` | `该页面。`（`manually` 已并入 L711） |

### app/src/auth/needs_sso_link_view.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12D7WG3VZKSEVPM8C8Z` | 57 | `Link SSO` | `关联 SSO` |
| `01KQXQV12J4EM1HV0EQTA43XCY` | 78 | `Your organization has enabled SSO for your account` | `您所在的组织已为您的账户启用 SSO` |
| `01KQXQV12942ERGYGFHE8F2GDE` | 79 | `Click the button below to link your Warp account to your SSO provider.` | `点击下方按钮，将您的 Warp 账户关联到您的 SSO 提供商。` |

### app/src/cloud_object/grab_edit_access_modal.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12B6PN1T9QFPDV1KN8K` | 13 | `Edit anyway` | `仍然编辑` |
| `01KQXQV12CAXJWZR5Z2BPGE662` | 16 | `If you take edit controls, the current editor will be forced into view mode` | `如果您接管编辑权，当前编辑者将被强制切换到查看模式` |
| `01KQXQV12G03W29SRR7AK0PA72` | 17 | `This notebook is currently being edited` | `此 Notebook 正在被编辑` |

### app/src/drive/cloud_object_naming_dialog.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12D45F4FBCBHBMJDJ9R` | 35 | `Notebook name` | `Notebook 名称` |
| `01KQXQV12C0GTVH82SHJ1EJMTE` | 36 | `Folder name` | `文件夹名称` |
| `01KQXQV12AWFBFNRW28MS236MS` | 37 | `Collection name` | `集合名称` |

### app/src/drive/empty_trash_confirmation_dialog.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129A95591A60H6ZGYYY` | 19 | `Are you sure you want to empty the trash?` | `确定要清空回收站吗？` |
| `01KQXQV12G9P8C77RT5J7NADYY` | 20 | `This action cannot be undone.` | `此操作无法撤销。` |
| `01KQXQV12JAWWKWPEEXPX1Q3V1` | 21 | `Yes, empty trash` | `是，清空回收站` |

### app/src/drive/sharing/dialog/mod.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12D2RBHV39FWV7HTTKY` | 80 | `No access` | `无访问权限` |
| `01KQXQV12JADQ6Z191DXT389PS` | 1763 | `Who has access` | `谁有访问权限` |
| `01KQXQV12DRPMKAFQS2P2MFXXX` | 2182 | `Only invited teammates` | `仅限受邀的团队成员` |
| `01KQXQV12GX5M5KBJPVBYBDSBG` | 2188 | `Teammates with the link` | `拥有链接的团队成员` |

### app/src/notebooks/file/mod.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CVTCAW72890PSRYXP` | 222 | `Focus Terminal Input from File` | `从文件聚焦终端输入` |
| `01KQXQV12EKQ2PRFHVFXTQX10Q` | 229 | `Reload file` | `重新加载文件` |
| `01KQXQV12E11K8EKAE415X13NM` | 950 | `Refresh file` | `刷新文件` |

### app/src/settings_view/billing_and_usage/billing_cycle_usage_rows.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEQDT3RJHEPFPH6BN6KJ0` | 142 | `Other members` | `其他成员` |
| `01KS2GEQNVE139ZHZDKJ26W49T` | 354 | `This is an automated agent on your team.` | `这是您团队中的自动化 Agent。` |
| `01KS2GEQRA6MKG7EFGFEMMHWYY` | 666 | `Your usage` | `您的用量` |

### app/src/settings_view/billing_and_usage/billing_cycle_usage_team_totals.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEQE9F18FAJQCCM8PQSEC` | 66 | `Overall usage` | `整体用量` |
| `01KS2GEQBA0JJWTXZ5HB3HTC65` | 90 | `Local agent usage` | `本地 Agent 用量` |
| `01KS2GEQA89VHY1S55KCRVZHM6` | 244 | `Limit: {}` | `上限：{}` |

### app/src/settings_view/features/working_directory.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DT0NM0EKP3X6V9XPA` | 148 | `New window` | `新建窗口` |
| `01KQXQV12GPGPE6SA2436H22RC` | 162 | `Split pane` | `拆分窗格` |
| `01KQXQV12ATMXSBBHCHYPRYRNS` | 373 | `Directory path` | `目录路径` |

### app/src/settings_view/privacy/add_regex_modal.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DBHJ42PRG0YWPXKVT` | 193 | `Name (optional)` | `名称（可选）` |
| `01KQXQV12EBRY3AY2KXCAZRNDP` | 201 | `Regex pattern` | `正则表达式模式` |
| `01KQXQV12C25HBXT5WA7Z5Z5Q1` | 235 | `Invalid regex` | `无效的正则表达式` |

### app/src/workspace/close_session_confirmation_dialog.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129EYGQ2D4FJ8JY0YKW` | 109 | `Close session` | `关闭会话` |
| `01KQXQV129DYGPVTBHVF6RR4NW` | 134 | `Close session?` | `关闭会话？` |
| `01KQXQV12J3SV3CZESK93GN0VX` | 136 | `You are about to close a session that is currently being shared. Closing it will end sharing for everyone.` | `您即将关闭一个正在共享的会话。关闭后，所有参与者的共享都将终止。` |

### app/src/workspace/delete_conversation_confirmation_dialog.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12ATG9DV1DCXJ57S53D` | 106 | `Delete '{}'?` | `删除 '{}'？`（保留 ASCII 单引号 + `{}` 占位符 + 全角问号） |
| `01KQXQV12AC2RGSJTQ39THPP56` | 107 | `Delete conversation?` | `删除对话？` |
| `01KQXQV12GVBQZ9F6Q9TNKVEDT` | 112 | `This conversation will be permanently deleted. This action cannot be undone.` | `此对话将被永久删除。此操作无法撤销。` |

### app/src/workspace/rewind_confirmation_dialog.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E2JCG7BF6Q3JPVHC6` | 191 | `Rewinding does not affect files edited manually or via shell commands.` | `倒带操作不会影响通过手动编辑或 shell 命令修改的文件。` |
| `01KQXQV12E7BCH9C5P1RKMRXRC` | 202 | `Rewind` | `倒带` |
| `01KQXQV129GFC4A82CCE36854Y` | 204 | `Are you sure you want to rewind? This will restore your code and conversation to before this point, and cancel any commands the agent is currently running. A copy of the original conversation will be saved in your conversation history.` | `确定要倒带吗？此操作会将您的代码和对话恢复到此节点之前，并取消 Agent 当前正在运行的所有命令。原对话的副本将保存在您的对话历史中。` |

### app/src/workspace/view/conversation_list/view.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HA3S3G62QPXMTWWVF` | 56 | `View all` | `查看全部` |
| `01KQXQV12CN3TKVXJH7MSBJCXE` | 957 | `Fork in new pane` | `在新窗格中派生` |
| `01KQXQV12CNA9Q14EPDF9SCV36` | 965 | `Fork in new tab` | `在新标签页中派生` |

### crates/warpui/src/platform/mac/menus.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV10K08VKM1PTG55SSRGM` | 31 | ` A mac-menu-specific map of key names to special characters used for the keyboard shortcuts` | **doc-comment 假阳性**：`target=null` + `flags=[do_not_translate, extractor_false_positive_doc_comment]`，不写译文 |
| `01KQXQV12FC5SBSAXZ4GY98E09` | 198 | `Show All` | `显示全部` |
| `01KQXQV129YDKRM2XKH2AY5XPC` | 201 | `Bring All to Front` | `全部窗口前置` |

### crates/warpui/src/rendering/wgpu/renderer.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12AP6S38RJP1W8AKSY9` | 21 | `Command encoder` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12C8BKH2Q9W1GQD5YMY` | 203 | `Frame capture staging buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12CSGCKT3VYQ3HT8YC6` | 210 | `Frame capture encoder` | **wgpu 调试标签**：`target=null` + `do_not_translate` |

### crates/warpui/src/rendering/wgpu/resources/quad.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12EG44FXM3F1C25N0GX` | 40 | `Quad Index Buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12E35NPKXJ1SWMXXMR2` | 46 | `Quad Vertex Buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |

### crates/warpui/src/rendering/wgpu/resources/uniforms.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12EG48VSPTAX8RZ997G` | 17 | `Quad Uniforms Bind Group Layout` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12H6RT5M0NY1GBXSFYQ` | 33 | `Uniforms buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12H9WNMRS299SQ5FR7G` | 40 | `Uniforms Bind Group` | **wgpu 调试标签**：`target=null` + `do_not_translate` |

## Decisions / Anomalies

- **wgpu 调试标签（8 条）**：均为 `wgpu::Device::create_*` / `RenderPassDescriptor` 等的 `label: Some("...")` 参数，作用是为 GPU 调试器（RenderDoc、wgpu validation log、Metal Frame Capture）提供资源命名。这些字符串**不会出现在任何用户可见的 UI**。处置遵循 IDENTITY_IDS 范式：`target=null`、`status=translated`、`flags=[batch_flag, do_not_translate, wgpu_debug_label]`。新增 `wgpu_debug_label` flag 用以区分一般 do_not_translate（如品牌名、缩写）与开发者专用调试标签。
- **mac/menus.rs L31 doc-comment 假阳性**：被 `scan_macro_tokens` 在 `lazy_static!` 宏体内扫描到 `///` doc 注释，误判为 UI 字符串。处置沿用项目既有惯例：`target=null` + `flags=[batch_flag, do_not_translate, extractor_false_positive_doc_comment]`。
- **macOS 标准菜单项（mac/menus.rs L198/L201）**：`Show All` 和 `Bring All to Front` 是 macOS Application/Window 菜单的标准项。沿用 macOS 中文本地化惯例（Apple 官方 zh_CN 资源）：`Show All → 显示全部`、`Bring All to Front → 全部窗口前置`。
- **占位符（2 条）**：
  - `Delete '{}'?` (L106, delete_conversation_confirmation_dialog.rs)：保留 ASCII 单引号 + `{}` 字面 + 句末问号换为全角「？」。
  - `Limit: {}` (L244, billing_cycle_usage_team_totals.rs)：冒号换中文全角「：」+ `{}` 字面保留。
- **链接尾随/前导片段（auth_override_warning_body L37, login_slide L469/L711）**：源串带边界空格以维持视觉间隔（链接和文本之间）。译文保持相同方向的边界空格，遵循 `whitespace single-direction` 约束。
  - L37 ` to import later.` 译 ` 以便后续导入。`：前置空格保留；句末英文句号 → 中文句号。
  - L469 `If you'd like to opt out of analytics, you can adjust your ` 译 `如需选择退出数据分析，您可以调整您的 `：尾部空格保留。
  - L711/L720 跨 span 重排：源 `[copy the URL] and open\nthe page manually.` 是一个连贯短语「复制 URL 并手动打开页面」被链接+换行拆为三段。中文「手动打开...页面」语序与英文不同，因此将 `manually` 从 L720 提前合并到 L711：L711 ` and open` → ` 并手动打开`（前置空格保留，无尾部空格——满足 single-direction）；L720 `the page manually.` → `该页面。`。最终拼接：「[copy the URL] 并手动打开该页面。」语义流畅、空格 single-direction 合规。
- **`Don't show again.` / `New tab` 未纳入**：两条均跨多文件复用（前者还出现在 `sharer_grant_body.rs` / `native_modal.rs`，后者还出现在 `welcome_view.rs ×2` / `session_config.rs`），需与其姊妹文件同批清扫。本批保留它们为 new，导致两个目标文件 (close_session_confirmation_dialog.rs / working_directory.rs) 残留 1 条 auto_ui-new，但 20 个文件中其余 18 个完整清零。
- **品牌字面保留**：`Warp`、`Warp Drive`、`Notebook`（在 Drive 上下文作为产品对象类别 — `Notebook name` → `Notebook 名称`）、`SSO`、`Agent`、`Fork`（动词，在 Warp 对话/会话分叉语境为产品动作专有名）、`shell`（小写命令解释器名）。
- **`Fork in new pane` / `Fork in new tab`（对话列表，L957/L965）**：Warp UI 中 `Fork` 是产品动作（分叉对话历史以新建并行分支）。glossary 既有 `fork → 派生` 条目（do_not_translate=false），且既有翻译以「派生」为主（11 处译文里 8 处用「派生」/「分叉」、3 处保留 `Fork`）；本批沿用 glossary 主译「派生」：`Fork in new pane → 在新窗格中派生`、`Fork in new tab → 在新标签页中派生`。
- **`Rewind` (workspace/rewind_confirmation_dialog L202)**：Warp UI 中的「倒带」是回退到对话/代码先前节点的产品动作。译「倒带」简洁直观；不译「回退」是因为「回退」在 Git/Editor 语境已被 undo/revert 占用。
- **`Edit anyway` (grab_edit_access_modal L13)**：抢编辑权对话框 CTA，源「无论如何编辑」→ 译「仍然编辑」更简洁，符合 Warp 既有「Continue anyway」→「仍然继续」的惯例。
- **`Show All` / `Bring All to Front` (macOS 菜单)**：参考 Apple 官方简体中文本地化（macOS Sequoia / Sonoma）：`Show All` → `显示全部`、`Bring All to Front` → `全部窗口前置`。这两条是 Window 菜单的标准项，用户在中文 macOS 系统中已习惯此译法。
- **`Focus Terminal Input from File` (notebooks/file/mod.rs L222)**：EditableBinding 描述，从 notebook 的文件视图聚焦到终端输入。译「从文件聚焦终端输入」对应键位绑定名「notebookview:focus_terminal_input」。

## Glossary delta

新增 1 条术语，`term_count` 93 → 94：

- `rewind` → `倒带`：UI 动词，回退对话/代码到先前节点的产品动作，与 undo/revert 区分。

注：`fork` 已在 glossary 中（`fork → 派生`），本批沿用，无变更。
