# batch composition

Total selected: **602** entries across 10 batches (target 600, status=new).

| Batch | files | entries |
|:---:|---|---:|
| **A** | app/src/ai/blocklist/action_model/execute/edit_documents.rs, app/src/ai/control_code_parser.rs, app/src/code/inline_diff.rs, app/src/drive/sharing/dialog/inheritance.rs, … (+10) | 59 |
| **B** | app/src/ai/agent/api/convert_conversation.rs, app/src/ai/agent/task.rs, app/src/ai/blocklist/action_model/execute/run_agents.rs, app/src/ai/skills/skill_manager.rs, … (+11) | 61 |
| **C** | app/src/ai/ambient_agents/scheduled.rs, app/src/ai/blocklist/action_model/execute/call_mcp_tool.rs, app/src/ai/blocklist/agent_view/orchestration_pill_bar.rs, app/src/ai/persisted_workspace.rs, … (+11) | 61 |
| **D** | app/src/ai/ambient_agents/spawn.rs, app/src/ai/blocklist/action_model/execute/request_file_edits.rs, app/src/ai/blocklist/agent_view/zero_state_block.rs, app/src/ai_assistant/requests.rs, … (+11) | 61 |
| **E** | app/src/ai/artifacts/mod.rs, app/src/ai/blocklist/agent_view/agent_view_block.rs, app/src/ai/blocklist/inline_action/aws_bedrock_credentials_error.rs, app/src/ai_assistant/transcript.rs, … (+11) | 61 |
| **F** | app/src/ai/auth_secret_types.rs, app/src/ai/blocklist/controller/input_context.rs, app/src/ai/blocklist/inline_action/orchestration_controls.rs, app/src/auth/auth_override_warning_body.rs, … (+11) | 61 |
| **G** | app/src/ai/blocklist/action_model/execute/get_files.rs, app/src/ai/blocklist/prompt/plan_and_todo_list.rs, app/src/ai/blocklist/prompt/prompt_alert.rs, app/src/code/global_buffer_model.rs, … (+11) | 61 |
| **H** | app/src/ai/blocklist/action_model/execute/request_file_edits/apply_diff_model.rs, app/src/ai/blocklist/suggested_rule_modal.rs, app/src/ai/facts/view/rule.rs, app/src/code/view.rs, … (+11) | 61 |
| **I** | app/src/ai/blocklist/inline_action/web_search.rs, app/src/ai/blocklist/summarization_cancel_dialog.rs, app/src/cloud_object/mod.rs, app/src/code_review/comments/diff_hunk_parser.rs, … (+10) | 58 |
| **J** | app/src/ai/blocklist/telemetry_banner.rs, app/src/ai/harness_availability.rs, app/src/code/editor/view/actions.rs, app/src/coding_entrypoints/project_buttons.rs, … (+10) | 58 |

## Full file-to-batch mapping

### Batch A (59 entries, 14 files)

- `app/src/ai/blocklist/action_model/execute/edit_documents.rs` — 5
- `app/src/ai/control_code_parser.rs` — 3
- `app/src/code/inline_diff.rs` — 5
- `app/src/drive/sharing/dialog/inheritance.rs` — 4
- `app/src/editor/view/element.rs` — 3
- `app/src/pane_group/tree.rs` — 3
- `app/src/session_management.rs` — 4
- `app/src/settings_view/billing_and_usage/billing_cycle_usage_rows.rs` — 5
- `app/src/terminal/local_tty/shell.rs` — 4
- `app/src/terminal/view/context_menu.rs` — 5
- `app/src/workspace/header_toolbar_item.rs` — 4
- `crates/http_client/src/lib.rs` — 5
- `crates/warpui_core/src/image_cache.rs` — 5
- `crates/warpui_core/src/integration/driver.rs` — 4

### Batch B (61 entries, 15 files)

