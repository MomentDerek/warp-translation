# Translate next auto_ui new entries — batch 60 entries 8 (Strategy: billing/AI settings hotspots + workflow/share modals + code-review + agent UI + participant sharing + auth secrets + auto-reload modals)

## Goal

清扫 **16 个 auto_ui-new 热点文件** 共 **60 条**，16 个文件全部清零。覆盖：app/src/settings_view/billing 模块（billing_and_usage_page_v2 6 条 + overage_limit_modal 5 条 = 11）+ ai_page（5）+ openwarp_launch_modal（5）+ profile_model_selector（5）+ features_page（4 panic）+ share_block_modal（4）+ workflow_view（4）+ universal_developer_input（3）+ enable_auto_reload_modal（3）+ block_list_element（3）+ participant_avatar_view（3）+ auth_secret_types（3）+ facts/view/rule（3）+ code_review/mod（3）+ workspace/view/right_panel（1）。

跨文件外溢清零（副作用清扫）：
- `app/src/workspace/global_actions.rs` 同步清零 3 条（与 features_page 共享 panic 串）。
- `app/src/workspace/view.rs` 同步清零 3 条（同上）。
- `app/src/workspace/view/build_plan_migration_modal.rs` 同步清零 1 条（与 enable_auto_reload_modal 共享 toast）。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/settings_view/billing_and_usage_page_v2.rs` | 6 | 计费/自动充值面板（受限提示 / 管理员管理 / 自动充值描述长文 ×2） |
| `app/src/settings_view/ai_page.rs` | 5 | AI 设置（Other 项 / 睡前自动移交 / 反馈技能 toggle + 描述 / 移交长描述） |
| `app/src/settings_view/billing_and_usage/overage_limit_modal.rs` | 5 | 超额限额模态（输入校验 ×2 / 提交按钮 / 说明文 ×2） |
| `app/src/terminal/profile_model_selector.rs` | 5 | 模型/Profile 选择器 tooltip（选择模型/Profile / Follow-up 模型锁定 / 编辑权限 / API 密钥管理） |
| `app/src/workspace/view/openwarp_launch_modal/view.rs` | 5 | OpenWarp 启动模态特性介绍（贡献 / Oz / auto open-weights 等 3 个 FeatureItem） |
| `app/src/settings_view/features_page.rs` | 4 | 上报序列化 panic ×3（FocusReporting / MouseReporting / ScrollReporting） + Pin position panic |
| `app/src/terminal/share_block_modal.rs` | 4 | 命令块分享模态（嵌入码已复制 / 脱敏开关说明 / 显示提示词 / 标题输入占位符） |
| `app/src/workflows/workflow_view.rs` | 4 | 工作流视图（别名说明 / Agent 模式 prompt 占位符 / 从回收站恢复 / Run in Warp 按钮） |
| `app/src/ai/auth_secret_types.rs` | 3 | AWS Bedrock 凭证字段占位符（Bearer token / Secret access key / Session token） |
| `app/src/ai/facts/view/rule.rs` | 3 | Rules 视图（描述长文 / 搜索占位符 / 禁用横幅） |
| `app/src/code_review/mod.rs` | 3 | code review 快捷键描述（保存所有 / 显示查找栏 / 切换文件导航） |
| `app/src/terminal/block_list_element.rs` | 3 | 命令块悬浮按钮（保存为工作流 / Tag agent / 含密命令块禁止保存提示） |
| `app/src/terminal/shared_session/participant_avatar_view.rs` | 3 | 协作头像角色切换菜单（切换角色 / 改为编辑者 / 改为查看者） |
| `app/src/terminal/universal_developer_input.rs` | 3 | Universal developer 输入（Agent Mode tooltip / Attach context / Slash commands） |
| `app/src/terminal/enable_auto_reload_modal.rs` | 3 | 自动充值启用模态（更新成功 toast / 失败 toast / 团队数据未找到） |
| `app/src/workspace/view/right_panel.rs` | 1 | 切换 Code Review 面板最大化（最后 1 条非共享条目，清零） |

继 batch-7 之后，auto_ui-new 余量 201 → 141（-60 主清扫，加上 3+3+1=7 条副作用外溢，净下降 60，文件全清零 16）；`translated` 2040 → 2100，`new` 4642 → 4582。

## What I already know

- 当前 `strings.json` 统计：`entry_count=6734`, `translated=2040`, `new=4642`, `fuzzy=52`。
- glossary 现有 95 条；本批沿用既有术语：`Warp` / `Agent` / `Agent Mode → Agent 模式` / `code_review → 代码审查` / `auto_reload → 自动充值` / `credit → 积分` / `keybinding → 快捷键` / `model → 模型` / `workflow → 工作流` / `add_on → 附加` / `harness → 执行环境` / `rule → 规则` / `prompt → 提示词` / `mcp → MCP` / `api_key → API 密钥` / `secret_redaction → 保密信息脱敏` / `tab → 标签页` / `session → 会话`。无新增术语，`term_count` 保持 95。
- **占位符**：3 条含命名占位符 — `{credits}` / `{price}`（billing_and_usage_page_v2 L1205）和 `{package_manager}` 等不在本批；本批共 1 条带 `{credits} {price}` 双占位符（恢复原 named placeholders），另需注意 `Restricted due to billing issue. Contact your team admin to update their payment method.` 等无占位符。无 strftime。
- **`.expect` 内部诊断 panic 串（4 条，features_page.rs）**：
  - `MouseReportingEnabled failed to serialize`（L1491）
  - `ScrollReportingEnabled failed to serialize`（L1500）
  - `FocusReportingEnabled failed to serialize`（L1509）
  - `Pin position should exist in default size percentages`（L3082）
  这些 panic 在崩溃时才显示。沿用 batch-7 翻译 panic 消息惯例（如 `Should have command bindings vector → 应有命令绑定向量`）。前 3 条含 Rust 结构体字段名标识符（`FocusReportingEnabled` 等），按 panic 消息处理：标识符保留英文，叙述部分译中文。
- **`Introducing 'auto (open-weights)'` (openwarp_launch_modal L65)**：单引号包裹的产品代号 `auto (open-weights)`，是 OpenWarp 新增的「自动选择最佳开源权重模型」配置标签。保留代号原文 `auto (open-weights)`，仅翻译外层引导词 `Introducing`：`隆重推出『auto (open-weights)』`。
- **`Warp's client code is now open source. Get started by using the /feedback skill to open an issue, and follow the contribution guidelines here.` (openwarp_launch_modal L48)**：含 `/feedback` 命令字面量，保留不译；末尾 `here` 是 inline_link 锚文本，译为「此处」。

