# Translate 380 entries via 6 parallel implementers (batch 19)

## Goal

继 batch-18（385 条 / 6 路并行）后，按文件粒度继续吃掉 `status=new` 队列。本批 6 路并行（每批 61–68 条），实现 agent 自行依据 `translation-contract` §1-12 决定动作。

`status=new`: 2283 → 1903（-380）期望。
`status=translated`: 4399 → 4779（+380）期望。

## Batch composition (6 × 61–68 = 380, by-file)

| Batch | 文件 | 条数 | 主要内容性质 |
|:---:|---|:---:|---|
| **A** | `app/src/settings_view/code_page.rs` + `app/src/settings/{mod, input, editor, font}.rs` | 61 | 设置面板（代码 / 输入 / 编辑器 / 字体）— UI label / search_terms 候选区 |
| **B** | `crates/ai/src/aws_credentials.rs` + `app/src/ai/blocklist/block/status_bar.rs` + `app/src/ai/blocklist/inline_action/{ask_user_question_view, requested_command, search_codebase}.rs` + `app/src/ai/blocklist/block.rs` + `app/src/ai/blocklist/action_model/execute/start_agent.rs` | 61 | AI 命令块 / inline-action / agent 执行启动 |
| **C** | `app/src/terminal/shared_session/{sharer/network, share_modal/body}.rs` + `app/src/terminal/session_settings.rs` + `app/src/terminal/buy_credits_banner.rs` + `app/src/terminal/view/ambient_agent/loading_screen.rs` + `app/src/terminal/model/{early_output, tmux/parser}.rs` | 61 | 终端共享会话 / 会话设置 / tmux parser（注意 panic 候选） |
| **D** | `app/src/workspace/view/{cloud_agent_capacity_modal/mod, global_search/view}.rs` + `crates/onboarding/src/{lib, slides/agent_slide, slides/free_user_no_ai_slide}.rs` + `app/src/workflows/workflow_view.rs` + `app/src/notebooks/file/mod.rs` | 67 | onboarding slide / 工作流 / 笔记本 / cloud agent 弹窗（典型 UI） |
| **E** | `app/src/themes/default_themes.rs` + `app/src/drive/{export, sharing/dialog/mod}.rs` + `app/src/util/file/external_editor/mod.rs` + `app/src/code/editor/find/view.rs` + `app/src/workspaces/gql_convert.rs` | 68 | 主题命名 / Drive 导出与分享 / 外部编辑器 / 查找视图 / GraphQL 转换（注意 protocol_key / 主题名是否为标识符） |
| **F** | `crates/warp_terminal/src/model/mode.rs` + `crates/node_runtime/src/lib.rs` + `crates/managed_secrets/src/envelope/hpke_impl.rs` + `crates/editor/src/render/model/debug.rs` | 62 | 终端模式 / Node runtime / HPKE 加密信封 / editor 调试输出（多为 panic/telemetry） |

候选文件：`candidates/batch-{A..F}.json`。每条字段 `{id, source, file, line, occurrences_kind, source_hash, audit_verdict, occurrences_count, occurrences_all}`。详细文件 → 条数映射见 `research/batch-19-composition.md`。

## Per-entry decision flow (实现 agent 自行判断)

严格按以下顺序，第一条命中即终止：

1. **doc-comment 假阳性**：源为文档注释片段（`/// ...`、文档块）→ `flag, do_not_translate, extractor_false_positive_doc_comment`，`target=null`。
2. **panic / .expect / unreachable / debug_assert** 字面量 → §10 `flag_panic_message`，`target=null`。
3. **telemetry / 日志-only 字面量**（追到 sink 是 `tracing::*`、telemetry pipeline、log file 而非 UI）→ §11 `flag_telemetry_payload`，`target=null`。
4. **`fn search_terms()` 返回的关键词串** → §12 双语追加 `<英文> <中文>`，`flag=search_terms_bilingual`。
5. **wgpu debug label / 测试 fixture / 外部协议键（如 YAML 字段名、序列化 schema、theme identifier）** → 相应子标签（`wgpu_debug_label` / `test_fixture` / `protocol_key`），`target=null`。
6. **常规 UI 文本** → 译为中文，遵守 §1-7（占位符、glossary、全角标点、`您`、register）。

