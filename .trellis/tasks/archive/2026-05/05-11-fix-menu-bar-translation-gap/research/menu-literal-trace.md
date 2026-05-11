# Menu literal source trace

## Summary

All D-class menu strings live as **plain `&'static str` positional arguments to `EditableBinding::new(name, description, action)`** (sometimes wrapped in `BindingDescription::new(...).with_custom_description(...)`) and a smaller set in `FixedBinding::custom(custom_action, action, description, ctx)`. They are spread across the `app/src/` crate (mostly `workspace/mod.rs`, `terminal/view/init.rs`, `editor/view/mod.rs`, `pane_group/.../mod.rs`). The wrapper menu item code (`CustomMenuItem::new(&default_name(action, ctx), ...)` in `app_menus.rs`) does NOT contain the literals; it looks them up at runtime via `description_for_custom_action` → the `BindingDescription` stored on the binding.

Critical wrinkle: `BindingDescription::new` runs `titlecase()` on the input at construction time (`crates/warpui_core/src/keymap.rs:115`). Source files therefore contain sentence-case ("Activate next pane") but the menu bar shows title-case ("Activate Next Pane"). Translation must be keyed on the **source literal as written** and applied either before titlecase, or both forms must be recognized.

The Help-menu "GitHub Issues..." string is a different pattern (positional `&'static str` to a helper `link_menu_item(title, link)` in `app/src/app_menus.rs:897`).

## Per-string findings

| String (source literal) | File:line | AST shape | Call context | Existing heuristic verdict |
|---|---|---|---|---|
| Switch to next tab | app/src/workspace/mod.rs:280 | `LitStr` 3rd arg | `FixedBinding::custom(CustomAction::CycleNextSession, action, "Switch to next tab", ctx)` | likely not_ui — positional `LitStr` to non-whitelisted constructor |
| Switch to previous tab | app/src/workspace/mod.rs:286 | same | `FixedBinding::custom(CustomAction::CyclePrevSession, …, "Switch to previous tab", …)` | same |
| Activate next pane | app/src/workspace/mod.rs:591 | `LitStr` 2nd arg | `EditableBinding::new("pane_group:navigate_next", "Activate next pane", WorkspaceAction::…)` | not_ui |
| Activate previous pane | app/src/workspace/mod.rs:583 | same | `EditableBinding::new("pane_group:navigate_prev", "Activate previous pane", …)` | not_ui |
| Rename the current tab | app/src/workspace/mod.rs:908 | same | `EditableBinding::new("workspace:rename_active_tab", "Rename the current tab", …)` | not_ui |
| Close the current tab | app/src/workspace/mod.rs:937 | same | `EditableBinding::new("workspace:close_active_tab", "Close the current tab", …)` | not_ui |
| Close other tabs | app/src/workspace/mod.rs:947 | same | `EditableBinding::new("workspace:close_other_tabs", "Close other tabs", …)` | not_ui |
| Clear command editor | app/src/editor/view/mod.rs:934 | same | `EditableBinding::new("editor_view:clear_buffer", "Clear command editor", EditorAction::CtrlC)` | not_ui |
| Add selection for next occurrence | app/src/editor/view/mod.rs:598 | same | `EditableBinding::new("editor_view:add_next_occurrence", "Add selection for next occurrence", …)` | not_ui |
| Add cursor above | app/src/editor/view/mod.rs:943 | same | `EditableBinding::new("editor_view:add_cursor_above", "Add cursor above", …)` | not_ui |
| Add cursor below | app/src/editor/view/mod.rs:950 | same | `EditableBinding::new("editor_view:add_cursor_below", "Add cursor below", …)` | not_ui |
| Go to line | app/src/code/editor/view/actions.rs:600 (also goto_line/view.rs:138) | same | `EditableBinding::new("…go_to_line", "Go to line", …)` | not_ui |
| Focus terminal input | app/src/terminal/view/init.rs:396 | same | `EditableBinding::new("terminal:focus_input", "Focus terminal input", …)` | not_ui |
| Launch configuration palette | app/src/workspace/mod.rs:993 | same | `EditableBinding::new("workspace:toggle_launch_config_palette", "Launch configuration palette", …)` | not_ui |
| Left Panel: Agent conversations | app/src/workspace/mod.rs:740 | 1st arg to `BindingDescription::new` which is 2nd arg of `EditableBinding::new` | `EditableBinding::new(NAME_CONST, BindingDescription::new("Left Panel: Agent conversations"), action)` | not_ui — nested call |
| Left Panel: Project explorer | app/src/workspace/mod.rs:749 | same nested form | same | not_ui |
| Left Panel: Global search | app/src/workspace/mod.rs:757 | same nested form | same | not_ui |
| Workflows | app/src/terminal/input.rs:1862 | `LitStr` 2nd arg | `EditableBinding::new("input:toggle_workflows", "Workflows", InputAction::SelectAndRefreshVoltron(VoltronItem::Workflows))` | not_ui (single-word) |
| Select previous block | app/src/terminal/view/init.rs:560 | `LitStr` 2nd arg | `EditableBinding::new(SELECT_PREVIOUS_BLOCK_ACTION_NAME, "Select previous block", TerminalAction::SelectPriorBlock)` | not_ui |
| Select next block | app/src/terminal/view/init.rs:569 | same | `EditableBinding::new(SELECT_NEXT_BLOCK_ACTION_NAME, "Select next block", …)` | not_ui |
| Select all blocks | app/src/terminal/view/init.rs:681,690,701 | same (3 copies) | `EditableBinding::new("terminal:select_all_blocks", "Select all blocks", …)` | not_ui |
| Scroll to top of selected block | app/src/terminal/view/init.rs:653 | same | `EditableBinding::new("terminal:scroll_to_top_of_selected_block", "Scroll to top of selected block", …)` | not_ui |
| Scroll to bottom of selected block | app/src/terminal/view/init.rs:662 | same | `EditableBinding::new("terminal:scroll_to_bottom_of_selected_block", "Scroll to bottom of selected block", …)` | not_ui |
| Share selected block | app/src/terminal/view/init.rs:578 | same | `EditableBinding::new("terminal:open_share_block_modal", "Share selected block", …)` | not_ui |
| Bookmark selected block | app/src/terminal/view/init.rs:587 | same | `EditableBinding::new("terminal:bookmark_selected_block", "Bookmark selected block", …)` | not_ui |
| Find within selected block | app/src/terminal/view/init.rs:596 | same | `EditableBinding::new("terminal:find", "Find within selected block", …)` | not_ui |
| Copy command and output | app/src/terminal/view/init.rs:605 | same | `EditableBinding::new("terminal:copy", "Copy command and output", TerminalAction::Copy)` | not_ui |
| Copy command | app/src/terminal/view/init.rs:623 | same | `EditableBinding::new("terminal:copy_commands", "Copy command", …)` | not_ui |
| Copy command output | app/src/terminal/view/init.rs:614 | same | `EditableBinding::new("terminal:copy_outputs", "Copy command output", …)` | not_ui |
| Share pane | app/src/pane_group/pane/view/mod.rs:44 | same | `EditableBinding::new("pane:share_pane_contents", "Share pane", PaneAction::ShareContents)` | not_ui |
| GitHub Issues... | app/src/app_menus.rs:928 | `LitStr` 1st arg | `link_menu_item("GitHub Issues...", links::GITHUB_ISSUES_URL.into())` — also `"Warp Documentation..."` line 927, `"Warp Slack Community..."` line 929, `"Send Feedback..."` line 910 | not_ui |

