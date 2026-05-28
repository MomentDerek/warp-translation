# Translate 360 entries via 6 parallel implementers (batch 14)

## Goal

继 batch-13（180 条、首次 6 路并行）后，本批将吞吐再翻一倍：**6 路并行 × 60 条 = 360 条**，按文件粒度指派（每批锁定一个文件），把当前 `status=new` 队列中的几个高密度文件一次性吃掉大头。

`status=new`: 4113 → 3753（-360）期望。

## Batch composition (6 × 60 = 360, single-file each)

每批锁定一个文件、取该文件最早出现的 60 条（按 `line` 升序），全部 `audit_verdict=uncertain`。每条由实现 agent 自行依据 [translation-contract](../../../spec/guides/translation-contract.md) §1-12 决定动作（translate / flag_panic_message / flag_telemetry_payload / bilingual_search_terms / flag_test_fixture / flag_extractor_false_positive_doc_comment / flag_wgpu_debug_label 等）。

| Batch | 文件 | 文件总 new 数 | 本批取数 | 主要内容性质 |
|:---:|---|:---:|:---:|---|
| **A** | `crates/ai/src/agent/action_result/mod.rs` | 116 | 60 | Agent action 结果展示标签 + 状态文本（多为 UI 翻译，少量 telemetry / panic）|
| **B** | `app/src/terminal/view.rs` | 114 | 60 | Terminal 视图：doc-comment、UI 文本、panic、telemetry 混合 |
| **C** | `app/src/workspace/view.rs` | 99 | 60 | Workspace 错误消息、Agent 面板 a11y、handoff 提示（多为 UI 翻译） |
| **D** | `app/src/settings/ai.rs` | 83 | 60 | AI 设置：tooltip + test fixture（"Can parse default … rule"）+ 说明文本 |
| **E** | `crates/warpui/examples/table-sample/root_view.rs` | 75 | 60 | warpui examples/ 下示例 demo — **整文件**为 example 二进制，多数应 `do_not_translate`（建议 `test_fixture` 或新子标签；见下方说明） |
| **F** | `app/src/terminal/input.rs` | 65 | 60 | Terminal 输入：UI 文本、doc-comment、handoff 提示 |

候选文件：`candidates/batch-{A..F}.json`，每条字段 `{id, source, file, line, occurrences_kind, source_hash, audit_verdict}`。

## Per-entry decision flow (实现 agent 自行判断)

按以下顺序：

1. **doc-comment 假阳性**：源以 `///` 或 ` ` 前缀、内容是 Rust 文档注释 → `flag, do_not_translate, extractor_false_positive_doc_comment`，`target=null`。
2. **panic / .expect / unreachable / debug_assert** 字面量 → §10 `flag_panic_message`，`target=null`。
3. **telemetry / 日志-only 字面量**（追到 sink 是 `tracing::*`、telemetry pipeline、log file 而非 UI）→ §11 `flag_telemetry_payload`，`target=null`。
4. **`fn search_terms()` 返回的关键词串** → §12 双语追加 `<英文> <中文>`，`flag=search_terms_bilingual`（不是 do_not_translate）。
5. **wgpu debug label / examples 内的 demo 数据**：
   - wgpu `TextureDescriptor.label` 等 → `flag, do_not_translate, wgpu_debug_label`。
   - **batch-E 整文件为 `warpui/examples/table-sample/` 下的 demo 二进制**，按 [[project_translation_flag_test_fixture]] 类比处置：默认 `flag, do_not_translate, test_fixture`，`target=null`。若个别字符串确为示例标题/说明且对真实用户有教学价值，可选择翻译，但 **优先 flag**。
6. **常规 UI 文本** → 译为中文，遵守 §1-7（占位符、glossary、全角标点、`您`、register）。

## Action-hint actions (output JSON 用)

- `translate` → `target=<中文>`, no extra subflag (BATCH_FLAG 自动加)。
- `flag_panic_message` / `flag_telemetry_payload` / `flag_extractor_false_positive_doc_comment` / `flag_test_fixture` / `flag_wgpu_debug_label` → `target=null`, `do_not_translate_subflags=[<sub>]`。
- `bilingual_search_terms` → `target=<英文> <中文>`, 加入 `bilingual_search_terms_ids`。

## Glossary (沿用)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`。本批新增候选：
- `Orchestrate` / `orchestrate` → 上下文决定：`协调`（动词）或保留 `Orchestrate`（指 Agent Mode 中的批量子 agent 功能）
- `Ambient Agent` → `环境代理`（或保留英文，由 agent 判断）
- `handoff` → `转交`（如 "Handoff to cloud" → `转交到云端`）

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
   - 状态计数：`new` -360, `translated` +360
   - 不变量未触动既有 translated 条目
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply

期望：`translated` 2569 → 2929 (+360), `new` 4113 → 3753 (-360), `fuzzy` 52 (不变), `entry_count` 6734 (不变)。

## Notes

- 6 个文件互不相交，候选 ID 跨批互斥（generator 已校验 360 unique ids）。
- 单文件批：实现 agent 可以读源文件上下文（`../warp/` 是 source 副本）来判定 panic / telemetry / UI sink。
- batch-E (`table-sample/root_view.rs`) 是 **整文件 examples 子集**，预期大部分将被 `flag_test_fixture` 而非翻译。这是 OK 的——examples/ 下的 demo 字符串不上线，按既有 [[project_translation_flag_test_fixture]] 政策处理。
