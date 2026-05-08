use serde::{Deserialize, Serialize};

/// Source kind of where a string literal was extracted from.
///
/// `Literal` = direct `LitStr` node; `MacroToken` = literal inside a macro
/// invocation token stream that we recursed into.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum LitKind {
    Literal,
    MacroToken,
}

/// One extracted string literal — file/line info for human review,
/// `byte_range` for the future `builder` to apply replacements safely.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RawString {
    pub file: String,
    pub line: usize,
    pub column: usize,
    pub byte_start: usize,
    pub byte_end: usize,
    pub value: String,
    pub kind: LitKind,
    pub macro_path: Option<String>,
    /// Enclosing call/method name (e.g. `Button::label`, `Dialog::new`).
    /// Captured during the AST walk so the heuristic can reason about UI
    /// methods/constructors without a second pass.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub parent_call: Option<String>,
    /// Argument index inside `parent_call` (0-based). `None` for non-call
    /// contexts.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub parent_call_arg_index: Option<usize>,
    /// Enclosing `const NAME: &str = "...";` / `static NAME: &str = "...";`
    /// identifier, if the literal sits inside such a definition.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub enclosing_const_name: Option<String>,
    /// True if this literal is inside `mod tests { .. }`, `#[cfg(test)]`, or
    /// `#[test]`. Captured during the walk because the heuristic needs it.
    #[serde(default, skip_serializing_if = "is_false")]
    pub in_test: bool,
    /// Enclosing struct-literal field name (e.g. `Foo { label: "..." }`
    /// captures `label`).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub struct_field: Option<String>,
}

fn is_false(b: &bool) -> bool {
    !*b
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParseFailure {
    pub file: String,
    pub error: String,
}

/// Output document of a raw extraction run (PR1 — no filtering/scoring yet).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RawExtract {
    pub source_root: String,
    pub source_commit: Option<String>,
    pub extracted_at: String,
    pub tool_version: String,
    pub stats: ExtractStats,
    pub strings: Vec<RawString>,
    pub parse_failures: Vec<ParseFailure>,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExtractStats {
    pub files_scanned: usize,
    pub files_parsed: usize,
    pub files_failed: usize,
    pub strings_found: usize,
    pub macro_token_strings: usize,
    pub skipped_macros_count: usize,
    /// `#[doc = "..."]` / `///` attribute literals suppressed at extraction.
    #[serde(default)]
    pub skipped_doc_attrs_count: usize,
}
