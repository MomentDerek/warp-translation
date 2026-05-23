# Translate next auto_ui new entries — batch 60 entries 11 (Strategy: finish 21 auto_ui-new leaves + expand into 22 code/footer.rs LSP labels + 21 notebooks/editor/view.rs a11y action labels = 64 entries; auto_ui-new hotspot zeroed)

## Goal

清扫 **3 个文件群组共 64 条**，覆盖 **23 个文件**：

1. **21 条** — 剩余 **全部 21 个 auto_ui-new 单条叶节点**，自此 auto_ui-new 队列彻底清零。
2. **22 条** — `app/src/code/footer.rs` LSP（语言服务器）管理 UI 标签（uncertain，但全部是真实 UI）。
3. **21 条** — `app/src/notebooks/editor/view.rs` 笔记本编辑器 a11y 动作描述（uncertain，全部是 `AccessibilityContent` 与 1 条 `.expect` panic）。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/code/footer.rs` | 22 | LSP/语言服务器管理：启用/安装/重启/停止服务器、Installing 占位符、语言支持不可用文案、`/update-tab-config` skill、用 Oz 修复配置等 |
| `app/src/notebooks/editor/view.rs` | 21 | a11y 动作标签：增/删/剪/粘整行 + 命令块切换/插入/复制 + 链接编辑/复制/打开 + 工具栏（查找/字符调色板/嵌入对象） + 1 条 `.expect` panic（"Just checked above"） |
| `app/src/util/tooltips.rs` | 1 | 秘密信息工具提示尾注（`*` 前缀） |
| `crates/onboarding/src/slides/third_party_slide.rs` | 1 | 第三方设置卡片标题（CLI agent toolbar） |
| `app/src/terminal/input/conversations/view.rs` | 1 | inline menu tab 标题（当前目录） |
| `app/src/terminal/shared_session/role_change_modal/sharer_grant_body.rs` | 1 | 角色变更模态 toggle（不再显示。） |
| `app/src/workspace/header_toolbar_editor.rs` | 1 | 头部工具栏编辑器标题 |
| `app/src/terminal/input/models/view.rs` | 1 | 模型选择器 tab 标题（"Full Terminal Use"） |
| `app/src/view_components/find.rs` | 1 | 查找工具栏 tooltip（在选中命令块中查找） |
| `crates/onboarding/examples/callout.rs` | 1 | onboarding callout 示例标题（示例文件，沿用 batch-7 examples/ 翻译惯例） |
| `app/src/workspace/view/build_plan_migration_modal.rs` | 1 | 构建套餐迁移错误模态 |
| `app/src/workspace/native_modal.rs` | 1 | `.expect` panic（模态按钮鼠标状态） |
| `app/src/terminal/input/profiles/search_item.rs` | 1 | profile 搜索项 footer（管理 Profile） |
| `app/src/tab_configs/session_config.rs` | 1 | worktree 分支名参数描述 |
| `crates/ui_components/src/lightbox.rs` | 1 | 灯箱空状态（无图片） |
| `app/src/terminal/shared_session/share_modal/body.rs` | 1 | 分享范围 radio label |
| `app/src/terminal/shared_session/sharer/network.rs` | 1 | 会话分享日额度限制 |
| `app/src/workflows/local_workflows.rs` | 1 | 调试工作流描述（dogfood only） |
| `crates/editor/src/render/element/paragraph.rs` | 1 | 段落块占位符（含 `'/'` → `『/』` 转换） |
| `app/src/workspace/view/crash_recovery.rs` | 1 | 崩溃恢复横幅描述（Xwayland / fractional scaling） |
| `app/src/workspace/view/vertical_tabs.rs` | 1 | 垂直标签栏工具提示（视图选项） |
| `crates/warpui_core/src/core/app.rs` | 1 | 视图树调试器窗口标题 |
| `app/src/workspace/home.rs` | 1 | Warp on Web 主页标题 |

继 batch-10 之后，`translated` 2220 → 2284，`new` 4462 → 4398，`fuzzy` 保持 52。**auto_ui-new 余量 21 → 0，热点彻底清零。**

## What I already know

- 当前 `strings.json` 统计（应用前）：`entry_count=6734`, `translated=2220`, `new=4462`, `fuzzy=52`。
- glossary 现有 95 条；本批沿用既有术语：`Warp` / `Warp on Web` / `Oz` / `Agent` / `MCP` / `Markdown` / `keybinding → 快捷键` / `LSP / language server → 语言服务器`（参照既有 `Restart server → 重启服务器`、`Show find bar in code review → 在代码审查中显示查找栏`、`Open view tree debugger → 打开视图树调试器`、`Manage profiles` 沿用既有 `Manage profile → 管理 Profile` 风格）/ `block → 命令块` / `worktree → worktree（保留英文）` / `profile → Profile（Warp 品牌词，保留）` / `xwayland → Xwayland`（OS 术语）/ `fractional scaling → 分数缩放` / `dogfood → 内部测试`。无新增术语，`term_count` 保持 95。
- **占位符**（10 条）：
  - `{}`（code/footer L373 `Enable {}`、L660 `Install {}`、L1618 `Installing {}...`、L1600、notebook view L3227 `Insert {} block`、L3152 `Open link: {}`、L3158 `Secondary click on {}`）— 位置占位符
  - `{root_name}`（code/footer L1525、L1664）— 命名占位符
  - `{code_block_type}`（notebook view L3261）— 命名占位符
  
  无 strftime。
- **`Installing {}...` (footer L1618)**：源用 ASCII `...`，按项目惯例转 `……`。译「正在安装 {}……」。
- **`Type text or Markdown, or '/' to insert content` (paragraph.rs L15)**：源含单引号包裹的 `'/'`。按项目惯例 `'…'` → `『…』`。译「键入文本或 Markdown，或输入 『/』 以插入内容」。
- **`.expect` 内部诊断 panic 串（2 条）**：
  - `Modal button mouse state should be set` (workspace/native_modal L163) — 模态按钮 mouse_state 缺失断言。
  - `Just checked above` (notebooks/editor/view L2103) — 紧邻 `self.hovered_block.is_some()` 守卫后的 `.expect()`。
  
  沿用 batch-7/8/9/10 panic 翻译惯例：叙述部分译中文，标识符如 `mouse state` 在中文里译「鼠标状态」（属常用词，可译），保留 panic 信息可读性。
- **`Don't show again.` (sharer_grant_body L149) vs 既有 `Don't show again` (batch-7) → 不再显示**：本条多个句号。沿用既有，译「不再显示。」（保留尾点）。注意 batch-10 的 `Don't show me again → 不再向我显示`（含 "me"）是另一句。
- **`Oops, something went wrong; your team data could not be found.` (build_plan_migration_modal L792)**：与既有 `'Oops, something went wrong; your team's data could not be found.' → '糟糕，出错了；未能找到您团队的数据。'`（同义，差所有格 `team's`）对齐。译「糟糕，出错了；未能找到您团队的数据。」。
- **`Welcome to Warp on Web` (workspace/home L11)**：与既有 `Welcome to terminal mode → 欢迎使用终端模式` 同模式。`Warp on Web` 保留品牌。译「欢迎使用 Warp on Web」。
- **`View Tree Debugger` (warpui_core/core/app L4250)**：dev 工具窗口标题。既有 `Open view tree debugger → 打开视图树调试器`，本条为窗口标题，去动词。译「视图树调试器」。
- **`Use Oz to update this config` (code/footer L1736)**：UI 错误恢复提示，按钮+解释合一。与既有 `Fix with Oz → 用 Oz 修复` 风格对齐。译「用 Oz 更新此配置」。
- **`/update-tab-config skill` (code/footer L319/L321)**：`/update-tab-config` 是斜杠命令字面值，保留英文。`skill` 译「技能」（与既有 `Enable built-in feedback skill → 启用内置反馈技能` 一致）。
- **`Language support is unavailable for {root_name}` 等 (code/footer L1525/L1594/L1600/L1606/L1664)**：与既有长文 `Would you like to enable available language support for this codebase? ... → 您是否希望为此代码库启用可用的语言支持？...` 中的 `language support → 语言支持` 一致。`Language server → 语言服务器`（与 `Restart server → 重启服务器` 通用 server → 服务器）一致。
- **`No images` (lightbox L167)**：灯箱无图片空状态。译「没有图片」（与既有 `'No matching themes!' → '未找到匹配的主题！'` 风格略不同 — 这里更通用，用「没有」而非「未找到」更贴 lightbox 语境；不强迫一致）。
- **`We detected a crash ... fractional scaling.` (crash_recovery L19)**：长警告横幅。`Xwayland` 是 OS 显示协议名（专有词），保留。`fractional scaling` 译「分数缩放」（Linux/Wayland 通用术语）。
- **`Shows the diagnostic log of shell commands run by prompt context chips (dogfood only)` (local_workflows L222)**：内部 dogfood 工作流描述。`dogfood only` 译「（仅限内部测试）」。`prompt context chips` 译「提示词上下文 chip」（与既有 `context_chips` 命名空间用语一致；`chip` 在 Warp UI 是专有 UI 元素，保留）。
- **`Just checked above` (notebooks/editor/view L2103, `.expect`)**：注释式 panic，断言一行之上的 `is_some()` 守卫成立。译「上方刚刚检查过」（直译式 panic，与 `.expect()` 风格匹配）。
- **`Insert {} block` (notebook view L3227)**：a11y 动作。`{}` 是 block 类型显示名（如 `code`、`task`）。译「插入 {} 命令块」（与既有 `Insert block → 插入命令块` 一致）。
- **`Copy Link` / `Edit Link` (notebook view L3148/L3143)**：与既有 `Copy link → 复制链接` 一致（大小写差异不分译）。译「复制链接」/「编辑链接」。
- **`Delete line left` / `Delete line right` / `Cut line left` / `Cut line right`**：与既有 `Cut all left → 剪切左侧所有内容` / `Delete all right → 删除右侧所有内容` / `Cut word left → 剪切左侧单词` 同结构。`line` 译「整行」。译「删除左侧整行」 / 「删除右侧整行」 / 「剪切左侧整行」 / 「剪切右侧整行」。
- **`De-select command` (notebook view L3253)**：与既有 `De-select shell commands → 取消选中 shell 命令` 同动词。译「取消选中命令」。
- **`Switch from selecting commands to selecting text` (notebook view L3254)**：`De-select command` 的 help 文。直译。译「从选中命令切换到选中文本」。
- **`Open block-insertion menu` / `Open embedded object search menu` (notebook view L3215/L3221)**：a11y 动作描述。译「打开命令块插入菜单」/「打开嵌入对象搜索菜单」。
- **`Show character palette` (notebook view L3206)**：macOS 系统字符面板入口。译「显示字符面板」（与既有 `Show find bar` → 显示查找栏一致）。
- **`Toggle task list` (notebook view L3270)**：a11y 动作。`task list` 是 Markdown 任务列表。译「切换任务列表」（与既有 `Toggle comment → 切换注释` 等 Toggle 模式一致）。
- **`Secondary click on {}` (notebook view L3158)**：a11y fallback for right-click on link without secondary action. `{}` 是链接 url（`**link` 是 Display impl 输出）。译「在 {} 上右键单击」（`Secondary click` = mac 上的「副键单击」，但简化为更通用的「右键单击」更贴近大众语义）。
- **`Open link: {}` (notebook view L3152)**：a11y 动作。译「打开链接：{}」。
- **`Open folder` (notebook view L2506)**：a11y 动作。译「打开文件夹」。
- **`Link copied` (notebook view L2837)**：toast。与既有 `Link copied. → 链接已复制。` 一致（差句号）。译「链接已复制」。
- **`Show find bar` (notebook view L3211)**：a11y 动作。与既有 `Show find bar in code review → 在代码审查中显示查找栏` 一致。译「显示查找栏」。
- **`Change code block language to {code_block_type}` (notebook view L3261)**：a11y 动作。`{code_block_type}` 是编程语言名。译「将代码块语言切换为 {code_block_type}」。
- **`Copy code block` (notebook view L3265)**：a11y 动作。译「复制代码块」。
- **`Edit toolbar` (header_toolbar_editor L20)**：模态标题。译「编辑工具栏」。
- **`Manage profiles` (terminal/input/profiles/search_item L17)**：profile 列表 footer label。`Profile` 保留品牌词，与既有 `Switch the active execution profile → 切换当前执行配置` 等用法对应但本条更短。译「管理 Profile」（与 batch-10 `Profile 编辑器` / `Manage profile`-类风格统一）。
- **`Full Terminal Use` (terminal/input/models/view L85)**：模型分类标签 — 支持「完整终端使用」（即可调用工具、文件 IO）的模型。译「完整终端能力」（更易理解，传达 capability 的语义）。
- **`Current Directory` (terminal/input/conversations/view L45)**：inline menu tab。译「当前目录」。
- **`Find in selected block` (view_components/find L50)**：tooltip。与既有 `Find in Notebook → 在笔记本中查找` / `Find in Terminal → 在终端中查找` 一致。译「在选中命令块中查找」。
- **`Share from selected block and onwards` (share_modal/body L216)**：分享范围 radio。译「从选中命令块开始分享」。
- **`Session sharing usage exceeded for the day. Please try again later.` (sharer/network L1245)**：会话分享日额度限制。译「今日会话分享用量已用完。请稍后重试。」。
- **`*Secrets are not sent to Warp's server.` (util/tooltips L206)**：含 `*` 前缀的尾注。`Warp's server` 保留撇号语义。译「*机密信息不会发送至 Warp 服务器。」。
- **`CLI agent toolbar` (onboarding/third_party_slide L180)**：toggle card 标题。与既有 `Edit CLI agent toolbelt → 编辑 CLI Agent 工具集` 一致 → `CLI Agent` 保留品牌。译「CLI Agent 工具栏」。
- **`Meet your Warp input` (onboarding/examples/callout L84)**：onboarding callout 示例标题。`Meet your X` 是介绍式英语，译「认识您的 Warp 输入」（与示例上下文搭配自然）。
- **`New worktree branch name` (tab_configs/session_config L134)**：worktree 参数描述。与既有 `New worktree config → 新建 worktree 配置` 一致 → `worktree` 保留英文。译「新建 worktree 分支名」。
- **`View options` (vertical_tabs L1373)**：tooltip。译「视图选项」。