## Scope by file

### app/src/settings_view/billing_and_usage_page_v2.rs (6)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEPRAD00RC94NVCF09D6K` | 81 | `Auto-reload is enabled` | `自动充值已启用` |
| `01KS2GEQC5EVC4YW6D9JSY85JK` | 82 | `Managed by your admin` | `由您的管理员管理` |
| `01KS2GEQKJXXA5M7BJGZN9XRQP` | 87 | `Restricted due to billing issue. Contact your team admin to update their payment method.` | `因账单问题受限。请联系团队管理员更新支付方式。` |
| `01KS2GEPQVP33JYKBB3H99NN59` | 89 | `Auto reload is disabled due to recent failed reload. Contact your team admin to update their payment method.` | `因近期充值失败，自动充值已禁用。请联系团队管理员更新支付方式。` |
| `01KS2GEQQT37VQQJPZFR5CNYAB` | 1209 | `Your admin has enabled auto-reload for add-on credits. When your personal add-on credit balance runs low, Warp will automatically purchase add-on credits and add them to your balance.` | `您的管理员已为附加积分启用自动充值。当您的个人附加积分余额不足时，Warp 将自动购买附加积分并添加到您的余额中。` |
| `01KS2GEQQZS6AABN0KPWFXQ430` | 1205 | `Your admin has enabled auto-reload for add-on credits. When your personal add-on credit balance runs low, Warp will automatically purchase {credits} credits for {price} and add them to your balance.` | `您的管理员已为附加积分启用自动充值。当您的个人附加积分余额不足时，Warp 将以 {price} 自动购买 {credits} 积分并添加到您的余额中。` |

