export const meta = {
  name: 'sync-upstream-translations',
  description: 'Pull upstream Warp (fast-forward only), run warp-zh-extractor, and identify translation changes (new / fuzzy / obsolete / deleted) by diffing strings.json before vs after.',
  whenToUse: 'After upstream Warp has likely moved, to sync ../warp and surface which translation entries changed and need attention. Read-only on the source repo; mutates only translations/strings.json and reports/.',
  phases: [
    { title: 'Sync & Extract', detail: 'snapshot strings.json, git fetch + ff-merge ../warp, run extractor, diff before vs after by id/status' },
    { title: 'Categorize', detail: 'fan out per source-area agents to classify changed entries (translate vs flag, priority)' },
    { title: 'Report', detail: 'synthesize a translation-change report into reports/' },
  ],
}

const REPO = '<HOME>/Documents/Codes/warp_translation'
const WARP = '<HOME>/Documents/Codes/warp'
const TOOLS = `${REPO}/tools`
const TABLE = `${REPO}/translations/strings.json`
const LOCK = `${REPO}/translations/.lock.json`
const BEFORE = '/tmp/warp-zh-strings.before.json'
const CMP = '/tmp/warp-zh-cmp.py'
const REPORT_JSON = `${REPO}/reports/sync-translation-changes.json`
const REPORT_MD = `${REPO}/reports/sync-translation-changes.md`

const SYNC_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['ffStatus', 'warpHeadBefore', 'warpHeadAfter', 'upstreamCommits', 'changedRsFiles', 'counts', 'byFile', 'samples', 'reportPath', 'notes'],
  properties: {
    ffStatus: { type: 'string', enum: ['updated', 'already-current', 'blocked'], description: 'updated = ff-merge applied new commits; already-current = HEAD already at origin/master; blocked = not fast-forwardable (do NOT force)' },
    warpHeadBefore: { type: 'string' },
    warpHeadAfter: { type: 'string' },
    upstreamCommits: { type: 'integer', description: 'number of new commits pulled (0 if already current or blocked)' },
    changedRsFiles: { type: 'array', items: { type: 'string' }, description: 'changed .rs files across the pulled commit range' },
    counts: {
      type: 'object', additionalProperties: false,
      required: ['new', 'fuzzy', 'obsolete', 'deleted'],
      properties: {
        new: { type: 'integer' }, fuzzy: { type: 'integer' },
        obsolete: { type: 'integer' }, deleted: { type: 'integer' },
      },
    },
    byFile: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['file', 'new', 'fuzzy', 'obsolete'],
        properties: {
          file: { type: 'string' }, new: { type: 'integer' },
          fuzzy: { type: 'integer' }, obsolete: { type: 'integer' },
        },
      },
    },
    samples: {
      type: 'array', description: 'up to 30 sample changed entries across new/fuzzy/obsolete',
      items: {
        type: 'object', additionalProperties: false,
        required: ['id', 'change', 'file', 'source'],
        properties: {
          id: { type: 'string' }, change: { type: 'string', enum: ['new', 'fuzzy', 'obsolete'] },
          file: { type: 'string' }, source: { type: 'string' },
        },
      },
    },
    reportPath: { type: 'string' },
    notes: { type: 'string', description: 'anything notable: ff-merge blocked reason, extractor warnings, parse failures' },
  },
}

const ANALYSIS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['area', 'files', 'summary', 'translateCount', 'flagCount', 'highlights'],
  properties: {
    area: { type: 'string', description: 'short human label for the feature area these files cover (e.g. "Settings / AI page", "Command palette")' },
    files: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string', description: '2-4 sentences: what changed and what it means for translation' },
    translateCount: { type: 'integer', description: 'changed entries that are genuine UI strings needing Chinese translation' },
    flagCount: { type: 'integer', description: 'changed entries that should be flagged do_not_translate per project policy (panic/expect, telemetry/log, test fixtures, product names, placeholders, shortcut modifiers, protocol/dict keys)' },
    highlights: { type: 'array', items: { type: 'string' }, description: 'notable individual entries or risks worth a human glance (ids or short quotes)' },
  },
}

const REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['headline', 'reportPath', 'recommendedNextStep'],
  properties: {
    headline: { type: 'string', description: 'one-line summary of the sync outcome' },
    reportPath: { type: 'string' },
    recommendedNextStep: { type: 'string' },
  },
}

