# Translate next auto_ui new entries — batch 60 entries 5 (Strategy A: drive + settings + code + AI document/transcript)

## Goal

清扫 **10 个 auto_ui-new 热点文件** 共 **60 条**。覆盖：工作流编辑模态 + 外部编辑器设置 + 项目浏览器（文件树）+ 代码视图键位 + 计费周期用量横幅 + AI 助手对话记录 + 团队删除/离开二次确认 + AI 规划文档菜单 + 键位设置 + 计费用量通用桶。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/drive/workflows/modal.rs` | 7 | 工作流编辑模态（标题占位符 / 参数 / 保存按钮 / 未保存提示） |
| `app/src/settings_view/features/external_editor.rs` | 7 | 外部编辑器设置（分组开关 / 默认应用 / 编辑器选择 / 布局 / Markdown 默认） |
| `app/src/code/file_tree/view.rs` | 7 | 项目浏览器空状态 + 文件/目录右键菜单 |
| `app/src/settings_view/billing_and_usage/billing_cycle_usage_section.rs` | 7 | 计费周期 refresh 时间 + 升级横幅链接尾随文本 |
| `app/src/code/view.rs` | 6 | 代码编辑器键位描述（保存 / 关闭标签 / 接受变更 / Markdown 预览） |
| `app/src/ai_assistant/transcript.rs` | 6 | AI 对话记录（后续问题 prompt + 生成中状态 + 准确性提示） |
| `app/src/drive/cloud_action_confirmation_dialog.rs` | 6 | 删除/离开团队二次确认对话框 |
| `app/src/ai/ai_document_view.rs` | 6 | AI 规划文档（标题 / 版本历史 / Drive 同步 / 导出 / Copy plan ID） |
| `app/src/settings_view/keybindings.rs` | 6 | 键位设置（搜索占位符 + 冲突提示 + 描述 + 同步说明） |
| `app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs` | 2 | 用量桶 `Suggested code diffs` + Tooltip Total usage 行 |

10 个文件全部清零至 auto_ui-new=0。继 batch-4（workspace sweep）之后，auto_ui-new 余量 381 → 321（-60）；`translated` 1860 → 1920，`new` 4822 → 4762。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=1860`, `fuzzy=52`, `new=4822`（auto_ui 381 / uncertain 4441）。
- glossary 现有 93 条；本批沿用既有术语（`Warp` / `Warp AI` / `Warp Drive` / `Markdown` / `WSL` / `MCP` / `Git` / `block→命令块` / `pane→窗格` / `tab→标签页` / `workflow→工作流` / `keybindings→键位` 等），无新增。
- **strftime 格式串**：`Resets %b %d, %-I:%M %p` (L392, billing_cycle_usage_section.rs) — `%b/%d/%-I/%M/%p` 为 chrono 格式指令，需字面保留。译文：`%b %d %-I:%M %p 重置`（前缀「重置」→后缀「重置」以匹配中文时间习惯；格式指令保持 ASCII）。
- **占位符**：仅 strftime `%` 指令；无 `{}` / `{name}` 命名占位符。
- **CTA 链接尾随片段**（billing_cycle_usage_section.rs L676/682/688/696）：紧跟 `"Upgrade to Build"` / `"Upgrade to Business"` / `"Contact sales"` / `"Open the admin panel"` 链接之后的句尾片段，源无前置空格，由渲染器在链接和文本之间留视觉间隔。译文同样无前置空格。
- **键位描述对的复用**（code/view.rs L96/L113）：`SAVE_FILE_BINDING_DESCRIPTION = "Save file"` 作为公共常量被 AI document view 复用；译文「保存文件」与 AI document 视图保持一致。

## Scope by file

### app/src/drive/workflows/modal.rs (7)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HSGVFPE2QRFK8FHE6` | 102 | `Untitled workflow` | `未命名工作流` |
| `01KQXQV1281ZWHHWZF7BPR5MMA` | 103 | `Add a description` | `添加描述` |
| `01KQXQV12D2HZ9YKHQCW5SBTKC` | 106 | `New argument` | `新建参数` |
| `01KQXQV12A6AZPG0305YYCPF0N` | 108 | `Default value (optional)` | `默认值（可选）` |
| `01KQXQV12FT6BJ59B1Q2GWNZHZ` | 109 | `Save workflow` | `保存工作流` |
| `01KQXQV12J87PQNW8QNA5XFXRS` | 113 | `You have unsaved changes.` | `您有未保存的更改。` |
| `01KQXQV12DNC2K24X9Q844YX7D` | 114 | `Keep editing` | `继续编辑` |

