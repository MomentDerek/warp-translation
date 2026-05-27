# Translate 602 entries via 10 parallel implementers (batch 20)

## Goal

继 batch-19（380 条 / 6 路并行）后，按文件粒度继续吃掉 `status=new` 队列。本批 **10 路并行**（每批 57–63 条），实现 agent 自行依据 `translation-contract` §1-12 决定动作。文件不跨批拆分。

- `status=new`: 1903 → 1301（-602）期望
- `status=translated`: 4779 → 5381（+602）期望
- `status=fuzzy`: 52（unchanged）

## Batch composition (10 × 57–63 = 602, by-file)

候选文件：`candidates/batch-{A..J}.json`。每条字段 `{id, source, file, line, occurrences_kind, source_hash, audit_verdict, occurrences_count, occurrences_all}`。完整文件→批次映射见 `research/batch-20-composition.md`。

| Batch | 文件（主要） | 条数 | 提示 |
|:---:|---|:---:|---|
| **A** | `crates/websocket/src/proxy.rs` (12), `app/src/window_settings.rs` (8), `crates/onboarding/src/callout/view.rs` (7), `app/src/drive/import/modal_body.rs` (7), `app/src/auth/auth_view_shared_helpers.rs` (6), `crates/computer_use/src/mac/keyboard.rs` (6), `app/src/search/command_palette/new_session/data_source.rs` (6), `app/src/terminal/ssh/util.rs` (6) | 58 | websocket proxy 多为日志 / panic；onboarding callout 直白 UI；mac keyboard 多 protocol_key / panic |
| **B** | `crates/ui_components/examples/library.rs` (11), `app/src/settings/import/config.rs` (8), `app/src/input_suggestions.rs` (7), `app/src/ai/blocklist/action_model/execute/grep.rs` (7), `crates/warp_core/src/semantic_selection/mod.rs` (7), `app/src/settings/privacy.rs` (6), `app/src/terminal/view/ambient_agent/auth_secret_ftux_view.rs` (6), `crates/managed_secrets/src/gcp.rs` (6) | 58 | `settings/privacy.rs` 大概率含 search_terms 双语区；`ui_components/examples` 多为 demo 标签；`managed_secrets/gcp.rs` 多为 panic/telemetry |
| **C** | `crates/warp_features/src/lib.rs` (11), `app/src/tab.rs` (8), `app/src/ai/blocklist/controller.rs` (7), `app/src/pane_group/pane/mod.rs` (7), `crates/warpui/examples/frame-capture-test/root_view.rs` (7), `app/src/settings_view/main_page.rs` (6), `app/src/terminal/view/ambient_agent/first_time_setup.rs` (6), `crates/warpui/examples/list/root_view.rs` (6) | 58 | `warp_features/lib.rs` 多为 feature flag 名 → protocol_key；warpui examples 多 demo label；`settings_view/main_page.rs` 含 search_terms |
| **D** | `app/src/autoupdate/mac.rs` (10), `app/src/code_review/git_dialog/commit.rs` (9), `app/src/ai/blocklist/task_status_sync_model.rs` (7), `app/src/search/command_search/view.rs` (7), `app/src/ai/agent/util.rs` (6), `app/src/auth/login_failure_notification.rs` (6), `app/src/tab_configs/new_worktree_modal.rs` (6), `app/src/terminal/view/inline_banner/shared_sessions.rs` (6), `crates/warpui/examples/resizable/root_view.rs` (6) | 63 | autoupdate/mac 含通知文案 + panic 混合；commit dialog 是 UI；login_failure 是 UI 通知 |
| **E** | `app/src/code/lsp_telemetry.rs` (10), `app/src/search/ai_context_menu/view.rs` (9), `app/src/ai/facts/view/rule_editor.rs` (7), `app/src/terminal/universal_developer_input.rs` (7), `app/src/ai/ai_document_view.rs` (6), `app/src/auth/mod.rs` (6), `app/src/tab_configs/session_config_rendering.rs` (6), `app/src/themes/theme_creator_body.rs` (6), `crates/warpui_core/src/async/native/mod.rs` (6) | 63 | **lsp_telemetry 全部 flag_telemetry_payload**；theme_creator_body 含主题名（区分 label / identifier）；async/native 多 panic |
| **F** | `crates/computer_use/src/windows/screenshot.rs` (10), `app/src/terminal/view/shared_session/conversation_ended_tombstone_view.rs` (9), `app/src/ai_assistant/panel.rs` (7), `app/src/terminal/view/inline_banner/notifications_discovery.rs` (7), `app/src/ai/ambient_agents/task.rs` (6), `app/src/code/file_tree/view.rs` (6), `app/src/terminal/alt_screen/alt_screen_element.rs` (6), `app/src/uri/mod.rs` (6), `crates/warpui_core/src/elements/formatted_text_element.rs` (6) | 63 | computer_use/windows/screenshot 多 panic/telemetry；tombstone / inline_banner 是终端用户可见 UI |
| **G** | `crates/warpui/src/windowing/winit/delegate.rs` (10), `crates/settings/src/macros.rs` (9), `app/src/code/editor/element/gutter_button.rs` (7), `app/src/terminal/view/ssh_remote_server_choice_view.rs` (7), `app/src/ai/artifacts/buttons.rs` (6), `app/src/code/local_code_editor.rs` (6), `app/src/terminal/available_shells.rs` (6), `app/src/util/file/external_editor/settings.rs` (6), `crates/warpui_core/src/text/header.rs` (6) | 63 | winit/delegate / settings macros 多 telemetry/panic；ssh_remote_server_choice 是 UI；external_editor/settings 含 search_terms |
| **H** | `crates/warpui_core/src/core/app.rs` (10), `crates/computer_use/src/linux/x11/mouse.rs` (8), `app/src/ai/llms.rs` (8), `app/src/workspace/action.rs` (7), `app/src/ai/blocklist/agent_view/agent_input_footer/toolbar_item.rs` (6), `app/src/coding_entrypoints/create_project_view.rs` (6), `app/src/terminal/cli_agent_sessions/plugin_manager/claude.rs` (6), `app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs` (6), `app/src/ai/artifact_download.rs` (5) | 62 | warpui_core/app + linux/x11/mouse 多 panic/telemetry；llms.rs 含 LLM 模型名 → protocol_key；hoa_onboarding 是 UI |
| **I** | `crates/warpui_core/src/integration/capture_recorder.rs` (10), `app/src/ai/mcp/file_mcp_watcher.rs` (8), `crates/repo_metadata/src/local_model.rs` (8), `app/src/workspace/view/free_tier_limit_hit_modal.rs` (7), `app/src/ai/blocklist/orchestration_events.rs` (6), `app/src/context_chips/node_version_popup.rs` (6), `app/src/terminal/general_settings.rs` (6), `crates/ai/src/diff_validation/mod.rs` (6) | 57 | capture_recorder 多 telemetry；free_tier_limit_hit_modal 是 UI；general_settings 含 search_terms；orchestration_events 多 telemetry |
| **J** | `crates/warpui_core/src/integration/step.rs` (10), `app/src/autoupdate/mod.rs` (8), `crates/warpui/examples/flex/root_view.rs` (8), `crates/editor/src/content/buffer.rs` (7), `app/src/ai/outline/native.rs` (6), `app/src/notebooks/link.rs` (6), `app/src/terminal/keys_settings.rs` (6), `crates/computer_use/src/linux/wayland/keyboard.rs` (6) | 57 | integration/step 多 telemetry；autoupdate/mod 是 UI；keys_settings 含 search_terms；wayland/keyboard 多 protocol_key |

