//! `warp-zh-builder` library — produces a translated copy of a Warp source
//! tree by:
//!   1. Mirroring the directory tree (skipping the same set of ignored dirs as
//!      the extractor walker).
//!   2. Re-parsing each `.rs` file with `syn`, collecting LitStr byte ranges
//!      via the extractor's visitor, then surgically rewriting only the
//!      literals whose translation table entry has a non-empty `target` and
//!      a translatable status.
//!
//! The replacement is applied in descending byte-range order so earlier ranges
//! aren't invalidated by later edits, per
//! `research/syn-string-extraction.md`. Files that fail to parse are copied
//! verbatim and recorded in the build report.

use std::collections::HashMap;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};

use warp_zh_extractor::{extract_file, Entry, Status, Table};

pub mod fsutil;
pub mod report;

pub use report::{BuildReport, BuildStats, FailureItem, UntranslatedFile};

/// Statuses whose `target` we apply during build. `new` and `obsolete` keep
/// the original English literal.
fn is_translatable_status(status: Status) -> bool {
    matches!(status, Status::Translated | Status::Approved | Status::Fuzzy)
}

/// Build an in-memory translation index keyed by source string. For ambiguous
/// cases where multiple entries share the same source (rare — only when
/// occurrences differ across files), the first one wins. Acceptable for MVP
/// because exact source matches are unique by construction in the table
/// (`group_fresh` keys by source value).
pub fn build_index(table: &Table) -> HashMap<&str, &Entry> {
    let mut idx: HashMap<&str, &Entry> = HashMap::with_capacity(table.entries.len());
    for e in &table.entries {
        idx.entry(e.source.as_str()).or_insert(e);
    }
    idx
}

/// Outcome of processing one `.rs` file.
#[derive(Debug, Clone, Default)]
pub struct FileOutcome {
    pub replacements: usize,
    pub kept_english: usize,
    pub parse_failed: bool,
    pub error: Option<String>,
}

/// Apply translations to the contents of one file. Returns the rewritten
/// source plus per-file counters. If `syn` fails to parse the file, the
/// source is returned unchanged and `parse_failed` is set.
pub fn translate_file_source(
    rel_path: &str,
    source: &str,
    index: &HashMap<&str, &Entry>,
) -> (String, FileOutcome) {
    let mut outcome = FileOutcome::default();

    // Re-use the extractor's visitor: it already gives us LitStr byte ranges
    // plus the source value. We don't need the audit/heuristic in the builder.
    let strings = match extract_file(Path::new(rel_path), rel_path, source) {
        Ok((strings, _counters)) => strings,
        Err(e) => {
            outcome.parse_failed = true;
            outcome.error = Some(format!("parse: {e}"));
            return (source.to_string(), outcome);
        }
    };

    // Collect (start, end, replacement) triples; only for entries with a
    // non-empty translatable target.
    let mut edits: Vec<(usize, usize, String)> = Vec::new();
    for raw in strings {
        let entry = match index.get(raw.value.as_str()) {
            Some(e) => *e,
            None => {
                // Literal not in the table at all (e.g. heuristic dropped it
                // as NotUi). Keep English silently.
                continue;
            }
        };
        let target = match entry.target.as_deref() {
            Some(t) if !t.is_empty() && is_translatable_status(entry.status) => t,
            _ => {
                outcome.kept_english += 1;
                continue;
            }
        };
        // Determine how the original literal was quoted (`"..."`, `r"..."`,
        // `r#"..."#`, possibly `b"..."`). Decide the safest output form and
        // skip if the source was a byte-string (those should never have been
        // extracted, but belt-and-suspenders).
        let original_slice = match source.get(raw.byte_start..raw.byte_end) {
            Some(s) => s,
            None => continue,
        };
        match render_replacement(original_slice, target) {
            Some(rep) => {
                edits.push((raw.byte_start, raw.byte_end, rep));
                outcome.replacements += 1;
            }
            None => {
                outcome.kept_english += 1;
            }
        }
    }

    if edits.is_empty() {
        return (source.to_string(), outcome);
    }

    // Sort by byte_start descending so applying earlier edits doesn't
    // invalidate the byte offsets of later edits.
    edits.sort_by(|a, b| b.0.cmp(&a.0));
    let mut out = source.to_string();
    for (start, end, rep) in edits {
        out.replace_range(start..end, &rep);
    }
    (out, outcome)
}

