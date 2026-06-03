# Check Report — pr-by-file-parallel-batch-26

## Overall Verdict: PASS

All 6 checks pass. `expected_total = 49`. Live `strings.json` status counts match the summary `after` block exactly. Flag closure holds for all 12 null-target entries and all 37 non-null entries. No collateral changes detected.

---

## Check 1 — apply_summary.json internal consistency: PASS

| Assertion | Expected | Actual | Result |
|---|---|---|---|
| delta.new == -expected_total | -49 | -49 | PASS |
| delta.translated == +expected_total | +49 | +49 | PASS |
| delta.fuzzy == 0 | 0 | 0 | PASS |
| applied == expected_total | 49 | 49 | PASS |
| batch_flag_count == expected_total | 49 | 49 | PASS |
| sum(per_action) == expected_total | 49 | 36+12+1 = 49 | PASS |
| after.new == 0 | 0 | 0 | PASS |

Note: `applied = 49`, `already = 0`. The task hint "(already == 0 on a fresh batch)" matches — `already` is 0, and `applied == expected_total` is the binding assertion, which holds.

## Check 2 — live status counts vs summary "after": PASS

`Counter(e['status'])` over `translations/strings.json`:

- translated: live 6862 == summary.after 6862 — PASS
- fuzzy: live 12 == summary.after 12 — PASS
- new: live 0 == summary.after 0 — PASS
- entry_count: live 6874 == summary 6874 — PASS

## Check 3 — Flag closure (batch scope): PASS

Live count of entries carrying `pr-by-file-parallel-batch-26`: 49 (12 null-target, 37 non-null).

- All 12 null-target entries: have `do_not_translate` AND exactly one sub-flag from the allowed set {panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key}. (All 12 are `telemetry_payload`, matching per_action.flag_telemetry_payload = 12.)
- All 37 non-null entries: carry NO sub-flag.
- Violations: 0.

## Check 4 — Spot-check invariants (8 random non-null entries): PASS

Seed 26 sample. Placeholders preserved, brand literals preserved, full-width punctuation used, no ASCII "...".

- "New environment" → "新建环境"
- "Local child agents are not supported in WASM builds." → "WASM 构建不支持本地子 Agent。" (WASM, Agent preserved)
- "Sending..." → "发送中……" (full-width ellipsis, no ASCII)
- "Custom · {}" → "自定义 · {}" ({} preserved)
- "Failed to load agents. Please close and try again." → "加载 Agent 失败。请关闭后重试。"
- "{file_path} L{start_line}-L{end_line} (+{lines_added} -{lines_removed}) -- run `git diff` ..." → all {placeholders} + `git diff` preserved, "——" full-width
- "Cloud Agent" → "云端 Agent"
- "Selected {}, {}." → "已选中 {}，{}。" (both {} preserved, full-width comma)

Placeholder mismatch count: 0. ASCII ellipsis count: 0.

## Check 5 — Bilingual entries (search_terms_bilingual): PASS

1 entry (matches per_action.bilingual_search_terms = 1). Target starts with `"<source> "`:

- source: `cloud handoff auto sleep ampersand & move to cloud local`
- target: `cloud handoff auto sleep ampersand & move to cloud local 云 切换 移交 自动 睡眠 休眠 与号 移至 本地`

Prefix `<source> ` confirmed. Violations: 0.

## Check 6 — No collateral: PASS

- Batch-flagged entries: 49 == expected_total 49.
- translated delta (+49) == batch additions: 49 batch entries previously `new`, all 49 now `translated` (37 non-null translated + 12 null-target marked translated/do_not_translate).
- fuzzy delta == 0: the 12 fuzzy entries are untouched, so no non-batch entry changed (target, status).
- new went 49 → 0; the disappearing 49 are exactly the batch entries.

No entries outside `pr-by-file-parallel-batch-26` had their (target, status) altered.
