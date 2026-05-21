# Translate privacy_page.rs auto_ui new entries

## Goal

接力 settings_view 翻译序列（appearance → billing → code → privacy），处理 `app/src/settings_view/privacy_page.rs` 中 `status=new` 且 `audit.verdict=auto_ui` 的 32 条用户可见文案（排除 1 条边界搜索关键字 tag，详见 Out of Scope）（Secret redaction / Custom regex / App analytics / Crash reports / Cloud conversation storage / Network log console / Data management / Privacy policy 等子区）。保持 `extract --check` 幂等、`warp-zh-builder` 重建、`cargo check -p warp` 通过。

## What I already know

- 当前 `translations/strings.json` 统计（上批 code 收尾）：`entry_count=6785`, `translated=1228`, `fuzzy=52`, `new=5454`, `obsolete=51`。
- `privacy_page.rs` 现有 `status=new` 共 45 条：`verdict=auto_ui` 33 条 + `verdict=uncertain` 12 条。
- **边界条目**：`01KQXQV12JH96FDFWJWAJSESV0` (`"secret redaction"` @ `privacy_page.rs:2020`) 虽被 audit 标为 `auto_ui`，但源码上下文是 `ToggleSettingActionPair::new("secret redaction", ...)` 搜索关键字 tag，与同位 uncertain 条目 `"app analytics"` (L2002) / `"crash reporting"` (L2010) 同源。为一致性本批排除（实际处理 32 条）。
- 12 条 uncertain 主要为 URL 模板（`{}/data_management`, `{}/data_management?customToken={}`）、search-keyword tag 串（`secret redaction safe mode hide` / `network log audit console data collection` / `telemetry usage analytics data collection` / 等小写关键词串）、和 `{count}` 这类裸 placeholder——沿用 code 批次惯例，全部保留作后续判例 / glossary 决议素材。
- 主题分簇（按 `privacy_page.rs:60-252` 源码）：
  - **Secret redaction**：`SAFE_MODE_TITLE` / `SAFE_MODE_DESCRIPTION` / `USER_SECRET_REGEX_*` / `Add regex pattern` / `Add regex` / `Add all` / `Secret visual redaction mode` / `Custom secret redaction` / `Enterprise secret redaction cannot be modified.` / `No enterprise regexes have been configured by your organization.`
  - **App analytics (telemetry)**：`Help improve Warp` / `App analytics help us make the product better...` (两版：OLD + 新版含 console interactions) / `On the free tier, analytics must be enabled to use AI features.`
  - **Crash reports**：`Send crash reports` / `Crash reports assist with debugging and stability improvements.`
  - **Cloud conversation storage (Agent)**：`Store AI conversations in the cloud` / `Agent conversations are only stored locally...` / `Agent conversations can be shared with others...` / `Your administrator has enabled zero data retention for your team. ...`
  - **Network log console**：`Network log console` / `View network logging` / `We've built a native console that allows you to view all communications from War...`
  - **Data management**：`Manage your data` / `At any time, you may choose to delete your Warp account permanently. ...` / `Visit the data management page` / `Read more about Warp's use of data`
  - **Privacy policy**：`Privacy policy` / `Read Warp's privacy policy`
  - **共享 admin/managed 文案**：`Enabled by your organization.` / `This setting is managed by your organization.`
- 现 glossary 59 条无 privacy/secret/analytics/crash/redaction 域术语；本批需新增。
- 翻译契约（沿用前批 PRD）：placeholder 完整、全角中文标点、glossary 一致、build + `cargo check -p warp` 通过。

## Assumptions

- 单批 32 条（33 - 1 边界 tag），介于 code (39) / billing-old (62) 之间，规模适中。
- 选择标准：`occurrence.file == app/src/settings_view/privacy_page.rs` + `audit.verdict==auto_ui` + `status==new`。
- 全部 33 条为用户可见 label / description / button / mode-label。
- Glossary 新增预估 6–8 条：`privacy_policy` / `secret_redaction` / `app_analytics` / `crash_reports` / `telemetry` / `regex` / `zero_data_retention` / `data_management`。

## Open Questions (blocking)

- (none — scope locked)

## Requirements

