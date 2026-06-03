# Check Report — batch apply `pr-by-file-parallel-batch-25`

## Overall Verdict: PASS

All 6 checks passed. 110 entries applied (75 translate, 5 bilingual_search_terms, 9 flag_telemetry_payload, 11 flag_panic_message, 10 flag_protocol_key). No collateral changes. No fixes required.

---

## Check 1 — apply_summary.json internal consistency: PASS

`expected_total = 110`

- `delta.new == -110` (== -expected_total) — PASS
- `delta.translated == +110` (== +expected_total) — PASS
- `delta.fuzzy == 0` — PASS
- `applied == 110` (== expected_total; summary reports 110 applied on this batch) — PASS
- `batch_flag_count == 110` (== expected_total) — PASS
- `sum(per_action) == 75+5+9+11+10 == 110` (== expected_total) — PASS

## Check 2 — live status counts vs apply_summary "after": PASS

Re-derived from `translations/strings.json`:
`Counter({'translated': 6796, 'fuzzy': 78, 'obsolete': 30})`

- translated 6796 == after.translated 6796 — PASS
- new 0 == after.new 0 — PASS
- fuzzy 78 == after.fuzzy 78 — PASS

Note: `obsolete: 30` is not tracked in the summary's `after` block; these are pre-existing entries unrelated to the batch (see Check 6).

## Check 3 — flag closure (batch scope): PASS

Live batch_flag_count = 110 (30 null-target, 80 non-null-target).

- All 30 null-target entries carry `do_not_translate` AND exactly one sub-flag from the allowed set {panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key}. — PASS
- All 80 non-null-target entries carry NO sub-flag. — PASS

0 violations.

## Check 4 — invariants on 8 random non-null-target entries: PASS

Sampled (seed=25): placeholders preserved, brand literals preserved, no ASCII "...", full-width punctuation used. Examples:

- `API key '{name}' saved.` -> `API 密钥“{name}”已保存。` (placeholder `{name}` preserved, full-width quotes + period, brand `API` preserved)
- `auto dismiss Rich Input after submitting prompt` -> `提交提示词后自动关闭 Rich Input` (brand `Rich Input` preserved)
- `Close tabs above` -> `关闭上方标签页`
- `Run metadata is not available` -> `运行元数据不可用`

Repo-wide scan of all 80 non-null targets: 0 ASCII-ellipsis, 0 sentence-final ASCII periods on CJK strings.

## Check 5 — bilingual entries (search_terms_bilingual): PASS

5 bilingual entries; each target starts with `<source> ` (source + single space + appended Chinese keywords). 0 failures.

- `autosuggestion ignore button hide` -> `autosuggestion ignore button hide 自动建议 忽略 按钮 隐藏`
- `iap staging gcloud proxy credentials` -> `iap staging gcloud proxy credentials 暂存 代理 凭据 凭证`
- `line number relative line vim gutter code editor` -> `... 行号 相对 行 编辑器 代码 槽`
- `open windows with custom size` -> `open windows with custom size 打开 窗口 自定义 大小 尺寸`
- `oz agent ai input natural language detection autodetection ...` -> source + appended terms

## Check 6 — no collateral: PASS

- Batch-flagged entry count = 110 == expected_total. — PASS
- All 110 batch entries now have status `translated`; translated delta (+110) equals batch additions. — PASS
- The 30 `obsolete` entries carry no batch flag and were not touched by this batch. No non-batch entry changed (target,status). — PASS
