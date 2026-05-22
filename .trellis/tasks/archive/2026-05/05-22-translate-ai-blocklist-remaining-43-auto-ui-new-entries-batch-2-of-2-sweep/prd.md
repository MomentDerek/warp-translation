# Translate ai/blocklist remaining 43 auto_ui new entries — batch 2 of 2 (sweep)

## Goal

清空 `app/src/ai/blocklist` 子目录的全部 `status=new` 且 `audit.verdict=auto_ui` 用户可见文案。接力 batch 1 of 50（已完成 51 条 Agent 控制簇）。本批 **43 条**横跨 **20 个叶节点文件**，涵盖：action_model 错误提示、block 命令块操作、code_diff 审阅动作、prompt_alert 计费告警、codebase 索引引导、conversation/credit 用量、Privacy/Rules/Telemetry 提示、Cancel/Resume 系列对话框。完成后 ai/blocklist 的 auto_ui new 余量归零。

## What I already know

- 当前 `translations/strings.json` 统计（batch 1 完成后）：`translated=1468`, `fuzzy=52`, `new=5214`。
- ai/blocklist auto_ui new：batch 1 切走 51 条后剩 **43 条**。本批清零。
- glossary 词族（batch 1 已固化复用）：`Agent / 命令块 / 窗格 / 标签页 / 模型 / MCP / API / API 密钥 / Agent 模式 / 富文本输入 / harness / take over control（语义复用）`。
- 文件 + 行号分簇（共 20 文件 / 43 条）：
  - **action_model/execute/{get_files,read_files,search_codebase}.rs (3) · Agent 行动错误提示**：
    - get_files.rs L173 `The search failed. Try another way to locate the relevant files.`
    - read_files.rs L253 `These files do not exist: {missing_files}` ← **含命名占位符 `{missing_files}`**
    - search_codebase.rs L237 `The search failed because the codebase is not available. Try another way to locate the relevant files.`
  - **block.rs (4) · 命令块顶层动作**：
    - L569 `Open in GitHub` ← GitHub 字面保留
    - L1301 `Review changes` / L1327 `Don't show again` / L1340 `Rewind to before this block` ← `block → 命令块`
  - **block/cli.rs (1)**：L181 `Take control of running command` ← 与 batch 1「接管控制权」语义对齐
  - **block/toggleable_items.rs (1)**：L180 `to toggle selection` ← 拼接片段（前缀为快捷键），需保留前导空格语义
  - **block/view_impl/output.rs (6) · 命令块输出栏动作**：L2095 `Resume conversation` / L3100 `Good response` / L3121 `Bad response` / L3193 `Continue conversation` / L3217 `Fork conversation` ← `fork` 新词 / L3393 `Show credit usage details`
  - **codebase_index_speedbump_banner.rs (4) · 代码库索引引导**：L21 `Indexing helps agents quickly understand context and provide targeted solutions...` (长句) / L25 `Index codebase` / L26 `Allow automatic indexing` / L30 `View status`
  - **history_model.rs (1)**：L2622 `Cancelled by user`
  - **inline_action/ask_user_question_view.rs (1)**：L1368 `Questions skipped`
  - **inline_action/code_diff_view.rs (5) · 代码 diff 审阅**：L132 `Accept and continue with agent` / L133 `Iterate with agent` / L214 `Edit Code Diff` / L2543 `Don't show me suggested code banners again` / L3148 `Requested Edit`
  - **inline_action/host_picker.rs (1)**：L53 `Custom host…` ← `…` U+2026 保留
  - **inline_action/search_codebase.rs (1)**：L244 `No results found`
  - **prompt/prompt_alert.rs (8) · AI 计费/告警**：L26 `To use AI features,` ← **拼接片段，末尾逗号 + 空格** / L30 `No internet connection` / L32 `At Limit -` ← **拼接片段，末尾 ` - `** / L33 `Restricted due to payment issue` / L34 `Out of credits` / L36 `Sign up for more AI credits` / L38 `Enable premium overages` / L39 `Increase monthly spend limit`
  - **suggested_rule_modal.rs (1)**：L48 `Suggested rule`
  - **summarization_cancel_dialog.rs (1)**：L173 `Cancel summarization?`
  - **task_status_sync_model.rs (1)**：L277 `Warp is temporarily overloaded. Please try again shortly.`
  - **telemetry_banner.rs (1)**：L136 `Manage privacy settings`
  - **usage/conversation_usage_view.rs (1)**：L671 `Hide details`
  - **view_util.rs (2)**：L39 `Attach as agent context` / L93 `Follow up with existing conversation`

## Assumptions

