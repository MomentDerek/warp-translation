# batch composition

Total selected: **600** entries across 8 batches (target 600, status=new).

| Batch | files | entries |
|:---:|---|---:|
| **A** | app/src/ai/blocklist/action_model/execute/read_skill.rs, app/src/ai/blocklist/action_model/execute/request_computer_use.rs, app/src/ai/blocklist/controller/response_stream.rs, app/src/ai/blocklist/history_model.rs, … (+36) | 75 |
| **B** | app/src/ai/blocklist/action_model/execute/search_codebase.rs, app/src/ai/blocklist/action_model/execute/upload_artifact.rs, app/src/ai/blocklist/inline_action/requested_action.rs, app/src/ai/blocklist/inline_action/web_fetch.rs, … (+36) | 75 |
| **C** | app/src/ai/blocklist/agent_view/agent_input_footer/editor.rs, app/src/ai/blocklist/agent_view/agent_message_bar.rs, app/src/ai/blocklist/inline_action/requested_script.rs, app/src/ai/blocklist/suggestion_chip_view.rs, … (+36) | 75 |
| **D** | app/src/ai/blocklist/agent_view/agent_input_footer/environment_selector.rs, app/src/ai/blocklist/agent_view/orchestration_conversation_links.rs, app/src/ai/blocklist/passive_suggestions/legacy.rs, app/src/ai/document/orchestration_config_block.rs, … (+36) | 75 |
| **E** | app/src/ai/agent/api/convert_to.rs, app/src/ai/agent_conversations_model.rs, app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs, app/src/ai/blocklist/block/pending_user_query_block.rs, … (+37) | 75 |
| **F** | app/src/ai/agent/conversation.rs, app/src/ai/agent_conversations_model/entry.rs, app/src/ai/blocklist/block/model/debug_model_impl.rs, app/src/ai/blocklist/block/view_impl/todos.rs, … (+37) | 75 |
| **G** | app/src/ai/agent/comment.rs, app/src/ai/blocklist/action_model/execute.rs, app/src/ai/blocklist/action_model/execute/read_files.rs, app/src/ai/blocklist/block/secret_redaction.rs, … (+37) | 75 |
| **H** | app/src/ai/blocklist/action_model/execute/fetch_conversation.rs, app/src/ai/blocklist/action_model/execute/file_glob.rs, app/src/ai/blocklist/action_model/execute/read_mcp_resource.rs, app/src/ai/blocklist/block/view_impl.rs, … (+37) | 75 |

## Full file-to-batch mapping

### Batch A (75 entries, 40 files)

- `app/src/ai/blocklist/action_model/execute/read_skill.rs` — 1
- `app/src/ai/blocklist/action_model/execute/request_computer_use.rs` — 2
- `app/src/ai/blocklist/controller/response_stream.rs` — 1
- `app/src/ai/blocklist/history_model.rs` — 2
- `app/src/ai/facts/manager.rs` — 1
- `app/src/ai/mcp/templatable_manager/oauth.rs` — 2
- `app/src/auth/auth_state.rs` — 1
- `app/src/changelog_model.rs` — 2
- `app/src/code_review/comment_rendering.rs` — 1
- `app/src/completer/mod.rs` — 2
- `app/src/env_vars/manager.rs` — 2
- `app/src/notebooks/mod.rs` — 1
- `app/src/pane_group/pane/notebook_pane.rs` — 2
- `app/src/search/ai_context_menu/code/data_source.rs` — 1
- `app/src/search/command_palette/view.rs` — 1
- `app/src/search/slash_command_menu/static_commands/commands.rs` — 3
- `app/src/settings/app_icon.rs` — 1
- `app/src/settings/gpu.rs` — 2
- `app/src/settings/ssh.rs` — 1
- `app/src/settings_view/custom_inference_modal.rs` — 3
- `app/src/settings_view/settings_file_footer.rs` — 1
- `app/src/system/info.rs` — 2
- `app/src/terminal/enable_auto_reload_modal.rs` — 3
- `app/src/terminal/input/models/model_spec_scores.rs` — 1
- `app/src/terminal/local_tty/server/protocol.rs` — 1
- `app/src/terminal/local_tty/unix.rs` — 2
- `app/src/terminal/model/tmux/mod.rs` — 1
- `app/src/terminal/shared_session/role_change_modal/viewer_request_body.rs` — 3
- `app/src/terminal/view/bookmarks.rs` — 2
- `app/src/terminal/view/shared_session/view_impl.rs` — 3
- `app/src/uri/browser_url_handler.rs` — 2
- `app/src/workspace/sync_inputs.rs` — 3
- `app/src/workspace/view/right_panel.rs` — 2
- `crates/computer_use/src/linux/x11/keyboard.rs` — 3
- `crates/editor/src/content/text.rs` — 2
- `crates/onboarding/src/slides/intention_slide.rs` — 3
- `crates/vim/src/vim.rs` — 2
- `crates/warpui/examples/segmented-control/root_view.rs` — 2
- `crates/warpui/src/rendering/wgpu/renderer.rs` — 3
- `crates/warpui_core/src/elements/stack/offset_positioning.rs` — 2

