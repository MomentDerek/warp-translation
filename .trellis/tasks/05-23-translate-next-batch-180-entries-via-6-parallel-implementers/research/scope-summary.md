# Scope Summary — 180-entry translation batch (6 × 30)

- **Date**: 2026-05-23
- **Source-of-truth**: `tools/translations/strings.json` (commit `fdd74928de30add61f15b7cc60c316f2da98a555`, 6734 entries, all `status=new`)
- **Total candidates**: 180 (6 batches × 30)

## Note on strings.json state

The current `strings.json` (last modified 2026-05-22 20:29) was rebuilt from scratch by the extractor. All 6734 entries are `status=new`, `target=null`, `flags=[]`. Earlier batches' work (the 2284 `translated` + 105 `flagged` from `archive/2026-05/05-23-translate-next-uncertain-new-entries-batch-60-entries-12/`) is NOT present in this file — those PRDs were against a different physical table. Implementer agents will be writing fresh `target` values into this clean snapshot.

Where the source string in this batch matches a string previously translated in batch 7–12, **implementers should reuse the prior Chinese rendering** (look it up in those archived PRDs / git history) to keep style continuity. The IDs differ; the source strings are stable.

## Counts per action_hint

| action_hint | count |
|---|---|
| `translate` | 59 |
| `bilingual_search_terms` | 47 |
| `flag_panic_message` | 41 |
| `flag_telemetry_payload` | 33 |
| **TOTAL** | **180** |

## Counts per file

| file | count |
|---|---|
| `app/src/settings_view/features_page.rs` | 90 |
| `app/src/settings_view/environments_page.rs` | 30 |
| `app/src/editor/view/model/mod.rs` | 22 |
| `app/src/terminal/view/action.rs` | 19 |
| `app/src/terminal/event.rs` | 11 |
| `app/src/editor/view/mod.rs` | 8 |

## Batch composition

### Batch A — features_page.rs panic + telemetry + UI label top-up (30)

- **File**: `app/src/settings_view/features_page.rs` (all 30)
- **Action mix**: `flag_panic_message` (11) + `flag_telemetry_payload` (3) + `translate` (16)
- **Cohesion**: same file; mixed action hints intentionally clustered to keep features_page.rs reviewable as a single PR.
- **Panic series** (lines 1491, 1500, 1509, 1718, 1726, 1735, 1765, 1774, 1783, 1815, 3082): all `.expect("...")` inside the settings-mutation handlers. Apply `flags=["do_not_translate", "panic_message"]`, `target=null`, `status="translated"` per contract §10.
- **Telemetry series** (lines 889, 899, 930): inside `fn telemetry_event(&self, ctx) -> TelemetryEvent` body, become `TelemetryEvent::FeaturesPageAction.value`. Apply `flags=["do_not_translate", "telemetry_payload"]`. Note:
  - L889 `Active Screen` — `.unwrap_or_else(|| "Active Screen".into())` filling `screen` index display in the telemetry value field. Not UI-rendered.
  - L899 `width: {:?}, height: {:?}` — Quake mode size telemetry.
  - L930 `{}s` — long-running notification threshold seconds suffix in telemetry value.
- **Translate series** (lines 118–301): `ToggleSettingActionPair::new("<lowercase label>", ...)` first-arg labels appearing in the Command Palette as `Enable {label}` / `Disable {label}`. These are identical to entries already translated in archived batch-12; implementer should reuse those Chinese renderings:
  - `Left Option key is Meta` → `左 Option 键为 Meta`
  - `Right Option key is Meta` → `右 Option 键为 Meta`
  - `Left Alt key is Meta` → `左 Alt 键为 Meta`
  - `Right Alt key is Meta` → `右 Alt 键为 Meta`
  - `copy on select within the terminal` → `终端内选中即复制`
  - `linux selection clipboard` → `Linux 选择剪贴板`
  - `autocomplete quotes, parentheses, and brackets` → `自动补全引号、圆括号和方括号`
  - `restore windows, tabs, and panes on startup` → `启动时恢复窗口、标签页和窗格`
  - `scroll reporting` → `滚动上报`
  - `completions while typing` → `输入时自动打开补全`
  - `command corrections` → `命令纠错`
  - `error underlining` → `错误下划线`
  - `syntax highlighting` → `语法高亮`
  - `audible terminal bell` → `终端响铃`
  - `autosuggestion keybinding hint` → `自动建议快捷键提示`
  - `Warp SSH wrapper` → `Warp SSH 包装器`

