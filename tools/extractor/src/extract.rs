use std::path::Path;

use proc_macro2::{TokenStream, TokenTree};
use syn::visit::{self, Visit};
use syn::{
    Attribute, Expr, ExprCall, ExprLit, ExprMethodCall, ExprStruct, FieldValue, ItemConst, ItemFn,
    ItemImpl, ItemMod, ItemStatic, Lit, LitStr, Macro, Member,
};

use crate::model::{LitKind, RawString};

/// Macros whose body we never look into. The literals inside are paths,
/// env names, format machinery, telemetry, or test data — never UI text.
///
/// Match is on the **last segment** of the macro path (`tracing::info!` →
/// `info`). If a project ever needs different behavior per crate, switch
/// to full-path matching here.
const SKIP_MACROS: &[&str] = &[
    // file/env/cfg
    "include_str", "include_bytes", "include",
    "env", "option_env", "concat", "stringify",
    "cfg", "cfg_attr",
    "file", "line", "column", "module_path",
    // logging / tracing
    "trace", "debug", "info", "warn", "error", "event", "span", "instrument",
    // print / panic / assert
    "println", "eprintln", "print", "eprint",
    "dbg", "todo", "unimplemented", "unreachable",
    "panic", "debug_panic",
    "assert", "assert_eq", "assert_ne",
    "debug_assert", "debug_assert_eq", "debug_assert_ne",
    // format error / anyhow
    "anyhow", "bail", "ensure",
    // metrics / telemetry
    "metric", "counter", "histogram", "gauge",
    // sql / json / graphql
    "sql", "query", "query_as", "json",
    // assets / objc
    "asset", "asset_path", "embed",
    "sel", "msg_send",
];

pub fn extract_file(
    file_path: &Path,
    rel_path: &str,
    source: &str,
) -> syn::Result<(Vec<RawString>, ExtractCounters)> {
    let ast = syn::parse_file(source)?;
    let mut visitor = Extractor::new(rel_path.to_string(), source);
    visitor.visit_file(&ast);
    let _ = file_path; // path passed for future provenance / ignored for now
    Ok((visitor.strings, visitor.counters))
}

#[derive(Debug, Default, Clone, Copy)]
pub struct ExtractCounters {
    pub literals: usize,
    pub macro_token_literals: usize,
    pub skipped_macros: usize,
    /// Number of `#[doc = "..."]` attributes whose literals were suppressed.
    /// `///` doc comments lower to one such attribute per line, so this also
    /// counts those.
    pub skipped_doc_attrs: usize,
}

struct Extractor<'src> {
    file: String,
    source: &'src str,
    strings: Vec<RawString>,
    counters: ExtractCounters,
    skip_depth: u32,
    test_depth: u32,
    /// (callee_path, current_arg_index) stack for nested calls.
    call_stack: Vec<CallFrame>,
    /// Stack of current struct-literal field names being recorded.
    field_stack: Vec<String>,
    /// Current const/static name, if we're inside such a binding.
    const_name: Option<String>,
}

#[derive(Debug, Clone)]
struct CallFrame {
    callee: String,
    /// Which argument is currently being visited. `None` until the visitor
    /// descends into the args list, then bumped per-argument.
    arg_index: Option<usize>,
}

impl<'src> Extractor<'src> {
    fn new(file: String, source: &'src str) -> Self {
        Self {
            file,
            source,
            strings: Vec::new(),
            counters: ExtractCounters::default(),
            skip_depth: 0,
            test_depth: 0,
            call_stack: Vec::new(),
            field_stack: Vec::new(),
            const_name: None,
        }
    }

    fn record(&mut self, span: proc_macro2::Span, value: String, kind: LitKind, mac: Option<String>) {
        let range = span.byte_range();
        let start = span.start();
        // `byte_range` may yield 0..0 for synthetic spans — guard against that
        // so the builder never emits an empty replacement window.
        if range.start == range.end {
            return;
        }
        // Sanity-check the span actually points inside the source buffer.
        // Out-of-bounds = synthetic / re-spanned token; skip rather than
        // record garbage offsets the builder cannot apply safely.
        if range.end > self.source.len() {
            return;
        }
        match kind {
            LitKind::Literal => self.counters.literals += 1,
            LitKind::MacroToken => self.counters.macro_token_literals += 1,
        }
        let (parent_call, parent_call_arg_index) = match self.call_stack.last() {
            Some(frame) => (Some(frame.callee.clone()), frame.arg_index),
            None => (None, None),
        };
        self.strings.push(RawString {
            file: self.file.clone(),
            line: start.line,
            column: start.column,
            byte_start: range.start,
            byte_end: range.end,
            value,
            kind,
            macro_path: mac,
            parent_call,
            parent_call_arg_index,
            enclosing_const_name: self.const_name.clone(),
            in_test: self.test_depth > 0,
            struct_field: self.field_stack.last().cloned(),
        });
    }

