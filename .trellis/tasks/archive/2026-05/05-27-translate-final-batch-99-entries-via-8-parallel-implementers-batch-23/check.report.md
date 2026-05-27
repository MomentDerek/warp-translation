# Check Report — batch-23 apply verification

**Overall verdict: PASS**

Batch flag: `pr-by-file-parallel-batch-23` · expected_total: 99

## Check 1 — apply_summary.json internal consistency: PASS
- `delta.new == -99` and `delta.translated == +99` and `delta.fuzzy == 0` ✓
- `applied == 99 == expected_total` ✓ (note: `already == 0` on fresh batch)
- `batch_flag_count == 99 == expected_total` ✓
- `sum(per_action) == 41+36+16+5+1 == 99 == expected_total` ✓

## Check 2 — live status counts vs summary "after": PASS
Live `Counter` from strings.json: `{'translated': 6682, 'fuzzy': 52}`.
Matches `after`: translated=6682, fuzzy=52, new=0 (absent ⇒ 0). ✓

## Check 3 — flag closure (batch scope): PASS
- 99 batch entries: 58 null-target, 41 non-null-target.
- Every null-target entry has `do_not_translate` AND exactly one sub-flag from the allowed set. 0 violations.
- Every non-null-target entry has NO sub-flag. 0 violations.

## Check 4 — spot-check 8 random non-null-target entries: PASS
Placeholders preserved, brand literals preserved (e.g. "Warp", "Warpify", "Markdown"), no ASCII "...". 0 issues across the sample. Examples:
- `Never Warpify this host` → `永不 Warpify 此主机`
- `# Warp Launch Configuration` → `# Warp 启动配置`
- `Type text or Markdown` → `输入文本或 Markdown`

## Check 5 — bilingual entries (search_terms_bilingual): PASS
0 entries carry `search_terms_bilingual` in this batch ⇒ vacuously satisfied. 0 violations.

## Check 6 — no collateral: PASS
- Batch-flagged count == 99 == expected_total.
- All 99 batch entries now have status `translated` (set == {'translated'}).
- `translated` delta (+99) equals batch additions (99 entries moved new→translated). No non-batch (target,status) changes implied.

## Summary
All 6 checks pass. 99/99 entries applied, flag closure intact, no collateral changes, summary internally consistent and matches live data.