(Note: many menu titles in `app_menus.rs` such as `"File"`, `"View"`, `"Tab"`, `"AI"`, `"Blocks"`, `"Drive"`, `"Window"`, `"Help"` are also positional `LitStr` 1st-arg to `Menu::new` — the B-class items already known and being fixed by adding `Menu::new[0]` to `UI_CONSTRUCTORS`.)

## Pattern groups

### Group 1 (dominant): `EditableBinding::new(name, description, action)` — 2nd positional arg is the user-visible description

- **Files**: `app/src/workspace/mod.rs` (~150+ occurrences), `app/src/terminal/view/init.rs` (~30+), `app/src/editor/view/mod.rs` (~10+), `app/src/pane_group/pane/view/mod.rs`, `app/src/terminal/input.rs`, `app/src/code/editor/**`, `app/src/root_view.rs`, `app/src/workspace/sync_inputs.rs`, etc.
- **AST shape**: `ExprCall` where callee is a `ExprPath` ending in segment `new`, and the path's previous segment is `EditableBinding`. The literal is `args[1]` of that call, type `Expr::Lit(LitStr)`.
- **Variant**: the 2nd arg is sometimes nested: `BindingDescription::new("…").with_custom_description(MAC_MENUS_CONTEXT, "…")` or `.with_dynamic_override(|ctx| …)`. The nested `BindingDescription::new("…")` literal is the same kind of UI string.
- **Variant 2**: 2nd arg can also be a runtime-built `if cond { "X" } else { "Y" }` (e.g. `app/src/terminal/view/init.rs:388` for "Cancel active process"). Both branches are user-facing.
- **Why current extractor misses it**: `EditableBinding::new` is not in any UI-constructor list, the 2nd-positional-arg position has no `name=`-like hint, and the strings are sentence-cased (no Title Case bonus), often multi-word but mundane verbs that look like docstrings.
- **Strings affected**: at least 200+ binding descriptions in `app/src/`, of which roughly 40-60 surface in the menu bar via `description_for_custom_action`.