### app/src/settings_view/features/external_editor.rs (7)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CXVG5KN85CVS19XFM` | 28 | `Group files into single editor pane` | `将文件分组到同一编辑器窗格` |
| `01KQXQV12H98VQ8VHZ2D69E567` | 29 | `When this setting is on, any files opened in the same tab will be automatically grouped into a single editor pane.` | `开启此设置后，同一标签页中打开的任何文件都将自动分组到同一编辑器窗格。` |
| `01KQXQV12AKP15Q77BX3B1TC31` | 149 | `Default App` | `默认应用` |
| `01KQXQV1292ZEWS1JA2ZFSD8NQ` | 283 | `Choose an editor to open file links` | `选择用于打开文件链接的编辑器` |
| `01KQXQV129F49S92XA0VHCFDA5` | 298 | `Choose an editor to open files from the code review panel, project explorer, and global search` | `选择用于从代码评审面板、项目浏览器和全局搜索打开文件的编辑器` |
| `01KQXQV129SV75C8035770V94J` | 313 | `Choose a layout to open files in Warp` | `选择在 Warp 中打开文件的布局` |
| `01KQXQV12D7EH88EJQQA0NMXY6` | 361 | `Open Markdown files in Warp's Markdown Viewer by default` | `默认使用 Warp 的 Markdown 查看器打开 Markdown 文件` |

### app/src/code/file_tree/view.rs (7)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12G6ZKB2CYEPTV5X14Z` | 75 | `The Project Explorer requires access to your local workspace, which isn't supported in remote sessions.` (注：源中是 U+2019 右单引号 `'`) | `项目浏览器需要访问您的本地工作区，这在远程会话中不受支持。` |
| `01KQXQV12GHQ0RRKWYPVX4ZA4M` | 76 | `The Project Explorer requires access to your local workspace. Open a new session or navigate to an active session to view.` | `项目浏览器需要访问您的本地工作区。请打开新会话或切换到活动会话查看。` |
| `01KQXQV12GS082X8GXFBTKN84Y` | 77 | `The Project Explorer doesn't currently work in WSL.` | `项目浏览器目前在 WSL 中不可用。` |
| `01KQXQV12DMH981WWXM3M23B7P` | 2347 | `New file` | `新建文件` |
| `01KRBDMFW6WXRTD2HWA7DT2GB1` | 2356 | `cd to directory` | `cd 到目录` |
| `01KQXQV1294KDXV6CDXSSPXHPQ` | 2406 | `Attach as context` | `作为上下文附加` |
| `01KQXQV12AY1P143VX80C5CYZB` | 2419 | `Copy relative path` | `复制相对路径` |

### app/src/settings_view/billing_and_usage/billing_cycle_usage_section.rs (7)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEQJRYS4Z9459JS6FDMT6` | 392 | `Resets %b %d, %-I:%M %p` (strftime) | `%b %d %-I:%M %p 重置`（chrono 格式指令字面保留；去掉英文逗号改用空格分隔以贴近中文时间表达） |
| `01KS2GEQS0C7FHH4N1WGTTD2PB` | 676 | `to see team-level credit usage.` | `查看团队级 credit 用量。` |
| `01KS2GEQPK7KCYT8MRMY4JZC3K` | 681 | `Upgrade to Business` | `升级到 Business` |
| `01KS2GEQRZRDD94EET1BZ5ZWEC` | 682 | `to see per-user credit attribution.` | `查看每位用户的 credit 归属。` |
| `01KS2GEQRYV1T4NQ8JQ3M69V3K` | 688 | `to see fine-grained credit attribution and set per-user spend limits.` | `查看细粒度 credit 归属并设置每位用户的支出上限。` |
| `01KS2GEQS17KEK10MJ368CYH3Q` | 696 | `to set per-user spend limits.` | `设置每位用户的支出上限。` |
| `01KS2GEQE6HWJRJ0CBCEMJAZRJ` | 717 | `Other team members' usage across add-on, pay-as-you-go, and cloud-only credits.` | `其他团队成员在附加包、按量付费和云端专属 credit 上的用量。` |

