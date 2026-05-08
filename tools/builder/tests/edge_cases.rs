//! Integration tests for `warp-zh-builder` covering edge cases that could
//! silently corrupt the rewritten Rust code:
//!   * raw vs regular vs byte-string source forms
//!   * duplicate occurrences of the same source within one file
//!   * non-translatable statuses (`new`, `obsolete`)
//!   * unicode passthrough (CJK targets)
//!   * targets containing characters that would need escaping in regular form
//!   * targets containing `"#` sequences (raw-string fallback hash escalation)
//!
//! These tests build a small in-memory translation table and feed it into
//! `translate_file_source` directly. After translation, the produced source
//! is re-parsed with `syn::parse_file` to confirm it is still valid Rust —
//! the strongest cheap correctness signal we can get without a full
//! `cargo check`.

use std::collections::HashMap;

use warp_zh_builder::{build_index, translate_file_source};
use warp_zh_extractor::heuristic::{Audit, Reason, Verdict};
use warp_zh_extractor::translation::{
    sha256_short, Entry, Metadata, Occurrence, Status, Table, TableStats,
};

fn mk_entry(source: &str, target: Option<&str>, status: Status) -> Entry {
    Entry {
        id: format!("ID-{}", sha256_short(source)),
        source: source.into(),
        source_hash: sha256_short(source),
        target: target.map(|t| t.into()),
        status,
        occurrences: vec![Occurrence {
            file: "x.rs".into(),
            line: 1,
            kind: "literal".into(),
            context_hint: None,
        }],
        notes: None,
        flags: Vec::new(),
        history: Vec::new(),
        audit: Audit {
            score: 8,
            verdict: Verdict::AutoUi,
            reasons: vec![Reason {
                code: "ui".into(),
                delta: 5,
            }],
        },
        first_seen_commit: "c".into(),
        last_seen_commit: "c".into(),
        obsoleted_at_run: None,
        created_at: "t".into(),
        updated_at: "t".into(),
    }
}

fn mk_table(entries: Vec<Entry>) -> Table {
    Table {
        schema_version: "1.0.0".into(),
        metadata: Metadata {
            source_repo: "..".into(),
            source_commit: None,
            tool_version: "test".into(),
            entry_count: entries.len(),
            stats: TableStats::default(),
            last_changed_at: None,
        },
        entries,
    }
}

/// Re-parse the produced source with `syn` — the strongest correctness check
/// we can apply without spinning up `cargo check`.
fn assert_parses(label: &str, src: &str) {
    if let Err(e) = syn::parse_file(src) {
        panic!("[{label}] produced invalid Rust: {e}\n----\n{src}\n----");
    }
}

/// Same source string appearing several times in one file must be replaced
/// every time (descending byte-range walk).
#[test]
fn duplicate_source_replaces_every_occurrence() {
    let table = mk_table(vec![mk_entry("OK", Some("确定"), Status::Translated)]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = "OK";
    let _ = "OK";
    let _ = "OK";
    let _ = ("OK", "OK");
}
"#;
    let (out, outcome) = translate_file_source("dup.rs", src, &idx);
    assert_eq!(outcome.replacements, 5, "got: {out}");
    assert_parses("duplicate_source", &out);
    assert_eq!(out.matches("\"确定\"").count(), 5);
    assert!(!out.contains("\"OK\""));
}

/// Entries with non-translatable status (`new`, `obsolete`) must NOT be
/// applied even if `target` is set somehow.
#[test]
fn non_translatable_status_keeps_english() {
    let table = mk_table(vec![
        mk_entry("New", Some("新"), Status::New),
        mk_entry("Old", Some("旧"), Status::Obsolete),
        mk_entry("Approved", Some("批准"), Status::Approved),
    ]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = "New";
    let _ = "Old";
    let _ = "Approved";
}
"#;
    let (out, outcome) = translate_file_source("status.rs", src, &idx);
    // Only Approved should have been applied.
    assert_eq!(outcome.replacements, 1, "got: {out}");
    assert_eq!(outcome.kept_english, 2, "got: {out}");
    assert!(out.contains("\"批准\""));
    assert!(out.contains("\"New\""));
    assert!(out.contains("\"Old\""));
    assert_parses("status_filter", &out);
}

