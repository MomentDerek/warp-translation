//! Translation table — schema, load/save, and incremental merge per
//! `research/translation-table-format.md` §3 / §4.
//!
//! Entries are keyed by an opaque ULID. Source text is the *real* identity:
//! exact-source matches reuse the entry, similar-source (Levenshtein ≥ 0.7)
//! claims the old entry and flips it to `fuzzy`, anything else is `new`.
//! Unclaimed old entries flip to `obsolete` and are hard-deleted after 3
//! grace runs.

use std::collections::{BTreeMap, HashSet};

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use strsim::normalized_levenshtein;
use ulid::Ulid;

use crate::heuristic::Audit;
use crate::model::RawString;

pub const SCHEMA_VERSION: &str = "1.0.0";
pub const FUZZY_THRESHOLD: f64 = 0.7;
pub const OBSOLETE_GRACE_RUNS: u32 = 3;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Status {
    New,
    Translated,
    Fuzzy,
    Approved,
    Obsolete,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Occurrence {
    pub file: String,
    pub line: usize,
    pub kind: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub context_hint: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HistoryItem {
    pub source: String,
    pub source_hash: String,
    pub changed_at: String,
}

/// Field order is locked here (in declaration order) and serialization
/// preserves it — diff stability depends on this.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Entry {
    pub id: String,
    pub source: String,
    pub source_hash: String,
    pub target: Option<String>,
    pub status: Status,
    pub occurrences: Vec<Occurrence>,
    pub notes: Option<String>,
    pub flags: Vec<String>,
    pub history: Vec<HistoryItem>,
    /// Audit info from the heuristic — score, verdict, reasons. Always
    /// present for surviving entries (auto_ui *or* uncertain).
    pub audit: Audit,
    pub first_seen_commit: String,
    pub last_seen_commit: String,
    /// Run number (from .lock.json) at which this entry first became
    /// `obsolete`. Used to age out obsolete entries after
    /// `OBSOLETE_GRACE_RUNS`. `None` while the entry is alive — that keeps
    /// re-runs with no source change byte-identical.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub obsoleted_at_run: Option<u64>,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct TableStats {
    #[serde(default)]
    pub new: usize,
    #[serde(default)]
    pub translated: usize,
    #[serde(default)]
    pub fuzzy: usize,
    #[serde(default)]
    pub approved: usize,
    #[serde(default)]
    pub obsolete: usize,
    #[serde(default)]
    pub uncertain: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Metadata {
    pub source_repo: String,
    pub source_commit: Option<String>,
    pub tool_version: String,
    pub entry_count: usize,
    pub stats: TableStats,
    /// Updated only when the entries actually change. Stored separately so
    /// idempotent re-runs leave the table byte-identical.
    pub last_changed_at: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename = "Table")]
pub struct Table {
    #[serde(rename = "$schema_version")]
    pub schema_version: String,
    pub metadata: Metadata,
    pub entries: Vec<Entry>,
}

impl Table {
    pub fn empty(source_repo: &str) -> Self {
        Self {
            schema_version: SCHEMA_VERSION.to_string(),
            metadata: Metadata {
                source_repo: source_repo.to_string(),
                source_commit: None,
                tool_version: env!("CARGO_PKG_VERSION").to_string(),
                entry_count: 0,
                stats: TableStats::default(),
                last_changed_at: None,
            },
            entries: Vec::new(),
        }
    }

    pub fn sort_canonical(&mut self) {
        self.entries.sort_by(|a, b| a.id.cmp(&b.id));
    }

    pub fn recompute_stats(&mut self) {
        let mut s = TableStats::default();
        for e in &self.entries {
            match e.status {
                Status::New => s.new += 1,
                Status::Translated => s.translated += 1,
                Status::Fuzzy => s.fuzzy += 1,
                Status::Approved => s.approved += 1,
                Status::Obsolete => s.obsolete += 1,
            }
            if matches!(
                e.audit.verdict,
                crate::heuristic::Verdict::Uncertain
            ) {
                s.uncertain += 1;
            }
        }
        self.metadata.entry_count = self.entries.len();
        self.metadata.stats = s;
    }
}

/// Lock file (gitignored) — tracks the run counter used by the obsolete
/// grace period.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct Lock {
    #[serde(default)]
    pub last_extract_commit: Option<String>,
    #[serde(default)]
    pub last_extract_at: Option<String>,
    #[serde(default)]
    pub extract_run_count: u64,
}