### app/src/settings_view/ai_page.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KRBDMFSV95Z6WRHX832P25B9` | 2549 | `Other` | `其他` |
| `01KS2GEPR2B1NQRKQ7P9SFD1NJ` | 6860 | `Auto-handoff before sleep` | `睡眠前自动移交` |
| `01KS2GEQQ1905GTK5TEXC0YGTZ` | 6873 | `When macOS is about to sleep, automatically moves the most recently focused running local Warp Agent conversation to Cloud Mode so it can keep working.` | `当 macOS 即将进入睡眠时，自动将最近聚焦且正在本地运行的 Warp Agent 对话移交至云端模式，以便继续工作。` |
| `01KS2GEQ3E562RX0CHZQ9R6BEM` | 6182 | `Enable built-in feedback skill` | `启用内置反馈技能` |
| `01KS2GEQA5WEEPDTH6D3H7FY1X` | 6191 | `Let Oz use Warp's built-in skill for turning Warp product feedback into GitHub issues.` | `允许 Oz 使用 Warp 内置技能将 Warp 产品反馈转化为 GitHub Issue。` |

### app/src/settings_view/billing_and_usage/overage_limit_modal.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12EYRM8N45SBRV21C6C` | 160 | `Please enter a valid currency amount` | `请输入有效的金额` |
| `01KQXQV12EHDA5VX44WRG5S1RC` | 163 | `Please enter a price between $0.01 and $10,000,000` | `请输入 $0.01 至 $10,000,000 之间的金额` |
| `01KQXQV12HM377NKCEPVFPQEJW` | 203 | `Warp will prevent use of premium models when this dollar limit is reached. Resets on a monthly basis.` | `当达到此美元额度时，Warp 将禁止使用高级模型。每月自动重置。` |
| `01KQXQV12DD3X7KN6GSY0R0DY3` | 211 | `Note that AI credits made near your chosen limit may exceed it by a few dollars.` | `请注意，接近所选额度的 AI 积分用量可能超出额度数美元。` |
| `01KQXQV12H99WBF2WB0TDTK62Z` | 271 | `Update` | `更新` |

### app/src/terminal/profile_model_selector.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129NXPTYW2ZX419YZT6` | 91 | `Choose an AI execution profile` | `选择 AI 执行 Profile` |
| `01KQXQV1292G1SEEB09WKC9DNS` | 92 | `Choose an agent model` | `选择 Agent 模型` |
| `01KS2GEQ6WVTDWBZNQNF0RJ48B` | 93 | `Follow-ups use the original run's model` | `后续追问使用原始运行的模型` |
| `01KQXQV12ESJKCXC8VH17X4CC0` | 94 | `Request edit access to change model` | `请求编辑权限以更换模型` |
| `01KQXQV12DJN9NDM0AC21XZE2W` | 551 | `Manage API keys` | `管理 API 密钥` |