const COMPARE_PY = String.raw`
import json, collections, sys
BEFORE = sys.argv[1]; AFTER = sys.argv[2]; OUT = sys.argv[3]
before = json.load(open(BEFORE)); after = json.load(open(AFTER))
b = {e['id']: e for e in before.get('entries', [])}
a = {e['id']: e for e in after.get('entries', [])}
def srcfile(e):
    occ = e.get('occurrences') or []
    return occ[0]['file'] if occ else '(no-occurrence)'
def short(s, n=120):
    s = (s or '').replace('\n', '\\n')
    return s if len(s) <= n else s[:n] + ' ...'
records = {'new': [], 'fuzzy': [], 'obsolete': [], 'deleted': []}
for i in a:
    if i not in b:
        e = a[i]; records['new'].append({'id': i, 'file': srcfile(e), 'source': e.get('source'), 'status': e.get('status')})
for i in b:
    if i not in a:
        e = b[i]; records['deleted'].append({'id': i, 'file': srcfile(e), 'source': e.get('source'), 'status': e.get('status')})
for i in set(a) & set(b):
    eb, ea = b[i], a[i]
    if eb.get('status') != ea.get('status'):
        if ea.get('status') == 'fuzzy':
            records['fuzzy'].append({'id': i, 'file': srcfile(ea), 'source': ea.get('source'), 'old_source': eb.get('source')})
        elif ea.get('status') == 'obsolete':
            records['obsolete'].append({'id': i, 'file': srcfile(ea), 'source': ea.get('source')})
byfile = collections.defaultdict(lambda: {'new': 0, 'fuzzy': 0, 'obsolete': 0})
for k in ('new', 'fuzzy', 'obsolete'):
    for r in records[k]:
        byfile[r['file']][k] += 1
byFile = [{'file': f, **c} for f, c in sorted(byfile.items())]
counts = {k: len(v) for k, v in records.items()}
report = {'counts': counts, 'byFile': byFile, 'records': records,
          'source_commit_before': before.get('metadata', {}).get('source_commit'),
          'source_commit_after': after.get('metadata', {}).get('source_commit')}
json.dump(report, open(OUT, 'w'), ensure_ascii=False, indent=2)
samples = []
for k in ('new', 'fuzzy', 'obsolete'):
    for r in records[k][:10]:
        samples.append({'id': r['id'], 'change': k, 'file': r['file'], 'source': short(r['source'])})
print(json.dumps({'counts': counts, 'byFile': byFile, 'samples': samples[:30]}, ensure_ascii=False))
`

phase('Sync & Extract')

const sync = await agent(
  `You are the sync+extract step of a translation-maintenance workflow for the warp_translation project.
The project translates Warp terminal UI strings to Chinese WITHOUT modifying the source repo. The source mirror lives at ${WARP} (git origin = warpdotdev/warp, branch master, treated read-only except for fast-forward pulls). The extractor (warp-zh-extractor) scans ../warp .rs files and incrementally merges string literals into the translation table ${TABLE}. Entry status transitions are the signal for translation changes: a brand-new id with status "new" = added string; an existing id flipped to "fuzzy" = upstream source text changed; flipped to "obsolete" or a removed id = string gone upstream.

Do EXACTLY these steps, in order, and stop + report if any step fails:

1. Snapshot the current table:
   cp ${TABLE} ${BEFORE}

2. Record the warp HEAD before, then fast-forward the mirror (NEVER create a merge commit, NEVER force):
   cd ${WARP}
   BEFORE_HEAD=$(git rev-parse HEAD)
   git fetch origin master
   REMOTE=$(git rev-parse origin/master)
   If REMOTE == BEFORE_HEAD: ffStatus = "already-current", do not merge.
   Else attempt: git merge --ff-only origin/master
     - success -> ffStatus = "updated"
     - failure (not fast-forwardable / local diverged) -> ffStatus = "blocked": run 'git merge --abort' if needed, set notes with the reason, SKIP step 4 (do not extract), still run nothing else, and report with counts all zero.
   AFTER_HEAD=$(git rev-parse HEAD)
   upstreamCommits = git rev-list --count $BEFORE_HEAD..$AFTER_HEAD  (0 if already-current/blocked)
   changedRsFiles = git diff --name-only $BEFORE_HEAD..$AFTER_HEAD -- '*.rs'  (empty if no new commits)

3. If ffStatus is "blocked", report now and stop. Otherwise continue.

4. Run the extractor (must run from ${TOOLS}; use absolute paths to avoid CWD traps):
   cd ${TOOLS}
   cargo run -q -p warp-zh-extractor -- extract --source ${WARP} --table ${TABLE} --lock ${LOCK}
   Capture stderr; note any parse failures or warnings.

5. Diff the table before vs after. Write this Python to ${CMP} verbatim, then run it:
---PYTHON BEGIN---
${COMPARE_PY}
---PYTHON END---
   Run: python3 ${CMP} ${BEFORE} ${TABLE} ${REPORT_JSON}
   It writes the full machine report to ${REPORT_JSON} and prints a JSON summary (counts, byFile, samples) to stdout.

6. Return the StructuredOutput using the printed summary plus the heads/commits you captured. samples = the printed samples array (already capped at 30). reportPath = ${REPORT_JSON}. Put extractor warnings / parse-failure notes / blocked reasons in notes (empty string if none).

Notes:
- If ffStatus is "already-current", the extractor may still surface changes from a manual edit, but typically counts will be 0 — that is fine, report honestly.
- Do NOT git commit anything. Do NOT touch any file other than ${BEFORE}, ${CMP}, ${TABLE} (via the extractor), and ${REPORT_JSON}.`,
  { schema: SYNC_SCHEMA, label: 'sync+extract' }
)

