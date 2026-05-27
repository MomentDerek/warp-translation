# Translation batch runbook

End-to-end procedure for running ONE parallel-translation batch (N implementers →
apply → check → commit → archive). Use this to start every subsequent batch.

The supporting tooling lives next to this file (`tools/translations/kit/`):
`build_batch.py`, `apply_batch.py`, `translate_batch.mjs`. None of it is
batch-number-specific — everything is passed at run time. See `README.md` for
the file reference; this RUNBOOK is the step-by-step.

---

## 0. Conventions (carry forward every batch)

| Thing | Value |
|---|---|
| Repo root | `<HOME>/Documents/Codes/warp_translation` |
| Source repo (where `.rs` live) | `<HOME>/Documents/Codes/warp` |
| Translation table | `translations/strings.json` (repo root — NOT `tools/translations/`) |
| Batch flag pattern | `pr-by-file-parallel-batch-<N>` |
| Default size | 8 implementers × ~75 entries = ~600 per batch |
| Why 8 | matches the Workflow concurrency cap `min(16, cores−2)` on this machine — all implementers run in one wave, no queueing |
| Policy | `.trellis/spec/guides/translation-contract.md` |
| Implementer / check agents | `trellis-implement` / `trellis-check`, model `opus` |

**Find the next batch number**: look at the newest `pr-by-file-parallel-batch-*`
flag in `strings.json`, or the newest `*-batch-N` task in `.trellis/tasks/archive/`.
Increment by 1.

```bash
python3 -c "import json,re;d=json.load(open('translations/strings.json'));\
fs={f for e in d['entries'] for f in (e.get('flags') or []) if f.startswith('pr-by-file-parallel-batch-')};\
print('latest batch:',max(int(re.search(r'(\d+)$',f).group(1)) for f in fs))"
```

---

## 1. Create + name the task

```bash
python3 ./.trellis/scripts/task.py create "translate next batch ~600 entries via 8 parallel implementers (batch <N>)"
# Note the printed task dir, e.g.:
TASK="$(python3 ./.trellis/scripts/task.py current)"
```

The task starts in `planning`. Brainstorm/prd is optional for a routine batch —
the workflow does not require `prd.md`.

## 2. Build candidates (auto file-pinned bins)

```bash
python3 tools/translations/kit/build_batch.py \
    --task-dir "$TASK" --num-batches 8 --target-total 600
```

Writes:
- `$TASK/candidates/batch-{A..H}.json` — one file per implementer
- `$TASK/candidates/manifest.json` — `{num_batches,total,batches:[{letter,count,files}]}`
- `$TASK/research/composition.md` — human-readable file→bin map

Files are never split across bins. Inspect `manifest.json`/`composition.md` to
sanity-check the split.

## 3. Start the task (planning → in_progress)