## Per-entry decision flow (实现 agent 自行判断)

严格按以下顺序，**第一条命中即终止**：

1. **doc-comment 假阳性**：源为文档注释片段（`/// ...`、文档块）→ `flag, do_not_translate, extractor_false_positive_doc_comment`，`target=null`。
2. **panic / .expect / unreachable / debug_assert** 字面量 → §10 `flag_panic_message`，`target=null`。
3. **telemetry / 日志-only 字面量**（追到 sink 是 `tracing::*`、telemetry pipeline、log file 而非 UI）→ §11 `flag_telemetry_payload`，`target=null`。
4. **`fn search_terms()` 返回的关键词串** → §12 双语追加 `<英文> <中文>`，加入 `bilingual_search_terms_ids`。
5. **wgpu debug label / 测试 fixture / 外部协议键（YAML 字段名、序列化 schema、theme/feature/model identifier）** → 相应子标签（`wgpu_debug_label` / `test_fixture` / `protocol_key`），`target=null`。
6. **常规 UI 文本** → 译为中文，遵守 §1-7（占位符、glossary、全角标点、`您`、register）。

### 本批专项提示

- **lsp_telemetry.rs（Batch E）**：函数名直接挂 telemetry —— 默认全部 `flag_telemetry_payload`，除非确实 trace 到 UI sink（罕见）。
- **integration/{capture_recorder, step}.rs / settings/macros.rs（Batch G / I / J）**：integration framework 日志/录制，几乎全部 `flag_telemetry_payload` 或 `flag_panic_message`。
- **warp_features/lib.rs（Batch C）**：feature flag 标识符（如 `"enable_xxx"`）→ `flag_protocol_key`；feature 的 UI 描述文字 → 翻译。
- **themes/theme_creator_body.rs（Batch E）**：主题名 identifier（如 `"dracula"`、序列化键）→ `flag_protocol_key`；主题显示标签 → 翻译。著名主题名（Dracula、Solarized、Monokai 等）保留英文。
- **ai/llms.rs（Batch H）**：LLM 模型 identifier（如 `"claude-3-5-sonnet"`、`"gpt-4"`）→ `flag_protocol_key`；UI 显示标签 → 翻译。
- **computer_use/{mac,linux,windows} keyboard / mouse / screenshot**：键名（如 `"shift"`、`"ctrl"`）→ `flag_protocol_key`；错误/panic → `flag_panic_message`；trace 日志 → `flag_telemetry_payload`。
- **search_terms 双语区**：以 `fn search_terms` 形式出现的关键词；新增中文同义关键词在原字面后追加一个半角空格再加中文，无标点。
- **websocket/proxy.rs、managed_secrets/gcp.rs、warpui_core/core/app.rs**：高度集中在 panic/telemetry，几乎不会有真正 UI 字符串；逐条 trace。
- **`crates/onboarding`、`*/inline_banner/*`、`*/auth*`、`*/tab*`、`*/settings_view*`、`*/workspace/view/*`、各类 `view.rs`/`modal*.rs`**：高概率 UI，直白翻译。

