# Translate next auto_ui new entries — batch 60 entries 7 (Strategy: wgpu render labels + onboarding callouts + UI examples + resource_center + theme_creator + context_chips + model_spec_scores + mcp_servers + app_icon + keybindings_page + customize_slide)

## Goal

清扫 **13 个 auto_ui-new 热点文件** 共 **60 条**，13 个文件全部清零。覆盖：crates/warpui wgpu 渲染层（image/glyph/rect 共 13 条调试标签）+ crates/ui_components/examples/library.rs（UI 库示例 8 条）+ crates/onboarding（callout/view 6 条 + customize_slide 3 条）+ app/src/settings（app_icon 5 条）+ app/src/resource_center（feature_section 5 条 + keybindings_page 4 条）+ app/src/themes/theme_creator_body（4 条）+ app/src/context_chips/display_chip（4 条）+ app/src/terminal/input/models/model_spec_scores（4 条）+ app/src/settings_view/mcp_servers/mod（4 条）。

跨文件外溢清零（副作用清扫）：
- `app/src/settings_view/appearance_page.rs` 同步清零 5 条（仅余 1 条非共享）。
- `app/src/terminal/profile_model_selector.rs` 同步清零 3 条（剩 6 条 → 留作下一批）。
- `app/src/workspace/view/right_panel.rs` 同步清零 1 条（剩 1 条非共享）。

| 文件 | 数量 | 说明 |
|---|---|---|
| `crates/warpui/src/rendering/wgpu/renderer/image.rs` | 5 | wgpu 调试标签（Shader / pipeline layout / render pipeline / instance buffer / texture） |
| `crates/warpui/src/rendering/wgpu/renderer/glyph.rs` | 4 | wgpu 调试标签（Shader / pipeline layout / Render pipeline / instance buffer） |
| `crates/warpui/src/rendering/wgpu/renderer/rect.rs` | 4 | wgpu 调试标签（Shader / pipeline layout / render pipeline / instance buffer） |
| `crates/ui_components/examples/library.rs` | 8 | UI 组件库示例标签（Dialog Title / Tooltip label / Primary or Secondary or Disabled × Default or Small） |
| `crates/onboarding/src/callout/view.rs` | 6 | onboarding 引导提示气泡标题/按钮 |
| `crates/onboarding/src/slides/customize_slide.rs` | 3 | onboarding 自定义页（Tab styling / Conversation history / Code review） |
| `app/src/settings/app_icon.rs` | 5 | 应用图标显示名（Classic 1/2/3 / Glass Sky / Warp 1） |
| `app/src/resource_center/section_views/feature_section.rs` | 5 | 资源中心分区（Getting Started / Maximize Warp / Advanced Setup / What's New? + 1 expect 诊断） |
| `app/src/resource_center/keybindings_page.rs` | 4 | 资源中心快捷键页（Input Editor / 跳转设置说明 / 切换面板提示 + 1 expect 诊断） |
| `app/src/themes/theme_creator_body.rs` | 4 | 主题创建器（Create theme / Select an image / Select a new image / Selecting image...） |
| `app/src/context_chips/display_chip.rs` | 4 | 上下文 chip 工具提示（Change git branch / Change working directory / View pull request / Working directory） |
| `app/src/terminal/input/models/model_spec_scores.rs` | 4 | 模型评分表（Model Specs 标题与描述 / Reasoning level 标题与描述） |
| `app/src/settings_view/mcp_servers/mod.rs` | 4 | MCP 服务器 Id 调试格式串（File-Based / Gallery / Templatable / Templatable Installation） |

