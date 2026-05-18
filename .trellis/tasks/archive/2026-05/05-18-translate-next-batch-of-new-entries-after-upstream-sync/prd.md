# Translate next batch of new entries after upstream sync

## Goal

Digest the 279 net-new strings introduced by the 05-15 upstream sync (`25652d73` → `b9ec4f39`, 357 commits) into translated entries with Chinese targets, keeping `extract --check` idempotent and the build green.

## What I already know

- Sync delta from journal: `added=279 changed=33 unchanged=6328 obsoleted=30`. Translated 735→728→732 after the 05-18 fuzzy refresh.
- Current table stats: `entry_count=6670`, `translated=732`, `fuzzy=30`, `new=5878`, `uncertain=4509`, `obsolete=30`.
- The 279 new entries' source-location breakdown:
  | Bucket | Count |
  |---|---|
  | `app/src` (UI strings) | 237 |
  | `crates/remote_server` | 27 |
  | `crates/ai` | 12 |
  | `crates/editor` | 2 |
  | `crates/warp_features` | 1 |
- Theme clusters inside the 237 UI strings:
  1. **Cloud handoff / cloud agents** — "Hand off to cloud", "Cloud handoff requires…", `&`-trigger compose mode, ~30+ strings
  2. **Custom endpoints / BYOK** — "Custom inference", "Add endpoint", "Anthropic/OpenAI/Google API key", validation messages, ~25 strings
  3. **Orchestration / Oz** — "Multi-agent orchestration", "Spawn N agents", "[Debug] Reset Oz Launch Modal", ~20 strings (glossary: Oz→Orchestration→编排)
  4. **Billing & credits** — "Personal credits", "Team credits", "Auto-reload", "Switch to Business", "monthly limit", ~15 strings
  5. **Remote codebase / SSH** — "Remote codebase search is unavailable…", `Remote server unexpected response for X` (mostly `crates/remote_server`), ~30 strings
  6. **Agent memory & harness** — "Agent Memory", "Agents will now store…", "Agent failed to start…", "Kill agent", ~10 strings
- Audit verdict roughly splits as: `auto` (high-confidence UI labels/copy) vs `uncertain` (error/log strings with format placeholders or rare-path technical messages).
- Glossary precedents already established: `multi-agent orchestration → 多 Agent 编排`, `Oz → 编排` (codename → public concept).

## Scope (locked — option 1: stable MVP)

Target: the **113 `auto_ui`-verdict entries** across these 7 themes (`remote_server` technical error logs excluded):

| Theme | auto_ui count |
|---|---|
| misc_ui | 44 |
| byok_endpoints | 26 |
| billing | 16 |
| remote_codebase | 10 |
| cloud_handoff | 9 |
| orchestration | 6 |
| agent_harness | 2 |

Excluded from this batch:
- 150 `uncertain`-verdict entries (mostly error strings with placeholders, low UX visibility) — stay as `status=new` until next batch.
- 16 `auto_ui` entries under `app/src/remote_server/server_model.rs` (technical buffer/diff errors) — UX-low; defer.
- 27 `crates/remote_server` log strings — same reason.

## Decisions (locked)

### Quality gate
Full rebuild + cargo check: translate → run `warp-zh-builder` to produce fresh `build/warp-zh/` against upstream `b9ec4f39` → `cargo check -p warp` must pass.

### Glossary additions
Append to `translations/glossary.json` before translating:

| Term | zh | Notes |
|---|---|---|
| `credit` / `credits` | 积分 | "Personal/Team/Free credits" → "个人/团队/免费积分"; "{credits} credits" → "{credits} 积分" |
| `auto-reload` | 自动充值 | 触发条件是 balance 跌破阈值后 refill，非"重载" |
| `handoff` / `hand off` | 移交 | 动作单向；非"交接/转交" |
| `cloud handoff` | 云端移交 (名词) / 移交至云端 (动作) | 视上下文 |
| `harness` | 执行环境 | "agent harness" = Claude Code/Codex 等运行框架 |
| `BYOK` | BYOK | 行业缩写保留；首次出现可注 "自带密钥" |
| `endpoint` | 端点 | "Custom endpoints" → "自定义端点" |
| `Oz` (codename) → orchestration | 编排 | 已在 05-18 fuzzy refresh 中确立 |