pub fn sha256_short(s: &str) -> String {
    let mut h = Sha256::new();
    h.update(s.as_bytes());
    let out = h.finalize();
    let mut hex = String::with_capacity(16);
    for b in &out[..8] {
        hex.push_str(&format!("{b:02x}"));
    }
    hex
}

/// Generate a ULID. We keep this thin so tests can shim it out via
/// `MergeOptions::id_generator`.
pub fn new_ulid() -> String {
    Ulid::new().to_string()
}

/// Aggregated representation of one *unique source string* found in the
/// fresh extract — the merge algorithm operates on these, not on raw
/// occurrences directly.
#[derive(Debug, Clone)]
pub struct FreshGroup {
    pub source: String,
    pub source_hash: String,
    pub occurrences: Vec<Occurrence>,
    pub audit: Audit,
}

#[derive(Debug, Default, Clone)]
pub struct MergeReport {
    pub added: Vec<String>,
    pub changed: Vec<String>,
    pub unchanged: Vec<String>,
    pub obsoleted: Vec<String>,
    pub hard_deleted: Vec<String>,
}

pub struct MergeOptions {
    pub source_commit: Option<String>,
    pub run_count: u64,
    pub now_iso: String,
    /// Override ULID gen for deterministic tests.
    pub id_generator: Box<dyn FnMut() -> String>,
}

impl MergeOptions {
    pub fn new(source_commit: Option<String>, run_count: u64, now_iso: String) -> Self {
        Self {
            source_commit,
            run_count,
            now_iso,
            id_generator: Box::new(new_ulid),
        }
    }
}

/// Group a fresh extract list by source value, keeping the most informative
/// audit (highest score) and merging occurrences. Inputs that don't survive
/// the heuristic (`NotUi`) are dropped here.
pub fn group_fresh(strings: Vec<(RawString, Audit)>) -> Vec<FreshGroup> {
    use crate::heuristic::Verdict;

    let mut by_source: BTreeMap<String, FreshGroup> = BTreeMap::new();
    for (raw, audit) in strings {
        if matches!(audit.verdict, Verdict::NotUi) {
            continue;
        }
        let occ = Occurrence {
            file: raw.file.clone(),
            line: raw.line,
            kind: match raw.kind {
                crate::model::LitKind::Literal => "literal".into(),
                crate::model::LitKind::MacroToken => "macro_arg".into(),
            },
            context_hint: build_context_hint(&raw),
        };
        let entry = by_source.entry(raw.value.clone()).or_insert_with(|| FreshGroup {
            source_hash: sha256_short(&raw.value),
            source: raw.value.clone(),
            occurrences: Vec::new(),
            audit: audit.clone(),
        });
        entry.occurrences.push(occ);
        if audit.score > entry.audit.score {
            entry.audit = audit;
        }
    }
    // Stabilize occurrence order per group.
    for g in by_source.values_mut() {
        g.occurrences.sort_by(|a, b| {
            a.file.cmp(&b.file).then(a.line.cmp(&b.line))
        });
    }
    by_source.into_values().collect()
}

fn build_context_hint(raw: &RawString) -> Option<String> {
    let mut parts: Vec<String> = Vec::new();
    if let Some(c) = &raw.parent_call {
        parts.push(c.clone());
    }
    if let Some(f) = &raw.struct_field {
        parts.push(format!("field:{f}"));
    }
    if let Some(c) = &raw.enclosing_const_name {
        parts.push(format!("const:{c}"));
    }
    if let Some(m) = &raw.macro_path {
        parts.push(format!("macro:{m}"));
    }
    if parts.is_empty() {
        None
    } else {
        Some(parts.join(" > "))
    }
}

