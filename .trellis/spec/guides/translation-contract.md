# Translation Contract (UI String Translation)

> Checklist for translating UI strings from English to Chinese in this project. Use this as a prompt prefix when translating, or as a review gate when checking translations.

---

## When to use this guide

- About to translate a batch of new entries in `translations/strings.json`
- About to merge an LLM-produced batch and need a review checklist
- Adding a new term to `translations/glossary.json`

---

## Translator's checklist (in order)

### 1. Read the entry's full audit context

Before writing the target, look at:

- `source` — the English string
- `audit.reasons[]` — which heuristic rules fired (gives you UI category hints)
- `occurrences[].file` and `occurrences[].context_hint` — where it appears (button vs dialog vs description)
- `occurrences[].parent_call` if present (e.g. `Button::label`, `Dialog::new`)

The audit trail is there for translators. Use it.

### 2. Check `format!()` substitution semantics for every placeholder

This is the trap that bit us. If the source has `{}` or `{name}`, find the `format!()` call in the source code and read what fills the slot at runtime.

**Example bug**:

Source: `"This is the {} limit of AI credits for your account."`

Looking at `app/src/ai/request_usage_model.rs:464-466`, the `{}` is filled by `"weekly"` / `"monthly"` / `"biweekly"` — English adjectives.

Wrong target: `"这是您账户每{}的 AI 额度上限。"` → renders as `"这是您账户每weekly的 AI 额度上限。"` (broken Chinese).

Correct target: `"这是您账户的 {} AI 额度上限。"` (let the English word stand alone, restructure the Chinese around it).

**Rule**: If `{}` substitutes to an English word, do NOT prepend Chinese function-words directly to it. Either:
- Restructure the sentence so the placeholder is bracketed by neutral context, OR
- Mark the entry `do_not_translate` and translate the surrounding format-call structure instead (PR-level decision)

### 3. Apply the glossary

Open `translations/glossary.json` and use it. If the source string contains any glossary term:

- Use the glossary's Chinese translation verbatim
- If `do_not_translate: true`, keep the English word in the target (e.g. `Agent`, `MCP`, `Warp`)
- If you disagree with a glossary decision, propose a glossary update — do NOT diverge silently

Common glossary terms to watch for: `Agent` (keep English), `block` → `命令块`, `pane` → `窗格`, `panel` → `面板`, `prompt` → `提示词` (AI) / `提示符` (shell — context-disambiguated).

### 4. Preserve placeholders, identifiers, and shortcut hints verbatim

These MUST appear unchanged in the target:

- `{name}` / `{0}` / `{count}` — placeholder syntax
- Config keys: `warp.pty.recording`, `warp.ai.enabled`
- File extensions: `.rs`, `.toml`
- Identifiers and commands: `git`, `ssh`, `cargo`, `pty`
- Keyboard hints: `⌘Q`, `Ctrl+K`, `Cmd+Shift+P`
- URLs / paths

Counts MUST match — if source has 2 placeholders, target has 2 placeholders with the same names.

### 5. Use Chinese full-width punctuation

| Use | Not |
|---|---|
| `。` | `.` |
| `？` | `?` |
| `！` | `!` |
| `：` | `:` |
| `，` | `,` |
| `（）` | `()` (when surrounding Chinese; keep half-width when surrounding code/identifier like `(⌘Q)` → `（⌘Q）`) |
| `——` | `--` (em-dash) |

Do NOT mix half- and full-width in the same string.

### 6. Pick a tone and stick with it

Use `您` (formal) throughout this project. Do NOT mix with `你`. The PR3 batch maintained 100% `您` consistency across 22 entries — preserve that invariant.

### 7. Match the register

| UI element | Style |
|---|---|
| Button label | Short, imperative: `退出`, `新建窗口`, `保存` (no trailing punctuation) |
| Menu item | Same as button label |
| Tooltip | Brief noun phrase or imperative |
| Dialog title | Concise, no trailing period (use `？` if interrogative: `退出 Warp？`) |
| Long description / settings text | Full sentences, ending in `。` |
| Error message | Direct, neutral, no exclamation marks |

