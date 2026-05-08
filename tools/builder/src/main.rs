use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::SystemTime;

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use tracing::{info, warn};

use warp_zh_builder::{
    build_index, collect_all_files, fsutil, translate_file_source, BuildReport, BuildStats,
    FailureItem, UntranslatedFile,
};
use warp_zh_extractor::translation::Table;

#[derive(Parser, Debug)]
#[command(name = "warp-zh-builder", version, about = "Build a translated copy of Warp")]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Build a translated copy of `--source` into `--out`.
    Build {
        /// Path to the Warp source root (e.g. ../../warp).
        #[arg(long)]
        source: PathBuf,

        /// Path to the translation table.
        #[arg(long, default_value = "../translations/strings.json")]
        table: PathBuf,

        /// Output directory for the translated source tree.
        #[arg(long, default_value = "../build/warp-zh")]
        out: PathBuf,

        /// Optional build report path.
        #[arg(long)]
        report: Option<PathBuf>,
    },
    /// List entries needing translation whose occurrences include any of the
    /// given path substrings. Emits JSON to stdout.
    ListBatch {
        #[arg(long, default_value = "../translations/strings.json")]
        table: PathBuf,
        /// Path substring filter (repeatable). Match if any occurrence's file
        /// contains the substring.
        #[arg(long = "filter", required = true)]
        filters: Vec<String>,
        /// Only entries with this status (default: new).
        #[arg(long, default_value = "new")]
        status: String,
    },
    /// Apply a JSON map of {id: target} to the translation table. Sets status
    /// to `translated` and adds the given flag(s) to each touched entry.
    ApplyBatch {
        #[arg(long, default_value = "../translations/strings.json")]
        table: PathBuf,
        /// Path to a JSON file shaped as `{ "flag": "pr3_first_batch",
        /// "translations": { "<id>": { "target": "..." | null,
        /// "do_not_translate": false } } }`.
        #[arg(long)]
        input: PathBuf,
        /// ISO timestamp to use for `updated_at` (defaults to now).
        #[arg(long)]
        now: Option<String>,
    },
}

fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    let cli = Cli::parse();
    match cli.cmd {
        Cmd::Build {
            source,
            table,
            out,
            report,
        } => run_build(&source, &table, &out, report.as_deref()),
        Cmd::ListBatch {
            table,
            filters,
            status,
        } => run_list_batch(&table, &filters, &status),
        Cmd::ApplyBatch { table, input, now } => run_apply_batch(&table, &input, now.as_deref()),
    }
}

