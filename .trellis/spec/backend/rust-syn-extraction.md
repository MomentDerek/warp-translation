# Rust Source Text Extraction with `syn::Visit`

> Patterns for tools that walk Rust source via `syn` and extract text artifacts (string literals, identifiers, attributes).

---

## Why this matters

`syn` lowers `///` doc comments to `#[doc = "..."]` attributes. A naive `Visit::visit_lit_str` implementation will capture every doc comment as if it were source content. In `warp-zh-extractor`, this misclassified ~32,000 entries (≈83% of the table) as candidate UI strings before the doc-attr filter was added.

The same trap applies to:
- `#[error("...")]` (thiserror format strings)
- `#[serde(rename = "...")]` (field-name aliases)
- `#[deprecated(note = "...")]` (developer-facing notes)
- Any procedural macro that lowers user-facing prose into attribute literals

If your tool extracts strings, you MUST decide for each attribute path whether its literals are in scope, and reject the rest at extraction time — not in a downstream heuristic.

---

## Pattern: `skip_depth` counter on `Visit::visit_attribute` and `Visit::visit_macro`

### Required behavior

- Maintain a `skip_depth: u32` field on the visitor.
- On entering a node whose path matches a skip list, increment `skip_depth`, recurse, decrement.
- In `visit_lit_str`, return immediately when `skip_depth > 0`.

### Reference implementation

From `tools/extractor/src/extract.rs`:

```rust
const SKIP_MACROS: &[&str] = &[
    "include_str", "include_bytes",
    "trace", "debug", "info", "warn", "error",
    "println", "eprintln", "panic",
    "assert", "assert_eq", "debug_assert",
    "anyhow", "bail", "ensure",
    "sql", "query", "json",
    // ... see source for full list
];

impl<'ast, 'src> Visit<'ast> for Extractor<'src> {
    fn visit_lit_str(&mut self, node: &'ast LitStr) {
        if self.skip_depth > 0 {
            return;
        }
        self.record(node.span(), node.value(), LitKind::Literal, None);
    }

    fn visit_attribute(&mut self, attr: &'ast Attribute) {
        let last = attr.path().segments.last().map(|s| s.ident.to_string());
        if matches!(last.as_deref(), Some("doc")) {
            self.skip_depth += 1;
            visit::visit_attribute(self, attr);
            self.skip_depth -= 1;
            return;
        }
        visit::visit_attribute(self, attr);
    }

    fn visit_macro(&mut self, mac: &'ast Macro) {
        let last = mac.path.segments.last().map(|s| s.ident.to_string()).unwrap_or_default();
        if SKIP_MACROS.contains(&last.as_str()) {
            self.skip_depth += 1;
            visit::visit_macro(self, mac);
            self.skip_depth -= 1;
            return;
        }
        // ...
    }
}
```

### Key invariants

1. The skip list is matched on the **last path segment** (`tracing::info` → `info`). Full-path matching is overkill; switch to it only when one tool needs different behavior per crate.
2. `skip_depth` MUST be incremented **before** recursing and decremented **after**, even if recursion panics — use a guard if your codebase tolerates panics.
3. `visit_lit_str` is the single chokepoint. Do not duplicate the skip check across other visit methods.
4. Macro bodies are opaque to `syn`'s AST — for non-skipped macros, scan the raw `TokenStream` for `Literal` nodes and apply the same `skip_depth` gate. See `Extractor::scan_macro_tokens` in the reference.

---

## Forbidden Pattern: Filtering doc comments via heuristic score

```rust
// Don't: reject doc comments downstream by penalizing leading whitespace
if value.starts_with(' ') || value.starts_with('\t') {
    score -= 3;  // hopes the threshold catches it
}
```

This will fail. Many doc comments still net positive on path bonuses + sentence-shape rules and slip into the table. The right place to filter is at AST traversal — categorical rejection, not statistical rejection.

---

## Required Tests

Any tool extending the visitor MUST include a unit test that asserts doc-attribute literals are dropped:

```rust
#[test]
fn doc_attribute_literals_are_suppressed() {
    let src = r#"
        /// This is a developer comment.
        #[doc = "Another developer comment"]
        struct Foo;

        impl Foo {
            fn bar(&self) {
                let _ = Button::label("X");
            }
        }
    "#;
    let (strings, _) = extract_file(Path::new("test.rs"), "test.rs", src).unwrap();
    let values: Vec<_> = strings.iter().map(|s| s.value.as_str()).collect();
    assert!(values.contains(&"X"));
    assert!(!values.iter().any(|v| v.contains("developer comment")));
}
```

