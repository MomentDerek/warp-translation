You are running UNATTENDED inside GitHub Actions CI. No human will answer
questions, so do not ask any — execute the steps and finish.

Your single job: run the project's EXISTING parallel-translation batch workflow
over the freshly-extracted `status=new` entries, then record a machine-readable
verdict. This message is an explicit request to use the Workflow tool.

Steps (do exactly these, in order):

1. Call the Workflow tool EXACTLY ONCE with:
   - scriptPath: ".claude/workflows/translate_batch.mjs"
   - args: __ARGS_JSON__
   Do NOT alter the args, add fields, or change paths. Do NOT run any other
   workflow. The args were computed by CI from candidates/manifest.json.

2. That workflow runs three phases on its own: Translate (one opus implementer
   per letter, each reads its candidates file + the translation contract and
   traces every literal to its sink in the source repo), Apply
   (tools/translations/kit/apply_batch.py — hard-fails on any placeholder /
   strftime / whitespace / brand / flag-closure violation), and Check
   (validates the apply deltas + flag closure + spot invariants). The Workflow
   tool returns an object whose `.check` is {verdict: "PASS"|"FAIL",
   critical_failures: [...], report_path: "..."}.

3. After the Workflow tool returns, WRITE a JSON file to "__STATUS_FILE__"
   containing exactly:
     {"verdict":"PASS"|"FAIL","critical_failures":[...],"note":"<short reason>"}
   - verdict = the check-phase verdict from the workflow result.
   - If the workflow errored, returned no `.check`, or any implementer failed to
     return, set verdict="FAIL" and explain in note.

4. Do NOT git commit, tag, or push. Do NOT edit build-translation.yml or any
   file other than what the Workflow tool writes plus the status file above.

Finish by replying with one line: the verdict you wrote to the status file.
