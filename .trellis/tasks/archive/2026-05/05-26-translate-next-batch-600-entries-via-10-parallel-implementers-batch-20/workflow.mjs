export const meta = {
  name: 'translate-batch-20',
  description: 'Batch-20: 10 parallel trellis-implement agents (opus) translate 602 entries by file, then apply + check.',
  phases: [
    { title: 'Translate' },
    { title: 'Apply' },
    { title: 'Check' },
  ],
}

const REPO_ROOT = '<HOME>/Documents/Codes/warp_translation'
const TASK_DIR = `${REPO_ROOT}/.trellis/tasks/05-26-translate-next-batch-600-entries-via-10-parallel-implementers-batch-20`
const SRC_REPO = '<HOME>/Documents/Codes/warp'
const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

function implementerPrompt(letter) {
  return `You are a translation implementer for batch-20 sub-batch ${letter}.

WORKING DIRECTORY:  ${REPO_ROOT}
SOURCE CODE ROOT:   ${SRC_REPO}
CANDIDATES FILE:    ${TASK_DIR}/candidates/batch-${letter}.json
OUTPUT FILE:        ${TASK_DIR}/outputs/batch-${letter}-output.json
POLICY (must read): ${REPO_ROOT}/.trellis/spec/guides/translation-contract.md
PRD (must read):    ${TASK_DIR}/prd.md

YOUR TASK:
1. Read the candidates file. It contains entries assigned to YOUR batch.
   Each entry has: { id, source, file, line, occurrences_kind, source_hash, audit_verdict, occurrences_count, occurrences_all }.
2. For EACH entry, decide one action by the decision flow in prd.md §"Per-entry decision flow":
   (1) doc-comment false-positive → flag_extractor_false_positive_doc_comment, target=null
   (2) panic / .expect / unreachable / debug_assert literal → flag_panic_message, target=null
   (3) telemetry / logging-only literal (sink is tracing::*, telemetry, log file — NOT UI) → flag_telemetry_payload, target=null
   (4) fn search_terms() keyword string → bilingual append "<source> <chinese>", id in bilingual_search_terms_ids
   (5) wgpu debug label / test fixture / protocol key (YAML field, serde key, identifier) → respective sub-flag, target=null
   (6) regular UI text → translate to Chinese per policy §1-7
   Apply rule in order; FIRST hit wins.
3. To make the right call, READ THE SOURCE at \`${SRC_REPO}/<file>:<line>\` for each entry. Trace where the literal flows
   (UI render? panic? tracing? serde key?). Do not guess from the source string alone.
4. Translation invariants (when target is NOT null and NOT bilingual):
   - Placeholders ({}, {name}, {0}) MUST be preserved exactly
   - strftime codes (%b, %d, %-I, %%) MUST be preserved exactly
   - Leading/trailing whitespace and newline shape preserved
   - Brand literals preserved: Warp, Warp Drive, Oz, MCP, Agent, PTY, REPL, GitHub, Slack, Stripe, Firebase, Fireworks, AWS, OAuth, JWT, Linux, Profile, OpenAI, Anthropic, HPKE, Node.js, tmux, GraphQL
   - Chinese punctuation must be full-width (，。；！？)
   - ASCII "..." must become "……"
5. Bilingual invariants: target starts with "<source> " (one ASCII space); no punctuation in the keyword string.
6. Flag invariants: target is null; do_not_translate_subflags[id] = ["<sub_name>"] (exactly one).
7. Sub-flag whitelist (exact strings):
   - panic_message
   - telemetry_payload
   - extractor_false_positive_doc_comment
   - test_fixture
   - wgpu_debug_label
   - protocol_key

OUTPUT (write to ${TASK_DIR}/outputs/batch-${letter}-output.json):
{
  "translations": {"<id>": "<chinese>" | null, ...},   // one entry per input id; null only for flagged
  "do_not_translate_subflags": {"<id>": ["<sub>"], ...},  // key set MUST equal ids with null translation
  "bilingual_search_terms_ids": ["<id>", ...],         // these ids' target is "<source> <chinese>"
  "notes": "free-text rationale, e.g., per-file action summary"
}

CRITICAL:
- Every id from the candidates file MUST appear in "translations".
- ids with null translation MUST be exactly the keys of do_not_translate_subflags.
- bilingual ids MUST have non-null target and MUST NOT be in subflags.
- DO NOT modify translations/strings.json directly — only write your output JSON.
- DO NOT create any other files.

When done, return ONLY a single-line JSON summary like:
{"batch":"${letter}","total":N,"translated":N1,"flagged":N2,"bilingual":N3,"output":"<path>"}
`
}

