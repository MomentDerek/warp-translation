# Translate 180 entries via 6 parallel implementers (batch 13)

## Goal

继 batch-12（uncertain-pool 首次扫描）后，本批 **6 路并行**处理 180 条 `status=new` 条目，覆盖三类近期被新策略解禁的工作：

1. **panic / telemetry 字面量"按策略不译"**（batch-12 PRD 列出但延后）— 现已由 `.trellis/spec/guides/translation-contract.md` §10/§11 codified。
2. **`fn search_terms()` 双语追加策略** — §12 codified；首次大规模落地。
3. **新增 uncertain-pool UI 扫描** — `billing_and_usage_page.rs` 与 `code_review_view.rs` 两个未被触达的高密度 UI 文件。

## Batch composition (6 × 30 = 180)

| Batch | 数量 | 文件 | 主要动作 |
|:---:|:---:|---|---|
| **A** | 30 | `settings_view/features_page.rs` (9 panic + 3 telemetry) + `settings_view/billing_and_usage_page.rs` (18 UI/format) | `flag_panic_message` × 9, `flag_telemetry_payload` × 3, `translate` × 18 |
| **B** | 30 | `settings_view/features_page.rs` × 30 search_terms | `bilingual_search_terms` × 30 |
| **C** | 30 | `settings_view/features_page.rs` × 17 + `settings_view/appearance_page.rs` × 13 search_terms | `bilingual_search_terms` × 30 |
| **D** | 30 | `editor/view/model/mod.rs` × 22 + `editor/view/mod.rs` × 8 panic strings | `flag_panic_message` × 30 |
| **E** | 30 | `terminal/view/action.rs` × 19 + `terminal/event.rs` × 11 telemetry labels | `flag_telemetry_payload` × 30 |
| **F** | 30 | `code_review/code_review_view.rs` × 30 UI | `translate` × 30 |

## Action-hint policy reference

- `translate` — 译为中文，遵循 [translation-contract](.trellis/spec/guides/translation-contract.md) §1-7。
- `flag_panic_message` — 见 §10：`target=null`, `status=translated`, `flags=[batch_flag, do_not_translate, panic_message]`。
- `flag_telemetry_payload` — 见 §11：`target=null`, `status=translated`, `flags=[batch_flag, do_not_translate, telemetry_payload]`。
- `bilingual_search_terms` — 见 §12：`target=<english + " " + chinese keywords>`, `status=translated`, `flags=[batch_flag, search_terms_bilingual]`（**不是** do_not_translate）。

## Glossary (沿用 batch-12 + 增量)

- 沿用：`Warp`, `Warp Drive`, `Oz`, `Agent`, `MCP`, `Profile`, `PTY`, `REPL`, `Linux`, `OAuth`, `JWT`, `Stripe`, `GitHub`, `Slack`, `Firebase`, `Fireworks`, `chip`, `token`, `Full Terminal Agent`, `Settings > AI > Voice`。
- 本批新增候选术语（实现 agent 可建议）：
  - `Code Review` → `代码审查` (feature 名首字母大写时保留英文 `Code Review`)
  - `credit(s)` → `credit(s)`（保留英文，与 Warp 计费 UI 一致）or `点数`（待定，参考既有译文）
  - `Buying…` → `购买中……`（`...` → `……`）
  - `diff` → `diff`（保留英文）
  - `panic_message` / `telemetry_payload` flag 不需要术语

## Process

1. 每个实现 agent 读 `candidates/batch-{X}.json`，按 `action_hint` 处置每条。
2. 输出写到 `outputs/batch-{X}-output.json`，schema：
   ```json
   {
     "translations": {"<id>": "<chinese>" | null, ...},
     "do_not_translate_subflags": {"<id>": ["panic_message" | "telemetry_payload"], ...},
     "bilingual_search_terms_ids": ["<id>", ...],
     "notes": "free text"
   }
   ```
3. 主 orchestrator 合并 6 个 output → 单个 `apply_translations.py` 运行。
4. trellis-check 验证 placeholder/glossary/whitespace 不变量。

## Counts after apply

期望：`translated` 2389 → 2569 (+180), `new` 4293 → 4113 (-180), `fuzzy` 52 (不变)。