### 8. Decide when to mark `do_not_translate`

Set `flags: ["do_not_translate", "<sub-flag>"]`, `target: null`, `status: "translated"` when:

- Brand or product names: `Warp`, `Warp Drive`, `MCP`, `AWS Bedrock`, `Wispr Flow`
- Format placeholder shells: `"{}"`, `"%b %d"`, `"v#.##.###"`
- Editor placeholder hints showing literal commands: `"e.g. ls .*"`, `"aws login"`
- Copyright / version strings
- See the `do_not_translate` sub-flag taxonomy below for category-specific rules

**Note on search-keyword strings**: these are NOT `do_not_translate` anymore — see the bilingual-append technique below.

### 9. `do_not_translate` sub-flag taxonomy

Always pair `do_not_translate` with exactly one sub-flag that names the reason. This keeps the flag namespace clean and lets future audits filter by category. Current sub-flags:

| Sub-flag | Use for | Rationale |
|---|---|---|
| `extractor_false_positive_doc_comment` | Rust `///` doc comments captured inside macro bodies (`lazy_static!`, `mod regexes { }`, etc.) by `scan_macro_tokens` bypassing the doc-attr gate | Not user-facing; extractor bug |
| `test_fixture` | Real string literals living in unit-test fixtures (`*/testing/*.rs`, `*/tests/*.rs`, `*_test.rs`, hardcoded sample data) | Never shipped to users |
| `wgpu_debug_label` | wgpu `TextureDescriptor.label`, `BufferDescriptor.label`, etc. — graphics-API debug names | Visible only in graphics debuggers, not the app UI |
| `panic_message` | `.expect("...")`, `panic!("...")`, `unreachable!("...")` strings — internal assertion messages | See §10 |
| `telemetry_payload` | String literals that flow into telemetry / log events (event names, dimension values, format strings consumed by tracing macros that don't render to UI) | See §11 |

A target-less entry MUST set `status: "translated"` (so it leaves the `new` queue) and `target: null`. The `do_not_translate` flag plus the sub-flag together communicate "intentionally untranslated".

### 10. Panic / `.expect` strings — keep English

Per project policy as of 2026-05-23, `.expect("...")` / `panic!("...")` / `unreachable!("...")` / `debug_assert!(_, "...")` string literals are **not translated**. Flag them `["do_not_translate", "panic_message"]` and leave `target: null`.

**Why**: panic strings are surfaced only when a crash occurs. They serve as diagnostic context for developers reading crash reports, stack traces, and minidumps — audiences that work in English regardless of UI locale. A Chinese panic string adds friction for those audiences without benefiting users (who never see panic text unless we ship a bug, and even then a localized panic doesn't make the crash less broken).

Earlier batches (7–11) translated some panic strings before this policy was set. They're frozen as-is for now; a future audit batch can convert them if needed. Going forward: flag.

### 11. Telemetry payload strings — keep English

String literals that flow into telemetry, logging, or analytics events (without being rendered in the UI) are **not translated**. Flag them `["do_not_translate", "telemetry_payload"]` and leave `target: null`.

Examples that qualify:
- Event names and dimension values passed to `tracing::info!`, `telemetry::record!`, `track_event!`-style macros without `format!` rendering for the user
- Format strings consumed by structured logging where the output goes to a logfile, not a UI surface (`width: {:?}, height: {:?}`, `{}s`, etc.)
- `1 million` / `10 million` style range bucket names used as analytics dimensions

When in doubt: trace the literal to its sink. If the sink is `eprintln!` to stderr that surfaces in a user-visible toast/dialog → translate. If the sink is a telemetry pipeline, log file, or developer console → flag.

### 12. Search-keyword strings (`fn search_terms`) — bilingual append

Settings widgets implement `fn search_terms(&self) -> &str` returning a space-separated lowercase keyword string. The matcher at `app/src/settings_view/settings_page.rs:1405` does `terms.to_lowercase()` then for each query word `terms_lower.contains(word)`. This means **appending Chinese keywords to the English keyword string preserves English search and unlocks Chinese search** simultaneously.

**Pattern**:

| Original (source) | Target (translation) |
|---|---|
| `link open desktop native redirect url intent deep link deeplink` | `link open desktop native redirect url intent deep link deeplink 链接 打开 桌面 原生 重定向 网址 意图 深度 跳转` |

**Rules**:

1. Keep every English keyword in the original order and spelling. Do not delete, reorder, or "correct" the source list — it represents the original author's UX intent for the English locale.
2. After the last English keyword, append one space then the Chinese keywords space-separated, lowercase (Chinese has no case but Latin acronyms mixed in must stay lowercase to match the `to_lowercase()` step).
3. Mirror the semantic content. Don't pad with marketing words; don't invent unrelated synonyms. Each Chinese keyword should correspond to at least one English keyword's meaning.
4. No punctuation (no `，` no `,` no `；`). The matcher splits on whitespace; punctuation becomes part of a "word" and breaks matching.
5. No duplicates. If a Chinese rendering happens to equal an English one (rare — maybe `mcp` → `mcp`), don't repeat it.
6. Optional but recommended: add `search_terms_bilingual` flag (alongside the normal `status: "translated"`, with the bilingual string in `target`) for future audits. This is **not** a `do_not_translate` flag — the entry IS translated, just using an additive technique.

**Why this works**: every English query word continues to match because the original keywords are still verbatim in the target. Chinese queries match because the Chinese keywords are now present too. Mixed queries (`"link 链接"`) also work — every whitespace-delimited word from the query must appear in the terms string, and both halves do.

**Anti-patterns**:

- Replacing English with Chinese only (`"链接 打开 桌面 ..."`) → breaks English search.
- Translating individual English words in place (`"链接 open desktop ..."`) → unreadable mid-string, partial coverage, easy to drift.
- Adding commas or full-width punctuation (`"link, open, desktop, 链接, 打开"`) → matcher sees `"link,"` as one word; `"link"` query fails to match.

---

## What stays English (default)

- Brand names: Warp, Drive, MCP, AI, API, Git, SSH, AWS, OpenAI
- Protocol / format names: HTTP, JSON, YAML, SQL
- Identifiers, config keys, file paths, URLs, regex patterns
- Keyboard shortcuts
- Code samples shown in user-facing text

---

## After translating

1. Run `cargo run -p warp-zh-extractor -- extract --source ../../warp --table ../translations/strings.json --check` — must exit 0.
2. Run `cargo run -p warp-zh-builder -- build --source ../../warp --table ../translations/strings.json --out ../build/warp-zh`.
3. Run `cd build/warp-zh && MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp` — must exit 0. If it fails inside a translated file, the most likely cause is a broken format-string mismatch or an unescaped quote.

---

## Anti-patterns

### Don't translate a placeholder name

Source: `"Welcome, {name}"` → Target: `"欢迎，{用户名}"` ❌ (renames the placeholder; runtime `format!()` will not find `{用户名}` and the string breaks)

Correct: `"欢迎，{name}"` ✓

### Don't drop a placeholder

Source: `"{count} items selected"` → Target: `"已选中项目"` ❌ (drops `{count}`; output reads `已选中项目` regardless of count)

Correct: `"已选中 {count} 项"` ✓

### Don't translate identifiers shown to the user

Source: `"Run with --verbose flag"` → Target: `"使用 --详细 标志运行"` ❌ (translated the CLI flag; the flag does not exist)

Correct: `"使用 --verbose 标志运行"` ✓

### Don't mix `您` and `你`

Source A: `"Sign in to your account"` → `"登录您的账户"`
Source B: `"Welcome back"` → `"欢迎回来，你"` ❌

Pick one register per project. This project uses `您`.