## Action-hint actions (output JSON 用)

- `translate` → `target=<中文>`, no extra subflag (BATCH_FLAG `pr-by-file-parallel-batch-20` 由 apply 脚本自动加)。
- `flag_panic_message` / `flag_telemetry_payload` / `flag_extractor_false_positive_doc_comment` / `flag_test_fixture` / `flag_wgpu_debug_label` / `flag_protocol_key` → `target=null`, `do_not_translate_subflags=[<sub>]`。
- `bilingual_search_terms` → `target=<英文> <中文>`, 加入 `bilingual_search_terms_ids`。

## Glossary (沿用 batch-19)

`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `Code Review`, `chip`, `token`, `Handoff`, `cloud task`, `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词`(AI) / `提示符`(shell), `tab` → `标签页`, `Orchestrate` → `协调`（动词）/ 保留英文（Agent Mode 功能名）, `handoff` → `转交`, `iTerm`/`iTerm2` 保留英文, `SSH` 保留, `AWS` 保留, `Wayland` 保留, `X11` 保留, `HPKE` 保留, `Node.js` 保留, `tmux` 保留, `GraphQL` 保留, `LSP` 保留, `MCP` 保留, `winit` 保留, `wgpu` 保留。

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

1. **10 路 trellis-implement 并行**（opus）。每路读自己的 `candidates/batch-{X}.json` + 翻译规约 (`.trellis/spec/guides/translation-contract.md`) + 源码（在 `<HOME>/Documents/Codes/warp` 工作目录）。
2. 主 orchestrator 收齐 10 份 output → 运行 `apply_translations.py` 合并到 `translations/strings.json`（仓库根目录，非 `tools/translations/`）。
3. trellis-check 验证：
   - placeholder/strftime/whitespace/brand 不变量
   - 状态计数：`new` -602, `translated` +602
   - 既有 `translated` 条目未被触碰
   - flag 闭包：每条 null target 都有 sub-flag；每条 sub-flag 都有 null target

## Counts after apply (expected)

- `new`: 1903 → 1301
- `translated`: 4779 → 5381
- `fuzzy`: 52 (unchanged)
- new entries with `pr-by-file-parallel-batch-20` flag: 602