/// Core merge — produces a fresh `Table` from `old` + `fresh`. Pure (no I/O).
pub fn merge(old: Table, fresh: Vec<FreshGroup>, opts: &mut MergeOptions) -> (Table, MergeReport) {
    let MergeOptions {
        source_commit,
        run_count,
        now_iso,
        id_generator,
    } = opts;

    let mut report = MergeReport::default();
    let mut new_entries: Vec<Entry> = Vec::with_capacity(fresh.len() + old.entries.len() / 4);
    let mut seen_old_ids: HashSet<String> = HashSet::new();

    // Index old by source for O(1) exact match.
    let mut old_by_source: BTreeMap<String, Entry> = BTreeMap::new();
    let mut old_by_id: BTreeMap<String, Entry> = BTreeMap::new();
    for e in old.entries {
        old_by_source.insert(e.source.clone(), e.clone());
        old_by_id.insert(e.id.clone(), e);
    }

    for g in fresh {
        // 3a. exact source match — keep status / target, just refresh meta.
        if let Some(existing) = old_by_source.get(&g.source).cloned() {
            if seen_old_ids.contains(&existing.id) {
                // Already claimed by something else this run (shouldn't happen
                // for exact match — sources are unique by group_fresh — but
                // belt-and-suspenders).
            } else {
                let mut e = existing;
                let id = e.id.clone();
                let occ_changed = e.occurrences != g.occurrences;
                let audit_changed = audit_differs(&e.audit, &g.audit);
                let commit_changed = e.last_seen_commit != source_commit.clone().unwrap_or_default();
                e.occurrences = g.occurrences;
                e.audit = g.audit;
                if let Some(c) = source_commit.clone() {
                    e.last_seen_commit = c;
                }
                // Entry is alive again — clear obsolete grace counter.
                e.obsoleted_at_run = None;
                if occ_changed || audit_changed || commit_changed {
                    e.updated_at = now_iso.clone();
                }
                seen_old_ids.insert(id.clone());
                new_entries.push(e);
                report.unchanged.push(id);
                continue;
            }
        }

        // 3c. fuzzy — find a similar unclaimed old source.
        if let Some(candidate_source) = find_similar(
            &g.source,
            old_by_source.keys().map(|s| s.as_str()),
            &old_by_source,
            &seen_old_ids,
        ) {
            let mut e = old_by_source.get(&candidate_source).cloned().unwrap();
            // Push old source into history.
            let mut history = e.history.clone();
            history.insert(
                0,
                HistoryItem {
                    source: e.source.clone(),
                    source_hash: e.source_hash.clone(),
                    changed_at: now_iso.clone(),
                },
            );
            history.truncate(5);
            let id = e.id.clone();
            e.history = history;
            e.source = g.source.clone();
            e.source_hash = g.source_hash.clone();
            e.status = Status::Fuzzy;
            e.occurrences = g.occurrences;
            e.audit = g.audit;
            if let Some(c) = source_commit.clone() {
                e.last_seen_commit = c;
            }
            e.obsoleted_at_run = None;
            e.updated_at = now_iso.clone();
            seen_old_ids.insert(id.clone());
            new_entries.push(e);
            report.changed.push(id);
            continue;
        }

        // 3d. brand-new entry.
        let id = (id_generator)();
        let entry = Entry {
            id: id.clone(),
            source: g.source.clone(),
            source_hash: g.source_hash.clone(),
            target: None,
            status: Status::New,
            occurrences: g.occurrences,
            notes: None,
            flags: Vec::new(),
            history: Vec::new(),
            audit: g.audit,
            first_seen_commit: source_commit.clone().unwrap_or_default(),
            last_seen_commit: source_commit.clone().unwrap_or_default(),
            obsoleted_at_run: None,
            created_at: now_iso.clone(),
            updated_at: now_iso.clone(),
        };
        new_entries.push(entry);
        report.added.push(id);
    }

    // 4. orphans → obsolete (with grace period).
    for (id, mut old_entry) in old_by_id {
        if seen_old_ids.contains(&id) {
            continue;
        }
        if old_entry.status == Status::Obsolete {
            // Already obsolete: check grace counter.
            let started = old_entry.obsoleted_at_run.unwrap_or(*run_count);
            let runs_since = run_count.saturating_sub(started);
            if runs_since >= OBSOLETE_GRACE_RUNS as u64 {
                report.hard_deleted.push(id);
                continue; // hard delete
            }
            // Still in grace; preserve byte-for-byte.
            new_entries.push(old_entry);
            continue;
        }
        // Newly obsoleted: stamp the run and timestamp.
        old_entry.status = Status::Obsolete;
        old_entry.occurrences = Vec::new();
        old_entry.obsoleted_at_run = Some(*run_count);
        old_entry.updated_at = now_iso.clone();
        new_entries.push(old_entry.clone());
        report.obsoleted.push(id);
    }

    let mut table = Table {
        schema_version: SCHEMA_VERSION.to_string(),
        metadata: Metadata {
            source_repo: old.metadata.source_repo,
            source_commit: source_commit.clone(),
            tool_version: env!("CARGO_PKG_VERSION").to_string(),
            entry_count: 0,
            stats: TableStats::default(),
            last_changed_at: old.metadata.last_changed_at.clone(),
        },
        entries: new_entries,
    };
    table.sort_canonical();
    table.recompute_stats();
    let changed_now = !report.added.is_empty()
        || !report.changed.is_empty()
        || !report.obsoleted.is_empty()
        || !report.hard_deleted.is_empty();
    if changed_now || table.metadata.last_changed_at.is_none() {
        table.metadata.last_changed_at = Some(now_iso.clone());
    }
    (table, report)
}