- `app/src/ai/agent/api/convert_conversation.rs` — 3
- `app/src/ai/agent/task.rs` — 3
- `app/src/ai/blocklist/action_model/execute/run_agents.rs` — 5
- `app/src/ai/skills/skill_manager.rs` — 3
- `app/src/context_chips/display_chip.rs` — 5
- `app/src/editor/view/model/display_map/mod.rs` — 3
- `app/src/editor/view/model/selections.rs` — 4
- `app/src/plugin/host/native/mod.rs` — 3
- `app/src/settings_view/environments_page.rs` — 4
- `app/src/settings_view/platform/create_api_key_modal.rs` — 5
- `app/src/terminal/local_tty/terminal_manager.rs` — 4
- `app/src/terminal/view/inline_banner/open_in_warp.rs` — 5
- `crates/ai/src/index/full_source_code_embedding/snapshot.rs` — 4
- `crates/onboarding/src/bin/main.rs` — 5
- `crates/warpui_core/src/ui_components/slider.rs` — 5

### Batch C (61 entries, 15 files)

- `app/src/ai/ambient_agents/scheduled.rs` — 4
- `app/src/ai/blocklist/action_model/execute/call_mcp_tool.rs` — 3
- `app/src/ai/blocklist/agent_view/orchestration_pill_bar.rs` — 5
- `app/src/ai/persisted_workspace.rs` — 4
- `app/src/billing/shared_objects_creation_denied_modal.rs` — 3
- `app/src/editor/view/voice.rs` — 4
- `app/src/env_vars/view/env_var_collection.rs` — 5
- `app/src/experiments/mod.rs` — 3
- `app/src/quit_warning/mod.rs` — 3
- `app/src/settings_view/platform_page.rs` — 4
- `app/src/settings_view/show_blocks_view.rs` — 5
- `app/src/terminal/model/grid/grid_handler.rs` — 4
- `app/src/terminal/view/inline_banner/prompt_suggestions.rs` — 5
- `crates/ai/src/project_context/global_rules.rs` — 4
- `crates/onboarding/src/slides/project_slide.rs` — 5

### Batch D (61 entries, 15 files)

- `app/src/ai/ambient_agents/spawn.rs` — 4
- `app/src/ai/blocklist/action_model/execute/request_file_edits.rs` — 3
- `app/src/ai/blocklist/agent_view/zero_state_block.rs` — 5
- `app/src/ai_assistant/requests.rs` — 4
- `app/src/chip_configurator/modal_shell.rs` — 3
- `app/src/external_secrets/mod.rs` — 3
- `app/src/launch_configs/launch_config.rs` — 4
- `app/src/lib.rs` — 5
- `app/src/referral_theme_status.rs` — 3
- `app/src/settings_view/referrals_page.rs` — 4
- `app/src/terminal/input.rs` — 5
- `app/src/terminal/model/session/command_executor/in_band_command_executor.rs` — 4
- `app/src/themes/theme_chooser.rs` — 5
- `crates/computer_use/src/linux/wayland/mouse.rs` — 4
- `crates/remote_server/src/transport.rs` — 5

### Batch E (61 entries, 15 files)

- `app/src/ai/artifacts/mod.rs` — 4
- `app/src/ai/blocklist/agent_view/agent_view_block.rs` — 3
- `app/src/ai/blocklist/inline_action/aws_bedrock_credentials_error.rs` — 5
- `app/src/ai_assistant/transcript.rs` — 4
- `app/src/code/editor/view.rs` — 3
- `app/src/menu.rs` — 4
- `app/src/notebooks/editor/find_bar.rs` — 5
- `app/src/notebooks/editor/mod.rs` — 3
- `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` — 3
- `app/src/settings_view/warpify_page.rs` — 4
- `app/src/terminal/local_tty/server/mod.rs` — 5
- `app/src/terminal/model/session/command_executor/remote_server_executor.rs` — 4
- `app/src/util/tooltips.rs` — 5
- `crates/computer_use/src/mac/mouse.rs` — 4
- `crates/repo_metadata/src/watcher.rs` — 5

### Batch F (61 entries, 15 files)

- `app/src/ai/auth_secret_types.rs` — 4
- `app/src/ai/blocklist/controller/input_context.rs` — 3
- `app/src/ai/blocklist/inline_action/orchestration_controls.rs` — 5
- `app/src/auth/auth_override_warning_body.rs` — 4
- `app/src/code_review/git_dialog/push.rs` — 3
- `app/src/notebooks/editor/notebook_command.rs` — 3
- `app/src/notebooks/manager.rs` — 4
- `app/src/plugin/host/native/runner.rs` — 5
- `app/src/reward_view.rs` — 3
- `app/src/terminal/cli_agent_sessions/plugin_manager/gemini.rs` — 4
- `app/src/terminal/model/block.rs` — 5
- `app/src/terminal/profile_model_selector.rs` — 4
- `app/src/workspace/cli_install.rs` — 5
- `crates/editor/src/render/element/mod.rs` — 4
- `crates/warp_completer/src/signatures/testing/legacy.rs` — 5