/// Pick a replacement form that re-quotes the translated string in a way the
/// Rust compiler can parse. Returns `None` for byte-string literals (`b"..."`
/// — never user-facing UI).
fn render_replacement(original_slice: &str, target: &str) -> Option<String> {
    // `b"..."` and `br"..."` are byte strings — refuse to translate.
    if original_slice.starts_with('b') {
        return None;
    }
    let was_raw = original_slice.starts_with('r');
    // Default: regular `"..."` with proper escaping.
    let regular = escape_regular(target);
    if !was_raw {
        return Some(regular);
    }
    // Source was raw. If the target is safe inside a regular string (it always
    // is — escape_regular handles every char), prefer regular form for
    // consistency. Some teams prefer to preserve raw form, but raw doesn't
    // permit `\u{...}` escapes anyway and the input is plain text.
    //
    // Exception: if escaping the target produces a string whose contents look
    // less readable due to many `\\` runs, fall back to raw with hashes that
    // don't appear in the target.
    if needs_many_escapes(target) {
        Some(escape_raw(target))
    } else {
        Some(regular)
    }
}

/// Heuristic: prefer raw form when target has 3+ backslashes or quotes that
/// would all need escaping in regular form. Mostly cosmetic — both forms
/// compile.
fn needs_many_escapes(target: &str) -> bool {
    let count = target.bytes().filter(|b| matches!(*b, b'\\' | b'"')).count();
    count >= 3
}