### app/src/code/view.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FE27129PB0GHKSD95` | 96 | `Save file` | `保存文件` |
| `01KQXQV12F3HMZSHZDZW1XVWWZ` | 113 | `Save file as` | `文件另存为` |
| `01KQXQV129WFPMXK2XMK8JZ2X6` | 120 | `Close all tabs` | `关闭所有标签页` |
| `01KQXQV129BHXPQ0JJ8P7DFGMB` | 127 | `Close saved tabs` | `关闭已保存的标签页` |
| `01KQXQV128DBE6DHP7HKX7Z59G` | 1087 | `Accept and save` | `接受并保存` |
| `01KQXQV12H2B0SEKFBAJ9M4DGW` | 2047 | `View Markdown preview` | `查看 Markdown 预览` |

### app/src/ai_assistant/transcript.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CF92SBBMP1Q4795XE` | 63 | `How do I fix this?` | `我该如何修复这个问题？` |
| `01KQXQV12FEKDF16JG7WRRDANS` | 64 | `Show examples.` | `展示一些示例。` |
| `01KQXQV12H4ZCJ2DFAKCHA1324` | 65 | `What should I do next?` | `接下来我该做什么？` |
| `01KQXQV12CB22K3WDC4KH5W4SR` | 66 | `Generating answer...` (ASCII `...`) | `正在生成回复……` (`...`→`……`) |
| `01KQXQV128EYTNG5GEM6KABSRM` | 67 | `AI responses can be inaccurate.` | `AI 的回复可能不准确。` |
| `01KQXQV12HJQ8JQTWJCE6XR2XC` | 69 | `Warp AI might forget earlier answers as conversations get long.` | `当对话变长时，Warp AI 可能会遗忘早期的回答。` |

### app/src/drive/cloud_action_confirmation_dialog.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129XN6ZCDWSCQDZR6K7` | 28 | `Are you sure you want to delete this team?` | `确定要删除此团队吗？` |
| `01KQXQV129PS980CXV1ZZF3N15` | 29 | `Are you sure you want to leave this team?` | `确定要离开此团队吗？` |
| `01KQXQV12A7J40EGJMA10YEAK8` | 31 | `Deleting this team will permanently delete it and all of its related content, including billing information or credits. You will not be able to restore them.` | `删除此团队将永久删除该团队及其所有相关内容，包括账单信息和 credit。删除后将无法恢复。` |
| `01KQXQV12J5X827743SAS7TRG0` | 32 | `You will need to be reinvited in order to rejoin.` | `如需重新加入，您需要被再次邀请。` |
| `01KQXQV12JZD3VJVK14963H941` | 34 | `Yes, delete` | `是，删除` |
| `01KQXQV12JQ9Q4MXX7M0YAT33F` | 35 | `Yes, leave` | `是，离开` |

### app/src/ai/ai_document_view.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12EBP82BPC0XBDS31X1` | 148 | `Planning document` | `规划文档` |
| `01KQXQV12G0V0BPPHWAD4ZCVT9` | 393 | `Show version history` | `显示版本历史` |
| `01KQXQV12FMW5EGKZ6BPHCE3PY` | 675 | `Save and auto-sync this plan to your Warp Drive` | `保存并自动同步此规划到您的 Warp Drive` |
| `01KQXQV12G6WQ76XWX56V8K3X4` | 1327 | `Show in Warp Drive` | `在 Warp Drive 中显示` |
| `01KQXQV12FRDE6N9N39Z0G8ZJA` | 1337 | `Save as markdown file` | `另存为 Markdown 文件` |
| `01KQXQV12AWMXQ3W55AASYZYWX` | 1354 | `Copy plan ID` | `复制规划 ID` |