### app/src/workspace/view/openwarp_launch_modal/view.rs (5)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H5WQFD8MBDRZ7AMEY` | 48 | `Warp's client code is now open source. Get started by using the /feedback skill to open an issue, and follow the contribution guidelines here.` | `Warp 的客户端代码现已开源。请使用 /feedback 技能提交 Issue 开始体验，并参考此处的贡献指南。` |
| `01KQXQV12DTPFMQC4H7M2D7FC4` | 56 | `Open Automated Development` | `开放自动化开发` |
| `01KQXQV12G4Z3MQ0Z3CRGH49M0` | 57 | `The Warp repo is managed by an agent-first workflow powered by Oz, our cloud agent orchestration platform.` | `Warp 仓库采用 Agent 优先的工作流管理，由我们的云端 Agent 编排平台 Oz 提供支持。` |
| `01KQXQV12CDMG6139PZME36CDR` | 65 | `Introducing 'auto (open-weights)'` | `隆重推出『auto (open-weights)』` |
| `01KQXQV12HWRB38E719TAGQHD6` | 66 | `We've added a new auto model that picks the best open weight model for a task, like Kimi or MiniMax.` | `我们新增了一个 auto 模型，能为任务挑选最优的开源权重模型，例如 Kimi 或 MiniMax。` |

### app/src/settings_view/features_page.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DXXQC7SEPS215WFHH` | 1491 | `MouseReportingEnabled failed to serialize` | `MouseReportingEnabled 序列化失败` |
| `01KQXQV12FX8XS6ETE4SEAZ41A` | 1500 | `ScrollReportingEnabled failed to serialize` | `ScrollReportingEnabled 序列化失败` |
| `01KQXQV12C2PNMTSFT38KTSP2X` | 1509 | `FocusReportingEnabled failed to serialize` | `FocusReportingEnabled 序列化失败` |
| `01KQXQV12EHTWCWMMH0N5A5WK7` | 3082 | `Pin position should exist in default size percentages` | `Pin 位置应存在于默认尺寸百分比中` |

### app/src/terminal/share_block_modal.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GT0RBYJN03R87CZK6` | 71 | `Title (optional)` | `标题（可选）` |
| `01KQXQV12BD9NCXCPSKVRXE6M7` | 549 | `Embed code copied.` | `嵌入代码已复制。` |
| `01KQXQV12G2WCQ6G9SJK9T3G4T` | 961 | `Show prompt` | `显示提示词` |
| `01KQXQV12EN40A6E8KN07QGWPA` | 1062 | `Redact secrets (API keys, passwords, IP addresses, PII etc.)` | `脱敏机密信息（API 密钥、密码、IP 地址、PII 等）` |

### app/src/workflows/workflow_view.rs (4)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BR2H003YSFQHY3J2S` | 151 | `Enter your prompt here... (e.g., 'Create a function to sort an array of objects by date' or 'Help me debug this React component').` | `在此输入您的提示词……（例如：『创建一个按日期对对象数组排序的函数』或『帮我调试这个 React 组件』）。` |
| `01KQXQV129Q59M106JGCEJ93FG` | 185 | `Aliases allow you to create short strings to execute workflows. Each alias can have different argument values and environment variables, and aliases are personal to you.` | `别名让您可以创建简短字符串以执行工作流。每个别名可以拥有不同的参数值和环境变量，且别名仅属于您个人。` |
| `01KQXQV12F8478CX9WKXTTZ74D` | 187 | `Run in Warp` | `在 Warp 中运行` |
| `01KQXQV12EHP2J9T6X1CJ6V99R` | 2890 | `Restore workflow from trash` | `从回收站恢复工作流` |

### app/src/ai/auth_secret_types.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEPRFSPACWTVGS21FHV3T` | 140 | `Bearer token` | `Bearer 令牌` |
| `01KS2GEQMAH941Z850D71GPS4E` | 165 | `Secret access key` | `Secret 访问密钥` |
| `01KS2GEQMXYMSC5W9HWG8Q88FJ` | 171 | `Session token (temporary credentials only)` | `Session 令牌（仅限临时凭证）` |

### app/src/ai/facts/view/rule.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12F22MSZT48D1M0WRFF` | 53 | `Rules enhance the agent by providing structured guidelines that help maintain consistency, enforce best practices, and adapt to specific workflows, including codebases or broader tasks.` | `规则通过提供结构化指引来增强 Agent 能力，帮助维持一致性、落实最佳实践，并适配特定工作流，涵盖代码库或更广泛的任务场景。` |
| `01KQXQV12F8RBZRA0EZDNFSCSB` | 55 | `Search rules` | `搜索规则` |
| `01KQXQV12J576KNDCXA9QGQPYG` | 62 | `Your rules are disabled and won't be used as context in sessions. You can ` | `您的规则已禁用，不会作为会话上下文使用。您可以 ` |

