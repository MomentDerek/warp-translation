# Check Report — Translation Batch 22

**Task**: translate next batch (600 entries via 8 parallel implementers, batch 22)
**Batch flag**: `pr-by-file-parallel-batch-22`
**Verdict**: **PASS**
**Mode**: read-only verification (no files modified)

> Note: a prior version of this report recorded FAIL because the apply step had
> not yet run. The apply has since completed (applied=600, already=0) and this
> report supersedes that result. All six checks now pass against the live
> `translations/strings.json`.

Validated `translations/strings.json` against `apply_summary.json` and `.trellis/spec/guides/translation-contract.md`.

---

## Check 1 — Delta correctness: PASS

Live recount of `strings.json` matches `apply_summary.json` exactly:

| metric | before | after | delta | expected |
|---|---|---|---|---|
| translated | 5983 | 6583 | +600 | +600 ✓ |
| new | 699 | 99 | −600 | −600 ✓ |
| fuzzy | 52 | 52 | +0 | +0 ✓ |
| entry_count | — | 6734 | — | 6734 ✓ |

`applied=600, already=0`.

## Check 2 — Flag closure: PASS

Entries carrying `pr-by-file-parallel-batch-22`: **600** (unique ids, no duplicates). All 600 have `status: "translated"` (none left in the `new` queue). Count == 600 == batch size.

## Check 3 — Sub-flag invariant: PASS

All 267 `do_not_translate` entries carry exactly one sub-flag and have `target: null` and `status: "translated"`. Live sub-flag tally matches `per_action`:

| sub-flag | live count | apply_summary |
|---|---|---|
| telemetry_payload | 119 | 119 ✓ |
| panic_message | 81 | 81 ✓ |
| protocol_key | 38 | 38 ✓ |
| extractor_false_positive_doc_comment | 15 | 15 ✓ |
| test_fixture | 14 | 14 ✓ |
| **dnt total** | **267** | 267 ✓ |
| translate (non-dnt) | 328 | 328 ✓ |
| bilingual_search_terms | 5 | 5 ✓ |
| **grand total** | **600** | 600 ✓ |

Conversely, all 328 translated + 5 bilingual entries have non-null targets. Zero violations in either direction.

## Check 4 — Bilingual invariant: PASS

All 5 `search_terms_bilingual` entries start with `<source> ` and the appended Chinese portion contains no forbidden punctuation:

| id | prefix `<source> ` | appended Chinese |
|---|---|---|
| 01KQXQV12JEAHNF0PRXC1D56RQ | ok | 工具 面板 命令面板 搜索 工作流 提示词 笔记本 环境变量 |
| 01KQXQV12JPESGX51MXZDJZB10 | ok | 注册 登录 |
| 01KQXQV12JR5G9224TP431XGX2 | ok | 快捷键 键盘 热键 按键绑定 |
| 01KQXQV12JSYWVSJJ8PBGKE18P | ok | mcp 服务器 |
| 01KS2GEQRXMSMFGAXKV4CBAQXY | ok | 套餐 账单 计费 用量 额度 上限 余额 概览 |

The repaired-validator case is confirmed: source `plan billing a.i. ai usage limit credits balance overview` (id `01KS2GEQRXMSMFGAXKV4CBAQXY`) contains a legitimate `.` in the source prefix, while the appended Chinese keywords are punctuation-free — exactly what the fix intended.

## Check 5 — Placeholder/whitespace/brand integrity: PASS

Checked the **full** set of 328 translated entries (exceeds the requested ~15 sample):
- Placeholder sets (`{…}`) identical source↔target: 0 mismatches.
- strftime codes (`%…`) identical: 0 mismatches.
- Leading/trailing whitespace preserved: 0 mismatches.

Repaired entry `01KQXQV12HM1CE1R7S2VPJK6SJ`: source `'When enabled, '` → target `'启用后， '`; trailing space preserved on both sides ✓.

Brand-literal spot-check (15 samples containing Warp/MCP/AI/API/Git/SSH/AWS/OpenAI/Drive): all brand tokens preserved verbatim in targets, 15/15 OK.

## Check 6 — No regressions: PASS

- Remaining `new` entries: 99 — none carry the batch-22 flag (untouched).
- `fuzzy`: 52 — unchanged, none carry the batch-22 flag.

---

## Summary

All 6 checks PASS. 600 batch-22 candidates applied cleanly: 333 translated (328 standard + 5 bilingual) and 267 intentionally-untranslated with correct sub-flags and null targets. Deltas match the apply summary, invariants hold across the full set, and no `new`/`fuzzy` regressions. No issues requiring repair.
