# Translate update_environment_form.rs auto_ui new entries

## Goal

接力 settings_view 翻译序列（appearance → billing → code → privacy → environments → update_environment_form），处理 `app/src/settings_view/update_environment_form.rs` 中 `status=new` 且 `audit.verdict=auto_ui` 的 30 条用户可见文案（环境创建/编辑表单：基本信息、GitHub 仓库选择、Docker 镜像建议、setup commands、共享、错误提示）。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 environments 收尾）：`translated=1290`, `fuzzy=52`。
- `update_environment_form.rs` 出现在 occurrences 中的 `status=new` 条目：`verdict=auto_ui` 30 条 + `verdict=uncertain` 19 条。本批仅处理 30 条 auto_ui。
- 主题分簇（按源码位置）：
  - **表单 header / 按钮**：`Create environment` (L120) / `Edit environment` (L1740) / `Delete environment` (L44) / `Share with team` (L1657)
  - **基本输入字段**：`Environment name` (L280) / `e.g., this environment is for all front end focused agents` (L369, placeholder) / `Docker image` (L267) / `Docker image reference` (L283) / `Setup command(s)` (L1866) / `Press Enter or click the submit button to add each command.` (L271) / `Setup commands run independently. Each command runs from the workspace root (/wo...)` (L287)
  - **GitHub repos 选择**：`Browse GitHub repos...` (L265) / `Enter repos (owner/repo format)` (L370) / `Paste repo URL(s)` (L371) / `Type owner/repo and press Enter to add, or select from dropdown.` (L2476) / `Missing a repo?` (L2502) / `Configure access on GitHub` (L2520) / `No repositories found` (L2689) / `Auth with GitHub` (L2119)
  - **Docker 镜像建议**：`Suggest image` (L3100) / `Warp will suggest a Docker image based on your selected repositories.` (L3103) / `You need to grant access to your GitHub repos to suggest a Docker image` (L3230) / `Open image at {docker_hub_url}` (L2974) / `We couldn't find a good match. We recommend using a custom Docker image for thes...` (L3265)
  - **错误提示**：`Couldn't load GitHub repos. You can paste repo URL(s), or retry.` (L1362) / `Failed to load GitHub repositories` (L2167) / `Failed to suggest a Docker image` (L1562) / `Failed to suggest a Docker image: {}` (L1589) / `Unknown response from suggestCloudEnvironmentImage` (L1575) / `Personal environments cannot be used with external integrations or team API keys` (L1694)
- 现有 environments 域 glossary（上批已加）：`environment / 环境`、`ambient_agent / ambient agent (do_not_translate)`、`repository / 仓库`、`base_image / 基础镜像`、`setup_commands / 设置命令`、`launch_agent / 启动 Agent`。
- 本批新增 glossary 候选：`docker_image / Docker 镜像`、`github_repos / GitHub 仓库`、`workspace_root / 工作区根目录`（如需要）。
- 翻译契约（沿用前批 PRD）：placeholder 完整、全角中文标点、glossary 一致、build + `cargo check -p warp` 通过。
- apply 脚本 stats 位置错位 known issue：`extract --check` 首轮可能报 not canonical，跑一次 `extract` 规范化后再 `--check`。

## Assumptions

- 单批 30 条，规模与 environments(30) / privacy(32) 接近。
- 选择标准：任一 `occurrence.file == app/src/settings_view/update_environment_form.rs` + `audit.verdict==auto_ui` + `status==new`。
- 全部 30 条为用户可见 label / placeholder / button / toast / error message / helper text。
- Glossary 新增预估 2-4 条（依实际复用情况，可能为零）。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 30 条 `status: new → translated`，`flags` 含 `pr-settings-update-env-form-batch`，`target` 非空。
- 严格遵守 placeholder（`{}`, `{docker_hub_url}`, `{0}` 原样）/快捷键/glossary 契约。
- 全角中文标点（避免半角 `,` `.` `?` `!`，URL/regex/code 字面值除外）。`...` 译为 `……`。
- `extract --check` exit 0（幂等）。
- 已有 1290 条 translated 逐字保留。
- glossary 必要时增补 update_environment_form 域术语（Docker 镜像 / GitHub 仓库等）。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 30 条 entries: `status: new → translated`, `flags` 含 `pr-settings-update-env-form-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1290 条 translated 逐字保留。
- [ ] glossary 一致性：Warp / Agent / AI / environment / ambient agent / repository / 您-register 不混译。
- [ ] placeholder integrity 100%（含 `{docker_hub_url}` named placeholder）。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone（settings 区域偏正式，对用户使用「您」）。
- Journal 记录 stats delta + notable decisions。
- Task archive。

## Out of Scope

- `update_environment_form.rs` 内 19 条 `verdict=uncertain` 条目（留作 uncertain 专项 sweep）。
- 其他 settings_view 单页（teams / referrals / execution_profile / mcp_servers / agent_assisted_environment_modal 等留下一批）。
- Extractor / builder 重构、translation-contract spec 修订。

## Decision (locked — Approach A)

**Approach A: 翻译 `update_environment_form.rs` 30 条 auto_ui new**

锁定理由：settings_view 序列继续接力；update_environment_form 是 environments_page 的兄弟模块（共享 ambient agent / environment / repository 术语），紧接 environments 批可最大化术语预热复用。

**Batch flag**: `pr-settings-update-env-form-batch`

## Technical Approach

1. 按 `any(occurrence.file == app/src/settings_view/update_environment_form.rs)` + `audit.verdict==auto_ui` + `status==new` 过滤，得 30 条。
2. 必要时增补 glossary（Docker 镜像 / GitHub 仓库 / workspace root 等），多数术语可复用上批 environments 词族。
3. 按主题簇翻译（表单 header → 基本字段 → GitHub repos → Docker 镜像建议 → 错误提示），写回 `target` / `status` / `flags` / `history` / `updated_at`。
4. apply 脚本沿用上批模板（含全角标点 invariant：半角 `,` `.` `?` `!` → 全角；URL/regex/`{}` placeholder 内字面值放行；`...` → `……`）。
5. `extract --check` 幂等校验；若首轮报 not in canonical form，跑一次 `extract`（无 --check）规范化后再 `--check`。
6. `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
7. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 源码上下文: `../warp/app/src/settings_view/update_environment_form.rs`（重点 L44-3300）。
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-21-translate-environments-page-rs-auto-ui-new-entries/prd.md`。
- 上轮 apply 脚本参考：`.trellis/tasks/archive/2026-05/05-21-translate-environments-page-rs-auto-ui-new-entries/apply_translations.py`。
- 候选 entry 清单（30 条，按行号排序）：L44, L120, L265, L267, L271, L280, L283, L287, L369, L370, L371, L1362, L1562, L1575, L1589, L1657, L1694, L1740, L1866, L2119, L2167, L2476, L2502, L2520, L2689, L2974, L3100, L3103, L3230, L3265。