### app/src/code_review/mod.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FTR0BMEHSJHBR9X4T` | 61 | `Save all unsaved files in code review` | `保存代码审查中所有未保存的文件` |
| `01KQXQV12GSWZQ1VT3MX084G9M` | 68 | `Show find bar in code review` | `在代码审查中显示查找栏` |
| `01KS2GEQNZYXKY53YQ760DH3CS` | 76 | `Toggle file navigation in code review` | `在代码审查中切换文件导航` |

### app/src/terminal/block_list_element.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GAHH57BFV1W2VAKT3` | 156 | `Tag agent for assistance` | `标记 Agent 协助` |
| `01KQXQV12F58T1CPER1N3P755M` | 158 | `Save as Workflow` | `另存为工作流` |
| `01KQXQV129TMAXVMG1QN3RXSV1` | 159 | `Blocks containing secrets cannot be saved.` | `包含机密信息的命令块无法保存。` |

### app/src/terminal/shared_session/participant_avatar_view.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DBWZ3Z3JSFWMBHYFR` | 167 | `Make editor` | `设为编辑者` |
| `01KQXQV12DJXGZBA98P80C79YG` | 173 | `Make viewer` | `设为查看者` |
| `01KQXQV129119ACA14M6A60TV2` | 587 | `Change role` | `切换角色` |

### app/src/terminal/universal_developer_input.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129RS9H82VPZY0SPYKW` | 205 | `Attach context` | `附加上下文` |
| `01KQXQV12GQ4YJ14BBJ05GH1S9` | 405 | `Slash commands` | `斜杠命令` |
| `01KQXQV129CA62RTCM0AZ6R3DW` | 1020 | `Agent Mode` | `Agent 模式` |

### app/src/terminal/enable_auto_reload_modal.rs (3)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV1292NF7H8KQJB5VXZ1Y` | 102 | `Auto-reload settings updated` | `自动充值设置已更新` |
| `01KQXQV12B31H1V0TEX2HP3AHR` | 112 | `Failed to enable auto-reload. Please try updating your settings in Billing & usage.` | `启用自动充值失败。请尝试在「计费与用量」中更新您的设置。` |
| `01KQXQV12DPNFAKTT1AY6S0QNF` | 390 | `Oops, something went wrong; your team's data could not be found.` | `糟糕，出错了；未能找到您团队的数据。` |

### app/src/workspace/view/right_panel.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GW8HDJFCH918XTJNJ` | 389 | `Toggle Maximize Code Review Panel` | `切换代码审查面板最大化` |

## Decisions / Anomalies

