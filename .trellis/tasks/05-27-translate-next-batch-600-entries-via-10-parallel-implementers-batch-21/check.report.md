# Check Report — batch-21 (pr-by-file-parallel-batch-21)

Date: 2026-05-27
Validator: trellis-check
Verdict: **PASS**

> Note: this report supersedes an earlier FAIL report that was written before the
> apply step ran. The apply step has since executed successfully
> (`outputs/apply_summary.json`, `applied_at: 2026-05-27T07:31:07Z`).

## Scope

Validation of completed parallel-translation batch-21 (manifest expected_total = 602,
sub-batches A–J). Apply step already ran; this report validates the result against the
five required invariants and the translation contract
(`.trellis/spec/guides/translation-contract.md`).

## Invariant Results

### 1. apply_summary.json deltas — PASS
- File exists at `outputs/apply_summary.json`.
- `delta.new == -602` ✓
- `delta.translated == 602` ✓ (recorded as `+602`)
- `applied == 602`, `already == 0`, `expected_total == 602`.
- `batch_flag_count == 602`, `entry_count == 6734`.

### 2. Flag count in strings.json — PASS
- Exactly **602** entries carry flag `pr-by-file-parallel-batch-21`
  (recomputed directly from `translations/strings.json`).

### 3. Flag closure — PASS
- 276 `do_not_translate` entries: every one has `target == null`,
  `status == "translated"`, and **exactly one** sub-flag from the whitelist
  {panic_message, telemetry_payload, extractor_false_positive_doc_comment,
  test_fixture, wgpu_debug_label, protocol_key}. Zero violations.
- 326 non-`do_not_translate` entries (319 translate + 7 search_terms_bilingual):
  every one has a **non-null** target. Zero violations.
- Per-action distribution recomputed from the table exactly matches
  apply_summary.json:
  - flag_telemetry_payload: 150
  - flag_panic_message: 63
  - flag_protocol_key: 29
  - flag_extractor_false_positive_doc_comment: 22
  - flag_test_fixture: 12
  - translate: 319
  - bilingual_search_terms: 7
  - Total: 602 ✓

### 4. Spot-checks — PASS
- **Placeholder preservation**: scanned all 326 translated targets; multiset of
  `{...}` tokens in source == target for every entry. **0 mismatches.**
- **Brand-literal preservation**: checked standalone brand tokens (Warp, Warp Drive,
  MCP, OpenAI, GitHub, AWS, Bedrock, SSH, Wispr Flow) present in source — all retained
  in target. **0 drops.**
- **strftime tokens** (`%b`, `%d`, …): multiset preserved across all translated
  entries. **0 mismatches.**
- **Whitespace edges**: leading/trailing whitespace parity between source and target
  preserved (e.g. `" tab "` → `" 个标签页 "`, `" windows"` → `" 个窗口"`). **0 mismatches.**
- Sample eyeball of 12 translated entries shows correct fragment recombination, `您`
  register, full-width punctuation, and placeholder positioning.

### 5. Previously-offending entry — PASS
- id `01KQXQV12G8TY6X7BTWNF1709K`
  - source: `The Agentic Development Environment`
  - target: `Agentic 开发环境`
  - The `Agent` brand literal is preserved (target contains "Agent"). ✓

## Notes (non-blocking)

- One fragment entry (`source: "anytime."` → `target: "重新启用。"`) is a sentence-fragment
  recombination where the Chinese restructures across split source segments. It is a
  translated (non-flagged) entry, passes placeholder/brand/edge checks, and is not a
  flag-closure violation. Flagged here only for awareness, not as a defect.

## Summary

All five invariants pass. 602 entries flagged, flag closure clean, placeholder/brand/
strftime/whitespace integrity intact, and the previously-offending brand-literal entry
is corrected.

{verdict: PASS}
