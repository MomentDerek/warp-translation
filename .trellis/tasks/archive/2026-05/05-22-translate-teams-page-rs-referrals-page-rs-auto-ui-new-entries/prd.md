# Translate teams_page.rs + referrals_page.rs auto_ui new entries

## Goal

接力 settings_view 翻译序列（appearance → billing → code → privacy → environments → update_environment_form → teams + referrals），处理 `app/src/settings_view/teams_page.rs` 中 18 条 + `app/src/settings_view/referrals_page.rs` 中 18 条 = 共 36 条 `status=new` 且 `audit.verdict=auto_ui` 的用户可见文案。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 update_environment_form 收尾）：`translated=1320`, `fuzzy=52`。
- `teams_page.rs` 共 18 条 auto_ui：团队容量警告 / 升级提示 / 邀请入口 / 上限文案。
- `referrals_page.rs` 共 18 条 auto_ui：推荐入口 / 邮件邀请 / 礼品列表 / 错误提示。
- 主题分簇（按文件）：
  - **teams_page.rs · 容量警告 banner**：`Your team is full` (L1924) / `You've exceeded your member limit` (L1925) / `Payment past due` (L1926) / `Subscription unpaid` (L1927)
  - **teams_page.rs · 详细解释**：`You've reached your plan's member limit.` (L1939) / `You've exceeded your plan's member limit. Existing team members keep their access...` (L1941) / `Team invites have been restricted due to an unpaid subscription.` (L1947) / `Your plan ({plan_display}) has a maximum capacity of {cap} members.` (L2893)
  - **teams_page.rs · CTA / 引导**：`Contact a team admin to grow the team.` (L1959) / `Upgrade to grow your team.` (L1963) / `Contact sales to grow your team.` (L1964) / `Update your payment information to restore access.` (L1966) / `Contact support to restore access.` (L1968) / `Contact sales` (L2007) / `Want to grow your team? ` (L2957)
  - **teams_page.rs · 邀请入口**：`Invite team members` (L2583) / `By email` (L2759) / `By discovery` (L3186)
  - **referrals_page.rs · 页面 header**：`Invite a friend to Warp` (L45) / `Sign up to participate in Warp's referral program` (L46) / `Get exclusive Warp goodies when you refer someone*` (L68) / `Certain restrictions apply.` (L99) / ` If you have any questions about the referral program, please contact referrals@warp.dev.` (L103)
  - **referrals_page.rs · 计数 / 状态**：`Current referral` (L90) / `Current referrals` (L91)
  - **referrals_page.rs · 礼品列表**：`Exclusive theme` (L158) / `Keycaps + stickers` (L165) / `Baseball cap` (L186) / `Premium Hydro Flask` (L200)
  - **referrals_page.rs · 邀请操作 toast / error**：`Failed to load referral code.` (L53) / `Link copied.` (L64) / `Successfully sent emails.` (L65) / `Successfully sent {} invites` (L339) / `Successfully sent invites to: {:?}` (L340) / `Please enter an email.` (L465) / `Please ensure the following email is valid: {invalid_email}` (L467)
- 现有 settings 域 glossary 已覆盖：Warp / Agent / AI / environment / repository / 您-register。本批潜在新增：`team / 团队`（如未存在）、`subscription / 订阅`、`referral / 推荐`、`upgrade / 升级`。
- 翻译契约（沿用前批 PRD）：placeholder 完整、全角中文标点、glossary 一致、build + `cargo check -p warp` 通过。
- apply 脚本 stats 位置错位 known issue 仍未修；若 `extract --check` 首轮失败需 canonicalize 一轮。

## Assumptions