fn run_build(source: &Path, table_path: &Path, out: &Path, report_path: Option<&Path>) -> Result<()> {
    let source = source
        .canonicalize()
        .with_context(|| format!("source dir not found: {}", source.display()))?;
    info!(source = %source.display(), out = %out.display(), "building translated copy");

    let table_bytes = fs::read_to_string(table_path)
        .with_context(|| format!("read table: {}", table_path.display()))?;
    let table: Table = serde_json::from_str(&table_bytes)
        .with_context(|| format!("parse table: {}", table_path.display()))?;
    let index = build_index(&table);
    info!(entries = table.entries.len(), "table loaded");

    // Reset the output dir if it already exists. Keep this scoped: only delete
    // when the user pointed at a directory the tool created (presence of a
    // marker file) OR when it doesn't yet exist. To be safe for MVP, refuse
    // to delete unless out doesn't exist or contains a previous build marker.
    let out_abs = out.to_path_buf();
    if out_abs.exists() {
        let marker = out_abs.join(".warp-zh-build-marker");
        if !marker.exists() {
            anyhow::bail!(
                "refusing to overwrite {}: missing .warp-zh-build-marker (delete the dir manually)",
                out_abs.display()
            );
        }
        fs::remove_dir_all(&out_abs)
            .with_context(|| format!("clean out: {}", out_abs.display()))?;
    }
    fs::create_dir_all(&out_abs)?;
    fs::write(out_abs.join(".warp-zh-build-marker"), b"warp-zh-builder\n")?;

    let files = collect_all_files(&source);
    info!(count = files.len(), "files discovered");

    let mut stats = BuildStats::default();
    let mut parse_failures: Vec<FailureItem> = Vec::new();
    let mut untranslated: Vec<UntranslatedFile> = Vec::new();

    for rel in &files {
        let src_path = source.join(rel);
        let dst_path = out_abs.join(rel);
        let rel_str = rel.to_string_lossy().replace('\\', "/");

        // Non-Rust files: byte copy.
        if rel.extension().and_then(|e| e.to_str()) != Some("rs") {
            fsutil::copy_file_bytes(&src_path, &dst_path)?;
            stats.files_copied += 1;
            continue;
        }

        // Rust files: read, translate, write.
        let source_text = match fs::read_to_string(&src_path) {
            Ok(t) => t,
            Err(e) => {
                // Binary or non-utf8 .rs (very unlikely) — just byte-copy.
                warn!(file = %rel_str, "non-utf8 .rs, byte-copying ({e})");
                fsutil::copy_file_bytes(&src_path, &dst_path)?;
                stats.files_copied += 1;
                continue;
            }
        };
        let (translated, outcome) = translate_file_source(&rel_str, &source_text, &index);
        if outcome.parse_failed {
            stats.files_parse_failed += 1;
            parse_failures.push(FailureItem {
                file: rel_str.clone(),
                error: outcome.error.unwrap_or_default(),
            });
            // Copy verbatim — preserves compilation if `syn` is stricter than
            // rustc, which does happen.
            fsutil::write_file(&dst_path, source_text.as_bytes())?;
            stats.files_copied += 1;
            continue;
        }
        if outcome.replacements > 0 {
            stats.files_modified += 1;
        } else {
            stats.files_copied += 1;
        }
        stats.literals_replaced += outcome.replacements;
        stats.literals_kept_english += outcome.kept_english;
        if outcome.kept_english > 0 {
            untranslated.push(UntranslatedFile {
                file: rel_str.clone(),
                kept_english: outcome.kept_english,
            });
        }
        fsutil::write_file(&dst_path, translated.as_bytes())?;
    }

    untranslated.sort_by(|a, b| b.kept_english.cmp(&a.kept_english).then(a.file.cmp(&b.file)));
    untranslated.truncate(50);

    let report = BuildReport {
        source_root: source.display().to_string(),
        source_commit: detect_git_commit(&source),
        out_root: out_abs.display().to_string(),
        built_at: now_iso8601(),
        tool_version: format!("warp-zh-builder {}", env!("CARGO_PKG_VERSION")),
        stats: stats.clone(),
        parse_failures,
        untranslated_files: untranslated,
    };

    if let Some(p) = report_path {
        fsutil::ensure_parent_dir(p)?;
        let json = serde_json::to_string_pretty(&report)?;
        fs::write(p, json + "\n")?;
        info!(report = %p.display(), "report written");
    }

    info!(
        copied = stats.files_copied,
        modified = stats.files_modified,
        parse_failed = stats.files_parse_failed,
        replaced = stats.literals_replaced,
        kept_english = stats.literals_kept_english,
        "build complete"
    );
    Ok(())
}

#[derive(serde::Serialize)]
struct ListItem<'a> {
    id: &'a str,
    source: &'a str,
    status: String,
    occurrences: Vec<&'a warp_zh_extractor::translation::Occurrence>,
    audit_score: i32,
    audit_reasons: Vec<&'a str>,
}

fn run_list_batch(table_path: &Path, filters: &[String], status_filter: &str) -> Result<()> {
    let table_bytes = fs::read_to_string(table_path)
        .with_context(|| format!("read table: {}", table_path.display()))?;
    let table: Table = serde_json::from_str(&table_bytes)
        .with_context(|| format!("parse table: {}", table_path.display()))?;

    let want_status = match status_filter {
        "new" => warp_zh_extractor::translation::Status::New,
        "translated" => warp_zh_extractor::translation::Status::Translated,
        "fuzzy" => warp_zh_extractor::translation::Status::Fuzzy,
        "approved" => warp_zh_extractor::translation::Status::Approved,
        "obsolete" => warp_zh_extractor::translation::Status::Obsolete,
        other => anyhow::bail!("unknown status: {other}"),
    };

    let mut out: Vec<ListItem> = Vec::new();
    for e in &table.entries {
        if e.status != want_status {
            continue;
        }
        // For new status entries we expect target == null; for others it could
        // be filled but caller can re-overwrite via apply-batch.
        let matches = e
            .occurrences
            .iter()
            .any(|o| filters.iter().any(|f| o.file.contains(f.as_str())));
        if !matches {
            continue;
        }
        out.push(ListItem {
            id: &e.id,
            source: &e.source,
            status: status_filter.to_string(),
            occurrences: e.occurrences.iter().collect(),
            audit_score: e.audit.score,
            audit_reasons: e.audit.reasons.iter().map(|r| r.code.as_str()).collect(),
        });
    }
    let json = serde_json::to_string_pretty(&out)?;
    println!("{json}");
    Ok(())
}