Assertion points:
1. The intended literal (`"X"`) survives.
2. Both `///` and `#[doc = "..."]` forms are dropped.
3. The visitor does not panic on malformed attribute paths.

---

## Extending the skip list

When you discover a new attribute or macro that should be skipped, add it to the constant in the same module — do not duplicate the list per file. Document the **reason** for inclusion in a comment line above the entry; this prevents accidental removal during cleanups.

```rust
const SKIP_MACROS: &[&str] = &[
    // file/env/cfg — these embed paths and identifiers, never UI text
    "include_str", "include_bytes", "env", "option_env",
    // logging — operator-facing, not user-facing
    "trace", "debug", "info", "warn", "error",
    // ...
];
```

---

## UI constructor whitelist: `(call_path, arg_index)` strategy

### Why arg-index matters

A naive constructor whitelist that promotes *every* positional `LitStr` arg of a call site will misclassify identifiers/action-names that sit alongside the UI string. The canonical example is `EditableBinding::new(name, description, action)`:

- `args[0]` is `"pane_group:navigate_next"` — an action ID; matches `regex:colon_ident`; must NOT be promoted.
- `args[1]` is `"Activate next pane"` — the user-visible menu label; must be promoted to `auto_ui`.
- `args[2]` is the `WorkspaceAction` enum value (no literal).

This pattern repeats in `FixedBinding::custom(custom_action, action, "Switch to next tab", ctx)` (UI string at index 2), `BindingDescription::with_custom_description(MAC_MENUS_CONTEXT, "Switch tab")` (index 1), and others. The extractor MUST capture `parent_call_arg_index` per `LitStr` (see `extract.rs::CallFrame`) and the heuristic MUST require the index to be in the constructor's allow-list before awarding the UI bonus.

### Adding a new entry to `UI_CONSTRUCTORS`

When extending `tools/extractor/src/heuristic.rs::UI_CONSTRUCTORS`, follow this checklist:

1. **Locate the call site.** Grep for the constructor; read 3-5 invocations to confirm which positional argument carries the user-visible label.
2. **Reject open-ended `None` allow-lists** unless every positional arg of the constructor is genuinely user-visible (rare — `Dialog::new(title, body)` qualifies, `BindingDescription::with_custom_description(context, description)` does NOT because arg 0 is an action-context identifier).
3. **Beware of `callee.contains(sig)` substring matching.** The current implementation matches the constructor sig as a substring of the full callee path, so `BindingDescription::new` also matches `BindingDescription::new_preserve_case`. For variants that share a prefix and share the same allow-list, the shorter sig wins — that is usually correct, but document it.
4. **Add a unit test** that asserts the new `(call_path, arg_index)` pair drives the verdict to `AutoUi` AND a complementary test that asserts a different arg index does NOT inherit the bonus.

### Nested calls

Group 3 in `research/menu-literal-trace.md` describes the nested pattern:

```rust
EditableBinding::new(
    "panel:agent_conversations",
    BindingDescription::new("Left Panel: Agent conversations"),
    action,
)
```

Here the inner `"Left Panel: ..."` literal's immediate `parent_call` is `BindingDescription::new`, not `EditableBinding::new`. The extractor's `call_stack` correctly records the deepest enclosing call, so the heuristic sees `BindingDescription::new` at arg 0. Both call-paths must therefore appear in `UI_CONSTRUCTORS` independently — the inner call cannot rely on the outer call's bonus.

### Caveat: runtime titlecase

`BindingDescription::new` applies `titlecase::titlecase()` to its input at runtime (`crates/warpui_core/src/keymap.rs:115`). The source literal `"Activate next pane"` displays as `"Activate Next Pane"`. The translation table is keyed by the **source literal as written**; a Chinese target like `"激活下一个窗格"` is unaffected by titlecase (no ASCII case to fold) and renders correctly. Do not be misled by user screenshots showing title-case strings — translate the sentence-case source as it appears in `strings.json`.

### Custom helpers in app crates

Project-local helpers like `app/src/app_menus.rs::link_menu_item(title, link)` are valid additions to `UI_CONSTRUCTORS`. The substring matcher will pick up the function name even though it is not a constructor; the whitelist is more accurately described as "calls whose chosen positional arg is user-visible text", not just `Type::method`-shaped paths.