继 batch-6 之后，auto_ui-new 余量 261 → 192（-60 主清扫，加上 5+3+1=9 条副作用外溢，净下降 60，文件全清零 13）；`translated` 1980 → 2040，`new` 4702 → 4642。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=1980`, `new=4702`, `fuzzy=52`。
- glossary 现有 94 条；本批沿用既有术语：`Warp` / `MCP` / `Agent` / `keybinding→快捷键` / `theme→主题` / `model→模型` / `workflow→工作流`。**新增 1 条**：`reasoning level → 推理强度`（AI 模型可控的「思考程度」滑杆，与 reasoning model 「推理模型」区分）。`term_count` 94 → 95。
- **占位符**：4 条 mcp_servers 条目含命名占位符（`{uuid}` × 3 / `{template_uuid}` × 1），均为格式化串，保留字面占位符。其他无占位符；无 strftime。
- **wgpu 调试标签（13 条，crates/warpui/src/rendering/wgpu/renderer/{image,glyph,rect}.rs）**：均为 `wgpu::*Descriptor { label: Some("...") }` 形式，仅在 GPU 调试器（RenderDoc / wgpu validation）中显示，**非用户可见 UI**。处置：`target=null` + `status=translated` + `flags=[..., do_not_translate, wgpu_debug_label]`。沿用 batch-6 同款处置。
- **`.expect` 内部诊断面板字符串（2 条）**：
  - `Expected valid mouse state`（feature_section.rs L280, `.expect`）
  - `Should have command bindings vector`（keybindings_page.rs L246, `.expect`）
  这两条是 Rust panic 时才会暴露的内部 invariant 消息。沿用既往 pr-post-sync-batch 翻译 panic 消息的惯例（如 `'API key header width handle should lock'` 已译为 `API 密钥表头宽度手柄应锁定`）。翻译为简洁中文 invariant 描述。
- **app_icon 显示名（5 条，settings/app_icon.rs）**：`Classic 1/2/3` 翻译为 `经典 1/2/3`；`Glass Sky` 译 `玻璃天空`（描述性主题名）；`Warp 1` 保留品牌+数字。这些是 macOS Dock 应用图标的可选样式名，用户在外观设置中可见。

## Scope by file

### crates/warpui/src/rendering/wgpu/renderer/image.rs (5)

| ID | Line | Source | Disposition |
|---|---|---|---|
| `01KQXQV12C9T9YCDNB9C09ANRQ` | 45 | `Image Shader` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12CYQBQT5J5XKXDDSHW` | 77 | `Image pipeline layout` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12C5PD6VQ2E8N7168WR` | 86 | `Image render pipeline` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12C6DS6GF9VB3XYFEWE` | 190 | `Image instance buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12CWBYYYHJNYDMDD3ZJ` | 253 | `Image texture` | **wgpu 调试标签**：`target=null` + `do_not_translate` |

### crates/warpui/src/rendering/wgpu/renderer/glyph.rs (4)

| ID | Line | Source | Disposition |
|---|---|---|---|
| `01KQXQV12CZ2E3Z32C083P9T4F` | 51 | `Glyph Shader` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12CFK12FTD49TP8BHXE` | 84 | `Glyph pipeline layout` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12CCXC28ACBQD7TYPEK` | 93 | `Glyph Render pipeline` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12CMW2H6QXNSBKFEJPC` | 256 | `Glyph instance buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |

### crates/warpui/src/rendering/wgpu/renderer/rect.rs (4)

| ID | Line | Source | Disposition |
|---|---|---|---|
| `01KQXQV12EHYCE096TDE762WRW` | 38 | `Rect Shader` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12EN1R207VXGECMQ60J` | 45 | `Rect pipeline layout` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12EZZA8H2H82VHK76WB` | 51 | `Rect render pipeline` | **wgpu 调试标签**：`target=null` + `do_not_translate` |
| `01KQXQV12EG5SFZHRRNBQRXPH8` | 203 | `Rect instance buffer` | **wgpu 调试标签**：`target=null` + `do_not_translate` |

### crates/ui_components/examples/library.rs (8)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HP9GQEM8DSH2QMP6D` | 261 | `Tooltip label` | `工具提示标签` |
| `01KQXQV12EVY74SVMEZ7DKZTS9` | 292 | `Primary / Default` | `主要 / 默认` |
| `01KQXQV12F4QZ24AGJBPTZB3HP` | 314 | `Secondary / Default` | `次要 / 默认` |
| `01KQXQV12BT624KA7W9P4KNC3E` | 337 | `Disabled / Default` | `禁用 / 默认` |
| `01KQXQV12E7BHT4K6Q32RPNPSR` | 378 | `Primary / Small` | `主要 / 小型` |
| `01KQXQV12FH78FBKPH4TSZZHGS` | 401 | `Secondary / Small` | `次要 / 小型` |
| `01KQXQV12BN7NPBRA40FKW32ZV` | 425 | `Disabled / Small` | `禁用 / 小型` |
| `01KQXQV12AV4DWGVXP35C2YJWY` | 481 | `Dialog Title` | `对话框标题` |

### crates/onboarding/src/callout/view.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DS2S5S98KPQ8H3RJ5` | 63 | `Meet the Warp input` | `认识 Warp 输入框` |
| `01KQXQV12G14692SJMYKNJWJZG` | 78 | `Talk to the agent` | `与 Agent 对话` |
| `01KS2GEQPT9EPFMY0MF14ETFHF` | 121 | `Welcome to terminal mode` | `欢迎使用终端模式` |
| `01KS2GEQRBWDSBPT1NBV40YT49` | 138 | `You're in terminal mode` | `您正处于终端模式` |
| `01KQXQV12BGSPZV4G35275SEXV` | 151 | `Enable Natural Language Detection` | `启用自然语言检测` |
| `01KS2GEQQE7EZTCPM1C68A9P73` | 160 | `You're in agent mode` | `您正处于 Agent 模式` |