### Batch B (75 entries, 40 files)

- `app/src/ai/blocklist/action_model/execute/search_codebase.rs` — 2
- `app/src/ai/blocklist/action_model/execute/upload_artifact.rs` — 1
- `app/src/ai/blocklist/inline_action/requested_action.rs` — 1
- `app/src/ai/blocklist/inline_action/web_fetch.rs` — 2
- `app/src/ai/facts/view/mod.rs` — 1
- `app/src/ai/predict/next_command_model.rs` — 2
- `app/src/auth/paste_auth_token_modal.rs` — 1
- `app/src/cloud_object/model/view.rs` — 2
- `app/src/code_review/diff_state/remote.rs` — 1
- `app/src/context_chips/builtins.rs` — 2
- `app/src/env_vars/view/fixed_view_components.rs` — 2
- `app/src/pane_group/pane/view/header/mod.rs` — 1
- `app/src/pane_group/pane/workflow_pane.rs` — 2
- `app/src/search/ai_context_menu/code/search_item.rs` — 1
- `app/src/search/command_search/history/history_search_item.rs` — 1
- `app/src/search/welcome_palette/view.rs` — 3
- `app/src/settings/changelog.rs` — 1
- `app/src/settings/import/view.rs` — 2
- `app/src/settings_view/admin_actions.rs` — 1
- `app/src/settings_view/keybindings.rs` — 3
- `app/src/settings_view/settings_page.rs` — 1
- `app/src/tab_configs/remove_confirmation_dialog.rs` — 2
- `app/src/terminal/input/inline_history/search_item.rs` — 3
- `app/src/terminal/input/plans/search_item.rs` — 1
- `app/src/terminal/local_tty/windows/mod.rs` — 1
- `app/src/terminal/model/blocks/selection.rs` — 2
- `app/src/terminal/platform.rs` — 1
- `app/src/terminal/shared_session/viewer/terminal_manager.rs` — 3
- `app/src/terminal/view/init_project/lsp_server_selector.rs` — 2
- `app/src/terminal/view/shell_terminated_banner.rs` — 3
- `app/src/util/bindings.rs` — 2
- `app/src/workspace/view/openwarp_launch_modal/view.rs` — 3
- `app/src/workspaces/workspace.rs` — 2
- `crates/computer_use/src/linux/x11/screenshot.rs` — 3
- `crates/editor/src/model.rs` — 2
- `crates/onboarding/src/slides/theme_picker_slide.rs` — 3
- `crates/warp_completer/src/completer/describe.rs` — 2
- `crates/warpui/src/windowing/winit/event_loop/key_events.rs` — 2
- `crates/warpui/src/windowing/winit/window.rs` — 3
- `crates/warpui_core/src/integration/action_log.rs` — 2

### Batch C (75 entries, 40 files)