### Batch G (61 entries, 15 files)

- `app/src/ai/blocklist/action_model/execute/get_files.rs` — 4
- `app/src/ai/blocklist/prompt/plan_and_todo_list.rs` — 3
- `app/src/ai/blocklist/prompt/prompt_alert.rs` — 5
- `app/src/code/global_buffer_model.rs` — 4
- `app/src/context_chips/context_chip.rs` — 3
- `app/src/notebooks/notebook/details_bar.rs` — 3
- `app/src/pane_group/mod.rs` — 4
- `app/src/root_view.rs` — 5
- `app/src/search/ai_context_menu/blocks/search_item.rs` — 3
- `app/src/terminal/event.rs` — 4
- `app/src/terminal/prompt_render_helper.rs` — 5
- `app/src/terminal/safe_mode_settings.rs` — 4
- `app/src/workspace/view/conversation_list/view.rs` — 5
- `crates/input_classifier/src/util.rs` — 4
- `crates/warp_logging/src/native.rs` — 5

### Batch H (61 entries, 15 files)

- `app/src/ai/blocklist/action_model/execute/request_file_edits/apply_diff_model.rs` — 4
- `app/src/ai/blocklist/suggested_rule_modal.rs` — 3
- `app/src/ai/facts/view/rule.rs` — 5
- `app/src/code/view.rs` — 4
- `app/src/drive/import/queue.rs` — 3
- `app/src/pane_group/pane/get_started_view.rs` — 3
- `app/src/search/ai_context_menu/diffset/search_item.rs` — 5
- `app/src/search/command_palette/launch_config/renderer.rs` — 4
- `app/src/search/search_bar.rs` — 3
- `app/src/terminal/input/models/data_source.rs` — 4
- `app/src/terminal/settings.rs` — 5
- `app/src/terminal/view/ssh_file_upload.rs` — 4
- `crates/ai/src/index/full_source_code_embedding/codebase_index.rs` — 5
- `crates/warp_core/src/assertions.rs` — 4
- `crates/warp_terminal/src/shell/mod.rs` — 5

### Batch I (58 entries, 14 files)

- `app/src/ai/blocklist/inline_action/web_search.rs` — 4
- `app/src/ai/blocklist/summarization_cancel_dialog.rs` — 3
- `app/src/cloud_object/mod.rs` — 5
- `app/src/code_review/comments/diff_hunk_parser.rs` — 4
- `app/src/drive/workflows/ai_assist.rs` — 3
- `app/src/pane_group/pane/local_harness_launch.rs` — 3
- `app/src/search/command_search/zero_state.rs` — 4
- `app/src/settings/code.rs` — 5
- `app/src/terminal/input/models/view.rs` — 4
- `app/src/terminal/ssh/install_tmux.rs` — 5
- `app/src/terminal/view/use_agent_footer/mod.rs` — 4
- `crates/computer_use/src/bin/use_computer.rs` — 5
- `crates/warp_terminal/src/model/grid/cell.rs` — 4
- `crates/warpui/src/platform/mac/text_layout.rs` — 5

### Batch J (58 entries, 14 files)

- `app/src/ai/blocklist/telemetry_banner.rs` — 3
- `app/src/ai/harness_availability.rs` — 4
- `app/src/code/editor/view/actions.rs` — 5
- `app/src/coding_entrypoints/project_buttons.rs` — 4
- `app/src/drive/workflows/enum_creation_dialog.rs` — 3
- `app/src/pane_group/pane/terminal_pane.rs` — 3
- `app/src/search/searcher.rs` — 4
- `app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs` — 5
- `app/src/terminal/input/rewind/search_item.rs` — 4
- `app/src/terminal/view/ambient_agent/block/entry.rs` — 5
- `app/src/warp_managed_paths_watcher.rs` — 4
- `crates/computer_use/src/linux/x11/mod.rs` — 5
- `crates/warpui/src/windowing/winit/fonts.rs` — 5
- `crates/warpui/src/windowing/winit/windows/network.rs` — 4

