# Parallel translation batch kit

Reusable tooling for the "N parallel implementers translate one batch" workflow.
Nothing here is batch-number-specific; per-batch values are passed as arguments.

> **Running the next batch?** Follow [`RUNBOOK.md`](./RUNBOOK.md) — the complete
> step-by-step (create task → build → workflow → apply → check → commit → finish).
> This README is the file/API reference.

## Files

| File | Role |
|---|---|
| `build_batch.py` | Pack `status=new` entries into N file-pinned bins. Writes `candidates/batch-*.json`, `candidates/manifest.json`, `research/composition.md`. |
| `apply_batch.py` | Merge implementer outputs into `translations/strings.json`. Discovers batch letters + expected total automatically. Writes `outputs/apply_summary.json`. |
| `resolve_upstream.py` | Resolve the latest upstream `warpdotdev/warp` release tag for a channel (`gh api` → `git ls-remote` fallback), compare to the pin (`strings.json` → `metadata.source_commit`), emit `should_run`/`upstream_tag`/`upstream_sha` GitHub-Actions outputs. Drives `daily-sync-translate.yml`. |
| `diff_table.py` | Diff a `strings.json` before/after an extractor run into `new`/`fuzzy`/`obsolete`/`deleted` (same logic `sync-upstream-translations.ts` uses inline). Emits a machine report + GH outputs. |
| `../../../.claude/workflows/translate_batch.mjs` | Claude Code Workflow: N implementers (opus) → apply → check. Fully parameterized via `args`. |
| `../../../.claude/workflows/sync-upstream-translations.ts` | Claude Code Workflow: pull upstream Warp (ff-only), re-extract, diff `strings.json`, categorize changes, emit a report. |
| `../../../.claude/workflows/daily-translate.prompt.md` | Headless-CI prompt template: instructs `claude -p` to run `translate_batch.mjs` over the day's `status=new` entries and write a PASS/FAIL status file. |

The daily CI pipeline (`.github/workflows/daily-sync-translate.yml`) chains
`resolve_upstream.py` → extractor → `diff_table.py` → `build_batch.py` →
headless Claude (`translate_batch.mjs`) → pin bump → release tag. See
[`.github/workflows/README.md`](../../../.github/workflows/README.md#daily-automation-daily-sync-translateyml).

The Python scripts are standalone (`python3 …`). The two `.mjs/.ts` workflow scripts live under
`.claude/workflows/` and require [Claude Code](https://claude.com/claude-code) to drive sub-agents.

## Per-batch run (e.g. batch 21)

```bash
# 1. create + start the task
python3 ./.trellis/scripts/task.py create "translate next batch ~600 entries via 8 parallel implementers (batch 21)"
TASK=.trellis/tasks/05-27-translate-next-batch-...-batch-21   # printed by create

# 2. build candidates (auto file-pinned bins)
python3 tools/translations/kit/build_batch.py \
    --task-dir "$TASK" --num-batches 8 --target-total 600

# 3. (optional) write prd.md, curate implement.jsonl/check.jsonl, then:
python3 ./.trellis/scripts/task.py start "$TASK"
```

Then launch the workflow. The main session reads `candidates/manifest.json` to build `letters`,
and invokes:

```js
Workflow({
  scriptPath: ".claude/workflows/translate_batch.mjs",
  args: {
    taskDir:   "<absolute path to $TASK>",
    repoRoot:  "<absolute path to this repo>",
    srcRepo:   "<absolute path to upstream warp clone>",
    batchFlag: "pr-by-file-parallel-batch-21",
    letters:   ["A","B","C","D","E","F","G","H"],   // from manifest.json
    activeTask: "<$TASK>"
  }
})
```

The workflow:
1. **Translate** — one `trellis-implement` (opus) per letter, each writes `outputs/batch-<L>-output.json`.
2. **Apply** — runs `apply_batch.py` (hard-fails on placeholder/brand/flag-closure violations), writes `outputs/apply_summary.json`.
3. **Check** — `trellis-check` validates the summary deltas + invariants, writes `check.report.md`.

## Invariants enforced by `apply_batch.py`

- placeholders `{}` / `{name}` and strftime `%b` codes preserved
- leading/trailing whitespace + newline shape preserved
- brand literals preserved; ASCII `...` rejected (must be `……`)
- flag closure: `target=null` ⇔ exactly one sub-flag in
  {panic_message, telemetry_payload, extractor_false_positive_doc_comment, test_fixture, wgpu_debug_label, protocol_key}
- bilingual target starts with `<source> `, no punctuation
- pre-existing `translated` rows untouched
- idempotent: re-running on applied rows is a no-op

## CWD note

Both scripts derive `translations/strings.json` from their own location (repo root = 3 levels up),
so they run correctly from anywhere. Override with `--strings` if needed.
