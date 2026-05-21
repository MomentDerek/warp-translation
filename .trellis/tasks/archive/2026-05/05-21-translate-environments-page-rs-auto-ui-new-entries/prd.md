# Translate environments_page.rs auto_ui new entries

## Goal

接力 settings_view 翻译序列（appearance → billing → code → privacy → environments），处理 `app/src/settings_view/environments_page.rs` 中 `status=new` 且 `audit.verdict=auto_ui` 的 30 条用户可见文案（Environments 列表 / 创建 / 编辑 / 分享 / 错误提示 / Get started 引导 / Quick setup 子流程 / Env 详情等子区）。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 privacy 收尾）：`entry_count=6734`, `translated=1260`, `fuzzy=52`, `new=5422`, `obsolete=0`。
- `environments_page.rs` 现有 `status=new` 共 34 条：`verdict=auto_ui` 30 条 + `verdict=uncertain` 4 条。
- 4 条 uncertain 主要为：单字 heading `"Environments"`（L85，与子区共名易冲突）、`{owner}/{repo}` 模板（L185）、`{} · {}` 分隔模板（L206）、search-keyword tag 串（L1045 `environments environment ambient agents github warp assisted manual configuration`）——沿用前批惯例全部保留。
- 主题分簇（按 `environments_page.rs` 源码）：
  - **概述 / 引导**：`Environments define where your ambient agents run...` (L86) / `You haven’t set up any environments yet.` (L1488) / `Choose how you’d like to set up your environment:` (L1497) / `Get started` (L1411)
  - **列表项 metadata**：`Last edited: {}` / `Last used: {}` / `Last used: never` / `Env ID: {}` / `Image: {}` / `Repos: {}` / `Setup commands: {}` / `Shared by Warp and {}` / `Shared by Warp and your team`
  - **搜索 / 状态**：`Search environments...` / `No environments match your search.`
  - **CRUD 成功提示**：`Successfully updated environment` / `Successfully created environment` / `Environment deleted successfully` / `Successfully shared environment`
  - **错误 / 警告**：`Failed to share environment with team` / `Unable to create environment: not logged in.` / `Unable to save: environment no longer exists.` / `Unable to share environment: you are not currently on a team.` / `Unable to share environment: environment is not yet synced.`
  - **Quick setup / Use the agent**：`Quick setup` / `Use the agent` / `Select the GitHub repositories you’d like to work with and we’ll suggest a base image and config` / `Choose a locally set up project and we’ll help you set up an environment based on it` / `Launch agent` / `View my runs`
- 现 glossary 关键术语：Warp / Agent / AI / 您-register。本批需新增：`environment(s)` / `ambient agent` / `repository(repos)` / `base image` / `setup commands` 等。
- 翻译契约（沿用前批 PRD）：placeholder 完整、全角中文标点、glossary 一致、build + `cargo check -p warp` 通过。
- 上批 code 批次曾混入半角 `,`，privacy 批已加全角标点校验；本批沿用。

## Assumptions

- 单批 30 条，规模与 privacy(32) / code(39) 接近。
- 选择标准：`occurrence.file == app/src/settings_view/environments_page.rs` + `audit.verdict==auto_ui` + `status==new`。
- 全部 30 条为用户可见 description / label / button / toast / error message。
- Glossary 新增预估 4–6 条：`environment` / `ambient_agent` / `repository` / `base_image` / `setup_commands` / `launch_agent`。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 30 条 `status: new → translated`，`flags` 含 `pr-settings-environments-batch`，`target` 非空。
- 严格遵守 placeholder（`{}`, `{name}`, `{0}` 原样）/快捷键/glossary 契约。
- 全角中文标点（避免半角 `,` `.` `?` `!`，URL/regex/code 字面值除外）。
- `extract --check` exit 0（幂等）。
- 已有 1260 条 translated 逐字保留。
- glossary 必要时增补 environments 域术语。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 30 条 entries: `status: new → translated`, `flags` 含 `pr-settings-environments-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1260 条 translated 逐字保留。
- [ ] glossary 一致性：Warp / Agent / AI / environment / ambient agent / 您-register 不混译。
- [ ] placeholder integrity 100%。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone（settings 区域偏正式，对用户使用「您」）。
- Journal 记录 stats delta + notable decisions。
- Task archive。

## Out of Scope

- `environments_page.rs` 内 4 条 `verdict=uncertain` 条目（heading `"Environments"` / `{owner}/{repo}` / `{} · {}` / search-keyword tag）。
- 其他 settings_view 单页（update_environment_form / teams / referrals / execution_profile / mcp_servers 等留下一批）。
- Extractor / builder 重构、translation-contract spec 修订。

## Decision (locked — Approach A)

**Approach A: 翻译 `environments_page.rs` 30 条 auto_ui new**

锁定理由：settings_view 序列继续接力；environments 是 ambient agent 主流程的入口页，glossary 新增刚好为后续 update_environment_form / teams 批次做术语预热。

**Batch flag**: `pr-settings-environments-batch`

## Technical Approach

1. 按 `occurrence.file == app/src/settings_view/environments_page.rs` + `audit.verdict==auto_ui` + `status==new` 过滤，得 30 条。
2. 增补 glossary（environments 域：`environment` / `ambient_agent` / `repository` / `base_image` / `setup_commands` / `launch_agent`，按需要）。
3. 按主题簇翻译（概述/引导 → 列表 metadata → 搜索 → CRUD 成功提示 → 错误警告 → Quick setup / Use the agent），写回 `target` / `status` / `flags` / `history` / `updated_at`。
4. apply 脚本内置全角标点 invariant（半角 `,` `.` `?` `!` → 全角），URL/regex/`{` placeholder 内字面值放行。
5. `extract --check` 幂等校验；若首轮报 not in canonical form，跑一次 `extract`（无 --check）规范化后再 `--check`。
6. `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
7. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 源码上下文: `<HOME>/Documents/Codes/warp/app/src/settings_view/environments_page.rs`（重点 L60-1900）。
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-21-translate-privacy-page-rs-auto-ui-new-entries/prd.md`。
- 上轮 apply 脚本参考：`.trellis/tasks/archive/2026-05/05-21-translate-privacy-page-rs-auto-ui-new-entries/apply_translations.py`。