Optionally write `prd.md` first (copy a prior batch's and bump numbers/hints),
then:

```bash
python3 ./.trellis/scripts/task.py start "$TASK"
```

## 4. Launch the workflow

The main session reads `letters` from the manifest and invokes the generic
workflow. `letters` is just `manifest.batches[*].letter`.

```js
Workflow({
  scriptPath: "tools/translations/kit/translate_batch.mjs",
  args: {
    taskDir:   "<absolute $TASK>",
    repoRoot:  "<HOME>/Documents/Codes/warp_translation",
    srcRepo:   "<HOME>/Documents/Codes/warp",
    batchFlag: "pr-by-file-parallel-batch-<N>",
    letters:   ["A","B","C","D","E","F","G","H"],
    activeTask: "<$TASK>"            // for the trellis sub-agent dispatch line
  }
})
```

Runs in the background; you get a notification on completion. `/workflows`
shows live progress.

**Phases:**
1. **Translate** — one `trellis-implement` (opus) per letter. Each reads its
   `candidates/batch-<L>.json` + the policy, traces each literal to its sink in
   `srcRepo`, and writes `outputs/batch-<L>-output.json`. Aborts before apply if
   any implementer fails to return.
2. **Apply** — runs `apply_batch.py --task-dir … --batch-flag …`. Hard-fails on
   any placeholder/strftime/whitespace/brand/flag-closure violation. Writes
   `outputs/apply_summary.json` (before/after/delta/per-action).
3. **Check** — `trellis-check` validates the summary deltas + flag closure +
   spot-check invariants, writes `check.report.md` and returns
   `{verdict: PASS|FAIL}`.

## 5. Read the result

The workflow result includes the per-batch summaries, the apply stdout, and the
check verdict. Confirm:

```bash
cat "$TASK/outputs/apply_summary.json"      # delta.new == -total, delta.translated == +total
cat "$TASK/check.report.md"                 # overall verdict PASS
```

If **FAIL**: read `check.report.md` for the failing check. Fix the offending
implementer output (or re-dispatch that one letter), then re-run only the apply
+ check — or resume the workflow:
`Workflow({scriptPath:".../translate_batch.mjs", resumeFromRunId:"<prior run id>"})`
(completed implementers return cached; edit the script/outputs first).

## 6. Commit

Phase 3.4 — the **main agent drives the commit** (state the plan, then commit):

```bash
git add translations/strings.json "$TASK"
git commit -m "chore(translations): batch-<N> — <total> entries (<X> UI + <Y> bilingual + <Z> flagged) across <F> files via 8 parallel implementers"
```

(Include the kit itself in the first commit that introduces/changes it.)

## 7. Finish

```
/trellis:finish-work
```

`/finish-work` refuses to run on a dirty tree (outside `.trellis/workspace/` and
`.trellis/tasks/`), so commit `translations/strings.json` first.

---

## Per-entry decision flow (what each implementer applies)

FIRST hit wins:

1. doc-comment false-positive (`/// …` fragment) → `flag_extractor_false_positive_doc_comment`, target=null
2. `panic!` / `.expect` / `unreachable!` / `debug_assert` literal → `flag_panic_message`, target=null
3. telemetry / log-only literal (sink = `tracing::*`, telemetry, log file — not UI) → `flag_telemetry_payload`, target=null
4. `fn search_terms()` keyword string → bilingual append `"<source> <中文>"` (id in `bilingual_search_terms_ids`)
5. wgpu debug label / test fixture / protocol key (serde/YAML field, feature/model/theme identifier) → matching sub-flag, target=null
6. regular UI text → translate to Chinese per `translation-contract.md`

Sub-flag whitelist (exactly one per flagged entry):
`panic_message`, `telemetry_payload`, `extractor_false_positive_doc_comment`,
`test_fixture`, `wgpu_debug_label`, `protocol_key`.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `apply_batch.py`: "expected K, got M" | An implementer dropped/added ids. Re-run that letter; ensure every candidate id is in `translations`. |
| `null_ids vs subflag_ids mismatch` | A flagged entry lacks a sub-flag, or a sub-flag points at a non-null target. Fix that output file. |
| `placeholders differ` / `brand literal missing` | Translation dropped a `{x}` / brand word. Fix the target. |
| check: delta wrong | Some rows weren't `new` at apply time (already translated in a prior batch), or candidate overlap. Inspect `apply_summary.json`. |
| `/finish-work` refuses | Working tree dirty — commit `translations/strings.json` first (step 6). |
| Re-running apply | Idempotent: already-applied rows report `already`, `applied=0`, no count change. Safe. |

---

## Why these scripts live at repo root, not in the task dir

Earlier batches copied a bespoke `apply_translations.py` into each task dir with
the batch number hardcoded. The kit replaces that: the scripts are batch-agnostic
and discover letters/totals at run time, so only `args`/CLI flags change per batch.
Old per-task `apply_translations.py` files remain in archived tasks for provenance
but are superseded by `kit/apply_batch.py`.
