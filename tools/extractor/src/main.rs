use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::SystemTime;

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use tracing::{info, warn};
use warp_zh_extractor::{
    classify, collect_rust_files, extract_file, group_fresh, merge,
    model::{ExtractStats, ParseFailure, RawExtract, RawString},
    translation::{Lock, MergeOptions, Table},
};

#[derive(Parser, Debug)]
#[command(name = "warp-zh-extractor", version, about = "Extract Rust string literals from Warp")]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Full pipeline: scan source, score literals, merge into translation table.
    Extract {
        /// Path to the Warp source root (e.g. ../warp).
        #[arg(long)]
        source: PathBuf,

        /// Translation table path (PR2 default output).
        #[arg(long, default_value = "../translations/strings.json")]
        table: PathBuf,

        /// Lock file (gitignored — tracks the obsolete grace counter).
        #[arg(long, default_value = "../translations/.lock.json")]
        lock: PathBuf,

        /// If set, exit non-zero when the table on disk is not in canonical
        /// (sorted, recomputed-stats) form. Used by CI.
        #[arg(long)]
        check: bool,
    },
    /// PR1 path: dump every visible string literal to a raw JSON report. No
    /// heuristic, no translation table.
    RawExtract {
        #[arg(long)]
        source: PathBuf,

        #[arg(long, default_value = "reports/raw-extract.json")]
        out: PathBuf,
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
        Cmd::Extract {
            source,
            table,
            lock,
            check,
        } => run_extract(&source, &table, &lock, check),
        Cmd::RawExtract { source, out } => run_raw_extract(&source, &out),
    }
}

fn run_extract(source: &Path, table_path: &Path, lock_path: &Path, check: bool) -> Result<()> {
    let source = source
        .canonicalize()
        .with_context(|| format!("source dir not found: {}", source.display()))?;
    info!(source = %source.display(), "scanning rust files");

    let files = collect_rust_files(&source);
    info!(count = files.len(), "rust files found");

    let mut all_strings: Vec<RawString> = Vec::new();
    let mut parse_failures: Vec<ParseFailure> = Vec::new();
    for path in &files {
        let rel = path
            .strip_prefix(&source)
            .unwrap_or(path)
            .to_string_lossy()
            .replace('\\', "/");
        let content = match fs::read_to_string(path) {
            Ok(c) => c,
            Err(e) => {
                parse_failures.push(ParseFailure {
                    file: rel,
                    error: format!("read: {e}"),
                });
                continue;
            }
        };
        match extract_file(path, &rel, &content) {
            Ok((strings, _counters)) => all_strings.extend(strings),
            Err(e) => parse_failures.push(ParseFailure {
                file: rel,
                error: format!("parse: {e}"),
            }),
        }
    }

    // Score every literal; drop NotUi here.
    let scored: Vec<_> = all_strings
        .into_iter()
        .map(|s| {
            let a = classify(&s);
            (s, a)
        })
        .collect();
    let kept_count = scored
        .iter()
        .filter(|(_, a)| !matches!(a.verdict, warp_zh_extractor::Verdict::NotUi))
        .count();
    info!(kept = kept_count, total = scored.len(), "scoring done");

    let fresh_groups = group_fresh(scored);

    // Load old table (or start empty) and lock.
    let old_table = load_table(table_path)?;
    let mut lock = load_lock(lock_path)?;
    lock.extract_run_count = lock.extract_run_count.saturating_add(1);

    let now = now_iso8601();
    let source_commit = detect_git_commit(&source);

    let mut opts = MergeOptions::new(source_commit.clone(), lock.extract_run_count, now.clone());
    let (mut new_table, report) = merge(old_table, fresh_groups, &mut opts);
    new_table.metadata.source_repo = source.display().to_string();

    // Always re-canonicalize before write so check mode is meaningful.
    new_table.sort_canonical();
    new_table.recompute_stats();

    if check {
        // Check mode: re-load on-disk version (if any) and compare canonical form.
        let on_disk = fs::read_to_string(table_path).unwrap_or_default();
        let want = canonical_json(&new_table)?;
        if on_disk.trim() != want.trim() {
            anyhow::bail!(
                "translation table is not in canonical form (run `extract` to fix)"
            );
        }
        info!("--check passed");
        return Ok(());
    }

    write_table(table_path, &new_table)?;
    lock.last_extract_commit = source_commit;
    lock.last_extract_at = Some(now);
    write_lock(lock_path, &lock)?;

    info!(
        added = report.added.len(),
        changed = report.changed.len(),
        unchanged = report.unchanged.len(),
        obsoleted = report.obsoleted.len(),
        hard_deleted = report.hard_deleted.len(),
        entries = new_table.entries.len(),
        "merge complete"
    );
    if !parse_failures.is_empty() {
        warn!(count = parse_failures.len(), "parse failures (see report json)");
    }
    Ok(())
}