/// Empty target must keep the English literal even when status is translated
/// (this is how `do_not_translate` brand names are encoded).
#[test]
fn empty_target_keeps_english() {
    let table = mk_table(vec![
        mk_entry("Warp", None, Status::Translated),
        mk_entry("Hello", Some(""), Status::Translated),
    ]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = "Warp";
    let _ = "Hello";
}
"#;
    let (out, outcome) = translate_file_source("empty.rs", src, &idx);
    assert_eq!(outcome.replacements, 0);
    assert_eq!(outcome.kept_english, 2);
    assert!(out.contains("\"Warp\""));
    assert!(out.contains("\"Hello\""));
    assert_parses("empty_target", &out);
}

/// Byte-string literals (`b"..."`, `br"..."`) must never be touched.
/// (The extractor doesn't yield them either — belt and suspenders.)
#[test]
fn byte_strings_untouched() {
    // Even if the table somehow contained an entry whose source string equals
    // the byte-string's value, the renderer guards against rewriting it. We
    // can't easily exercise that path because the extractor won't yield byte
    // strings, but we can confirm files containing them parse and pass through
    // unchanged for non-matching content.
    let table = mk_table(vec![mk_entry("Hello", Some("你好"), Status::Translated)]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _: &[u8] = b"Hello";
    let _: &[u8] = br"Hello";
    let _ = "Hello";
}
"#;
    let (out, outcome) = translate_file_source("bytes.rs", src, &idx);
    // Only the regular string literal should have been rewritten.
    assert_eq!(outcome.replacements, 1, "got: {out}");
    assert!(out.contains("b\"Hello\""), "byte string mutated: {out}");
    assert!(out.contains("br\"Hello\""), "byte raw string mutated: {out}");
    assert!(out.contains("\"你好\""), "regular string not translated: {out}");
    assert_parses("byte_strings", &out);
}

/// CJK / Unicode targets are passed through verbatim — UTF-8 in source is
/// legal Rust.
#[test]
fn unicode_target_passthrough() {
    let table = mk_table(vec![
        mk_entry("Quit Warp?", Some("退出 Warp？"), Status::Translated),
        mk_entry("emoji", Some("✓ 完成 🎉"), Status::Translated),
    ]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = "Quit Warp?";
    let _ = "emoji";
}
"#;
    let (out, outcome) = translate_file_source("unicode.rs", src, &idx);
    assert_eq!(outcome.replacements, 2);
    assert!(out.contains("\"退出 Warp？\""), "got: {out}");
    assert!(out.contains("\"✓ 完成 🎉\""), "got: {out}");
    assert_parses("unicode", &out);
}

/// Special characters in the target that need escaping in a regular string.
/// Verifies `escape_regular` produces parseable Rust.
#[test]
fn target_with_escapes_in_regular_form() {
    let table = mk_table(vec![
        mk_entry("path", Some("C:\\Users\\name"), Status::Translated),
        mk_entry("quoted", Some("say \"hi\""), Status::Translated),
        mk_entry("multi", Some("line1\nline2\ttab"), Status::Translated),
        mk_entry("control", Some("bell\x07end"), Status::Translated),
        mk_entry("nul", Some("a\0b"), Status::Translated),
    ]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = "path";
    let _ = "quoted";
    let _ = "multi";
    let _ = "control";
    let _ = "nul";
}
"#;
    let (out, outcome) = translate_file_source("escapes.rs", src, &idx);
    assert_eq!(outcome.replacements, 5, "got: {out}");
    assert_parses("escapes", &out);
    // Spot-check a couple of the produced literals.
    assert!(
        out.contains("\"C:\\\\Users\\\\name\""),
        "backslashes not escaped: {out}"
    );
    assert!(
        out.contains("\"say \\\"hi\\\"\""),
        "quotes not escaped: {out}"
    );
    assert!(out.contains("\\n"), "newline not escaped: {out}");
    assert!(out.contains("\\t"), "tab not escaped: {out}");
}