## Scope by file

### app/src/util/tooltips.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV128JN2JRX0BYNZV0B9S` | 206 | `*Secrets are not sent to Warp's server.` | `*机密信息不会发送至 Warp 服务器。` |

### crates/onboarding/src/slides/third_party_slide.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129M97YSH8GF78FRBAZ` | 180 | `CLI agent toolbar` | `CLI Agent 工具栏` |

### app/src/terminal/input/conversations/view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12AS0865E39T56FM7P4` | 45 | `Current Directory` | `当前目录` |

### app/src/terminal/shared_session/role_change_modal/sharer_grant_body.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12B71JN4J8FYR2SAQMM` | 149 | `Don't show again.` | `不再显示。` |

### app/src/workspace/header_toolbar_editor.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BBZABG9EX7CJ1G757` | 20 | `Edit toolbar` | `编辑工具栏` |

### app/src/terminal/input/models/view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CCJQ8ZWXH2XX6YDXH` | 85 | `Full Terminal Use` | `完整终端能力` |

### app/src/view_components/find.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CW7VPTP38A0BJJN80` | 50 | `Find in selected block` | `在选中命令块中查找` |

### crates/onboarding/examples/callout.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DB8AVGNF99AKWQZNZ` | 84 | `Meet your Warp input` | `认识您的 Warp 输入` |