### crates/onboarding/src/slides/customize_slide.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GYA6HSB3RTKNZJE34` | 219 | `Tab styling` | `标签页样式` |
| `01KQXQV12A336C8B2AKQAA1FD2` | 261 | `Conversation history` | `对话历史` |
| `01KQXQV129X24N8Y3CHG0FRG0J` | 375 | `Code review` | `代码审查` |

### app/src/settings/app_icon.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129EMX64ARZNHHPMB7Q` | 76 | `Classic 1` | `经典 1` |
| `01KQXQV12963N6Y7BHKFQJ0R07` | 77 | `Classic 2` | `经典 2` |
| `01KQXQV12929FE9119VXJVRWDP` | 78 | `Classic 3` | `经典 3` |
| `01KQXQV12C572J0YNHZMNKFE23` | 80 | `Glass Sky` | `玻璃天空` |
| `01KQXQV12HA8QDY151P3TTT988` | 90 | `Warp 1` | `Warp 1`（品牌名+数字保留） |

### app/src/resource_center/section_views/feature_section.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HS80GB87ADA8XXZYF` | 41 | `What's New?` | `新功能？` |
| `01KQXQV12C924X9AXRHEZ0F90H` | 42 | `Getting Started` | `快速入门` |
| `01KQXQV12D1YS80AH7NB4NM9EF` | 43 | `Maximize Warp` | `用足 Warp` |
| `01KQXQV129YFCJEAF4FPK98DAX` | 44 | `Advanced Setup` | `高级设置` |
| `01KQXQV12BY7N9Z5FEHFQAB3T4` | 280 | `Expected valid mouse state` | `应为有效的鼠标状态`（`.expect` 内部诊断） |

### app/src/resource_center/keybindings_page.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12F54CX3039EVN9QZ9C` | 246 | `Should have command bindings vector` | `应有命令绑定向量`（`.expect` 内部诊断） |
| `01KQXQV12G2D6X6EKEGV6SHX18` | 359 | `To toggle this panel` | `切换此面板` |
| `01KQXQV12CRJN06NPE2YRY55PV` | 397 | `Go to settings > keyboard shortcuts to configure custom keybindings` | `前往「设置 > 键盘快捷键」配置自定义快捷键` |
| `01KQXQV12CJEE825FXPHGR2JTD` | 427 | `Input Editor` | `输入编辑器` |

### app/src/themes/theme_creator_body.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FR51ZYHA71E2CC9VH` | 40 | `Select an image` | `选择图片` |
| `01KQXQV12FYYA8P2D3GTVC1P95` | 41 | `Selecting image...` | `正在选择图片……`（ASCII `...` → 中文省略号 `……`） |
| `01KQXQV12FPYDEDEYCXHV532QV` | 42 | `Select a new image` | `重新选择图片` |
| `01KQXQV12AMF66QMG4ZVGR7QKK` | 44 | `Create theme` | `创建主题` |

### app/src/context_chips/display_chip.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129Q7FVW4JTAN9RK948` | 1097 | `Change git branch` | `切换 git 分支` |
| `01KQXQV12HRT7YPZ5AGHANHJ4P` | 1164 | `View pull request` | `查看 Pull Request` |
| `01KQXQV129TJH7WHKY2MRAWWR8` | 1344 | `Change working directory` | `切换工作目录` |
| `01KQXQV12J5QMZ3GR9JB3D0Q03` | 1391 | `Working directory` | `工作目录` |

### app/src/terminal/input/models/model_spec_scores.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DXX99614GYH8SDJ7F` | 18 | `Model Specs` | `模型规格` |
| `01KQXQV12HZ5S50MNVBDA0YYF2` | 19 | `Warp's benchmarks for how well a model performs in our harness, the rate at which it consumes credits, and task speed.` | `Warp 对模型在我们测试框架中的表现、消耗 credit 速率及任务速度的基准测试。` |
| `01KQXQV12EK33PHJH7XPJ10QEW` | 21 | `Reasoning level` | `推理强度` |
| `01KQXQV12C6A9S0RPMW1FAR9ZN` | 22 | `Increased reasoning levels consume more credits and have higher latency, but higher performance for complicated tasks.` | `提高推理强度会消耗更多 credit 并增加延迟，但在复杂任务上的表现更佳。` |