fn audit_differs(a: &Audit, b: &Audit) -> bool {
    a.score != b.score || a.verdict != b.verdict || a.reasons.len() != b.reasons.len()
}

fn find_similar<'a>(
    fresh: &str,
    candidates: impl Iterator<Item = &'a str>,
    old_by_source: &BTreeMap<String, Entry>,
    seen: &HashSet<String>,
) -> Option<String> {
    let mut best: Option<(f64, String)> = None;
    for c in candidates {
        if let Some(entry) = old_by_source.get(c) {
            if seen.contains(&entry.id) {
                continue;
            }
        }
        let sim = normalized_levenshtein(fresh, c);
        if sim >= FUZZY_THRESHOLD {
            match &best {
                None => best = Some((sim, c.to_string())),
                Some((bs, _)) if sim > *bs => best = Some((sim, c.to_string())),
                _ => {}
            }
        }
    }
    best.map(|(_, s)| s)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::heuristic::{Reason, Verdict};

    fn dummy_audit() -> Audit {
        Audit {
            score: 8,
            verdict: Verdict::AutoUi,
            reasons: vec![Reason {
                code: "ui_method:label".into(),
                delta: 5,
            }],
        }
    }

    fn group(source: &str) -> FreshGroup {
        FreshGroup {
            source: source.into(),
            source_hash: sha256_short(source),
            occurrences: vec![Occurrence {
                file: "app/src/foo.rs".into(),
                line: 10,
                kind: "literal".into(),
                context_hint: None,
            }],
            audit: dummy_audit(),
        }
    }

    fn id_seq(seq: Vec<&'static str>) -> Box<dyn FnMut() -> String> {
        let mut iter = seq.into_iter();
        Box::new(move || iter.next().unwrap().to_string())
    }

    fn opts(run: u64, ids: Vec<&'static str>) -> MergeOptions {
        MergeOptions {
            source_commit: Some("commit1".into()),
            run_count: run,
            now_iso: "2026-05-04T00:00:00Z".into(),
            id_generator: id_seq(ids),
        }
    }

    #[test]
    fn unchanged_path_keeps_id_and_target() {
        let mut o1 = opts(1, vec!["01HW0000000000000000000001"]);
        let (table1, _) = merge(Table::empty("../warp"), vec![group("Active AI")], &mut o1);
        let id = table1.entries[0].id.clone();

        // Translator fills in target.
        let mut table_translated = table1.clone();
        table_translated.entries[0].target = Some("活动 AI".into());
        table_translated.entries[0].status = Status::Translated;

        let mut o2 = opts(2, vec![]);
        let (table2, report) = merge(table_translated, vec![group("Active AI")], &mut o2);
        assert_eq!(table2.entries.len(), 1);
        assert_eq!(table2.entries[0].id, id);
        assert_eq!(table2.entries[0].target.as_deref(), Some("活动 AI"));
        assert_eq!(table2.entries[0].status, Status::Translated);
        assert_eq!(report.unchanged, vec![id]);
        assert!(report.added.is_empty());
    }

    #[test]
    fn new_path_assigns_id() {
        let mut o = opts(1, vec!["01HW0000000000000000000001"]);
        let (table, report) = merge(Table::empty("../warp"), vec![group("Hello")], &mut o);
        assert_eq!(report.added.len(), 1);
        assert_eq!(table.entries[0].status, Status::New);
        assert!(table.entries[0].target.is_none());
    }

    #[test]
    fn fuzzy_path_carries_target_and_history() {
        // Old/new source must be similar enough that normalized Levenshtein
        // ≥ 0.7 — single-word edit (typo) is the canonical case.
        let mut o1 = opts(1, vec!["01HW0000000000000000000001"]);
        let (mut t1, _) = merge(
            Table::empty("../warp"),
            vec![group("Show agent tips when typing")],
            &mut o1,
        );
        t1.entries[0].target = Some("输入时显示代理提示".into());
        t1.entries[0].status = Status::Translated;
        let id = t1.entries[0].id.clone();

        // New source: same shape, two extra chars — well above 0.7.
        let mut o2 = opts(2, vec![]);
        let (t2, report) = merge(
            t1,
            vec![group("Show agent tips while typing.")],
            &mut o2,
        );
        assert_eq!(report.changed, vec![id.clone()], "report={report:?}");
        let entry = t2.entries.iter().find(|e| e.id == id).unwrap();
        assert_eq!(entry.status, Status::Fuzzy);
        assert_eq!(entry.target.as_deref(), Some("输入时显示代理提示"));
        assert_eq!(entry.source, "Show agent tips while typing.");
        assert_eq!(entry.history.len(), 1);
        assert_eq!(entry.history[0].source, "Show agent tips when typing");
    }

    #[test]
    fn obsolete_path_grace_then_hard_delete() {
        let mut o1 = opts(1, vec!["01HW0000000000000000000001"]);
        let (t1, _) = merge(Table::empty("../warp"), vec![group("Beta Feature")], &mut o1);
        let id = t1.entries[0].id.clone();

        // Run 2: source disappears → obsolete (obsoleted_at_run = 2).
        let mut o2 = opts(2, vec![]);
        let (t2, r2) = merge(t1, vec![], &mut o2);
        assert_eq!(r2.obsoleted, vec![id.clone()]);
        assert!(r2.hard_deleted.is_empty());
        let e = t2.entries.iter().find(|e| e.id == id).unwrap();
        assert_eq!(e.status, Status::Obsolete);
        assert_eq!(e.obsoleted_at_run, Some(2));
        assert!(e.occurrences.is_empty());

        // Run 3: still missing — still in grace.
        let mut o3 = opts(3, vec![]);
        let (t3, r3) = merge(t2, vec![], &mut o3);
        assert!(r3.hard_deleted.is_empty(), "still in grace at run 3");
        assert_eq!(t3.entries.len(), 1);

        // Run 5: 3 grace runs since obsoleted_at_run=2 → hard delete.
        let mut o5 = opts(5, vec![]);
        let (t5, r5) = merge(t3, vec![], &mut o5);
        assert_eq!(r5.hard_deleted, vec![id]);
        assert!(t5.entries.is_empty());
    }

    #[test]
    fn idempotent_unchanged_run_preserves_updated_at() {
        let mut o1 = opts(1, vec!["01HW0000000000000000000001"]);
        let (t1, _) = merge(Table::empty("../warp"), vec![group("Active AI")], &mut o1);
        let updated_at_v1 = t1.entries[0].updated_at.clone();

        // Second run with the same fresh group at a later "now": updated_at
        // must NOT bump because nothing actually changed.
        let mut o2 = MergeOptions {
            source_commit: Some("commit1".into()),
            run_count: 2,
            now_iso: "2026-05-04T01:00:00Z".into(),
            id_generator: id_seq(vec![]),
        };
        let (t2, _) = merge(t1, vec![group("Active AI")], &mut o2);
        assert_eq!(t2.entries[0].updated_at, updated_at_v1);
    }
}
