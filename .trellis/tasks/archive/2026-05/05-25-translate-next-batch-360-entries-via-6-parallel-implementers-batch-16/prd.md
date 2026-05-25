# Translate 371 entries via 6 parallel implementers (batch 16)

## Goal

继 batch-15（331 条 / 6 路并行）后，按文件粒度继续吃掉 `status=new` 队列的高密度文件。本批 6 路并行，每路负责一个文件（或一组同域文件），实现 agent 自行依据 `translation-contract` §1-12 决定动作。

`status=new`: 3422 → 3051（-371）期望。
`status=translated`: 3260 → 3631（+371）期望。

## Batch composition (6 × ~62 = 371, by-file)

| Batch | 文件 | 条数 | 主要内容性质 |
|:---:|---|:---:|---|
| **A** | `app/src/ai/blocklist/passive_suggestions/static_prompt_suggestions.rs` | 46 | AI 被动建议：静态提示词卡片标题/描述（UI 文本为主） |
| **B** | `app/src/ai/blocklist/block/view_impl/common.rs` + `app/src/settings/ai.rs` | 64 | AI 块视图通用文本 + AI 设置文本（共享 AI 命名空间） |
| **C** | `app/src/ai/agent_tips.rs` + `app/src/terminal/view/ambient_agent/tips.rs` | 80 | Agent 提示语 + 环境 agent 提示语（两类 tips 同域） |
| **D** | `app/src/editor/view/mod.rs` + `app/src/settings_view/appearance_page.rs` | 64 | 编辑器视图 + 外观设置页（UI 文本） |
| **E** | `app/src/settings/import/iterm_parser.rs` + `app/src/terminal/view/init_project/mod.rs` | 65 | iTerm 导入解析 + 工程初始化（init/import 域；解析器多为错误/状态文本） |
| **F** | `app/src/drive/index.rs` + `app/src/search/data_source.rs` | 52 | Warp Drive 索引视图 + 搜索数据源（小型综合域） |

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

## Glossary (沿用 batch-15)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`, `Orchestrate` → `协调`（动词）/ 保留英文（Agent Mode 功能名）, `handoff` → `转交`，`iTerm`/`iTerm2` 保留英文。

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
   - 状态计数：`new` -371, `translated` +371
   - 既有 `translated` 条目未被触碰
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply (expected)

- `new`: 3422 → 3051
- `translated`: 3260 → 3631
- `fuzzy`: 52 (unchanged)
- new entries with `pr-by-file-parallel-batch-16` flag: 371

## Risks / Notes

- 沿用 batch-15 不变量与 apply 脚本结构；仅 BATCH_FLAG / EXPECTED_TOTAL / sub-batch 描述更新。
- batch-15 已经处理过 `app/src/ai/blocklist/block/view_impl/output.rs`，但 `common.rs` / `passive_suggestions/static_prompt_suggestions.rs` 是新文件，无重叠。
- C 批包含 80 条（两个 tips 文件），略高；实现 agent 可一次性吃完，因为两文件均为短句卡片，单条复杂度低。
- F 批 `drive/index.rs` 与 `search/data_source.rs` 是不同域但都偏短、混合 UI + 错误文本，规模适中。