### app/src/settings_view/mcp_servers/mod.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12G0N1SN2NBGFWMFBHZ` | 48 | `Templatable MCP Id: {template_uuid}` | `可模板化 MCP Id：{template_uuid}` |
| `01KQXQV12GCYCTMKAPZC2XAK8V` | 51 | `Templatable MCP Installation Id: {uuid}` | `可模板化 MCP 安装 Id：{uuid}` |
| `01KQXQV12CJ917PS9ZCTDPEA33` | 53 | `Gallery MCP Id: {uuid}` | `Gallery MCP Id：{uuid}` |
| `01KQXQV12CDCGTMNJNR49Q493Y` | 54 | `File-Based MCP Id: {uuid}` | `基于文件的 MCP Id：{uuid}` |

## Decisions / Anomalies

- **wgpu 调试标签（13 条）**：沿用 batch-6 范式，处置为 `target=null` + `flags=[BATCH_FLAG, do_not_translate, wgpu_debug_label]`。这些字符串仅用于 GPU 调试器资源命名，不会出现在任何用户可见 UI。
- **`.expect` 内部诊断（2 条）**：
  - `Expected valid mouse state` → `应为有效的鼠标状态`
  - `Should have command bindings vector` → `应有命令绑定向量`
  沿用 pr-post-sync-batch 处置 panic 消息的惯例（如 `API key header width handle should lock` 已译为中文）。这些 panic 消息在崩溃时才会显示给用户，翻译为中文有助于用户/支持人员排查。
- **`Code review`（customize_slide L375）**：onboarding 自定义页 toggle 卡片标题，译「代码审查」。glossary 已有 `Code Review` 在多处译为「代码审查」（参考 settings_view/code 子树批次）。
- **`Conversation history` / `Tab styling`**：onboarding 自定义页项。`Conversation history → 对话历史`，`Tab styling → 标签页样式`（沿用 `tab → 标签页` glossary）。
- **`Code review` 跨文件**：该 ID 同时出现在 `app/src/workspace/view/right_panel.rs:?`，副作用清零 1 条；right_panel.rs 还剩 1 条非共享。
- **`What's New?` (feature_section L41)**：资源中心栏目标题，译「新功能？」保持问号语气（探索性提示）。也可译为「最新动态」/「更新内容」；考虑到这是一个 section title 并搭配 `Getting Started`/`Advanced Setup`/`Maximize Warp`，统一为简短名词性短语风格，「新功能？」直观对应原文。源已用 ASCII `?`，译为全角「？」。
- **`Maximize Warp` (feature_section L43)**：资源中心栏目，意为「充分发挥 Warp 的能力」。译「用足 Warp」简洁口语化，符合 onboarding/资源中心引导语风格。
- **`Reasoning level` (model_spec_scores L21)**：模型「思考深度」可控参数滑杆，与 `reasoning model`（推理模型）区分。glossary 新增 `reasoning level → 推理强度`。
- **`credit`/`credits` (model_spec_scores L19/L22)**：项目沿用既有惯例保留英文 `credit`，与 glossary `credit` 条目一致（产品计费单位）。
- **`Glass Sky` (app_icon L80)**：应用图标的样式描述名（玻璃风格的天空配色），译「玻璃天空」直观传达视觉风格。`Warp 1` (L90) 保留品牌+版本号样式名不译。`Classic 1/2/3` 译为「经典 1/2/3」（一致采用全角空格惯例：数字与汉字间英文空格，本批沿用 `经典 1` 形式与 macOS 中文系统命名风格一致）。
- **`Templatable MCP Id` / `Gallery MCP Id` / `File-Based MCP Id`**：调试/日志格式串，命名占位符 `{uuid}` / `{template_uuid}` 严格保留。「Id」保留英文大写首字母（数据库主键缩写惯例，与 ID/Identifier 区分）。`Gallery` 是 Warp MCP 子产品名（MCP Gallery），保留英文。
- **`Selecting image...` (theme_creator_body L41)**：含 ASCII 三点省略号，按项目惯例转为中文省略号 `……`：`正在选择图片……`。
- **`Go to settings > keyboard shortcuts to configure custom keybindings` (keybindings_page L397)**：含设置路径 `settings > keyboard shortcuts`，引用具体 UI 路径。译文使用「设置 > 键盘快捷键」并加书名号引号标识为 UI 路径名：「前往『设置 > 键盘快捷键』配置自定义快捷键」（实际采用普通方角引号 `「」`）。
- **`Change git branch` (display_chip L1097)**：保留小写 `git` 命令名（glossary `Git → Git` 但 `git branch` 是命令片段，按命令字面保留小写）。

## Glossary delta

新增 1 条术语，`term_count` 94 → 95：

- `reasoning level` → `推理强度`：AI 模型可控的「思考深度」参数滑杆，提高时消耗更多 credit 并增加延迟，但复杂任务表现更佳。与 `reasoning model`（推理模型）区分：reasoning level 是某些模型的可调节强度参数，reasoning model 是模型类别。