- 选中 32 条 `status: new → translated`，`flags` 含 `pr-settings-privacy-batch`，`target` 非空。
- 严格遵守 placeholder（`{}`, `{name}`, `{0}` 原样）/快捷键/glossary 契约。
- 全角中文标点（避免半角 `,` `.` `?` `!`，URL/regex/code 字面值除外）。
- `extract --check` exit 0（幂等）。
- 已有 1228 条 translated 逐字保留。
- glossary 必要时增补 privacy 域术语。
- `warp-zh-builder` 重建 `build/warp-zh/`。
- `cargo check -p warp` 在 `build/warp-zh/` 通过。

## Acceptance Criteria

- [ ] 32 条 entries: `status: new → translated`, `flags` 含 `pr-settings-privacy-batch`, 非空 `target`。
- [ ] `extract --check` exit 0（幂等）。
- [ ] 已有 1228 条 translated 逐字保留。
- [ ] glossary 一致性：Warp / Agent / AI / regex / 您-register 不混译。
- [ ] placeholder integrity 100%。
- [ ] `warp-zh-builder` 重建成功。
- [ ] `cargo check -p warp` 通过。

## Definition of Done

- 翻译沿用既有 tone（settings 区域偏正式，对用户使用「您」）。
- Journal 记录 stats delta + notable decisions。
- Task archive。

## Out of Scope

- `privacy_page.rs` 内 12 条 `verdict=uncertain` 条目（含 URL 模板 / search-keyword tag / 裸 `{count}` placeholder）。
- 1 条边界 `auto_ui` tag `01KQXQV12JH96FDFWJWAJSESV0` (`"secret redaction"` @ L2020) —— ToggleSettingActionPair 搜索关键字，与 4 个 uncertain 兄弟一并到下批处理。
- 其他 settings_view 单页（environments / update_environment_form / teams 留下一批）。
- Extractor / builder 重构、translation-contract spec 修订。

## Decision (locked — Approach A)

**Approach A: 翻译 `privacy_page.rs` 32 条 auto_ui new（排除 1 条边界 search-keyword tag）**

锁定理由：settings_view 序列继续接力；privacy 是单文件主题最聚焦的隐私/数据域；glossary 复用率低（需新增 privacy 域），正好作下一批的预热。

**Batch flag**: `pr-settings-privacy-batch`

## Technical Approach

1. 按 `occurrence.file == app/src/settings_view/privacy_page.rs`（或 `auth_view_shared_helpers.rs` —— 部分 telemetry/crash/cloud-storage entries 实际定义在那里被本页引用）+ `audit.verdict==auto_ui` + `status==new` 过滤；显式排除 `01KQXQV12JH96FDFWJWAJSESV0`，得 32 条。
2. 增补 glossary（privacy 域：`privacy_policy` / `secret_redaction` / `app_analytics` / `crash_reports` / `telemetry` / `regex` / `zero_data_retention` / `data_management`，按需要）。
3. 按主题簇翻译（Secret redaction → App analytics → Crash reports → Cloud storage → Network log → Data management → Privacy policy），写回 `target` / `status` / `flags` / `history` / `updated_at`。
4. `extract --check` 幂等校验；若首轮报 not in canonical form，跑一次 `extract`（无 --check）规范化后再 `--check`（沿 code 批次经验）。
5. `warp-zh-builder` 重建 `build/warp-zh/`，`cargo check -p warp` 通过。
6. Journal + `task.py archive`。

## Technical Notes

- Source-of-truth: `translations/strings.json`。
- Glossary: `translations/glossary.json`。
- Builder: `tools/builder/` → `build/warp-zh/`。
- 源码上下文: `<HOME>/Documents/Codes/warp/app/src/settings_view/privacy_page.rs:60-252`（常量定义 / `build_page()` 主组件树）。
- 上轮 PRD: `.trellis/tasks/archive/2026-05/05-21-translate-next-batch-of-new-auto-ui-entries-settings-view-code-page/prd.md`。
- 上轮 apply 脚本参考：`.trellis/tasks/archive/2026-05/05-21-translate-next-batch-of-new-auto-ui-entries-settings-view-code-page/apply_translations.py`。
- 注意：drafter 在 code 批次混入了半角 `,`（违反 §5）—— 本批前先在 apply 脚本中加全角标点 invariant 校验，或在翻译草稿后批量替换为全角 `，`。
