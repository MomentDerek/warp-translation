# Translate 331 entries via 6 parallel implementers (batch 15)

## Goal

继 batch-14（360 条 / 6 路并行）后，按文件粒度继续吃掉 `status=new` 队列的高密度文件。本批 6 路并行，每路负责一个文件（或一组同域文件），实现 agent 自行依据 `translation-contract` §1-12 决定动作。

`status=new`: 3753 → 3422（-331）期望。
`status=translated`: 2929 → 3260（+331）期望。

## Batch composition (6 × ~55 = 331, by-file)

| Batch | 文件 | 条数 | 主要内容性质 |
|:---:|---|:---:|---|
| **A** | `app/src/terminal/view.rs` | 59 | Terminal 视图：UI 文本、doc-comment、panic、telemetry 混合（batch-14 已吃了 60 条，本次为剩余条目） |
| **B** | `crates/ai/src/agent/action_result/mod.rs` | 56 | Agent action 结果展示标签 + 状态文本（batch-14 已吃了 60 条，本次为剩余） |
| **C** | `crates/ai/src/agent/action/mod.rs` | 54 | Agent action 定义：动作名称、错误信息、状态文本 |
| **D** | `app/src/ai/blocklist/block/view_impl/output.rs` | 53 | AI 命令块输出视图：流式渲染、a11y、状态文本 |
| **E** | `app/src/workspace/view.rs` + `app/src/workspace/view/vertical_tabs.rs` | 65 | Workspace 视图集群：tab 操作、命令面板、handoff 提示（batch-14 已吃了 60 条 view.rs，本次为剩余 + vertical_tabs） |
| **F** | `app/src/ai/agent/mod.rs` | 44 | AI Agent 模块：会话/工具状态、错误信息、可见 UI 文本 |

候选文件：`candidates/batch-{A..F}.json`，每条字段 `{id, source, file, line, occurrences_kind, source_hash, audit_verdict}`。所有条目 `audit_verdict=uncertain`。

## Per-entry decision flow (实现 agent 自行判断)

严格按以下顺序，第一条命中即终止：

1. **doc-comment 假阳性**：源以 `///` 或文档结构（开头空白 + 注释体）+ Rust 文档语义 → `flag, do_not_translate, extractor_false_positive_doc_comment`，`target=null`。
2. **panic / .expect / unreachable / debug_assert** 字面量 → §10 `flag_panic_message`，`target=null`。
3. **telemetry / 日志-only 字面量**（追到 sink 是 `tracing::*`、telemetry pipeline、log file 而非 UI）→ §11 `flag_telemetry_payload`，`target=null`。
4. **`fn search_terms()` 返回的关键词串** → §12 双语追加 `<英文> <中文>`，`flag=search_terms_bilingual`（不是 do_not_translate）。
5. **wgpu debug label / 测试 fixture** → 相应子标签，`target=null`。
6. **常规 UI 文本** → 译为中文，遵守 §1-7（占位符、glossary、全角标点、`您`、register）。

## Action-hint actions (output JSON 用)

- `translate` → `target=<中文>`, no extra subflag (BATCH_FLAG 自动加)。
- `flag_panic_message` / `flag_telemetry_payload` / `flag_extractor_false_positive_doc_comment` / `flag_test_fixture` / `flag_wgpu_debug_label` → `target=null`, `do_not_translate_subflags=[<sub>]`。
- `bilingual_search_terms` → `target=<英文> <中文>`, 加入 `bilingual_search_terms_ids`。

## Glossary (沿用 batch-14)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`, `Orchestrate` → `协调`（动词）/ 保留英文（Agent Mode 功能名）, `handoff` → `转交`。

## Output schema (each implementer agent)

写入 `outputs/batch-{X}-output.json`：

```json
{
  "translations": {"<id>": "<中文>" | null, ...},
  "do_not_translate_subflags": {"<id>": ["panic_message" | "telemetry_payload" | "extractor_false_positive_doc_comment" | "test_fixture" | "wgpu_debug_label"], ...},
  "bilingual_search_terms_ids": ["<id>", ...],
  "notes": "free text"
}
```

不变量（apply 时校验）：
- `do_not_translate_subflags` 的 key 集 **必须等于** `translations` 中 value=null 的 id 集。
- `bilingual_search_terms_ids` 中的 id 必须 target 非空、不在 subflags 中。
- 翻译条目（target 非空）必须保留所有 `{placeholder}`、`%strftime` 代码、首尾空白、换行形状、品牌字面量；中文标点必须全角；ASCII `...` 必须改为 `……`。
- 双语 target 必须以 `<source> ` 开头，且不含 `,.，。；;！!？?` 等标点。

## Process

1. 6 路 trellis-implement 并行（opus）。每路读自己的 `candidates/batch-{X}.json` + 翻译规约。
2. 主 orchestrator 收齐 6 份 output，运行 `apply_translations.py` 合并到 `translations/strings.json`。
3. trellis-check 验证：
   - placeholder/strftime/whitespace/brand 不变量
   - 状态计数：`new` -331, `translated` +331
   - 既有 `translated` 条目未被触碰
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply (expected)

- `new`: 3753 → 3422
- `translated`: 2929 → 3260
- `fuzzy`: 52 (unchanged)
- new entries with `pr-by-file-parallel-batch-15` flag: 331

## Risks / Notes

- batch-14 已经处理过 `terminal/view.rs`、`action_result/mod.rs`、`workspace/view.rs` 各 60 条。**实现 agent 不要重复翻译**：候选 JSON 仅包含本次的剩余条目。
- `workspace/view.rs` 和 `vertical_tabs.rs` 共享 workspace 命名空间（tab、`Tabs`、`Vertical Tabs`），E batch 实现 agent 处理时需保持术语一致。
- 主进程合并时 `apply_translations.py` 启用幂等保护：重复翻译已 translated 条目会被跳过且报告。