/// Source was a raw string (`r"..."`); target contains many backslashes/quotes
/// → `escape_raw` fallback path. The output must still parse.
#[test]
fn raw_source_with_escape_heavy_target() {
    let table = mk_table(vec![mk_entry(
        "PATH",
        Some(r#"a"b"c"d\e\f"#),
        Status::Translated,
    )]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = r"PATH";
}
"#;
    let (out, outcome) = translate_file_source("raw.rs", src, &idx);
    assert_eq!(outcome.replacements, 1, "got: {out}");
    assert_parses("raw_escape_heavy", &out);
}

/// Source was raw, target contains `"#` sequences that force the
/// hash-escalation path in `escape_raw`. Output must still parse.
#[test]
fn raw_source_target_with_quote_hash_sequences() {
    // 5+ quotes/backslashes total to trigger needs_many_escapes(>=3).
    let target = "weird \"# end \" inside \"\"# more";
    let table = mk_table(vec![mk_entry("X", Some(target), Status::Translated)]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let _ = r"X";
}
"#;
    let (out, outcome) = translate_file_source("hashy.rs", src, &idx);
    assert_eq!(outcome.replacements, 1, "got: {out}");
    assert_parses("hashy", &out);

    // Re-parse and confirm the literal value matches the target exactly.
    let ast = syn::parse_file(&out).expect("parses");
    let mut found: Option<String> = None;
    syn::visit::visit_file(
        &mut LitStrCollector { values: &mut found },
        &ast,
    );
    assert_eq!(found.as_deref(), Some(target));
}

struct LitStrCollector<'a> {
    values: &'a mut Option<String>,
}
impl<'ast, 'a> syn::visit::Visit<'ast> for LitStrCollector<'a> {
    fn visit_lit_str(&mut self, node: &'ast syn::LitStr) {
        if self.values.is_none() {
            *self.values = Some(node.value());
        }
    }
}

/// `syn::parse_file` failure path: an entirely invalid `.rs` returns the
/// original source unchanged with `parse_failed = true`.
#[test]
fn parse_failure_preserves_source_byte_for_byte() {
    let bad_src = "fn main() { let x =";
    let idx: HashMap<&str, &Entry> = HashMap::new();
    let (out, outcome) = translate_file_source("bad.rs", bad_src, &idx);
    assert!(outcome.parse_failed);
    assert_eq!(out, bad_src);
}

/// Several edits in one file must remain byte-correct (descending order).
/// Verifies no off-by-one in `replace_range`.
#[test]
fn many_edits_one_file_round_trip() {
    let table = mk_table(vec![
        mk_entry("Alpha", Some("甲"), Status::Translated),
        mk_entry("Beta", Some("乙"), Status::Translated),
        mk_entry("Gamma", Some("丙"), Status::Translated),
        mk_entry("Delta", Some("丁"), Status::Translated),
    ]);
    let idx = build_index(&table);
    let src = r#"
fn ui() {
    let v = vec!["Alpha", "Beta", "Gamma", "Delta", "Alpha", "Beta"];
    let _ = v;
}
"#;
    let (out, outcome) = translate_file_source("many.rs", src, &idx);
    assert_eq!(outcome.replacements, 6, "got: {out}");
    assert_parses("many_edits", &out);
    assert!(out.contains("\"甲\""));
    assert!(out.contains("\"乙\""));
    assert!(out.contains("\"丙\""));
    assert!(out.contains("\"丁\""));
    assert!(!out.contains("\"Alpha\""));
}
