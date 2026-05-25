# Translate 383 entries via 6 parallel implementers (batch 17)

## Goal

继 batch-16（371 条 / 6 路并行）后，按文件粒度继续吃掉 `status=new` 队列。本批 6 路并行（每批 ~63 条），实现 agent 自行依据 `translation-contract` §1-12 决定动作。

`status=new`: 3051 → 2668（-383）期望。
`status=translated`: 3631 → 4014（+383）期望。

## Batch composition (6 × ~63 = 383, by-file)

| Batch | 文件 | 条数 | 主要内容性质 |
|:---:|---|:---:|---|
| **A** | `app/src/code_review/{telemetry_event, git_dialog/mod, code_review_view, comment_list_view}.rs` | 66 | Code Review 域（telemetry + UI + 对话框） |
| **B** | `app/src/ai/blocklist/action_model/execute/request_file_edits/diff_application.rs` + `app/src/ai/mcp/templatable_manager/native.rs` + `app/src/ai/aws_credentials.rs` | 67 | AI 内部：diff 执行 / MCP 模板管理 / AWS 凭据 |
| **C** | `app/src/terminal/view/block_onboarding/onboarding_agentic_suggestions_block.rs` + `app/src/ai/blocklist/{usage/conversation_usage_view, block/view_impl/orchestration}.rs` + `app/src/ai/execution_profiles/mod.rs` | 63 | onboarding 建议 + AI 用量 / orchestration / 执行 profile |
| **D** | `app/src/workspace/tab_settings.rs` + `app/src/settings_view/{update_environment_form, mod}.rs` | 57 | 工作区与设置页面（UI 文本） |
| **E** | `app/src/remote_server/server_model.rs` + `crates/remote_server/src/client/mod.rs` + `app/src/terminal/{ssh/error, share_block_modal}.rs` | 65 | 远程会话 / SSH 错误 / 共享命令块 |
| **F** | `app/src/workspace/view/{build_plan_migration_modal, launch_modal/oz_launch}.rs` + `app/src/cloud_object/toast_message.rs` + `app/src/context_chips/mod.rs` | 65 | 工作区视图 / Toast / 上下文 chip |

候选文件：`candidates/batch-{A..F}.json`，每条字段 `{id, source, file, line, occurrences_kind, source_hash, audit_verdict}`。所有条目 `audit_verdict=uncertain`。

## Per-entry decision flow (实现 agent 自行判断)

严格按以下顺序，第一条命中即终止：

1. **doc-comment 假阳性**：源以 `///` 或文档结构（开头空白 + 注释体）+ Rust 文档语义 → `flag, do_not_translate, extractor_false_positive_doc_comment`，`target=null`。
2. **panic / .expect / unreachable / debug_assert** 字面量 → §10 `flag_panic_message`，`target=null`。
3. **telemetry / 日志-only 字面量**（追到 sink 是 `tracing::*`、telemetry pipeline、log file 而非 UI）→ §11 `flag_telemetry_payload`，`target=null`。注意 `code_review/telemetry_event.rs` 文件名即提示，但仍需逐条追 sink 确认。
4. **`fn search_terms()` 返回的关键词串** → §12 双语追加 `<英文> <中文>`，`flag=search_terms_bilingual`（不是 do_not_translate）。
5. **wgpu debug label / 测试 fixture / protocol_key** 等外部协议键 → 相应子标签，`target=null`。
6. **常规 UI 文本** → 译为中文，遵守 §1-7（占位符、glossary、全角标点、`您`、register）。

## Action-hint actions (output JSON 用)

- `translate` → `target=<中文>`, no extra subflag (BATCH_FLAG 自动加)。
- `flag_panic_message` / `flag_telemetry_payload` / `flag_extractor_false_positive_doc_comment` / `flag_test_fixture` / `flag_wgpu_debug_label` → `target=null`, `do_not_translate_subflags=[<sub>]`。
- `bilingual_search_terms` → `target=<英文> <中文>`, 加入 `bilingual_search_terms_ids`。

## Glossary (沿用 batch-16)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`, `Orchestrate` → `协调`（动词）/ 保留英文（Agent Mode 功能名）, `handoff` → `转交`，`iTerm`/`iTerm2` 保留英文，`SSH` 保留，`AWS` 保留。

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
   - 状态计数：`new` -383, `translated` +383
   - 既有 `translated` 条目未被触碰
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply (expected)

- `new`: 3051 → 2668
- `translated`: 3631 → 4014
- `fuzzy`: 52 (unchanged)
- new entries with `pr-by-file-parallel-batch-17` flag: 383

## Risks / Notes

- Batch A 包含 `code_review/telemetry_event.rs`：文件名提示 telemetry，但仍需逐条追 sink 确认（不要无脑全部 flag）。
- Batch B 的 `diff_application.rs` 可能含较多 panic/assert 字面量（diff 应用逻辑常见 invariant 校验），逐条判断。
- Batch B 的 `aws_credentials.rs` 可能含错误消息（panic-vs-UI 需要看 caller）。
- Batch E 的 SSH `error.rs` 多为 `thiserror` / `anyhow` 错误文本：通常是 UI（用户看得到 SSH 失败原因），但部分仅传到 telemetry — 追 sink 决定。
