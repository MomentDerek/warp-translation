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

Set `flags: ["pr*_first_batch", "do_not_translate"]` and leave `target` null when:

- Brand or product names: `Warp`, `Warp Drive`, `MCP`, `AWS Bedrock`, `Wispr Flow`
- Search-keyword strings (lowercase multi-word, used for in-app search match — translation breaks search)
- Format placeholder shells: `"{}"`, `"%b %d"`, `"v#.##.###"`
- Editor placeholder hints showing literal commands: `"e.g. ls .*"`, `"aws login"`
- Copyright / version strings

Do NOT use `do_not_translate` as a workaround for entries the heuristic should have rejected (panic strings, action IDs). Flag those upstream for a heuristic fix instead.

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