### app/src/workspace/view/build_plan_migration_modal.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DBGSZW0210MK25N47` | 792 | `Oops, something went wrong; your team data could not be found.` | `糟糕，出错了；未能找到您团队的数据。` |

### app/src/workspace/native_modal.rs (1) — .expect panic

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DR2R2QYFB7EFQWFCD` | 163 | `Modal button mouse state should be set` | `模态按钮应已设置鼠标状态` |

### app/src/terminal/input/profiles/search_item.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DV0KBS22B01725PKC` | 17 | `Manage profiles` | `管理 Profile` |

### app/src/tab_configs/session_config.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DY82VRSRV726VYXKT` | 134 | `New worktree branch name` | `新建 worktree 分支名` |

### crates/ui_components/src/lightbox.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DYXPJJM484CRV3TZ4` | 167 | `No images` | `没有图片` |

### app/src/terminal/shared_session/share_modal/body.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FT2BFZVMW8NACFB8B` | 216 | `Share from selected block and onwards` | `从选中命令块开始分享` |

### app/src/terminal/shared_session/sharer/network.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FVH966QDG3WH3YCQQ` | 1245 | `Session sharing usage exceeded for the day. Please try again later.` | `今日会话分享用量已用完。请稍后重试。` |

### app/src/workflows/local_workflows.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GZVF44C24JS1S2MQ2` | 222 | `Shows the diagnostic log of shell commands run by prompt context chips (dogfood only)` | `显示提示词上下文 chip 运行的 shell 命令诊断日志（仅限内部测试）` |