    fn scan_macro_tokens(&mut self, tokens: TokenStream, mac_path: &str) {
        for tt in tokens {
            match tt {
                TokenTree::Group(g) => self.scan_macro_tokens(g.stream(), mac_path),
                TokenTree::Literal(lit) => {
                    let span = lit.span();
                    let raw = lit.to_string();
                    if let Some(value) = parse_string_literal(&raw) {
                        self.record(span, value, LitKind::MacroToken, Some(mac_path.to_string()));
                    }
                }
                TokenTree::Ident(_) | TokenTree::Punct(_) => {}
            }
        }
    }
}

/// Detect whether an attribute expresses a test context (`#[test]`,
/// `#[cfg(test)]`, `#[tokio::test]`, `#[rstest]`, etc.).
fn attr_is_test(attr: &syn::Attribute) -> bool {
    let path = path_to_string(attr.path());
    let last = path.rsplit("::").next().unwrap_or("");
    if last == "test" {
        return true;
    }
    if last == "cfg" {
        // crude: if the cfg meta tokens contain `test` ident, treat as test
        let tokens = attr.meta.to_token_stream_string();
        return tokens.contains("test");
    }
    false
}

trait MetaToTokens {
    fn to_token_stream_string(&self) -> String;
}

impl MetaToTokens for syn::Meta {
    fn to_token_stream_string(&self) -> String {
        use quote::ToTokens;
        let mut ts = proc_macro2::TokenStream::new();
        self.to_tokens(&mut ts);
        ts.to_string()
    }
}

fn path_to_string(p: &syn::Path) -> String {
    p.segments
        .iter()
        .map(|s| s.ident.to_string())
        .collect::<Vec<_>>()
        .join("::")
}

/// Render an expression that names a callee (path or method receiver) into a
/// short readable form. We only need the last identifier(s); the heuristic
/// looks at suffixes.
fn callee_for_call(call: &ExprCall) -> String {
    match &*call.func {
        Expr::Path(p) => path_to_string(&p.path),
        other => {
            // Fallback: stringify whatever the callee is.
            use quote::ToTokens;
            let mut ts = proc_macro2::TokenStream::new();
            other.to_tokens(&mut ts);
            ts.to_string()
        }
    }
}

fn callee_for_method(call: &ExprMethodCall) -> String {
    // Synthesize "<receiver>.method" for the heuristic; receiver is summarized.
    let method = call.method.to_string();
    format!(".{method}")
}

impl<'ast, 'src> Visit<'ast> for Extractor<'src> {
    fn visit_lit_str(&mut self, node: &'ast LitStr) {
        if self.skip_depth > 0 {
            return;
        }
        self.record(node.span(), node.value(), LitKind::Literal, None);
    }

    fn visit_attribute(&mut self, attr: &'ast Attribute) {
        // `///` doc comments and `#[doc = "..."]` attributes lower to a `doc`
        // path attribute carrying a string literal. These document Rust code
        // for developers — never user-facing UI — so suppress recording while
        // descending into them. Same mechanism as the `SKIP_MACROS` list.
        let last = attr
            .path()
            .segments
            .last()
            .map(|s| s.ident.to_string())
            .unwrap_or_default();
        if last == "doc" {
            self.counters.skipped_doc_attrs += 1;
            self.skip_depth += 1;
            visit::visit_attribute(self, attr);
            self.skip_depth -= 1;
            return;
        }
        visit::visit_attribute(self, attr);
    }

    fn visit_macro(&mut self, mac: &'ast Macro) {
        let last = mac
            .path
            .segments
            .last()
            .map(|s| s.ident.to_string())
            .unwrap_or_default();
        let full_path = mac
            .path
            .segments
            .iter()
            .map(|s| s.ident.to_string())
            .collect::<Vec<_>>()
            .join("::");

        if SKIP_MACROS.contains(&last.as_str()) {
            self.counters.skipped_macros += 1;
            // Walk into nested AST nodes (attributes, nested macros) but suppress
            // literal recording while inside a skip macro.
            self.skip_depth += 1;
            visit::visit_macro(self, mac);
            self.skip_depth -= 1;
            return;
        }

        // Outside the skip list: scan the macro body tokens for string literals
        // that the AST visitor never sees (because syn keeps macro bodies opaque).
        if self.skip_depth == 0 {
            self.scan_macro_tokens(mac.tokens.clone(), &full_path);
        }
        visit::visit_macro(self, mac);
    }