- 本批 43 条 < 50 上限。结构是「长尾叶节点扫荡」：每文件 1–6 条，多数 ≤2 条。
- 选择标准：`occurrence.file ∈ ai/blocklist 所有 20 文件` + `audit.verdict==auto_ui` + `status==new`，详细 ID 已固化为 `candidates.json`。
- 特殊字面值/占位符保护：
  - **L253 `{missing_files}`** —— 命名占位符必须原样保留。
  - **L569 `GitHub`** —— 品牌名字面保留。
  - **L21 `agents`** 复数普通词 —— 按 glossary `agent → Agent` 译为「Agent」（不加「们」）。
  - **L181 `Take control of running command`** —— 与 batch 1 L93 `Take over control` 语义统一：`接管运行中的命令` 或 `接管运行中命令的控制权`（短一些更适合按钮文案，倾向前者）。
  - **L180 `to toggle selection`** —— 拼接片段，前缀有快捷键键名（如 `Space `）。保留**前导空格**：`target = " 切换选中"`（半角空格在前缀拼接处）。
  - **L32 `At Limit -`** —— 末尾 ` - ` 是拼接连字符 + 空格。target 保留尾随 ` - `（半角连字符 + 半角空格）。
  - **L26 `To use AI features,`** —— 末尾 `, ` 是拼接逗号 + 空格。译为 `要使用 AI 功能，` —— **注意末尾全角逗号 + 半角空格**（保留拼接空格的同时切换全角逗号）。**或保留半角逗号** 取决于拼接对端处理；按既往 mcp_servers L69 经验，**字面保留原 ASCII `, ` 拼接片段**最安全。实施时取 `要使用 AI 功能, `（半角逗号 + 半角空格）。
  - **L48 `Suggested rule`** —— Rules 功能名，复用现有「规则」译法（如已存在）；译为「建议的规则」。
  - **L3217 `Fork conversation`** —— `fork` 在 git/agent 语境下的「派生 / 分叉」。**glossary 暂无 fork 条目**，新增：`fork conversation → 派生会话`（参考 git 行业惯例「派生」）。
- glossary 新增预估 2–3 条：
  - `fork` → 「派生」（动词；conversation/会话/branch 上下文）
  - `rule` / `suggested_rule` → 「规则」/「建议的规则」（Suggested Rules 功能名）
  - `credit` → 「额度」（AI credits / credit usage 上下文）

## Open Questions (blocking)

- (none — scope locked，glossary 增补方向已定)

## Requirements

- 选中 43 条 entries: `status: new → translated`，`flags` 含 `pr-ai-blocklist-sweep-batch`，`target` 非空。
- 严格遵守 placeholder（**`{missing_files}` 不可丢失或重命名**）/快捷键/glossary 契约。
- 拼接片段字面规则：
  - L32 `At Limit -` → target 末尾保留 ` - `
  - L26 `To use AI features,` → target 末尾保留 ASCII `, ` 拼接（不切全角逗号）
  - L180 `to toggle selection` → target 首字符为半角空格（拼接前缀）
- `GitHub` 字面保留；`Agent` 按 glossary 保留英文；`Warp` 品牌保留。
- 全角中文标点（除拼接片段例外）。`...` → `……`。L53 `…` U+2026 原样。
- `extract --check` exit 0（幂等）。
- 已有 1468 条 translated 逐字保留。
- glossary 一致性：Agent / MCP / API / 命令块 / 窗格 / 标签页 / 模型 / 控制权语义不混译。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 43 条 entries: `status: new → translated`, `flags` 含 `pr-ai-blocklist-sweep-batch`, 非空 `target`。
- [ ] L253 `{missing_files}` placeholder 在 target 中原样出现一次。
- [ ] L569 `GitHub` 在 target 中字面出现。
- [ ] L32 target 末尾 ` - `（半角连字符 + 半角空格）保留。
- [ ] L26 target 末尾 ASCII `, ` 拼接片段保留（不切全角）。
- [ ] L180 target 首字符为半角空格。
- [ ] L181 与 batch 1 L93「接管控制权」语义自洽。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1468 条 translated 逐字保留。
- [ ] glossary 新增 `fork` / `rule` / `credit` 三条（如已存在则复用）。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。
- [ ] ai/blocklist 子目录 auto_ui new 余量归零（验证：过滤后 0 条）。

## Definition of Done

- 翻译 tone：错误提示克制中性，按钮短句无主语，告警类「您」register。
- glossary 按需新增 `fork` / `rule` / `credit`。
- Journal 记录 stats delta（`translated 1468 → 1511`）+ ai/blocklist 子目录清零 + 控制权语义续接。
- Task archive（脚本会自动 commit chore(task): archive）。

## Out of Scope

- ai/blocklist 子目录的 `verdict=uncertain` 条目（约 200+，需人工审，留 uncertain 专项 sweep）。
- ai/blocklist 之外的 auto_ui new 热点（terminal/view 37 条 / command_palette 32 条 / cli_agent_sessions 31 条 等）—— 留后续 PRD。

## Decision (locked — Approach A)

**Approach A: ai/blocklist 子目录长尾清扫 43 条**

锁定理由：
1. **一次清零 ai/blocklist auto_ui new** —— 最大热点（94 条）经过两批完全解决，后续可彻底转向下一热点（terminal/view 37 条）。
2. 长尾叶节点散文件适合一次扫掉 —— 每文件 1–6 条，留下批会反复进入相同上下文，效率低。
3. 与 batch 1 在同一时间窗口完成，控制权 / Agent / 命令块 等语义一致性最强。
4. 拼接片段 (L26 / L32 / L180) 集中处理，与 mcp_servers L69 经验（末尾空格保留）一脉相承。