### Batch B — features_page.rs search_terms bilingual append (30)

- **File**: `app/src/settings_view/features_page.rs` (all 30)
- **Action**: `bilingual_search_terms` (30)
- **Cohesion**: same file, single action.
- **Pattern** (per contract §12): `fn search_terms(&self) -> &str { "<lowercase english keywords>" }` inside settings-widget `impl`s. Implementer appends Chinese keywords after the English ones, separated by single spaces, no punctuation, no duplicates, mirroring semantic content.
- **Lines**: 4183, 4243, 4338, 4391, 4437, 4459, 4506, 4557, 4604, 4651, 4737, 4784, 4829, 4890, 4949, 5134, 5173, 5210, 5232, 5280, 5349, 5494, 5540, 5586, 5632, 5682, 5728, 5775, 5824, 5933 (first 30 of 47).
- **Example**: `link open desktop native redirect url intent deep link deeplink` → `link open desktop native redirect url intent deep link deeplink 链接 打开 桌面 原生 重定向 网址 意图 深度 跳转 deeplink`. Keep English exact; append Chinese semantic mirror; no commas.
- **Flags**: per contract §12 hint #6, optionally add `flags=["search_terms_bilingual"]` (NOT a do_not_translate; entry IS translated).

### Batch C — features_page.rs search_terms remaining + UI label top-up (30)

- **File**: `app/src/settings_view/features_page.rs` (all 30)
- **Action mix**: `bilingual_search_terms` (17 remaining) + `translate` (13 top-up labels)
- **Lines (search_terms)**: 5985, 6041, 6093, 6141, 6196, 6326, 6384, 6431, 6486, 6544, 6591, 6695, 6768, 6814, 6859, 6895, 6947 (the remaining 17 of 47).
- **Translate top-up** (lines 313–489): more `ToggleSettingActionPair` labels (same family as Batch A). Suggested Chinese renderings, continuing prior style:
  - `show tooltip on click on links` → `点击链接时显示提示`
  - `quit warning modal` → `退出警告对话框`
  - `alias expansion` → `别名展开`
  - `middle-click paste` → `中键粘贴`
  - `code as default editor` → `将 code 设为默认编辑器`
  - `input hint text` → `输入提示文字`
  - `editing commands with Vim keybindings` → `使用 Vim 快捷键编辑命令`
  - `Vim unnamed register as system clipboard` → `Vim 无名寄存器作为系统剪贴板`
  - `Vim status bar` → `Vim 状态栏`
  - `focus reporting` → `焦点上报`
  - `smart select` → `智能选中`
  - `terminal input message line` → `终端输入消息行`
  - `slash commands in terminal mode` → `终端模式下的斜杠命令`

### Batch D — editor panic_message (30)

- **Files**: `app/src/editor/view/model/mod.rs` (22) + `app/src/editor/view/mod.rs` (8)
- **Action**: `flag_panic_message` (30)
- **Cohesion**: cross-file but single action; both files are the same editor subsystem; all entries are `.expect(...)` invariant-failure messages.
- **All entries are inside `.expect(...)` calls on the same line or 1-3 lines below a `.something()` chain.** Implementer should NOT translate; set `target=null`, `flags=["do_not_translate", "panic_message"]`, `status="translated"`.
- **Editor mod.rs lines** (L976–L2807): selection/buffer/anchor invariant assertions.
- **Editor view/mod.rs lines** (L3833, 3838, 3854, 4243, 5584, 5662, 5968, 5974): same diagnostic phrasing family.

### Batch E — terminal telemetry_payload (30)

- **Files**: `app/src/terminal/view/action.rs` (19) + `app/src/terminal/event.rs` (11)
- **Action**: `flag_telemetry_payload` (30)
- **Cohesion**: both files contain `impl Display for X` or `impl Debug for X` enum-fmt blocks where the string literal is the event/action name written to a tracing macro or string. None of these surface in UI.
- **terminal/view/action.rs** (L478–L676): `impl Display for Action` `fn fmt()` — each `Action` enum variant has a `write!(f, "<literal>")` rendering. These render into log/tracing pipelines, not UI.
- **terminal/event.rs** (L411–L488, first 11): `impl Debug for Event` `fn fmt()` — same pattern. Examples: `BlockStarted({:?}, Done bootstrapping: {:?})`, `RemoteServerReady(session: {session_id:?})`, `TmuxInstallFailed(line: {line}, command: {command})`.
- All 30 → `target=null`, `flags=["do_not_translate", "telemetry_payload"]`, `status="translated"`.
- **NOT in this batch** (4 leftover terminal/event.rs entries): `AgentTaggedInChanged(...)`, `Handler({:?})`, `FinishUpdate({})`, `ShellSpawned({:?})`, `ImageReceived(...)` — defer to a future batch (same flag treatment).