### crates/editor/src/render/element/paragraph.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H2YXM451D0MCNZS56` | 15 | `Type text or Markdown, or '/' to insert content` | `键入文本或 Markdown，或输入 『/』 以插入内容` |

### app/src/workspace/view/crash_recovery.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H3PHF5THXE9BRGJ3R` | 19 | `We detected a crash during application startup, and adjusted your settings to use Xwayland for windowing. This can result in blurry text if you are using fractional scaling.` | `我们检测到应用启动时发生了崩溃，已调整您的设置改用 Xwayland 进行窗口管理。如果您正在使用分数缩放，这可能导致文本模糊。` |

### app/src/workspace/view/vertical_tabs.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H7YBWXR56KZ4Q64HV` | 1373 | `View options` | `视图选项` |

### crates/warpui_core/src/core/app.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HJKGBMP0EY7RRC3SH` | 4250 | `View Tree Debugger` | `视图树调试器` |

### app/src/workspace/home.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HQZAW4PS4Z87DVANT` | 11 | `Welcome to Warp on Web` | `欢迎使用 Warp on Web` |

### app/src/code/footer.rs (22)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BNGHWDFE4B49YAD7K` | 684 | `Enable servers` | `启用服务器` |
| `01KQXQV12BRZ68XRATEWWFGEQC` | 321 | `Enable AI to use the /update-tab-config skill` | `允许 AI 使用 /update-tab-config 技能` |
| `01KQXQV12BSHTS1PH6M74KY7PV` | 373 | `Enable {}` | `启用 {}` |
| `01KQXQV12C61KWYKWMEGAS3922` | 1618 | `Installing {}...` | `正在安装 {}……` |
| `01KQXQV12CDC500EDAPPTJE31N` | 682 | `Install servers` | `安装服务器` |
| `01KQXQV12CGHH5BNS3055Y45AQ` | 660 | `Install {}` | `安装 {}` |
| `01KQXQV12D0QZ2EYGD6P5STFBV` | 1664 | `Language support is unavailable for {root_name}` | `{root_name} 没有可用的语言支持` |
| `01KQXQV12D38BV4S4CG5WZAY0V` | 1375 | `Manage servers` | `管理服务器` |
| `01KQXQV12DB2FPQTKNDX2NM1KH` | 1600 | `Language support is not currently enabled for {}` | `{} 当前未启用语言支持` |
| `01KQXQV12DG4T2AQB4D9YDJB5Z` | 1606 | `Language server is unavailable for this codebase` | `此代码库没有可用的语言服务器` |
| `01KQXQV12DJYRT6000GJKNW1B5` | 1525 | `Language support is not currently enabled for {root_name}` | `{root_name} 当前未启用语言支持` |
| `01KQXQV12DP7BDAZGYY0DS8JFZ` | 1594 | `Language support is unavailable for this file type` | `此文件类型没有可用的语言支持` |
| `01KQXQV12E1BWXJJ6S64NPG107` | 1292 | `Restart all servers` | `重启所有服务器` |
| `01KQXQV12EH3BY4XWTVSJ3KA1D` | 1179 | `Open logs` | `打开日志` |
| `01KQXQV12ENYZHN0VMM2MJ464F` | 319 | `Open agent input with the /update-tab-config skill` | `使用 /update-tab-config 技能打开 Agent 输入` |
| `01KQXQV12EYWK584GRN3X0SHTP` | 1268 | `Remove server` | `移除服务器` |
| `01KQXQV12G3GMVHPJN979CKVY3` | 1350 | `Start all stopped servers` | `启动所有已停止的服务器` |
| `01KQXQV12GCY62C8BAXYDP3JRQ` | 1320 | `Stop all servers` | `停止所有服务器` |
| `01KQXQV12GEKM8K6VWV6VYM8V7` | 1224 | `Stop server` | `停止服务器` |
| `01KQXQV12GRJNJ102A44ZQXPS5` | 1352 | `Start all servers` | `启动所有服务器` |
| `01KQXQV12GRRRCHFSXKVP44T83` | 1246 | `Start server` | `启动服务器` |
| `01KQXQV12HWCEMYF6TFGDZ51DN` | 1736 | `Use Oz to update this config` | `用 Oz 更新此配置` |

