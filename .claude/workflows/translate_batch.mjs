export const meta = {
  name: 'translate-batch',
  description: 'Generic parallel-translation batch: N implementers (opus) translate file-pinned candidates, then apply + check. Parameterized via args.',
  phases: [
    { title: 'Translate' },
    { title: 'Apply' },
    { title: 'Check' },
  ],
}

// ---------------------------------------------------------------------------
// args contract (all required unless noted):
// {
//   taskDir:    "/abs/path/to/.trellis/tasks/<task>",   // candidates/, outputs/ live here
//   repoRoot:   "<repo>",
//   srcRepo:    "../warp",     // where the .rs source lives
//   batchFlag:  "pr-by-file-parallel-batch-21",          // flag stamped on every applied entry
//   letters:    ["A","B",...],                            // one implementer per letter
//   policyPath: "<repoRoot>/.trellis/spec/guides/translation-contract.md",  // optional, defaulted
//   activeTask: ".trellis/tasks/<task>"                  // optional; for trellis sub-agent dispatch line
// }
// The main session derives `letters` from candidates/manifest.json before launch.
// ---------------------------------------------------------------------------

if (!args || !args.taskDir || !args.repoRoot || !args.srcRepo || !args.batchFlag || !Array.isArray(args.letters)) {
  throw new Error('translate-batch requires args = {taskDir, repoRoot, srcRepo, batchFlag, letters[]}. ' +
    'Pass absolute paths so sub-agents can chdir reliably; no hardcoded defaults.')
}

const TASK_DIR = args.taskDir
const REPO_ROOT = args.repoRoot
const SRC_REPO = args.srcRepo
const BATCH_FLAG = args.batchFlag
const LETTERS = args.letters
const POLICY = args.policyPath || `${REPO_ROOT}/.trellis/spec/guides/translation-contract.md`
const ACTIVE_TASK = args.activeTask || TASK_DIR
const KIT_DIR = `${REPO_ROOT}/tools/translations/kit`