### 本批专项提示

- **Batch A**：`settings/{input,editor,font}.rs` 大概率有 `fn search_terms()` 关键词区（沿用 batch-12/15/16 风格 → 双语追加）。`code_page.rs` 多为 UI label。
- **Batch B**：`crates/ai/src/aws_credentials.rs` 与 batch-17 burned 的 `app/src/ai/aws_credentials.rs` 是**不同文件**（crate vs app）。trace sink 决定每条是否 UI；`start_agent.rs` 启动错误大概率 UI 可见。
- **Batch C**：`terminal/model/early_output.rs` / `tmux/parser.rs` 多为 model 层 parser，注意 `panic!` / `unreachable!` / debug log → 多走 `flag_panic_message` / `flag_telemetry_payload`。
- **Batch D**：`crates/onboarding/*` 是终端用户首屏 — 直白翻译。
- **Batch E**：`themes/default_themes.rs` 的主题字面量需区分 **显示标签**（翻译）vs **identifier/序列化 key**（`flag_protocol_key`）。著名主题专有名词（Dracula、Solarized 等）保留英文。`workspaces/gql_convert.rs` 多为 GraphQL 字段名 → `flag_protocol_key`。
- **Batch F**：`hpke_impl.rs`、`editor/render/model/debug.rs` 几乎可以默认 `flag_panic_message` / `flag_telemetry_payload`；`warp_terminal/model/mode.rs` 模式名要看是否对外（"Normal"/"Insert" 这种通常是 UI label）；`node_runtime/lib.rs` 混杂，需逐条 trace。

## Action-hint actions (output JSON 用)

- `translate` → `target=<中文>`, no extra subflag (BATCH_FLAG 自动加)。
- `flag_panic_message` / `flag_telemetry_payload` / `flag_extractor_false_positive_doc_comment` / `flag_test_fixture` / `flag_wgpu_debug_label` / `flag_protocol_key` → `target=null`, `do_not_translate_subflags=[<sub>]`。
- `bilingual_search_terms` → `target=<英文> <中文>`, 加入 `bilingual_search_terms_ids`。

## Glossary (沿用 batch-18)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`, `Orchestrate` → `协调`（动词）/ 保留英文（Agent Mode 功能名）, `handoff` → `转交`，`iTerm`/`iTerm2` 保留英文，`SSH` 保留，`AWS` 保留，`Wayland` 保留，`X11` 保留，`HPKE` 保留，`Node.js` 保留，`tmux` 保留，`GraphQL` 保留。

## Output schema (each implementer agent)

写入 `outputs/batch-{X}-output.json`：

```json
{
  "translations": {"<id>": "<中文>" | null, ...},
  "do_not_translate_subflags": {"<id>": ["panic_message" | "telemetry_payload" | "extractor_false_positive_doc_comment" | "test_fixture" | "wgpu_debug_label" | "protocol_key"], ...},
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

1. 6 路 trellis-implement 并行（opus）。每路读自己的 `candidates/batch-{X}.json` + 翻译规约 + 源码（在 `<HOME>/Documents/Codes/warp` 工作目录）。
2. 主 orchestrator 收齐 6 份 output，运行 `apply_translations.py` 合并到 `translations/strings.json`（仓库根目录，非 `tools/translations/`）。
3. trellis-check 验证：
   - placeholder/strftime/whitespace/brand 不变量
   - 状态计数：`new` -380, `translated` +380
   - 既有 `translated` 条目未被触碰
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply (expected)

- `new`: 2283 → 1903
- `translated`: 4399 → 4779
- `fuzzy`: 52 (unchanged)
- new entries with `pr-by-file-parallel-batch-19` flag: 380
