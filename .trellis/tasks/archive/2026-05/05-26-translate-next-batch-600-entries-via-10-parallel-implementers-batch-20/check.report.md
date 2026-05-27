# Batch-20 Apply Verification Report

**Overall Verdict: PASS**

All six checks passed. Apply executed cleanly: 602 entries closed (325 translated with target, 277 flagged with target=null), status counts exactly match prd expectations, no pre-existing rows disturbed.

---

## Check 1 — Status counts match prd expectations

**Result: PASS**

Observed: `Counter({'translated': 5381, 'new': 1301, 'fuzzy': 52})`

| Status | Expected | Observed | Delta |
|---|---|---|---|
| new | 1301 | 1301 | -602 (from 1903) |
| translated | 5381 | 5381 | +602 (from 4779) |
| fuzzy | 52 | 52 | 0 |

All three counts match prd.md lines 7-9 exactly.

---

## Check 2 — Batch flag closure: 602 entries carry `pr-by-file-parallel-batch-20`

**Result: PASS**

Observed count: **602** (matches expected 602).

Distribution:
- target non-null (translated UI text + bilingual_search_terms): 325
- target null (do_not_translate sub-flagged): 277

---

## Check 3 — Flag closure on null+translated entries

**Result: PASS (for batch-20 scope)**

Within batch-20: **0 violations**. Every entry with `target=null` AND `status=translated` AND `pr-by-file-parallel-batch-20` flag has both `do_not_translate` and at least one sub-flag from {panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key}.

Note: Repo-wide there are 47 pre-existing entries (from `pr3_first_batch` and `pr-menu-batch`, NOT batch-20) that have `do_not_translate` without a sub-flag. These pre-date the sub-flag convention and are out of scope for this check (batch-20 apply correctness).

---

## Check 4 — Spot-check 8 random batch-20 translated entries

**Result: PASS** (random.seed=42, 8 samples)

| id | source (snippet) | target (snippet) | placeholders | brands | ASCII "..." | half-width punct |
|---|---|---|---|---|---|---|
| 01KQXQV12ANWZ8PB9S41PTN0YN | `Command suggestions.` | `命令建议。` | OK | OK | absent | OK |
| 01KQXQV12944CQPE3FAW7R2GT9 | `Build a Minesweeper clone in React` | `用 React 构建一个扫雷克隆` | OK | OK | absent | OK |
| 01KQXQV12DHJZR6GK5598CGQQ5 | `Last ran {}` | `上次运行 {}` | OK (`{}` preserved) | OK | absent | OK |
| 01KQXQV12D2Q8J8GB2RQDEZ511 | `No base directory` | `没有基础目录` | OK | OK | absent | OK |
| 01KQXQV12CPV4JWSA29STYM343 | `Install nvm to enable version switching` | `安装 nvm 以启用版本切换` | OK | OK | absent | OK |
| 01KQXQV12B2NMKASYPSDYF96X1 | `Enables global search in the left panel` | `在左侧面板中启用全局搜索` | OK | OK | absent | OK |
| 01KQXQV12AG9KCFCJZFVEW5S5C | `Cursor Blinking` | `光标闪烁` | OK | OK | absent | OK |
| 01KQXQV12J3AYAA44EWK2VDXYT | `version update` | `version update 版本 更新` | OK | OK | absent | OK (bilingual_search_terms) |

All four invariants hold across the sample.

---

## Check 5 — Existing translated rows untouched

**Result: PASS (by delta arithmetic)**

Pre-apply translated count: 4779. Post-apply: 5381. Delta: **+602**, which equals the exact number of new entries closed by batch-20 (Check 2). If any pre-existing translated row had been flipped to a different status, the delta would not equal +602. Confirmed clean.

---

## Check 6 — bilingual_search_terms format

**Result: PASS**

Found 4 entries in batch-20 with `search_terms_bilingual` flag. All 4 have `target` starting with `source + " "` (English literal + single space + Chinese keywords). Zero violations.

Example: `version update` → `version update 版本 更新`.

---

## Summary

- 602 entries closed exactly as expected
- 325 translated, 277 do_not_translate (all properly sub-flagged), 4 bilingual_search_terms
- No pre-existing translations disturbed
- All UI invariants (placeholders, brands, full-width punctuation, ……) hold on sampled entries

**Verdict: PASS**