#[derive(serde::Deserialize)]
struct ApplyInput {
    #[serde(default = "default_flag")]
    flag: String,
    translations: std::collections::BTreeMap<String, ApplyEntry>,
}

#[derive(serde::Deserialize)]
struct ApplyEntry {
    /// Target string. `null` means the entry is intentionally not translated
    /// (proper noun / brand). The `do_not_translate` flag will still be added
    /// and status will go to `translated` so the builder skips re-asking.
    #[serde(default)]
    target: Option<String>,
    #[serde(default)]
    do_not_translate: bool,
    #[serde(default)]
    notes: Option<String>,
}

fn default_flag() -> String {
    "pr3_first_batch".into()
}

fn run_apply_batch(table_path: &Path, input_path: &Path, now: Option<&str>) -> Result<()> {
    let now_iso = now.map(|s| s.to_string()).unwrap_or_else(now_iso8601);

    let input_bytes = fs::read_to_string(input_path)
        .with_context(|| format!("read input: {}", input_path.display()))?;
    let input: ApplyInput = serde_json::from_str(&input_bytes)
        .with_context(|| format!("parse input: {}", input_path.display()))?;

    let table_bytes = fs::read_to_string(table_path)
        .with_context(|| format!("read table: {}", table_path.display()))?;
    let mut table: Table = serde_json::from_str(&table_bytes)
        .with_context(|| format!("parse table: {}", table_path.display()))?;

    let mut applied = 0usize;
    let mut missing: Vec<String> = Vec::new();
    let by_id: std::collections::HashMap<String, usize> = table
        .entries
        .iter()
        .enumerate()
        .map(|(i, e)| (e.id.clone(), i))
        .collect();
    for (id, payload) in &input.translations {
        let idx = match by_id.get(id) {
            Some(&i) => i,
            None => {
                missing.push(id.clone());
                continue;
            }
        };
        let entry = &mut table.entries[idx];
        // Apply target.
        match &payload.target {
            Some(t) if !t.is_empty() => entry.target = Some(t.clone()),
            _ => entry.target = None,
        }
        entry.status = warp_zh_extractor::translation::Status::Translated;
        if let Some(n) = &payload.notes {
            entry.notes = Some(n.clone());
        }
        if !entry.flags.iter().any(|f| f == &input.flag) {
            entry.flags.push(input.flag.clone());
        }
        if payload.do_not_translate
            && !entry.flags.iter().any(|f| f == "do_not_translate")
        {
            entry.flags.push("do_not_translate".into());
        }
        entry.updated_at = now_iso.clone();
        applied += 1;
    }

    if !missing.is_empty() {
        warn!(missing = ?missing, "some ids not found in table");
    }

    table.sort_canonical();
    table.recompute_stats();
    table.metadata.last_changed_at = Some(now_iso.clone());

    let mut json = serde_json::to_string_pretty(&table)?;
    if !json.ends_with('\n') {
        json.push('\n');
    }
    fs::write(table_path, json)
        .with_context(|| format!("write table: {}", table_path.display()))?;

    info!(applied, missing = missing.len(), "apply-batch complete");
    Ok(())
}

fn detect_git_commit(source: &Path) -> Option<String> {
    let output = Command::new("git")
        .args(["-C"])
        .arg(source)
        .args(["rev-parse", "HEAD"])
        .output()
        .ok()?;
    if !output.status.success() {
        return None;
    }
    let s = String::from_utf8(output.stdout).ok()?;
    let s = s.trim();
    if s.is_empty() {
        None
    } else {
        Some(s.to_string())
    }
}

fn now_iso8601() -> String {
    let dur = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .unwrap_or_default();
    let secs = dur.as_secs();
    format_iso(secs)
}

fn format_iso(secs: u64) -> String {
    let days = (secs / 86_400) as i64;
    let rem = secs % 86_400;
    let h = rem / 3600;
    let m = (rem % 3600) / 60;
    let s = rem % 60;
    let (y, mo, d) = days_to_ymd(days);
    format!("{y:04}-{mo:02}-{d:02}T{h:02}:{m:02}:{s:02}Z")
}

fn days_to_ymd(mut z: i64) -> (i32, u32, u32) {
    z += 719_468;
    let era = if z >= 0 { z } else { z - 146_096 } / 146_097;
    let doe = (z - era * 146_097) as u64;
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let y = yoe as i64 + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = if m <= 2 { y + 1 } else { y };
    (y as i32, m as u32, d as u32)
}