    fn visit_expr_call(&mut self, node: &'ast ExprCall) {
        let callee = callee_for_call(node);
        // Visit the callee expression itself with no frame (no arg index).
        self.visit_expr(&node.func);
        self.call_stack.push(CallFrame {
            callee,
            arg_index: None,
        });
        for (idx, arg) in node.args.iter().enumerate() {
            if let Some(frame) = self.call_stack.last_mut() {
                frame.arg_index = Some(idx);
            }
            self.visit_expr(arg);
        }
        self.call_stack.pop();
    }

    fn visit_expr_method_call(&mut self, node: &'ast ExprMethodCall) {
        // Visit the receiver outside any frame so its inner literals aren't
        // tagged as method-call args.
        self.visit_expr(&node.receiver);
        let callee = callee_for_method(node);
        self.call_stack.push(CallFrame {
            callee,
            arg_index: None,
        });
        for (idx, arg) in node.args.iter().enumerate() {
            if let Some(frame) = self.call_stack.last_mut() {
                frame.arg_index = Some(idx);
            }
            self.visit_expr(arg);
        }
        self.call_stack.pop();
    }

    fn visit_field_value(&mut self, node: &'ast FieldValue) {
        let name = match &node.member {
            Member::Named(id) => id.to_string(),
            Member::Unnamed(idx) => idx.index.to_string(),
        };
        self.field_stack.push(name);
        // If the field's value is just a string literal, record it directly
        // so the field name shows up in struct_field even when no enclosing
        // call frame is active.
        if let Expr::Lit(ExprLit { lit: Lit::Str(_), .. }) = &node.expr {
            // fall through to default visit — visit_lit_str will pick it up
        }
        visit::visit_field_value(self, node);
        self.field_stack.pop();
    }

    fn visit_expr_struct(&mut self, node: &'ast ExprStruct) {
        // Only the field values are relevant for struct_field tagging; the
        // path itself is unrelated.
        self.visit_path(&node.path);
        for field in &node.fields {
            self.visit_field_value(field);
        }
        if let Some(rest) = &node.rest {
            self.visit_expr(rest);
        }
    }

    fn visit_item_const(&mut self, node: &'ast ItemConst) {
        let prev = self.const_name.replace(node.ident.to_string());
        visit::visit_item_const(self, node);
        self.const_name = prev;
    }

    fn visit_item_static(&mut self, node: &'ast ItemStatic) {
        let prev = self.const_name.replace(node.ident.to_string());
        visit::visit_item_static(self, node);
        self.const_name = prev;
    }

    fn visit_item_mod(&mut self, node: &'ast ItemMod) {
        let bumped = node.ident == "tests"
            || node.ident == "test"
            || node.attrs.iter().any(attr_is_test);
        if bumped {
            self.test_depth += 1;
        }
        visit::visit_item_mod(self, node);
        if bumped {
            self.test_depth -= 1;
        }
    }

    fn visit_item_fn(&mut self, node: &'ast ItemFn) {
        let bumped = node.attrs.iter().any(attr_is_test);
        if bumped {
            self.test_depth += 1;
        }
        visit::visit_item_fn(self, node);
        if bumped {
            self.test_depth -= 1;
        }
    }

    fn visit_item_impl(&mut self, node: &'ast ItemImpl) {
        let bumped = node.attrs.iter().any(attr_is_test);
        if bumped {
            self.test_depth += 1;
        }
        visit::visit_item_impl(self, node);
        if bumped {
            self.test_depth -= 1;
        }
    }
}

/// Decode a raw token literal of the form `"..."`, `r"..."`, `r#"..."#`, or
/// `b"..."` into the string value it represents. Returns `None` for non-string
/// literals (numeric, char, byte-string, etc.).
fn parse_string_literal(raw: &str) -> Option<String> {
    // Try syn::Lit which understands all Rust literal forms.
    let lit: syn::Lit = syn::parse_str(raw).ok()?;
    match lit {
        syn::Lit::Str(s) => Some(s.value()),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;

    /// `///` and `#[doc = "..."]` are doc-attribute literals; they document
    /// Rust code for developers and must never reach the translation table.
    /// Only the genuine `Button::label("X")` LitStr should survive.
    #[test]
    fn doc_attribute_literals_are_suppressed() {
        let src = r#"
/// Top-level function doc.
/// Spans two lines.
fn build() {
    Button::label("X");
}

#[doc = "Y"]
struct Widget;
"#;
        let (strings, counters) =
            extract_file(Path::new("dummy.rs"), "dummy.rs", src).expect("parse");
        let values: Vec<&str> = strings.iter().map(|s| s.value.as_str()).collect();
        assert_eq!(values, vec!["X"], "only the UI literal should remain");
        assert!(
            counters.skipped_doc_attrs >= 3,
            "expected at least 3 skipped doc attrs (2 `///` lines + 1 `#[doc]`), got {}",
            counters.skipped_doc_attrs
        );
    }
}
