# Translate 385 entries via 6 parallel implementers (batch 18)

## Goal

继 batch-17（383 条 / 6 路并行）后，按文件粒度继续吃掉 `status=new` 队列。本批 6 路并行（每批 ~64 条），实现 agent 自行依据 `translation-contract` §1-12 决定动作。

`status=new`: 2668 → 2283（-385）期望。
`status=translated`: 4014 → 4399（+385）期望。

## Batch composition (6 × ~64 = 385, by-file)

| Batch | 文件 | 条数 | 主要内容性质 |
|:---:|---|:---:|---|
| **A** | `app/src/search/slash_command_menu/static_commands/mod.rs` + `app/src/terminal/input/slash_commands/mod.rs` + `app/src/terminal/model/ansi/mod.rs` + `app/src/workflows/categories.rs` + `app/src/launch_configs/save_modal.rs` | 67 | 斜杠命令、ANSI 模型、工作流分类、启动配置保存 |
| **B** | `crates/warpui/src/rendering/wgpu/resources.rs` + `crates/warpui/examples/{table-sample, flex-expand}/root_view.rs` + `crates/warpui/src/platform/mac/menus.rs` | 59 | warpui 渲染资源 / 示例 / mac 菜单（注意 wgpu_debug_label 与示例 fixture） |
| **C** | `crates/computer_use/src/linux/wayland/{screenshot, session}.rs` + `app/src/autoupdate/linux.rs` + `app/src/font_fallback.rs` + `crates/warp_util/src/path.rs` | 65 | Linux Wayland / 自动更新 / 字体回退 / 路径工具（多为底层逻辑，注意 panic/telemetry） |
| **D** | `app/src/auth/{auth_view_body, login_slide}.rs` + `app/src/billing/shared_objects_creation_denied_body.rs` + `app/src/settings_view/{teams_page, privacy_page}.rs` | 66 | 登录视图 / 计费弹窗 / 团队 + 隐私设置（典型 UI 文本） |
| **E** | `app/src/terminal/shared_session/viewer/network.rs` + `app/src/workspace/mod.rs` + `app/src/terminal/warpify/settings.rs` + `app/src/terminal/block_list_element.rs` + `app/src/notebooks/notebook.rs` | 67 | 共享会话网络、工作区、warpify 设置、命令块列表、笔记本 |
| **F** | `app/src/ai/blocklist/block/cli.rs` + `app/src/ai/blocklist/inline_action/{code_diff_view, run_agents_card_view}.rs` + `app/src/ai/conversation_details_panel.rs` + `app/src/ai/agent/conversation_yaml.rs` | 61 | AI 命令块 CLI / 内联动作 / 会话详情 / YAML 对话（注意 yaml 字段 key 可能是 protocol_key 候选） |

候选文件：`candidates/batch-{A..F}.json`。每条字段 `{id, source, file, line, occurrences_kind, source_hash, audit_verdict, occurrences_count, occurrences_all}`。

## Per-entry decision flow (实现 agent 自行判断)

严格按以下顺序，第一条命中即终止：

1. **doc-comment 假阳性**：源为文档注释片段（`/// ...`、文档块）→ `flag, do_not_translate, extractor_false_positive_doc_comment`，`target=null`。
2. **panic / .expect / unreachable / debug_assert** 字面量 → §10 `flag_panic_message`，`target=null`。
3. **telemetry / 日志-only 字面量**（追到 sink 是 `tracing::*`、telemetry pipeline、log file 而非 UI）→ §11 `flag_telemetry_payload`，`target=null`。
4. **`fn search_terms()` 返回的关键词串** → §12 双语追加 `<英文> <中文>`，`flag=search_terms_bilingual`。
5. **wgpu debug label / 测试 fixture / 外部协议键（如 YAML 字段名、Wayland 协议串）** → 相应子标签（`wgpu_debug_label` / `test_fixture` / `protocol_key`），`target=null`。
6. **常规 UI 文本** → 译为中文，遵守 §1-7（占位符、glossary、全角标点、`您`、register）。

### 本批专项提示

- **Batch B**：`warpui/examples/*` 多为开发示例，字面量很可能是 fixture/debug-label，不向终端用户暴露 → 倾向 `flag_test_fixture` 或 `flag_wgpu_debug_label`，但仍逐条看 caller。`wgpu/resources.rs` 多为 wgpu debug label。
- **Batch C**：`wayland/*.rs` 多为系统集成日志，需追 sink；`autoupdate/linux.rs` 错误消息常出现在通知 UI，需翻译。`warp_util/src/path.rs` 多为内部 utility，注意 panic 字面量。
- **Batch F**：`conversation_yaml.rs` 中的 YAML 字段 key（如 `"role"`, `"content"`, `"name"` 等用于序列化 schema 的字符串）属于 `protocol_key`，target=null；user-facing 文本则翻译。

## Action-hint actions (output JSON 用)

- `translate` → `target=<中文>`, no extra subflag (BATCH_FLAG 自动加)。
- `flag_panic_message` / `flag_telemetry_payload` / `flag_extractor_false_positive_doc_comment` / `flag_test_fixture` / `flag_wgpu_debug_label` / `flag_protocol_key` → `target=null`, `do_not_translate_subflags=[<sub>]`。
- `bilingual_search_terms` → `target=<英文> <中文>`, 加入 `bilingual_search_terms_ids`。

## Glossary (沿用 batch-17)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`, `Orchestrate` → `协调`（动词）/ 保留英文（Agent Mode 功能名）, `handoff` → `转交`，`iTerm`/`iTerm2` 保留英文，`SSH` 保留，`AWS` 保留，`Wayland` 保留，`X11` 保留。

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

1. 6 路 trellis-implement 并行（opus）。每路读自己的 `candidates/batch-{X}.json` + 翻译规约 + 源码（在 `../warp` 工作目录）。
2. 主 orchestrator 收齐 6 份 output，运行 `apply_translations.py` 合并到 `translations/strings.json`。
3. trellis-check 验证：
   - placeholder/strftime/whitespace/brand 不变量
   - 状态计数：`new` -385, `translated` +385
   - 既有 `translated` 条目未被触碰
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply (expected)

- `new`: 2668 → 2283
- `translated`: 4014 → 4399
- `fuzzy`: 52 (unchanged)
- new entries with `pr-by-file-parallel-batch-18` flag: 385