### Batch F — environments_page.rs UI sweep — translate (30)

- **File**: `app/src/settings_view/environments_page.rs` (all 30)
- **Action**: `translate` (30)
- **Cohesion**: single file, single action — clean UI translation work, no policy nuance.
- **Lines** (L85–L1488, of 32 total entries; excluded L1045 which is a `search_terms` bilingual candidate — leave for a future batch):
  - **Section titles / heroes**: L85 `Environments`, L1411 `Get started`, L1452 `Quick setup`, L1488 `You haven't set up any environments yet.`
  - **Descriptions**: L86 `Environments define where your ambient agents run. ...`, L1455 `Select the GitHub repositories you'd like to work with ...`, L1469 `Choose a locally set up project ...`
  - **Toasts**: L639/L657/L674/L697/L699 success/failure messages
  - **Error states**: L769/L796/L965/L973 unable-to-X dialog text
  - **Buttons**: L1411 `Get started`, L1433 `Launch agent`, L1466 `Use the agent`
  - **List metadata format strings**: L185 `{owner}/{repo}`, L194 `Last edited: {}`, L200 `Last used: {}`, L203 `Last used: never`, L206 `{} · {}`
  - **Search placeholder**: L376 `Search environments...` → `搜索环境……`
  - **Empty state**: L1290 `No environments match your search.` → `没有匹配您搜索的环境。`
  - **Loading**: L1405 `Loading...` → `加载中……`
- **Format placeholder caveats**:
  - L185 `{owner}/{repo}` — both slots are owner/repo identifiers (English). Keep as `{owner}/{repo}` (no translation needed, but to leave the queue: `target="{owner}/{repo}"` with `flags=["do_not_translate", "format_placeholder_shell"]` may be cleaner — or just translate as-is since it has no English words). Implementer judgement: probably flag as `do_not_translate, format_placeholder_shell`.
  - L194 `Last edited: {}` / L200 `Last used: {}` / L1320 `Shared by Warp and {}` — `{}` substitutes to dates/team-names, both English-stable. Translate around it: `上次编辑：{}` / `上次使用：{}` / `由 Warp 与 {} 共享`.
  - L206 `{} · {}` — pure separator format; mark `do_not_translate, format_placeholder_shell`.
  - L1762 `Env ID: {}`, L1817 `Image: {}`, L1825 `Repos: {}`, L1830 `Setup commands: {}` — translate label, keep `{}`.
- **Smart quotes**: L1455, L1469, L1488, L1497 use Unicode `'` (U+2019) — preserve in target if you keep apostrophes; if Chinese fully replaces the English they may disappear naturally.

## Glossary deltas needed

Existing terms reusable as-is: `Warp`, `Warp Drive`, `Agent`, `MCP`, `Oz`, `Profile`, `Linux`, `Vim`, `SSH`, `PTY`, `REPL`, `token`, `chip`.

New term proposals (implementer may flag for glossary update if any are confirmed):
- `ambient agent` → `常驻 Agent`（环境中常驻运行的 Agent；与 `Cloud Agent → 云端 Agent` 区分）  ← from environments_page.rs L86. **Confirm with user before committing**; alternative: keep `ambient` English.
- `environment` (in Warp environments-page sense — a containerized agent runtime) → `环境`（与系统环境变量上下文 `environment variable → 环境变量` 区分；此处指 Warp Environments 特性的实体）.
- `Env ID` → `环境 ID`（L1762）.
- `Setup commands` → `配置命令`（L1830）.

No new term required for batches A–E (all `do_not_translate` or known-vocabulary UI labels).

## Edge cases for implementers

1. **Batch A L3082** `Pin position should exist in default size percentages` — the only non-`failed to serialize` panic in features_page.rs. Same treatment: `do_not_translate, panic_message`.