fn run_raw_extract(source: &Path, out: &Path) -> Result<()> {
    let source = source
        .canonicalize()
        .with_context(|| format!("source dir not found: {}", source.display()))?;
    info!(source = %source.display(), "scanning rust files (raw)");
    let files = collect_rust_files(&source);
    let mut all_strings: Vec<RawString> = Vec::new();
    let mut parse_failures: Vec<ParseFailure> = Vec::new();
    let mut stats = ExtractStats {
        files_scanned: files.len(),
        ..Default::default()
    };
    for path in &files {
        let rel = path
            .strip_prefix(&source)
            .unwrap_or(path)
            .to_string_lossy()
            .replace('\\', "/");
        let content = match fs::read_to_string(path) {
            Ok(c) => c,
            Err(e) => {
                parse_failures.push(ParseFailure {
                    file: rel,
                    error: format!("read: {e}"),
                });
                continue;
            }
        };
        match extract_file(path, &rel, &content) {
            Ok((strings, counters)) => {
                stats.files_parsed += 1;
                stats.macro_token_strings += counters.macro_token_literals;
                stats.skipped_macros_count += counters.skipped_macros;
                stats.skipped_doc_attrs_count += counters.skipped_doc_attrs;
                all_strings.extend(strings);
            }
            Err(e) => {
                stats.files_failed += 1;
                parse_failures.push(ParseFailure {
                    file: rel,
                    error: format!("parse: {e}"),
                });
            }
        }
    }
    stats.strings_found = all_strings.len();
    let extract = RawExtract {
        source_root: source.display().to_string(),
        source_commit: detect_git_commit(&source),
        extracted_at: now_iso8601(),
        tool_version: env!("CARGO_PKG_VERSION").to_string(),
        stats,
        strings: all_strings,
        parse_failures,
    };
    if let Some(parent) = out.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent)?;
        }
    }
    let json = serde_json::to_string_pretty(&extract)?;
    fs::write(out, json)?;
    info!(out = %out.display(), strings = extract.stats.strings_found, "raw extract done");
    Ok(())
}

fn load_table(path: &Path) -> Result<Table> {
    if !path.exists() {
        return Ok(Table::empty(""));
    }
    let bytes = fs::read_to_string(path)
        .with_context(|| format!("read table: {}", path.display()))?;
    let table: Table = serde_json::from_str(&bytes)
        .with_context(|| format!("parse table: {}", path.display()))?;
    Ok(table)
}

fn load_lock(path: &Path) -> Result<Lock> {
    if !path.exists() {
        return Ok(Lock::default());
    }
    let bytes = fs::read_to_string(path).with_context(|| format!("read lock: {}", path.display()))?;
    let lock: Lock = serde_json::from_str(&bytes).unwrap_or_default();
    Ok(lock)
}

fn write_table(path: &Path, table: &Table) -> Result<()> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent)?;
        }
    }
    let json = canonical_json(table)?;
    fs::write(path, json).with_context(|| format!("write table: {}", path.display()))?;
    Ok(())
}

/// Canonical serialization: pretty-printed JSON + trailing newline. Field
/// order is fixed by struct layout; entries are sorted by id.
fn canonical_json(table: &Table) -> Result<String> {
    let mut s = serde_json::to_string_pretty(table)?;
    if !s.ends_with('\n') {
        s.push('\n');
    }
    Ok(s)
}

fn write_lock(path: &Path, lock: &Lock) -> Result<()> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent)?;
        }
    }
    let json = serde_json::to_string_pretty(lock)?;
    fs::write(path, json + "\n")?;
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