- `app/src/ai/blocklist/agent_view/agent_input_footer/editor.rs` — 1
- `app/src/ai/blocklist/agent_view/agent_message_bar.rs` — 2
- `app/src/ai/blocklist/inline_action/requested_script.rs` — 1
- `app/src/ai/blocklist/suggestion_chip_view.rs` — 2
- `app/src/ai/mcp/http_client.rs` — 1
- `app/src/ai_assistant/utils.rs` — 2
- `app/src/code/diff_viewer.rs` — 1
- `app/src/code/find_references_view.rs` — 2
- `app/src/coding_entrypoints/clone_repo_view.rs` — 1
- `app/src/context_chips/display_menu.rs` — 2
- `app/src/notebooks/active_notebook_data.rs` — 2
- `app/src/plugin/app/mod.rs` — 2
- `app/src/plugin/host/native/logging.rs` — 1
- `app/src/search/ai_context_menu/commands/search_item.rs` — 1
- `app/src/search/command_search/projects/project_search_item.rs` — 1
- `app/src/settings/block_visibility.rs` — 3
- `app/src/settings/cloud_preferences.rs` — 1
- `app/src/settings/pane.rs` — 2
- `app/src/settings_view/agent_assisted_environment_modal.rs` — 1
- `app/src/tab_configs/action_sidecar.rs` — 1
- `app/src/tab_configs/params_modal.rs` — 3
- `app/src/tab_configs/session_config.rs` — 2
- `app/src/terminal/input/profiles/search_item.rs` — 1
- `app/src/terminal/local_tty/spawner.rs` — 3
- `app/src/terminal/model/blockgrid.rs` — 1
- `app/src/terminal/recorder.rs` — 2
- `app/src/terminal/shared_session/participant_avatar_view.rs` — 1
- `app/src/terminal/view/ambient_agent/auth_secret_ftux_dropdown.rs` — 3
- `app/src/terminal/view/inline_banner/anonymous_user_ai_sign_up.rs` — 2
- `app/src/terminal/view/tooltips.rs` — 3
- `app/src/util/git.rs` — 2
- `app/src/workspace/view/orchestration_launch_modal/view.rs` — 3
- `crates/ai/src/skills/parse_skill.rs` — 2
- `crates/computer_use/src/windows/keyboard.rs` — 3
- `crates/field_mask/src/lib.rs` — 2
- `crates/warp_completer/src/completer/engine/command.rs` — 3
- `crates/warp_files/src/lib.rs` — 2
- `crates/warpui/src/windowing/winit/fonts/windows.rs` — 2
- `crates/warpui_core/src/async/wasm/mod.rs` — 3
- `crates/warpui_core/src/notification.rs` — 2

### Batch D (75 entries, 40 files)

- `app/src/ai/blocklist/agent_view/agent_input_footer/environment_selector.rs` — 1
- `app/src/ai/blocklist/agent_view/orchestration_conversation_links.rs` — 2
- `app/src/ai/blocklist/passive_suggestions/legacy.rs` — 1
- `app/src/ai/document/orchestration_config_block.rs` — 2
- `app/src/ai/mcp/parsing.rs` — 1
- `app/src/auth/auth_manager.rs` — 2
- `app/src/code/editor/comment_editor.rs` — 1
- `app/src/code_review/comments/convert.rs` — 2
- `app/src/completer/js.rs` — 1
- `app/src/default_terminal/mac.rs` — 2
- `app/src/notebooks/editor/block_insertion_menu.rs` — 2
- `app/src/prompt/editor_modal.rs` — 2
- `app/src/remote_server/codebase_index_model.rs` — 1
- `app/src/search/ai_context_menu/notebooks/search_item.rs` — 1
- `app/src/search/command_search/settings.rs` — 1
- `app/src/settings/import/alacritty_parser.rs` — 1
- `app/src/settings/init.rs` — 3
- `app/src/settings_view/ai_page.rs` — 1
- `app/src/settings_view/billing_and_usage/billing_cycle_usage_section.rs` — 2
- `app/src/tab_configs/session_config_modal.rs` — 3
- `app/src/terminal/block_filter.rs` — 2
- `app/src/terminal/cli_agent_sessions/plugin_manager/codex.rs` — 1
- `app/src/terminal/input/prompts/data_source.rs` — 1
- `app/src/terminal/local_tty/windows/environment.rs` — 3
- `app/src/terminal/model/iterm_image.rs` — 1
- `app/src/terminal/rich_history.rs` — 2
- `app/src/terminal/shared_session/role_change_modal/sharer_response_body.rs` — 1
- `app/src/terminal/view/ambient_agent/model.rs` — 3
- `app/src/terminal/view/inline_banner/aws_bedrock_login.rs` — 2
- `app/src/util/link_detection.rs` — 3
- `app/src/util/traffic_lights/windows/renderer_state.rs` — 2
- `app/src/workspaces/team.rs` — 3
- `crates/channel_versions/src/lib.rs` — 2
- `crates/computer_use/src/windows/mouse.rs` — 3
- `crates/input_classifier/src/onnx/candle.rs` — 2
- `crates/warp_core/src/ui/color/hex_color.rs` — 3
- `crates/warp_logging/src/wasm.rs` — 2
- `crates/warpui/src/windowing/winit/notifications/wasm.rs` — 2
- `crates/warpui_core/src/elements/new_scrollable/mod.rs` — 3
- `crates/warpui_core/src/text_layout.rs` — 2