- 双文件合并单批 36 条，规模可控（环境批 30、privacy 32、code 39，本批 36 居中）。
- 选择标准：`occurrence.file ∈ {app/src/settings_view/teams_page.rs, app/src/settings_view/referrals_page.rs}` + `audit.verdict==auto_ui` + `status==new`。
- 全部 36 条为用户可见 banner / button / placeholder / toast / error / 礼品 label。
- Glossary 新增预估 2-4 条（取决于既有词表）。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 36 条 `status: new → translated`，`flags` 含 `pr-settings-teams-referrals-batch`，`target` 非空。
- 严格遵守 placeholder（`{}`, `{plan_display}`, `{cap}`, `{invalid_email}`, `{:?}` 原样）/快捷键/glossary 契约。
- 全角中文标点（避免半角 `,` `.` `?` `!`，URL/regex/code/email 字面值除外）。`...` 译为 `……`。
- 邮件地址 `referrals@warp.dev` 保留原样。
- 末尾 `*` 标记（脚注引用）保留。
- `extract --check` exit 0（幂等）。
- 已有 1320 条 translated 逐字保留。
- glossary 必要时增补 team / subscription / referral 域术语。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 36 条 entries: `status: new → translated`, `flags` 含 `pr-settings-teams-referrals-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1320 条 translated 逐字保留。
- [ ] glossary 一致性：Warp / Agent / AI / team / subscription / referral / 您-register 不混译。
- [ ] placeholder integrity 100%（含 `{plan_display}` / `{cap}` / `{invalid_email}` named placeholder + `{:?}` debug 占位符）。
- [ ] 邮件 `referrals@warp.dev` 原样、`*` 脚注标记原样。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone（settings 区域偏正式，对用户使用「您」）。
- Journal 记录 stats delta + notable decisions。
- Task archive。

## Out of Scope

- `teams_page.rs` 12 条 `verdict=uncertain` 条目（留作 uncertain 专项 sweep）。
- 其他 settings_view 单页（execution_profile / mcp_servers / agent_assisted_environment_modal / main_page 等留下一批）。
- Extractor / builder 重构、translation-contract spec 修订。

## Decision (locked — Approach A)

**Approach A: 双文件合并批 teams + referrals 共 36 条 auto_ui new**

锁定理由：两个文件主题独立但都偏短文案（banner / button / toast），合并一批可避免 17/18 条的小尾巴 task，与历史 30-40 条规模对齐；术语领域不重叠（team subscription vs. referral 礼品），互不污染。

**Batch flag**: `pr-settings-teams-referrals-batch`

## Technical Approach

1. 按 `any(occurrence.file ∈ {teams_page.rs, referrals_page.rs})` + `audit.verdict==auto_ui` + `status==new` 过滤，得 36 条。
2. 必要时增补 glossary（team / subscription / referral / upgrade 等）。
3. 按主题簇翻译（teams 容量警告 → CTA → 邀请；referrals header → 礼品 → toast/error），写回 `target` / `status` / `flags` / `history` / `updated_at`。
4. apply 脚本沿用上批模板（含全角标点 invariant；URL/email/regex/`{}` placeholder 内字面值放行；`...` → `……`）。
5. `extract --check` 幂等校验；若首轮报 not in canonical form，跑一次 `extract`（无 --check）规范化后再 `--check`。
6. `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
7. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 源码上下文:
  - `../warp/app/src/settings_view/teams_page.rs`（重点 L1924-3186）
  - `../warp/app/src/settings_view/referrals_page.rs`（重点 L45-467）
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-22-translate-update-environment-form-rs-auto-ui-new-entries/prd.md`。
- 上轮 apply 脚本参考：`.trellis/tasks/archive/2026-05/05-22-translate-update-environment-form-rs-auto-ui-new-entries/apply_translations.py`。
- 候选 entry 清单（36 条）：
  - teams_page.rs (18): L1924, L1925, L1926, L1927, L1939, L1941, L1947, L1959, L1963, L1964, L1966, L1968, L2007, L2583, L2759, L2893, L2957, L3186
  - referrals_page.rs (18): L45, L46, L53, L64, L65, L68, L90, L91, L99, L103, L158, L165, L186, L200, L339, L340, L465, L467