### Group 2: `FixedBinding::custom(custom_action, action, description, ctx)` — 3rd positional arg is description

- **Files**: `app/src/workspace/mod.rs` (~10 occurrences). Examples at lines 280 ("Switch to next tab"), 286 ("Switch to previous tab"), 292 ("Create New Window"), 299 ("New File"), 309 ("Zoom In"), 316 ("Zoom Out"), 323 ("Reset Zoom"), 333 ("Increase font size"), 340 ("Decrease font size").
- **AST shape**: `ExprCall` where callee is `ExprPath` ending in segments `FixedBinding::custom`. Literal at `args[2]`.
- **Strings affected**: ~10. Includes "Switch to next tab" / "Switch to previous tab" (currently appearing in the bug).

### Group 3: `BindingDescription::new(&str)` direct nested call

- **Files**: `app/src/workspace/mod.rs` (~30+ occurrences for left panels, settings, drive, etc.).
- **AST shape**: `ExprCall` to `BindingDescription::new` with a single `LitStr` arg, typically appearing as inner expression of an outer `EditableBinding::new(…)` 2nd arg.
- **Why important**: even if Group 1 detection works only on the outer call's `args[1]`, that arg here is a CALL expression, not a literal. The literal is one level deeper. Either (a) detection must recurse into nested calls when args[1] is a method-chain seed, or (b) `BindingDescription::new[0]` must be its own UI constructor entry.
- **Strings affected**: includes "Left Panel: Agent conversations", "Left Panel: Project explorer", "Left Panel: Global search", "Close Window", "Crash the app (for testing sentry-native)", many others.

### Group 4: Custom helper function `link_menu_item(title, link)` and `Menu::new(title, items)`

- **Files**: `app/src/app_menus.rs:897` (`link_menu_item`), and `Menu::new` calls throughout the same file.
- **AST shape**: positional `LitStr` 1st arg.
- **Strings affected**: "GitHub Issues...", "Warp Documentation...", "Warp Slack Community...", "Send Feedback..." plus the 10 top-level menu titles ("Warp", "File", "Edit", "View", "Tab", "AI", "Blocks", "Drive", "Window", "Help"). The 10 top-level titles are B-class already being fixed.

### Group 5: Conditional string returning a UI label (less common but present)

- Example: `app/src/terminal/view/init.rs:388` — `EditableBinding::new("…", if foo { "Cancel and clear command" } else { "Cancel active process" }, …)`.
- AST shape: `args[1]` is `Expr::If` whose branches are `Expr::Lit(LitStr)`. Currently both literals lack any UI hint; the extractor sees them as bare literals inside a function body.
- Frequency: handful of cases — not the bulk, but should be covered if Group 1 detection is taught to descend into branch expressions.

## Heuristic implications

### Group 1 + Group 3 fix (catches the dominant pattern)

- **AST hook needed**: in `Visit::visit_expr_call`, record on the enclosing scope:
  - `enclosing_call_path: Option<String>` — set to the trailing `Type::method` (e.g. `"EditableBinding::new"`, `"FixedBinding::custom"`, `"BindingDescription::new"`, `"BindingDescription::with_custom_description"`).
  - `arg_index_in_call: Option<usize>` — set per visited arg so a `RawString` knows its position.