### Batch E (75 entries, 41 files)

- `app/src/ai/agent/api/convert_to.rs` — 1
- `app/src/ai/agent_conversations_model.rs` — 1
- `app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs` — 1
- `app/src/ai/blocklist/block/pending_user_query_block.rs` — 2
- `app/src/ai/cloud_agent_config/mod.rs` — 1
- `app/src/ai/execution_profiles/editor/mod.rs` — 2
- `app/src/ai/mcp/reconnecting_peer.rs` — 1
- `app/src/auth/web_handoff.rs` — 2
- `app/src/code/editor/goto_line/view.rs` — 1
- `app/src/code_review/diff_menu.rs` — 2
- `app/src/drive/import/nodes.rs` — 2
- `app/src/drive/items/env_var_collection.rs` — 1
- `app/src/notebooks/editor/embedded_item.rs` — 2
- `app/src/resource_center/keybindings_page.rs` — 1
- `app/src/search/action/search_item.rs` — 2
- `app/src/search/ai_context_menu/rules/search_item.rs` — 1
- `app/src/search/external_secrets/external_secret_search_item.rs` — 1
- `app/src/settings/input_mode.rs` — 1
- `app/src/settings/select.rs` — 3
- `app/src/settings_view/billing_and_usage/usage_history_entry.rs` — 1
- `app/src/settings_view/mcp_servers/server_card.rs` — 2
- `app/src/terminal/alt_screen_reporting.rs` — 3
- `app/src/terminal/cli_agent_sessions/plugin_manager/opencode.rs` — 2
- `app/src/terminal/grid_renderer.rs` — 1
- `app/src/terminal/input/repos/search_item.rs` — 1
- `app/src/terminal/model/blocks.rs` — 3
- `app/src/terminal/model/kitty.rs` — 1
- `app/src/terminal/shared_session/share_modal/denied_body.rs` — 1
- `app/src/terminal/ssh/warpify.rs` — 2
- `app/src/terminal/view/block_onboarding/onboarding_prompt_block.rs` — 3
- `app/src/terminal/view/inline_banner/aws_cli_not_installed.rs` — 2
- `app/src/util/windows.rs` — 3
- `app/src/voltron.rs` — 2
- `app/src/workspaces/update_manager.rs` — 3
- `crates/computer_use/src/mac/screenshot.rs` — 2
- `crates/editor/src/content/core.rs` — 3
- `crates/languages/src/lib.rs` — 2
- `crates/warp_server_client/src/cloud_object/mod.rs` — 2
- `crates/warp_server_client/src/drive/sharing.rs` — 3
- `crates/warpui_core/src/core/mod.rs` — 2
- `crates/warpui_core/src/keymap.rs` — 3

### Batch F (75 entries, 41 files)