fn escape_regular(s: &str) -> String {
    let mut out = String::with_capacity(s.len() + 2);
    out.push('"');
    for c in s.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '"' => out.push_str("\\\""),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '\0' => out.push_str("\\0"),
            c if (c as u32) < 0x20 => {
                use std::fmt::Write;
                write!(out, "\\u{{{:x}}}", c as u32).expect("write to string");
            }
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

/// Emit `r#"..."#` (or more hashes if the target itself contains `"#`).
fn escape_raw(s: &str) -> String {
    let mut hashes = 1usize;
    loop {
        let needle: String =
            std::iter::once('"').chain(std::iter::repeat_n('#', hashes)).collect();
        if !s.contains(&needle) {
            break;
        }
        hashes += 1;
        if hashes > 8 {
            // Pathological — fall back to escaped regular string.
            return escape_regular(s);
        }
    }
    let pad = "#".repeat(hashes);
    format!("r{pad}\"{s}\"{pad}")
}

/// List every file (relative paths) under `root`, skipping ignored dirs.
/// Symlinks are followed only at the leaf level (matches walkdir defaults).
pub fn collect_all_files(root: &Path) -> Vec<PathBuf> {
    use walkdir::WalkDir;
    let mut out = Vec::new();
    for entry in WalkDir::new(root)
        .follow_links(false)
        .into_iter()
        .filter_entry(|e| {
            !warp_zh_extractor::is_ignored_dir(e.file_name().to_string_lossy().as_ref())
        })
    {
        let entry = match entry {
            Ok(e) => e,
            Err(_) => continue,
        };
        if entry.file_type().is_file() {
            if let Ok(rel) = entry.path().strip_prefix(root) {
                out.push(rel.to_path_buf());
            }
        }
    }
    out.sort();
    out
}

/// Configuration for one builder run.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BuildConfig {
    pub source_root: PathBuf,
    pub out_root: PathBuf,
    pub table_path: PathBuf,
    pub report_path: Option<PathBuf>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn render_regular_string_basic() {
        assert_eq!(render_replacement("\"X\"", "你好"), Some("\"你好\"".to_string()));
    }

    #[test]
    fn render_regular_string_escapes() {
        assert_eq!(
            render_replacement("\"hi\"", "say \"hi\" \\ now\n"),
            Some("\"say \\\"hi\\\" \\\\ now\\n\"".to_string())
        );
    }

    #[test]
    fn render_byte_string_skipped() {
        assert!(render_replacement("b\"X\"", "你好").is_none());
        assert!(render_replacement("br\"X\"", "你好").is_none());
    }

    #[test]
    fn render_raw_falls_back_when_many_escapes() {
        // 3 backslashes / quotes in the target → emit raw with hashes.
        let out = render_replacement("r\"X\"", "a\"b\"c\"d").unwrap();
        assert!(out.starts_with("r#\""));
        assert!(out.ends_with("\"#"));
    }

    #[test]
    fn translate_file_replaces_only_translated_entries() {
        // Build a minimal table with one Translated entry.
        use warp_zh_extractor::translation::{
            sha256_short, Entry, Metadata, Occurrence, Status, Table, TableStats,
        };
        use warp_zh_extractor::heuristic::{Audit, Reason, Verdict};

        let entry = Entry {
            id: "ID1".into(),
            source: "Hello".into(),
            source_hash: sha256_short("Hello"),
            target: Some("你好".into()),
            status: Status::Translated,
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
                reasons: vec![Reason { code: "ui".into(), delta: 5 }],
            },
            first_seen_commit: "c".into(),
            last_seen_commit: "c".into(),
            obsoleted_at_run: None,
            created_at: "t".into(),
            updated_at: "t".into(),
        };
        let table = Table {
            schema_version: "1.0.0".into(),
            metadata: Metadata {
                source_repo: "..".into(),
                source_commit: None,
                tool_version: "test".into(),
                entry_count: 1,
                stats: TableStats::default(),
                last_changed_at: None,
            },
            entries: vec![entry],
        };
        let idx = build_index(&table);
        let src = r#"fn main() { let _ = "Hello"; let _ = "Untouched"; }"#;
        let (out, outcome) = translate_file_source("x.rs", src, &idx);
        assert!(out.contains("\"你好\""), "got: {out}");
        assert!(out.contains("\"Untouched\""));
        assert_eq!(outcome.replacements, 1);
        assert!(!outcome.parse_failed);
    }

    #[test]
    fn parse_failure_returns_unchanged() {
        let src = "fn main() { let bad =";
        let idx: HashMap<&str, &Entry> = HashMap::new();
        let (out, outcome) = translate_file_source("x.rs", src, &idx);
        assert_eq!(out, src);
        assert!(outcome.parse_failed);
    }

    #[test]
    fn descending_apply_handles_multiple_edits() {
        use warp_zh_extractor::translation::{
            sha256_short, Entry, Metadata, Occurrence, Status, Table, TableStats,
        };
        use warp_zh_extractor::heuristic::{Audit, Reason, Verdict};

        fn mk(src: &str, tgt: &str) -> Entry {
            Entry {
                id: src.into(),
                source: src.into(),
                source_hash: sha256_short(src),
                target: Some(tgt.into()),
                status: Status::Translated,
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
                    reasons: vec![Reason { code: "ui".into(), delta: 5 }],
                },
                first_seen_commit: "c".into(),
                last_seen_commit: "c".into(),
                obsoleted_at_run: None,
                created_at: "t".into(),
                updated_at: "t".into(),
            }
        }
        let table = Table {
            schema_version: "1.0.0".into(),
            metadata: Metadata {
                source_repo: "..".into(),
                source_commit: None,
                tool_version: "test".into(),
                entry_count: 0,
                stats: TableStats::default(),
                last_changed_at: None,
            },
            entries: vec![mk("Alpha", "甲"), mk("Beta", "乙"), mk("Gamma", "丙")],
        };
        let idx = build_index(&table);
        let src = r#"fn f() { ["Alpha", "Beta", "Gamma"]; }"#;
        let (out, outcome) = translate_file_source("x.rs", src, &idx);
        assert_eq!(outcome.replacements, 3);
        assert!(out.contains("\"甲\""));
        assert!(out.contains("\"乙\""));
        assert!(out.contains("\"丙\""));
    }
}