### app/src/notebooks/editor/view.rs (21)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129YS0P2BPCBK4K6EDH` | 3261 | `Change code block language to {code_block_type}` | `将代码块语言切换为 {code_block_type}` |
| `01KQXQV12A1ZMWYR17S9FY6RHA` | 3168 | `Delete line left` | `删除左侧整行` |
| `01KQXQV12A6CVNCN3S0XFG5QF8` | 3192 | `Cut line left` | `剪切左侧整行` |
| `01KQXQV12AE1P84YPW3JHEGX81` | 3265 | `Copy code block` | `复制代码块` |
| `01KQXQV12AG0HQ8QD6EVSRJ2W2` | 3253 | `De-select command` | `取消选中命令` |
| `01KQXQV12ANKTQQWEE623CM7D3` | 3148 | `Copy Link` | `复制链接` |
| `01KQXQV12ARM95N3SDAGGFV77A` | 3174 | `Delete line right` | `删除右侧整行` |
| `01KQXQV12AX4FC87Q5XZ8KQWB9` | 3195 | `Cut line right` | `剪切右侧整行` |
| `01KQXQV12BZV7PTD470RXQY5Z5` | 3143 | `Edit Link` | `编辑链接` |
| `01KQXQV12C1N173BJ4TA04Z4HB` | 3227 | `Insert {} block` | `插入 {} 命令块` |
| `01KQXQV12D219137720CXV0ZB9` | 2103 | `Just checked above` | `上方刚刚检查过` |
| `01KQXQV12DCJ1V9QZ39WJE5F0M` | 2837 | `Link copied` | `链接已复制` |
| `01KQXQV12E5H16FRVFP3J0NX5M` | 3215 | `Open block-insertion menu` | `打开命令块插入菜单` |
| `01KQXQV12E77KCFF82TZ3HFZ06` | 3221 | `Open embedded object search menu` | `打开嵌入对象搜索菜单` |
| `01KQXQV12EA2QXCD68T69GA7T1` | 2506 | `Open folder` | `打开文件夹` |
| `01KQXQV12EB92XBTVY6BQGMASY` | 3152 | `Open link: {}` | `打开链接：{}` |
| `01KQXQV12F26VTYD04PPVQC8XZ` | 3211 | `Show find bar` | `显示查找栏` |
| `01KQXQV12FPPYRQ9VY2CYZDFS6` | 3206 | `Show character palette` | `显示字符面板` |
| `01KQXQV12FSEEQ7DRXK027SBWB` | 3158 | `Secondary click on {}` | `在 {} 上右键单击` |
| `01KQXQV12GRHY9YSZBKVFC8V0Y` | 3254 | `Switch from selecting commands to selecting text` | `从选中命令切换到选中文本` |
| `01KQXQV12HK69JYGVCPKDSM4C9` | 3270 | `Toggle task list` | `切换任务列表` |