2. **Batch B/C — `search_terms` already-Chinese-friendly strings**: a few search_terms lines may already contain identifier-like fragments (e.g. `gpu vulkan dx12 directx12`). Keep those identifiers verbatim in the English half AND append Chinese semantic equivalents (`GPU 图形 后端 驱动`). Do not invent acronyms.

3. **Batch B/C — `mcp` lowercase**: when an English keyword is itself `mcp` (brand identifier kept lowercase per author intent), the Chinese half should still NOT duplicate it. `MCP` is a glossary `do_not_translate` brand; in this matcher context the lowercased form is what matters.

4. **Batch D — `unreachable!` / `panic!` not present in our selection**: all 30 are `.expect(...)`. The `panic_message` flag is the correct sub-flag (covers all of `.expect` / `panic!` / `unreachable!` / `debug_assert!`).

5. **Batch E — `terminal/view/action.rs` `{{ ... }}` literal braces**: many entries contain `{{` / `}}` which `format!` parses as literal `{` / `}`. These are intentional in the source. Implementer doesn't translate, but should preserve them verbatim if a future audit decides to translate (not this batch).

6. **Batch E — `terminal/event.rs` L424 `Pre-Interactive SSH Session`**: looks like a UI-shape string but actually `write!(f, "Pre-Interactive SSH Session")` inside `impl Debug for Event::fmt()`. It's a Debug rendering of an enum variant — telemetry, not UI. Flag.

7. **Batch F L185 `{owner}/{repo}`**: per `do_not_translate` sub-flag taxonomy, this is closest to `format_placeholder_shell` but that sub-flag is not in the current taxonomy. Either:
   - (a) Add `format_placeholder_shell` as a new sub-flag (requires glossary/spec update first).
   - (b) Translate as identity `{owner}/{repo}` (target = source) — schema-allowed but slightly redundant.
   - (c) Skip and defer.
   
   **Recommended**: (b) — set `target="{owner}/{repo}"`, `status="translated"`, no flag. Implementer should pick this unless directed otherwise.

8. **L1320 `Shared by Warp and {}`** vs **L1321 `Shared by Warp and your team`**: L1321 is the team-known fallback. Translate as `由 Warp 与您的团队共享。` (full sentence) and L1320 as `由 Warp 与 {} 共享。`. Note L1320 omits trailing period in source — preserve absence; L1321 also omits period in source.

9. **Batch F search_terms entry skipped**: L1045 `environments environment ambient agents github warp assisted manual configuration` is a `search_terms` bilingual candidate; left out of this batch. Future batch can apply bilingual append: `... 环境 常驻 agent github warp 辅助 手动 配置`.

10. **`features_page.rs` truly-deferred items NOT in any of these batches**:
    - Long settings descriptions (e.g. L705 `Setting the limit above 100k lines may impact performance...`) — should translate, but didn't fit in 30-slot batches A/C. Defer.
    - L6261/L6271/L6280 dynamic tooltip text (`{key} accepts autosuggestions.` etc.) — UI translation, defer.
    - L7235 `Current backend: {}` — UI text, defer.
    - L884 `1 million` / `10 million` (if present as entries) — telemetry analytics-dimension strings, would be flag, defer.

## File manifest

```
research/
├── candidates-A.json   (30 — features_page.rs mixed)
├── candidates-B.json   (30 — features_page.rs search_terms bilingual)
├── candidates-C.json   (30 — features_page.rs search_terms bilingual + UI labels)
├── candidates-D.json   (30 — editor panic_message)
├── candidates-E.json   (30 — terminal telemetry_payload)
├── candidates-F.json   (30 — environments_page.rs UI translate)
└── scope-summary.md    (this file)
```

Each `candidates-X.json` is a JSON array of objects with the schema:

```json
{
  "id": "01KS7TBZ...",
  "source": "the english string",
  "file": "app/src/.../foo.rs",
  "line": 1234,
  "occurrences_kind": "literal" | "macro_arg",
  "audit_verdict": "auto_ui" | "uncertain",
  "action_hint": "translate" | "flag_panic_message" | "flag_telemetry_payload" | "flag_extractor_false_positive_doc_comment" | "flag_test_fixture" | "bilingual_search_terms",
  "category": "free-form descriptor"
}
```

Implementer reads the batch JSON + this scope-summary + the translation-contract spec (§10 panic, §11 telemetry, §12 search_terms), then mutates `tools/translations/strings.json` for those 30 entries only.