- `app/src/ai/agent/conversation.rs` — 1
- `app/src/ai/agent_conversations_model/entry.rs` — 1
- `app/src/ai/blocklist/block/model/debug_model_impl.rs` — 1
- `app/src/ai/blocklist/block/view_impl/todos.rs` — 2
- `app/src/ai/cloud_environments/mod.rs` — 1
- `app/src/ai/harness_display.rs` — 2
- `app/src/ai/skills/file_watchers/utils.rs` — 1
- `app/src/autoupdate/channel_versions.rs` — 2
- `app/src/code/editor/nav_bar.rs` — 1
- `app/src/code_review/diff_state/local.rs` — 2
- `app/src/drive/mod.rs` — 2
- `app/src/drive/workflows/arguments.rs` — 1
- `app/src/notebooks/editor/link_editor.rs` — 2
- `app/src/resource_center/main_page.rs` — 1
- `app/src/search/ai_context_menu/diffset/data_source.rs` — 2
- `app/src/search/ai_context_menu/skills/search_item.rs` — 1
- `app/src/search_bar.rs` — 1
- `app/src/settings/linux.rs` — 1
- `app/src/settings/theme.rs` — 3
- `app/src/settings_view/billing_and_usage_dispatch.rs` — 1
- `app/src/settings_view/mcp_servers/update_modal.rs` — 2
- `app/src/terminal/block_list_settings.rs` — 3
- `app/src/terminal/command_corrections_denylist.rs` — 2
- `app/src/terminal/history.rs` — 1
- `app/src/terminal/input/user_query/search_item.rs` — 1
- `app/src/terminal/model/session.rs` — 3
- `app/src/terminal/model/session/command_executor/tmux_executor.rs` — 1
- `app/src/terminal/shared_session/share_modal/mod.rs` — 1
- `app/src/terminal/view/ambient_agent/block/setup_command_text.rs` — 2
- `app/src/terminal/view/init_environment/mode_selector.rs` — 3
- `app/src/terminal/view/inline_banner/ssh.rs` — 2
- `app/src/workflows/command_parser.rs` — 3
- `app/src/workflows/manager.rs` — 2
- `crates/ai/src/agent/citation.rs` — 3
- `crates/computer_use/src/screenshot_utils.rs` — 2
- `crates/editor/src/render/element/mermaid.rs` — 3
- `crates/natural_language_detection/src/lib.rs` — 2
- `crates/warp_util/src/assets.rs` — 2
- `crates/warpui/examples/formatted-text/root_view.rs` — 3
- `crates/warpui_core/src/elements/min_size.rs` — 2
- `crates/warpui_extras/src/secure_storage/linux.rs` — 3

### Batch G (75 entries, 41 files)

- `app/src/ai/agent/comment.rs` — 2
- `app/src/ai/blocklist/action_model/execute.rs` — 1
- `app/src/ai/blocklist/action_model/execute/read_files.rs` — 2
- `app/src/ai/blocklist/block/secret_redaction.rs` — 1
- `app/src/ai/blocklist/code_block.rs` — 2
- `app/src/ai/connected_self_hosted_workers.rs` — 1
- `app/src/ai/local_child_harnesses.rs` — 2
- `app/src/app_services/windows/registry.rs` — 1
- `app/src/autoupdate/windows.rs` — 2
- `app/src/code/language_server_extension.rs` — 1
- `app/src/code_review/git_dialog/pr.rs` — 2
- `app/src/drive/settings.rs` — 2
- `app/src/env_vars/view/command_dialog/command_dialog_view.rs` — 1
- `app/src/notebooks/editor/model.rs` — 2
- `app/src/resource_center/mod.rs` — 1
- `app/src/search/ai_context_menu/workflows/search_item.rs` — 1
- `app/src/search/command_search/ai_queries/ai_queries_search_item.rs` — 2
- `app/src/settings/accessibility.rs` — 1
- `app/src/settings/native_preference.rs` — 1
- `app/src/settings_view/billing_and_usage/billing_cycle_usage_team_totals.rs` — 3
- `app/src/settings_view/features_page.rs` — 1
- `app/src/settings_view/privacy/add_regex_modal.rs` — 2
- `app/src/terminal/bootstrap.rs` — 3
- `app/src/terminal/input/inline_menu/message_bar.rs` — 1
- `app/src/terminal/input/skills/data_source.rs` — 2
- `app/src/terminal/ligature_settings.rs` — 1
- `app/src/terminal/model/terminal_model.rs` — 1
- `app/src/terminal/session_settings/working_directory_config.rs` — 3
- `app/src/terminal/shared_session/viewer/event_loop.rs` — 1
- `app/src/terminal/view/ambient_agent/footer.rs` — 2
- `app/src/terminal/view/link_detection.rs` — 2
- `app/src/terminal/view/open_in_warp.rs` — 3
- `app/src/workflows/info_box.rs` — 3
- `app/src/workspace/header_toolbar_editor.rs` — 2
- `crates/ai/src/index/full_source_code_embedding/manager.rs` — 3
- `crates/editor/src/content/edit.rs` — 2
- `crates/editor/src/render/model/mod.rs` — 3
- `crates/onboarding/src/callout/model.rs` — 2
- `crates/warpui/examples/animated-gradient-text/root_view.rs` — 2
- `crates/warpui/examples/percentage/root_view.rs` — 3
- `crates/warpui_core/src/elements/new_scrollable/dual_axis_config.rs` — 2