- **Scoring rule**: when emitting a `RawString`, if `enclosing_call_path` ∈ {`EditableBinding::new`@arg1, `FixedBinding::custom`@arg2, `BindingDescription::new`@arg0, `BindingDescription::new_preserve_case`@arg0, `BindingDescription::with_custom_description`@arg1, `Menu::new`@arg0, `MenuItemFields::new`@arg0}, promote score by a strong margin (e.g. +6, enough to push above `auto_ui` threshold). Optionally also require: non-empty, < 80 chars, contains at least one ASCII letter, not all-lowercase-snake-case.
- **False-positive risk**:
  - Some `EditableBinding::new(name="workspace:foo", description="…")` calls register `"[Debug] …"` strings (debug-mode-only menu items shown in the command palette, see `app/src/workspace/mod.rs:188-254`). These ARE UI strings even though leading `[Debug]` is unusual. Risk: low — they should be translated too (debug builds aren't shipped to end users, but no harm).
  - Some action names contain pure identifiers like `"workspace:crash"` — these are the 1st arg (`args[0]`), NOT what gets promoted. The arg-index filter `args[1]` (not `args[0]`) on `EditableBinding::new` prevents this.
  - `Menu::new` 1st arg already a known B-class fix. No new risk.

### Group 4 fix (link helper + Menu titles)

- **AST hook needed**: same `enclosing_call_path`/`arg_index_in_call` machinery from Group 1.
- **Scoring rule**: add `link_menu_item`@arg0 to a smaller whitelist with `+4`. Because `link_menu_item` is a custom helper local to `app/src/app_menus.rs`, this is project-specific. An alternative: a "path module ends in `app_menus`" path-aware bonus could catch it generically.
- **False-positive risk**: minimal — `link_menu_item` only takes display titles.

### Group 5 fix (conditional expressions)

- **AST hook needed**: when entering an `Expr::If` / `Expr::Match` whose containing `arg_index_in_call` is in a UI-call slot, propagate the `enclosing_call_path`/`arg_index_in_call` context down so literals in branches inherit the UI verdict.
- **Scoring rule**: same as Group 1.
- **False-positive risk**: low; the propagation is only active under UI calls.

### Cross-cutting: titlecase mismatch

- The runtime applies `titlecase::titlecase()` to `BindingDescription::new` input. Source literals are sentence-case, displayed strings are title-case. Any translation lookup that runs **after** titlecase application will miss sentence-case keys. Either:
  - The translator pipeline must translate the `BindingDescription` raw string before it is fed into `titlecase()` (so the key matches the source literal exactly), OR
  - The translation table must include both casing variants, OR
  - The titlecase call must be bypassed for non-ASCII (translated) strings.
- This is **not a heuristic problem** but it explains why translating the literal as written may still produce English-looking menu items unless the titlecase step is accounted for. The extractor's job is just to capture the source literal exactly.

## Recommended scope for B+D heuristic fix

- **Minimum (B only)**: add `Menu::new`@arg0 to `UI_CONSTRUCTORS`. Catches the 10 top-level menu titles.
- **Medium (B + most of D — ~80% of missing strings)**: extend `UI_CONSTRUCTORS` (or equivalent positional-arg whitelist) with:
  - `EditableBinding::new`@arg1
  - `FixedBinding::custom`@arg2
  - `BindingDescription::new`@arg0
  - `BindingDescription::new_preserve_case`@arg0
  - `BindingDescription::with_custom_description`@arg1
  - `MenuItemFields::new`@arg0
  - `Menu::new`@arg0 (B fix)
  - `link_menu_item`@arg0
  - This requires the extractor to track `(call_path, arg_index)` for the immediate enclosing `ExprCall` around each `LitStr`.
- **Maximum (also catches branch-expression literals — Group 5)**: above, plus propagation through `Expr::If` / `Expr::Match` / `Expr::Block` branches so literals in conditional UI args inherit the UI verdict. Risk: tiny additional surface, no meaningful FP risk.
- **Note**: the existing `description_for_custom_action` runtime path means we don't need to chase the `CustomMenuItem::new(&default_name(...))` call sites — they don't contain literals. The fix is upstream at the binding registration site.

## Files inspected

- <HOME>/Documents/Codes/warp/app/src/app_menus.rs (lines 75-932)
- <HOME>/Documents/Codes/warp/app/src/util/bindings.rs (lines 1-470)
- <HOME>/Documents/Codes/warp/app/src/workspace/mod.rs (lines 155-1010)
- <HOME>/Documents/Codes/warp/app/src/terminal/view/init.rs (lines 388-710)
- <HOME>/Documents/Codes/warp/app/src/editor/view/mod.rs (lines 590-970)
- <HOME>/Documents/Codes/warp/app/src/pane_group/pane/view/mod.rs (lines 35-50)
- <HOME>/Documents/Codes/warp/app/src/terminal/input.rs (lines 1855-1880)
- <HOME>/Documents/Codes/warp/app/src/voltron.rs (lines 85-100)
- <HOME>/Documents/Codes/warp/crates/warpui_core/src/core/app.rs (lines 1700-1820)
- <HOME>/Documents/Codes/warp/crates/warpui_core/src/keymap.rs (lines 110-170, 490-665)