### app/src/settings_view/keybindings.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FF2YDGK2QQ3YMNG0D` | 60 | `Search by name or by keys (ex. "cmd d")` | `按名称或按键搜索（例如 "cmd d"）`（保留 ASCII 引号 + 键位字面） |
| `01KQXQV12GZNS8K1SH5EEQBY1F` | 61 | `This shortcut conflicts with other keybinds` | `此快捷键与其他键位冲突` |
| `01KQXQV129ZEF1W5T9CJXNG960` | 986 | `Add your own custom keybindings to existing actions below.` | `为下方现有操作添加您的自定义键位。` |
| `01KQXQV12J4ZP4SNXWQCW51RAQ` | 1041 | `to reference these keybindings in a side pane at anytime.` | `即可随时在侧边面板查阅这些键位。` |
| `01KQXQV12D2B3807CY030V11B3` | 1121 | `Keyboard shortcuts are not synced to the cloud` | `键盘快捷键不会同步到云端` |
| `01KQXQV12AKE5CXQ0KT2HREYMM` | 1129 | `Configure keyboard shortcuts` | `配置键盘快捷键` |

### app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEQN6CFV21S1T1XEDC350` | 114 | `Suggested code diffs` | `建议的代码差异` |
| `01KS2GEQP1QSVQW6RBH1DFPR99` | 293 | `Total usage` | `总用量` |

## Decisions / Anomalies

- **strftime 格式串 `Resets %b %d, %-I:%M %p`**：`%b/%d/%-I/%M/%p` 是 chrono 的格式指令，必须按字面保留；不被 `{...}` 占位符校验捕获，但需手工守护。源串「Resets <date>」是「重置时间」的英文表达；中文常以「<时间> 重置」收尾，更符合阅读习惯。最终：`%b %d %-I:%M %p 重置`，去掉英文逗号、改用空格分隔字段。
- **CTA 尾随片段（billing_cycle_usage_section 4 条）**：源串紧跟链接锚文本之后，无前置空格——按渲染器逻辑由组件自身留视觉间隔。译文同样无前置空格；句末英文句点→中文句号。
- **`credit` 字面保留**：「credit」在 Warp 计费语境中为产品专有名词（积分单位），不译为「积分」以避免与游戏化语境混淆；与 settings_view/billing_and_usage_page_v2 之前批次保持一致。glossary 中已有 `credit` 条目。
- **`Markdown` 字面保留**：作为格式名是品牌名，不译。
- **`WSL` 字面保留**：缩写，不译。
- **`Warp Drive` 字面保留**：品牌名。
- **`Business`（计划名）字面保留**：Warp 订阅档位名「Business」是商品 SKU 名称，保持英文。
- **`Show examples.` 句末英文句点**：保留中文句号「。」。
- **`Generating answer...` ASCII `...`**：转换为「……」（U+2026 双字符）。
- **`How do I fix this?` 问号**：转中文问号「？」。
- **U+2019 右单引号 (file_tree/view.rs L75)**：源中 `isn't` 实际为 `isn't`（带 U+2019）。中文译文用「不受支持」绕过，无引号问题。
- **`cd to directory` (file_tree L2356)**：右键菜单项执行 `cd` 命令到该目录；译为「cd 到目录」，保留 `cd` 命令字面。
- **`"cmd d"` 键位示例 (keybindings.rs L60)**：源中以 ASCII `\"cmd d\"` 形式嵌入，需保留 ASCII 引号 + 小写键名（与 batch-4 `Shift + ctrl + space` 同策略——键位字面）。
- **`Save file` 跨视图复用 (code/view.rs L96)**：`SAVE_FILE_BINDING_DESCRIPTION` 公共常量被 AI 规划文档视图复用，译文「保存文件」与该视图保持一致。
- **`Save file as` (code/view.rs L113)**：仿照 Windows/macOS 文件菜单惯用语「文件另存为」（而非「另存文件」），符合用户认知。
- **`Suggested code diffs` (billing_cycle_usage_common L114)**：用量分桶名，译「建议的代码差异」对应 AI 生成建议代码这一计费维度。
- **`Total usage` (billing_cycle_usage_common L293)**：Tooltip 中的合计行标签，译「总用量」。
- **CamelCase 品牌：`Default App` 译「默认应用」**：在「macOS 中由系统挑选编辑器」语境下，对应「Default App」选项。

## Glossary delta

无新增。沿用既有 93 条术语。`term_count` 保持 93。
