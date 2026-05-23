# Spec update — translation policy for panic / telemetry / search_terms

## Goal

Codify three translation policy decisions surfaced as anomalies during batch 12 (uncertain-pool sweep). The decisions are:

1. **Panic strings** (`.expect("...")`, `panic!("...")`, `unreachable!("...")`, `debug_assert!(_, "...")`) → do not translate; flag `["do_not_translate", "panic_message"]`.
2. **Telemetry / log-only payloads** → do not translate; flag `["do_not_translate", "telemetry_payload"]`.
3. **`fn search_terms` strings** → translate by APPENDING Chinese keywords to the original English (additive, not replacement). Optional `search_terms_bilingual` flag.

## What I already know

- The translation contract lives at `.trellis/spec/guides/translation-contract.md`.
- Pre-existing `do_not_translate` sub-flags in use: `extractor_false_positive_doc_comment`, `test_fixture`, `wgpu_debug_label`.
- `fn search_terms` matcher behavior: `app/src/settings_view/settings_page.rs:1405` does `terms.to_lowercase()` then `terms_lower.contains(query_word)` per whitespace-split word. Builder does byte-range replacement of the source literal with `target`. Therefore appending Chinese after the English string preserves English matching and unlocks Chinese matching — no tooling change required.
- Batches 7–11 translated some panic strings under the older "translate narrative, keep identifiers English" convention. Per the new policy, those are frozen as-is; a future audit batch may revisit.

## Changes

### `.trellis/spec/guides/translation-contract.md`

Edited §8 to drop the blanket "search-keyword strings can't be translated" claim and the panic-string footnote, then appended new §9–§12:

- **§9 `do_not_translate` sub-flag taxonomy** — table of `extractor_false_positive_doc_comment` / `test_fixture` / `wgpu_debug_label` / `panic_message` / `telemetry_payload`.
- **§10 Panic / `.expect` strings — keep English** — rationale + retro note.
- **§11 Telemetry payload strings — keep English** — sink-tracing rule for ambiguous cases.
- **§12 Search-keyword strings (`fn search_terms`) — bilingual append** — pattern, rules, anti-patterns, why-it-works explanation citing the matcher implementation.

### Memory updates

Mirrored the three policies as `project` memories so future sessions / spawned agents pick them up:

- `project_translation_flag_panic_message.md`
- `project_translation_flag_telemetry_payload.md`
- `project_translation_search_terms_bilingual.md`

Updated `MEMORY.md` index.

## Decisions / Anomalies

- **Retro-conversion of existing panic translations** — deferred. Not in scope of this task. Surfaced as a future audit batch question.
- **`search_terms_bilingual` flag — opt-in, not required** — flag is recommended for audit traceability but not strictly necessary; the entry is a normal `status: "translated"` with the bilingual string in `target`.
- **Capitalization in bilingual search_terms** — the matcher lowercases everything before `contains`, so technically case doesn't affect matching. The spec asks translators to keep Latin acronyms lowercase anyway for consistency with the source convention.