### Batch flag
`pr-post-sync-batch` (与既有 `pr3_first_batch` / `pr-menu-batch` 命名风格一致)

## Acceptance Criteria (final)

- [ ] 113 entries: `status: new → translated`, `flags` 含 `pr-post-sync-batch`, 非空 `target`
- [ ] `extract --check` exit 0（幂等）
- [ ] 现存 227 (pr3) + 506 (menu) + 732 (post-fuzzy-refresh) 已翻译条目逐字保留
- [ ] glossary.json 新增 7 个术语条目（credit/auto-reload/handoff/cloud-handoff/harness/byok/endpoint），`term_count` 32 → 39
- [ ] 所有 113 条的目标文本满足 translation-contract checklist：占位符完整 / 快捷键修饰符原样 / glossary 一致
- [ ] `warp-zh-builder` 跑过，`build/warp-zh/` 重建，marker file 写入
- [ ] `cargo check -p warp` 在 `build/warp-zh/` 通过

## Technical Approach

1. **Glossary 增补**：先把 7 个术语写入 `translations/glossary.json`，term_count 字段同步。
2. **Filter & translate 113 entries**：用 Python 脚本筛出目标条目（status=new + first_seen_commit prefix b9ec4f39 + audit.verdict=auto_ui + 排除 path 含 `app/src/remote_server/server_model.rs`），按 7 个主题簇分批人工/LLM 翻译，写回 entries[*].target + status=translated + flags += [pr-post-sync-batch]，刷新 updated_at / history。
3. **Idempotency check**：`cargo run -p warp-zh-extractor --release -- extract --check` 必须 exit 0。
4. **Build**：`cargo run -p warp-zh-builder --release` → 输出至 `build/warp-zh/`。
5. **Verify**：`cargo check -p warp` on `build/warp-zh/`（预计 ~3 min，b9ec4f39 是首次构建）。
6. **Journal + archive**。

## Plan (single PR, no decomposition)

113 条是一次性可消化的量；不拆 child task。

## Requirements (evolving)

- Translate selected entries with `flags=[pr-post-sync-batch]` (or similar batch tag), 100% glossary/placeholder consistency.
- `extract --check` remains idempotent after translation.
- Preserve all 227 `pr3_first_batch` + 503 `pr-menu-batch` + 732 currently-translated entries verbatim.

## Acceptance Criteria (evolving)

- [ ] Selected entries' `status` flipped from `new` → `translated` with non-empty `target`.
- [ ] `extract --check` exit 0.
- [ ] Glossary consistency check passes (no `Agent`/智能体 or 智能体/Agent mix; orchestration→编排; cloud→云端; credits→积分; etc — to be confirmed).
- [ ] Placeholder integrity: every `{name}` / `{:?}` / `%b %d` preserved verbatim in target.
- [ ] (If build chosen) `cargo check -p warp` passes on `build/warp-zh/`.

## Definition of Done

- Translations follow existing tone (concise, command-bar style) and glossary.
- Journal entry recorded with stats delta.
- Task archived.

## Out of Scope (explicit)

- Translating the other 5,599 pre-existing `status=new` entries from the original extraction.
- Refactoring extractor heuristics (unless a new gap shows up).
- Glossary expansion — only add new terms when a cluster forces it (e.g., BYOK, credit, auto-reload).

## Technical Notes

- Source-of-truth file: `translations/strings.json` (single canonical table).
- Builder: `tools/builder/` → produces `build/warp-zh/` from upstream `../warp` + table.
- Prior batches: pr3_first_batch (227), pr-menu-batch (506) — recorded in journal sessions 1–2.

## Research References

(to add if research needed — most context is in journal & glossary already)
