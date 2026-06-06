# PRD — Daily upstream-release sync → incremental translate → package & release

## 目标

每天定时（GitHub Actions cron）无人值守地：

1. **捞上游发布** — 查询 `warpdotdev/warp` 最新发布 tag（默认 `dev` 频道，格式
   `v0.YYYY.MM.DD.HH.MM.{dev|preview|stable}_NN`），与本仓库当前 pin
   (`translations/strings.json` 的 `metadata.source_commit`) 比对，决定是否需要跑。
2. **增量翻译** — clone 上游到目标 tag，跑 `warp-zh-extractor` 增量抽取
   （新增/fuzzy/obsolete 状态变化），对 `status=new` 用现有翻译 workflow
   (`build_batch.py` + `.claude/workflows/translate_batch.mjs`，headless Claude Code，
   opus 并行 implementer) 翻译并 apply + check；fuzzy 走 RUNBOOK 的 resync。
3. **打包发布** — 更新 pin（`DEFAULT_WARP_REF` + strings.json metadata），提交到 main，
   打与上游同名的 tag，复用现有 `build-translation.yml`（tag push 触发
   package + GitHub Release，`*dev*` 自动 prerelease）。

密钥全部走 GitHub Secrets：`ANTHROPIC_API_KEY`（headless Claude）+ 一个有
`contents:write` 的 PAT（`WARP_ZH_PAT`，用于 push tag 以触发下游 release——
默认 `GITHUB_TOKEN` 推 tag 不会触发其它 workflow）。

## 约束 / 复用

- **复用现有 workflow**：`build-translation.yml`（build/package/release）、
  `.claude/workflows/translate_batch.mjs`、`tools/translations/kit/{build_batch,apply_batch}.py`。
- 上游源仓库只读（按 tag checkout，不改）。
- 翻译策略遵循 `translation-contract.md` 与 RUNBOOK 的 per-entry 决策流。
- pin 的权威来源是 `strings.json` 的 `metadata.source_commit`（已提交）；
  `DEFAULT_WARP_REF` 是它的镜像，需同步更新。

## 交付物

- `.github/workflows/daily-sync-translate.yml` — 主调度 workflow（cron + dispatch）。
- `tools/translations/kit/resolve_upstream.py` — 解析最新上游 tag、与 pin 比对、输出 GH Actions 变量。
- `tools/translations/kit/diff_table.py` — 抽取前后 strings.json 的 new/fuzzy/obsolete diff（复用 sync workflow 的 COMPARE_PY 逻辑）。
- 对 `build-translation.yml` 的最小改动：heavy `package` 仅在 tag push / dispatch 时跑（避免 daily commit 推 main 时重复重型构建）。
- `.github/workflows/README.md` 增补 daily 链路说明 + secrets 配置。
- 本地模拟验证（act 结构校验 + detect 逻辑实跑 + extractor 增量 diff 实跑）。

## 非目标

- 不在本任务内做 macOS 签名/公证（沿用 `--nosign`）。
- 不改翻译质量策略本身。