### Batch H (75 entries, 41 files)

- `app/src/ai/blocklist/action_model/execute/fetch_conversation.rs` — 2
- `app/src/ai/blocklist/action_model/execute/file_glob.rs` — 1
- `app/src/ai/blocklist/action_model/execute/read_mcp_resource.rs` — 2
- `app/src/ai/blocklist/block/view_impl.rs` — 1
- `app/src/ai/blocklist/codebase_index_speedbump_banner.rs` — 2
- `app/src/ai/execution_profiles/model_menu_items.rs` — 1
- `app/src/ai/mcp/mod.rs` — 2
- `app/src/appearance.rs` — 1
- `app/src/bin/generate_settings_schema.rs` — 2
- `app/src/code_review/code_review_header/mod.rs` — 1
- `app/src/code_review/mod.rs` — 2
- `app/src/drive/workflows/modal.rs` — 2
- `app/src/env_vars/view/menus.rs` — 1
- `app/src/notebooks/editor/omnibar.rs` — 2
- `app/src/resource_center/section_views/feature_section.rs` — 1
- `app/src/search/command_palette/tabs/search_item.rs` — 1
- `app/src/search/command_search/warp_ai.rs` — 2
- `app/src/settings/alias_expansion.rs` — 1
- `app/src/settings/scroll.rs` — 1
- `app/src/settings_view/billing_and_usage_page_v2.rs` — 3
- `app/src/settings_view/mcp_servers_page.rs` — 1
- `app/src/settings_view/warp_drive_page.rs` — 2
- `app/src/terminal/cli_agent.rs` — 3
- `app/src/terminal/input/inline_menu/view.rs` — 1
- `app/src/terminal/links.rs` — 2
- `app/src/terminal/local_tty/event_loop.rs` — 1
- `app/src/terminal/model/tmux/commands.rs` — 1
- `app/src/terminal/shared_session/role_change_modal/sharer_grant_body.rs` — 3
- `app/src/terminal/terminal_size_element.rs` — 1
- `app/src/terminal/view/block_onboarding/onboarding_drive_sharing_block.rs` — 2
- `app/src/terminal/view/shared_session/sharer/inactivity_modal.rs` — 3
- `app/src/undo_close/settings.rs` — 2
- `app/src/workflows/local_workflows.rs` — 3
- `app/src/workspace/hoa_onboarding/tab_config_step.rs` — 2
- `crates/computer_use/src/lib.rs` — 3
- `crates/editor/src/content/selection_model.rs` — 2
- `crates/onboarding/examples/callout.rs` — 3
- `crates/settings_value_derive/src/lib.rs` — 2
- `crates/warpui/examples/autotracking/root_view.rs` — 2
- `crates/warpui/src/platform/mac/fonts.rs` — 3
- `crates/warpui_core/src/elements/selectable_area.rs` — 2