phase('Translate')

const summaries = await parallel(
  LETTERS.map((letter) => () =>
    agent(implementerPrompt(letter), {
      label: `translate:batch-${letter}`,
      phase: 'Translate',
      agentType: 'trellis-implement',
      model: 'opus',
    })
  )
)

log(`translate phase done; ${summaries.filter(Boolean).length}/${LETTERS.length} agents returned`)

phase('Apply')

const applyResult = await agent(
  `Run the apply script for batch-20 and report results.

WORKING DIRECTORY: ${REPO_ROOT}

Steps:
1. Verify all 10 output files exist: ls -la ${TASK_DIR}/outputs/
2. Run: python3 ${TASK_DIR}/apply_translations.py
3. If exit code is non-zero, print stderr verbatim and stop.
4. On success, print the script's full stdout (per-action breakdown + delta).

Return ONLY: {"status":"ok"|"error","stdout_tail":"<last 30 lines>","stderr":"<if any>"}`,
  { label: 'apply_translations', phase: 'Apply', agentType: 'trellis-implement', model: 'opus' }
)

log(`apply done: ${typeof applyResult === 'string' ? applyResult.slice(0, 200) : JSON.stringify(applyResult).slice(0, 200)}`)

phase('Check')

const checkResult = await agent(
  `Verify batch-20 apply correctness using trellis-check methodology.

WORKING DIRECTORY: ${REPO_ROOT}
TASK DIR:          ${TASK_DIR}
STRINGS FILE:      translations/strings.json

Checks (report PASS/FAIL per check with evidence):

1. Status counts match prd.md expected:
   - new: 1903 → 1301 (Δ -602)
   - translated: 4779 → 5381 (Δ +602)
   - fuzzy: 52 (unchanged)
   Use: python3 -c "import json; d=json.load(open('translations/strings.json')); from collections import Counter; print(Counter(e['status'] for e in d['entries']))"

2. Batch flag closure: every entry with flag "pr-by-file-parallel-batch-20" exists; count == 602.
   python3 -c "import json; d=json.load(open('translations/strings.json')); c=sum(1 for e in d['entries'] if 'pr-by-file-parallel-batch-20' in (e.get('flags') or [])); print(c)"

3. Flag closure: every entry with target=null AND status=translated has at least one of the sub-flags
   {panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key}
   AND has "do_not_translate" flag.

4. Spot-check invariants on 8 random translated entries (target non-null) from batch-20:
   - placeholders preserved
   - brand literals preserved
   - ASCII "..." absent (must be "……")
   - no half-width punctuation , . ; ! ? in the body of UI text (commas/periods only)

5. Existing translated rows untouched: confirm pre-apply translated entries' (target, status) pairs are unchanged.
   Hint: pre-apply count was 4779; post-apply 5381 with delta exactly +602 implies no pre-existing flips.

6. bilingual_search_terms entries (search "search_terms_bilingual" flag in batch-20 ids): verify each target starts with source + " ".

OUTPUT: a markdown report saved to ${TASK_DIR}/check.report.md with one section per check + an overall PASS/FAIL verdict at top.

Return ONLY: {"verdict":"PASS"|"FAIL","critical_failures":[<list>],"report_path":"${TASK_DIR}/check.report.md"}`,
  { label: 'trellis-check', phase: 'Check', agentType: 'trellis-check', model: 'opus' }
)

return {
  per_batch: summaries,
  apply: applyResult,
  check: checkResult,
}