## Decisions / Anomalies

- **本批从 `uncertain` verdict 中扩展取词** —— 此前批次主要清扫 `auto_ui` verdict 条目；本批 auto_ui-new 仅余 21 条单条叶节点，已全部取完。剩余 4441 条 `status=new` 全部为 `uncertain` verdict。需要按文件抽样判定 user-facing。本批取 `code/footer.rs`（22 条全部 LSP 管理 UI，纯按钮/工具提示）和 `notebooks/editor/view.rs`（21 条全部为 `AccessibilityContent::new(...)` 与一条紧邻的 `.expect` panic）。两文件抽查结论：100% user-facing UI，无 telemetry / 内部 enum 名 / debug-only 字符串混入。
- **`auto_ui-new 队列清零标志**：本批后所有 `status=new + verdict=auto_ui` 条目全部翻转为 `translated`。后续批次须从 `uncertain` 集合中按文件分簇取词。
- **panic 串处置**：2 条 `.expect` panic（`Modal button mouse state should be set` / `Just checked above`）沿用 batch-7/8/9/10 panic 翻译惯例，叙述译中文，无标识符需保留。
- **`'/' → 『/』` 单引号转换**：paragraph.rs L15 含 ASCII 单引号包裹的字符 `'/'`，按项目惯例 `'…'` → `『…』`。
- **`...` → `……` 转换**：code/footer.rs L1618 `Installing {}...` 含 ASCII ellipsis，按项目惯例转 `……`。
- **`Manage profiles` (terminal/input/profiles/search_item L17)**：`profiles` 在此处指 terminal session profile（终端 Profile 配置，与 ai/execution_profiles/Profile 同为品牌词），保留 Profile 大写。译「管理 Profile」。
- **`Full Terminal Use` (terminal/input/models/view L85)**：来自 `InlineModelSelectorTab::FullTerminalUse`，是 AI 模型按「完整终端能力」分类（指可调用 shell tools 的模型）。译「完整终端能力」（avoid 字面「完整终端使用」，capability 含义更清晰）。
- **`Don't show again.` vs `Don't show again`**：sharer_grant_body L149 末尾有句号，沿用既有 `Don't show again → 不再显示`，加句号。不与 batch-10 `Don't show me again → 不再向我显示`（含 "me"）合并。
- **`Open agent input with the /update-tab-config skill` (code/footer L319)**：`/update-tab-config` 是 Warp 斜杠命令字面，**保留**。`Agent` 大写保留（品牌）。译「使用 /update-tab-config 技能打开 Agent 输入」。
- **`Enable AI to use the /update-tab-config skill` (code/footer L321)**：与上同源（toggle 状态切换）。译「允许 AI 使用 /update-tab-config 技能」。
- **`Language support is unavailable for {root_name}` 等 5 条**：5 条同类语言支持/服务器不可用文案，统一按「{name}/此类型 + 状态描述」语序排版。Chinese 中宾语前置自然。
- **`We detected a crash during application startup ... fractional scaling.` (crash_recovery L19)**：Linux Wayland 崩溃恢复横幅。`Xwayland`（X-on-Wayland 兼容层）保留；`fractional scaling`（分数缩放）译中文。译文使用「检测到 ... 已调整 ... 可能导致」陈述链。
- **`prompt context chips (dogfood only)` (local_workflows L222)**：`prompt context chips` 是 Warp 内部 prompt 输入栏上方的「上下文 chip」UI 元素（小芯片）；`chip` 保留英文，与代码模块名一致。`dogfood only` 译「（仅限内部测试）」（符合中文括号注解风格）。
- **`Insert {} block` (notebook view L3227)**：`{}` 是 block 类型 label（如 "code"/"task"）。中文「插入 {} 命令块」中 `{}` 作为定语前置，自然。
- **`Secondary click on {}` (notebook view L3158)**：macOS 的 "Secondary click"（mouse 副键）= 大多语境下的「右键」。`{}` 是链接 URL Display 输出，可能含特殊字符；保留位置。译「在 {} 上右键单击」。
- **`onboarding/examples/callout.rs (Meet your Warp input)`**：示例文件（cargo example），不在生产应用中渲染。沿用 batch-7 `crates/ui_components/examples/library.rs` 翻译惯例 — **照常翻译**（既有先例在 batch-7 翻译了 8 条 examples/library.rs 标签）。

## Glossary delta

无新增术语。`term_count` 保持 95。

新增 *用法*（沿用既有词条不新增 term）：
- `language server` → `语言服务器`（与 `Restart server → 重启服务器` 通用 server → 服务器 一致）
- `language support` → `语言支持`（与既有长文中既有用法一致）
- `fractional scaling` → `分数缩放`
- `Xwayland` → `Xwayland`（OS 协议名，保留）
- `chip` → `chip`（保留英文，与代码命名空间一致）
- `dogfood (only)` → `（仅限）内部测试`
- `task list` → `任务列表`（Markdown 标准术语）
- `character palette` → `字符面板`（macOS 系统术语）