**Batch flag**: `pr-ai-blocklist-sweep-batch`

## Technical Approach

1. 读取 `candidates.json` 锁定 43 条 entry id。
2. glossary 检查：
   - `fork` 不存在 → 新增 `{"en": "fork", "zh": "派生", "notes": "Git/Agent 上下文动词。'Fork conversation' → '派生会话'；'Fork branch' → '派生分支'。与 'branch / 分支' 区分：fork 强调从某点复制出独立副本，branch 强调既有线索的分叉。", "do_not_translate": false}`
   - `rule` 不存在 → 新增 `{"en": "rule", "zh": "规则", "notes": "Warp Rules 功能，约束 Agent 行为的规则文件。'Suggested rule' → '建议的规则'；'Rules' (页面标题) → '规则'。", "do_not_translate": false}`
   - `credit` 不存在 → 新增 `{"en": "credit", "zh": "额度", "notes": "AI 计费单位。'AI credits' → 'AI 额度'；'credit usage' → '额度使用'；'Out of credits' → '额度不足'；'monthly spend limit' → '每月消费上限'。", "do_not_translate": false}`
3. 按 20 文件 / 12 主题簇翻译，写回 `target` / `status=translated` / `flags 追加 pr-ai-blocklist-sweep-batch` / `updated_at`。
4. 特殊处理（实施时锚定）：
   - L173 → `搜索失败。请尝试用其他方式定位相关文件。`
   - L253 → `以下文件不存在：{missing_files}`（占位符原样）
   - L237 → `搜索失败，因为代码库不可用。请尝试用其他方式定位相关文件。`
   - L569 → `在 GitHub 中打开`
   - L1301 → `审阅变更`
   - L1327 → `不再显示`
   - L1340 → `回退至此命令块之前`
   - L181 → `接管运行中的命令`
   - L180 → ` 切换选中`（首字符半角空格）
   - L2095 → `恢复会话`
   - L3100 → `好的回复`
   - L3121 → `差的回复`
   - L3193 → `继续会话`
   - L3217 → `派生会话`
   - L3393 → `显示额度使用详情`
   - L21 → `索引能帮助 Agent 快速理解上下文并提供针对性的解决方案……`
   - L25 → `索引代码库`
   - L26 (codebase) → `允许自动索引`
   - L30 (codebase) → `查看状态`
   - L2622 → `已被用户取消`
   - L1368 → `已跳过提问`
   - L132 → `接受并继续与 Agent 协作`
   - L133 → `与 Agent 迭代`
   - L214 → `编辑代码差异`
   - L2543 → `不再向我显示建议代码横幅`
   - L3148 → `请求的编辑`
   - L53 → `自定义主机…`（U+2026 保留）
   - L244 → `未找到结果`
   - L26 (prompt) → `要使用 AI 功能, `（末尾 ASCII `, ` 保留）
   - L30 (prompt) → `无网络连接`
   - L32 → `已达上限 - `（末尾 ASCII ` - ` 保留）
   - L33 → `因付款问题受限`
   - L34 → `额度不足`
   - L36 → `注册以获取更多 AI 额度`
   - L38 → `启用超额付费`
   - L39 → `提升每月消费上限`
   - L48 → `建议的规则`
   - L173 (cancel) → `取消摘要？`
   - L277 → `Warp 暂时过载。请稍后再试。`
   - L136 (telemetry) → `管理隐私设置`
   - L671 → `隐藏详情`
   - L39 (view_util) → `作为 Agent 上下文附加`
   - L93 (view_util) → `跟进现有会话`
5. apply 脚本沿用 batch 1 模板（`apply_translations.py`），增加：
   - placeholder integrity 断言：`{missing_files}` 在 L253 target 中恰好出现一次。
   - 拼接片段断言：L26/L32 target 末尾匹配特定字面；L180 target 首字符为 ` `（空格）。
   - GitHub / Warp / Agent / API 字面保留断言。
6. `extract --check` 幂等校验。
7. `warp-zh-builder` 重建，`cargo check -p warp` 通过。
8. 子目录清零验证：重新过滤 `ai/blocklist` + `auto_ui` + `new` → 应为 0 条。
9. Journal + `task.py archive`（脚本自动 commit）。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`（81 → 预计 84 条）。
- Builder: `tools/builder/` → `build/warp-zh/`。
- Candidates (固化): `.trellis/tasks/05-22-translate-ai-blocklist-remaining-43-auto-ui-new-entries-batch-2-of-2-sweep/candidates.json`（43 条）。
- 源码上下文（20 文件）: 见 `candidates.json` 中 `file` 字段。
- 上轮 (batch 1) PRD: `.trellis/tasks/archive/2026-05/05-22-translate-ai-blocklist-auto-ui-new-entries-batch-1-of-50/prd.md`。
- 上轮 apply 脚本: `.trellis/tasks/archive/2026-05/05-22-translate-ai-blocklist-auto-ui-new-entries-batch-1-of-50/apply_translations.py`。