if (!sync) {
  log('Sync agent returned no result.')
  return { error: 'sync-failed' }
}

if (sync.ffStatus === 'blocked') {
  log(`Upstream merge BLOCKED (not fast-forwardable): ${sync.notes}. Aborted before extract — no changes made.`)
  return sync
}

const total = sync.counts.new + sync.counts.fuzzy + sync.counts.obsolete + sync.counts.deleted
log(`Upstream: ${sync.upstreamCommits} new commit(s) (${sync.warpHeadBefore.slice(0, 8)}..${sync.warpHeadAfter.slice(0, 8)}), ${sync.changedRsFiles.length} changed .rs file(s).`)
log(`Translation changes — new:${sync.counts.new} fuzzy:${sync.counts.fuzzy} obsolete:${sync.counts.obsolete} deleted:${sync.counts.deleted}`)

if (total === 0) {
  log('No translation changes after sync. Nothing to categorize.')
  return { sync }
}

const changedFiles = (sync.byFile || []).filter(f => (f.new + f.fuzzy + f.obsolete) > 0)
const MAX_AGENTS = 12
const chunkSize = Math.max(1, Math.ceil(changedFiles.length / MAX_AGENTS))
const chunks = []
for (let i = 0; i < changedFiles.length; i += chunkSize) chunks.push(changedFiles.slice(i, i + chunkSize))
if (chunks.length < changedFiles.length) {
  log(`${changedFiles.length} changed source files grouped into ${chunks.length} categorize batches (cap ${MAX_AGENTS}, ~${chunkSize} files/batch).`)
}

phase('Categorize')

const POLICY = `Project flagging policy (recommend do_not_translate / flag, NOT a Chinese target) for: .expect()/panic!/unreachable! messages (panic_message); log/telemetry-only literals (telemetry_payload); literals inside unit-test fixtures (test_fixture); product/brand names; format placeholders and shortcut/key modifiers (keep as-is); external-format dictionary/protocol keys (e.g. plist keys). Genuine user-facing UI strings should be translated to Chinese. "search_terms" functions get bilingual append (Chinese added to English), not replacement.`

const analyses = await pipeline(
  chunks,
  (chunk, _orig, idx) =>
    agent(
      `You are categorizing translation changes for one batch of source files in the warp_translation project.
The full machine report of changed entries is at ${REPORT_JSON} (JSON: { counts, byFile, records:{ new[], fuzzy[], obsolete[], deleted[] } } — each record has id, file, source, and for fuzzy also old_source).

Focus ONLY on these source files (ignore entries for other files):
${chunk.map(c => `  - ${c.file}  (new:${c.new} fuzzy:${c.fuzzy} obsolete:${c.obsolete})`).join('\n')}

Steps:
1. Read ${REPORT_JSON} and filter records whose 'file' is in your list above.
2. Read the relevant source files under ${WARP} as needed to understand what each changed string is (UI label? log line? panic message? test fixture?). The source repo is read-only — do not edit it.
3. Classify each changed entry as either "needs Chinese translation" or "should be flagged do_not_translate" using the policy below.
4. Return a StructuredOutput: a short feature-area label, the file list, a 2-4 sentence summary of what changed and why it matters for translation, translateCount, flagCount, and highlights (notable ids/quotes or risks worth a human glance).

${POLICY}

Be concise and accurate. Do not translate anything yourself — this step only identifies and classifies.`,
      { schema: ANALYSIS_SCHEMA, phase: 'Categorize', label: `categorize:${idx + 1}/${chunks.length}` }
    )
)

const good = analyses.filter(Boolean)

phase('Report')

const report = await agent(
  `You are writing the final translation-change report for a warp_translation upstream sync.

Sync summary:
- Upstream commits pulled: ${sync.upstreamCommits} (${sync.warpHeadBefore} -> ${sync.warpHeadAfter})
- Changed .rs files in range: ${sync.changedRsFiles.length}
- Translation changes: new=${sync.counts.new}, fuzzy=${sync.counts.fuzzy}, obsolete=${sync.counts.obsolete}, deleted=${sync.counts.deleted}
- Full machine report: ${REPORT_JSON}

Per-area categorizations (JSON): ${JSON.stringify(good)}

Write a clear, well-structured Markdown report to ${REPORT_MD} in Chinese (the project's working language). Include:
1. 概要 (commit range, counts, total entries needing attention).
2. 按区域分类的变更 (one section per area: 摘要, 需翻译 vs 需标记 计数, 重点条目).
3. fuzzy 条目提醒 (these had upstream source changes — existing Chinese targets may now be stale and need review).
4. obsolete / deleted 条目 (strings removed upstream).
5. 建议的下一步 (e.g. how many translation batches, which areas to prioritize).
Keep it skimmable with tables/bullets. Then return a StructuredOutput with a one-line headline, the reportPath (${REPORT_MD}), and the recommended next step.`,
  { schema: REPORT_SCHEMA, label: 'report' }
)

log(`Done. ${report?.headline || ''}`)
return { sync, analyses: good, report }