- **`credit/credits` (本批多处)**：沿用 glossary `credit → 积分` 与既有翻译惯例（约 90% 现有翻译使用「积分」）。本批 `add-on credits` 一律译为「附加积分」（沿用 `add_on → 附加` glossary 组合）。
- **`Auto-reload / auto-reload` (本批多处)**：沿用 glossary `auto_reload → 自动充值`（指余额自动补充，非 reload 按钮）。
- **`Profile / execution profile` (profile_model_selector L91)**：UI 中常作产品功能名，保留英文 `Profile` 不译（与既有 `Profile Editor` 等术语保持一致；尚未入 glossary 但有事实标准）。
- **`Follow-ups` (profile_model_selector L93)**：对话中的后续提问/追问。译「后续追问」（已有相似项目用法）。
- **`/feedback` (openwarp_launch_modal L48)**：斜杠命令字面量，保留不译。
- **`auto (open-weights)` (openwarp_launch_modal L65)**：模型选项代号，保留原文。「Introducing」译为「隆重推出」+ 中文方角引号 `『』`（源使用 ASCII 单引号 `'`，按项目 punctuation 惯例转为方角引号）。
- **`auto model` / `open weight model` (openwarp_launch_modal L66)**：`auto` 是模型代号，保留小写英文不译；`open weight model` 译「开源权重模型」（开放权重发布的 LLM）。
- **`Oz` (openwarp_launch_modal L57, ai_page L6191)**：Warp 的云端 Agent 编排平台产品名，保留英文不译。
- **`GitHub issues` (ai_page L6191)**：产品/平台专有术语，译「GitHub Issue」（保留 `GitHub Issue` 单数形式，因 Issue 在中文社区已是常用专有名词）。
- **`PII` (share_block_modal L1062)**：Personally Identifiable Information 的英文缩写。技术语境下保留英文缩写。
- **`Bearer token` / `Secret access key` / `Session token` (auth_secret_types)**：AWS Bedrock 凭证字段占位符。`Bearer` / `Secret` / `Session` 保留英文（OAuth / AWS 协议术语），`token`/`access key` 译为「令牌」/「访问密钥」。
- **`Tag agent for assistance` (block_list_element L156)**：`tag` 在此为动词「标记/@」。译「标记 Agent 协助」（保持 Agent 不译）。
- **`Slash commands` (universal_developer_input L405)**：斜杠命令（以 `/` 开头的命令），译「斜杠命令」。
- **`Save as Workflow` (block_list_element L158)**：保留 `Workflow` 译为「工作流」。
- **`Billing & usage` (enable_auto_reload_modal L112)**：设置页面名引用。译「计费与用量」（标准设置导航项）。
- **`.expect` panic 串（4 条，features_page.rs）**：沿用 batch-7 翻译 panic 惯例。前 3 条 `*ReportingEnabled failed to serialize` — `*ReportingEnabled` 是 Rust 结构体类型名（CamelCase 标识符），按惯例保留英文，叙述部分译「序列化失败」。第 4 条 `Pin position should exist in default size percentages` 中 `Pin` 是 Warp Quake Mode pin position 概念（钉住位置），保留英文 `Pin`，其余译中文。
- **`'Create a function to sort an array of objects by date'` 等单引号短语 (workflow_view L151)**：源使用 ASCII 单引号包裹示例 prompt。译文转为中文方角引号 `『』`（已是项目其他单引号包裹的处置惯例）。三点省略号 `...` 转为 `……`。
- **`Restricted due to billing issue` (billing_and_usage_page_v2 L87)**：账户因账单问题受限。译「因账单问题受限」。
- **`Toggle Maximize Code Review Panel` (right_panel L389)**：与 batch-6/7 同一文件中其他「Toggle Maximize *」keybinding 命名风格保持一致。`Code Review` 译「代码审查」（glossary）。
- **`Make editor` / `Make viewer` (participant_avatar_view)**：协作角色变更菜单。译「设为编辑者」/「设为查看者」更符合中文菜单动词搭配。
- **`Attach context` (universal_developer_input L205)**：附加上下文（chip configurator 入口）。
- **`Restore workflow from trash` (workflow_view L2890)**：「Trash」译为「回收站」（参照 macOS 系统术语）。
- **`Update` (overage_limit_modal L271)**：模态提交按钮。译「更新」。
- **`Embed code copied.` (share_block_modal L549)**：`Embed code` = 嵌入代码 (HTML/iframe 嵌入片段)。译「嵌入代码已复制。」保留句末句号。
- **`Show prompt` (share_block_modal L961)**：显示分享条目附带的提示词（Agent prompt）。译「显示提示词」沿用 glossary `prompt → 提示词`。
- **`Cloud Mode` (ai_page L6873)**：Warp Agent 的云端运行模式（与 Local Mode 对应）。译「云端模式」。

## Glossary delta

无新增术语。`term_count` 保持 95。
