# Check report — batch-24

**Verdict: PASS**

(Supersedes an earlier stale report written before the apply step ran. The apply has since
completed: `apply_summary.json` is present, 60 entries carry `pr-by-file-parallel-batch-24`,
and `new` is now 0.)

Batch flag: `pr-by-file-parallel-batch-24` · 60 entries (35 translate + 19 telemetry_payload + 4 extractor_false_positive_doc_comment + 1 protocol_key + 1 bilingual_search_terms) · entry_count 6794.

## 1. Flag closure — PASS

- 60 candidate ids (A..H) == 60 output ids == 60 entries carrying `pr-by-file-parallel-batch-24` in `strings.json`. No id dropped, none added.
- Every candidate id resolves to an entry in the table; all `status: translated`.

## 2. Delta correctness — PASS

- Live status counts: `translated 6722`, `fuzzy 65`, `obsolete 7`, `new 0`.
- Matches `apply_summary.after` exactly: new 60→0, translated +60, fuzzy unchanged at 65.
- Recounted per-action from the applied table equals `apply_summary.per_action` (translate 35 / telemetry_payload 19 / protocol_key 1 / extractor_false_positive_doc_comment 4 / bilingual_search_terms 1).

## 3. Sub-flag integrity — PASS

- Every `do_not_translate` entry (24 of them) carries exactly one whitelist sub-flag and `target: null`.
- Every translated/bilingual entry (36) has a non-null, non-empty Chinese target.
- Output-file declared sub-flags agree with the applied-table flags for every id.

## 4. Spot-checks vs per-entry decision flow — PASS

- GPU identifier `Intel(R) UHD Graphics 620` (wgpu/resources.rs:498) → flagged `protocol_key`, target null. Correct (matched via `adapter_info.name.contains(...)`, external driver string).
- secrets.rs `///` fragments (ids GT0…, HP6…, JJV…, KJQ…) → `extractor_false_positive_doc_comment`, target null. Correct (captured inside `lazy_static!` body).
- `safe_error!` / `safe_warn!` args (remote.rs, notebooks/file/mod.rs, remote_server/client/mod.rs) and `tracing`/Display-impl format strings (event.rs:441, diff_hunk_parser.rs:23, telemetry_event.rs:572) → `telemetry_payload`, target null. Correct.
- teams_page link-suffix fragments `01KSMD6JWV0GHKMKJ5R25KBW08` and `01KSMD6K83NT1Q79YPJDZ5B3G1` both preserve the leading ASCII space in the target (`" ，以…"`). `01KSMD6TGBZ4GKGP0H8NJPXH1N` preserves the trailing ASCII space. Correct.
- Brand/identifier verbatim: `Warp`, `Bedrock`, `API` (→ "API 密钥"), `Agent`, `run_agents` all preserved. Placeholder parity holds for every translated entry (flagged entries with placeholders kept null per policy).
- search_terms bilingual `01KSMD72AP6R5M0HWV6MD48632`: target starts with the verbatim English keyword list + a space, then space-separated lowercase Chinese, no punctuation. Correct.

## 5. 'Remove server' vs 'Remove Member' collision — IN-BATCH OK; PRE-EXISTING ISSUE NOTED (out of scope)

- The new batch-24 entry `01KSMD6ZJHNCMPKXWFWQZ6RY4W` ("Remove server", footer.rs:1264) → `移除服务器`. Correct and in-scope.
- **Finding (not a batch-24 failure):** the pre-existing entry `01KQXQV12EYWK584GRN3X0SHTP` (cloud_action_confirmation_dialog.rs:32, const `REMOVE_TEAM_MEMBER_RELOAD_CREDITS_CONFIRM_TEXT`) now has `source: "Remove Member"` but a **stale target `移除服务器` ("Remove server")**. Its `history` shows the upstream source changed `Remove server → Remove Member` in the same 2026-05-27 sync, which flipped it to `status: fuzzy` but left the old translation in place. Correct target is `移除成员`.
  - This entry is NOT in batch-24 (no batch flag, status `fuzzy`). The batch apply correctly left fuzzy at 65, so fixing it here would break the validated "fuzzy unchanged" invariant and mix an unrelated edit into the batch commit. **Left unmodified by design.** Recommend correcting in the next fuzzy-resweep / batch (set target `移除成员`, status `translated`).

## Validators

- `warp-zh-extractor … --check` → exit 0 ("--check passed"); table consistent with source (3299 files scanned).
- Apply-time hard validators (placeholder parity, strftime, whitespace, brand preservation, flag closure) already green per the apply step; placeholder parity and brand preservation independently re-verified here — no violations.