function implementerPrompt(letter) {
  return `Active task: ${ACTIVE_TASK}

You are a translation implementer for sub-batch ${letter} (batch flag ${BATCH_FLAG}).

WORKING DIRECTORY:  ${REPO_ROOT}
SOURCE CODE ROOT:   ${SRC_REPO}
CANDIDATES FILE:    ${TASK_DIR}/candidates/batch-${letter}.json
OUTPUT FILE:        ${TASK_DIR}/outputs/batch-${letter}-output.json
POLICY (must read): ${POLICY}

TASK:
1. Read the candidates file — entries assigned to YOUR batch. Each row:
   { id, source, file, line, occurrences_kind, source_hash, audit_verdict, occurrences_count, occurrences_all }.
2. For EACH entry decide ONE action by this flow (FIRST hit wins):
   (1) doc-comment false-positive (source is a /// doc fragment) -> flag_extractor_false_positive_doc_comment, target=null
   (2) panic / .expect / unreachable! / debug_assert literal       -> flag_panic_message, target=null
   (3) telemetry / logging-only literal (sink is tracing::*, telemetry pipeline, log file — NOT UI) -> flag_telemetry_payload, target=null
   (4) fn search_terms() keyword string -> bilingual append "<source> <chinese>", id goes in bilingual_search_terms_ids
   (5) wgpu debug label / test fixture / protocol key (YAML field, serde key, feature/model/theme identifier) -> respective sub-flag, target=null
   (6) regular UI text -> translate to Chinese per policy
3. READ THE SOURCE at \`${SRC_REPO}/<file>:<line>\` for each entry and trace where the literal flows
   (UI render? panic? tracing? serde key?). Do not guess from the source string alone.
4. Translation invariants (target NOT null, NOT bilingual):
   - placeholders ({}, {name}, {0}) preserved exactly
   - strftime codes (%b, %d, %-I, %%) preserved exactly
   - leading/trailing whitespace + newline shape preserved
   - brand literals preserved: Warp, Warp Drive, Oz, MCP, Agent, PTY, REPL, GitHub, Slack, Stripe,
     Firebase, Fireworks, AWS, OAuth, JWT, Linux, Profile, OpenAI, Anthropic, HPKE, Node.js, tmux, GraphQL
   - Chinese punctuation full-width (，。；！？); ASCII "..." -> "……"
5. Bilingual invariants: target starts with "<source> " (one ASCII space); no punctuation in keyword string.
6. Flag invariants: target null; do_not_translate_subflags[id] = ["<sub>"] (exactly one of:
   panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key).

OUTPUT — write ${TASK_DIR}/outputs/batch-${letter}-output.json:
{
  "translations": {"<id>": "<chinese>" | null, ...},
  "do_not_translate_subflags": {"<id>": ["<sub>"], ...},
  "bilingual_search_terms_ids": ["<id>", ...],
  "notes": "free-text per-file rationale"
}

INVARIANTS (apply step re-checks these and FAILS hard on violation):
- every candidate id appears in "translations"
- ids with null translation == exact key set of do_not_translate_subflags
- bilingual ids have non-null target and are NOT in subflags
- DO NOT touch translations/strings.json; only write your output JSON; create no other files.

Return ONLY one line: {"batch":"${letter}","total":N,"translated":N1,"flagged":N2,"bilingual":N3}`
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

const returned = summaries.filter(Boolean).length
log(`translate done: ${returned}/${LETTERS.length} implementers returned`)
if (returned < LETTERS.length) {
  throw new Error(`only ${returned}/${LETTERS.length} implementers returned — aborting before apply`)
}

phase('Apply')

const applyResult = await agent(
  `Active task: ${ACTIVE_TASK}

Run the generic apply step for batch flag ${BATCH_FLAG}.

WORKING DIRECTORY: ${REPO_ROOT}

Steps:
1. Confirm ${LETTERS.length} outputs exist: ls ${TASK_DIR}/outputs/batch-*-output.json
2. Run: python3 ${KIT_DIR}/apply_batch.py --task-dir "${TASK_DIR}" --batch-flag "${BATCH_FLAG}"
3. If exit code != 0, print stderr verbatim and STOP (do not retry blindly).
4. On success, print stdout and confirm ${TASK_DIR}/outputs/apply_summary.json was written.

Return ONLY: {"status":"ok"|"error","stdout_tail":"<last 30 lines>","stderr":"<if any>"}`,
  { label: 'apply_batch', phase: 'Apply', agentType: 'trellis-implement', model: 'opus' }
)

log(`apply done`)

phase('Check')

const checkResult = await agent(
  `Active task: ${ACTIVE_TASK}

Verify the batch apply for flag ${BATCH_FLAG}. The apply step wrote a machine-readable summary —
use it instead of hardcoded numbers.

WORKING DIRECTORY: ${REPO_ROOT}
SUMMARY FILE:      ${TASK_DIR}/outputs/apply_summary.json
STRINGS FILE:      translations/strings.json

Checks (report PASS/FAIL per check with evidence):

1. Read apply_summary.json. Assert internal consistency:
   - delta.new == -expected_total  AND  delta.translated == +expected_total  AND  delta.fuzzy == 0
   - applied == expected_total (already == 0 on a fresh batch)
   - batch_flag_count == expected_total
   - sum(per_action values) == expected_total

2. Re-derive live status counts from strings.json and confirm they equal apply_summary "after":
   python3 -c "import json;from collections import Counter;d=json.load(open('translations/strings.json'));print(Counter(e['status'] for e in d['entries']))"

3. Flag closure (batch scope): every entry carrying ${BATCH_FLAG} with target=null has both
   'do_not_translate' and exactly one sub-flag from
   {panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key}.
   Every ${BATCH_FLAG} entry with non-null target has NO sub-flag.

4. Spot-check invariants on 8 random ${BATCH_FLAG} entries with non-null target:
   placeholders preserved, brand literals preserved, no ASCII "...", full-width punctuation.

5. bilingual entries (flag search_terms_bilingual within ${BATCH_FLAG}): each target starts with "<source> ".

6. No collateral: confirm the only entries whose (target,status) changed are the ${BATCH_FLAG} ones
   (count of batch-flagged == expected_total, and translated delta == batch additions).

OUTPUT: write a markdown report to ${TASK_DIR}/check.report.md (overall verdict at top, one section per check).
Return ONLY: {"verdict":"PASS"|"FAIL","critical_failures":[...],"report_path":"${TASK_DIR}/check.report.md"}`,
  { label: 'trellis-check', phase: 'Check', agentType: 'trellis-check', model: 'opus' }
)

return { per_batch: summaries, apply: applyResult, check: checkResult }
