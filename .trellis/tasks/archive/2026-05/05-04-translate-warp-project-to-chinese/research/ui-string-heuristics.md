# Research: UI 字符串自动判定启发式（无 i18n 框架的 Rust 项目）

- **Query**: 在没有 i18n 框架的 Rust 项目中，如何自动判定哪些字符串字面量是用户可见 UI 文本，避免误译日志/标识符/正则等非 UI 字符串
- **Scope**: 内部 (Warp 仓库结构 + AST 调用点) + 外部 (cargo-i18n / xtr / i18next-parser / fluent-rs 启发式)
- **Date**: 2026-05-04
- **Source repo**: `<HOME>/Documents/Codes/warp`

---

## 摘要

经过对 Warp 仓库 (`app/src/settings_view/*.rs`, `app/src/app_menus.rs`, `app/src/command_palette.rs`, `crates/warpui/src/platform/mac/menus.rs` 等) 的实地采样，UI 字符串具有非常明显的"调用点签名"。
推荐采用 **白名单优先 + 黑名单兜底 + 调用点 AST 评分** 的混合判定算法：

1. 用 `syn` 解析 `.rs` 文件，遍历所有 `LitStr` 节点；
2. 对每个字面量，先按 **路径白/黑名单** 给基础分；
3. 再看 **父节点上下文**（外层 `MethodCall`/`Call`/`Macro`/`#[attr]`/`Match`/`const fn` 名）调整分数；
4. 再用 **正则黑名单** 否决形态明显非 UI 的字符串（路径、URL、UUID、snake_case、CSS 类、SQL 等）；
5. 最终 score ≥ 阈值 → 进入翻译表，否则丢弃。
6. **mark UI 与 mark not-UI 的最终决定权交给开发者审核**（在翻译表中保留 `decision` / `note` 列），算法只做粗筛。

---

## (a) Warp 仓库目录白名单/黑名单清单

### 白名单（几乎全部字面量都是 UI 文本，权重 +3）

按目录优先级（高→低）：

| 路径（相对 `warp/`） | 说明 |
|---|---|
| `app/src/settings_view/**/*.rs` | 设置页：about/ai/code/appearance/billing/teams/keybindings/mcp_servers/features/privacy/platform/referrals 等。**排除** `*_tests.rs` / `*_test.rs` / `mod_test.rs` |
| `app/src/app_menus.rs` | 主菜单栏（File / Edit / View / Tab / Blocks / AI / Drive / Window / Help） |
| `crates/warpui/src/platform/mac/menus.rs` | Mac 菜单底层（极少字面量，主要是数据透传，仍归为 UI 候选） |
| `app/src/menu.rs` | 通用菜单组件 |
| `app/src/command_palette.rs` | 命令面板 keybinding 列表（行为标识符不译，但相邻 description 译） |
| `app/src/search/command_palette/**/*.rs` | 命令面板视图（排除 `*_test*.rs`） |
| `app/src/wasm_nux_dialog.rs` | NUX 引导对话框 |
| `app/src/banner/**/*.rs` | 顶部横幅 |
| `app/src/notification.rs` | 桌面通知文本（注意：错误通知默认不译，需白名单） |
| `app/src/quit_warning/**/*.rs` | 退出确认对话框 |
| `app/src/workspace/*confirmation_dialog.rs` (`close_session_confirmation_dialog.rs`, `rewind_confirmation_dialog.rs`, `delete_conversation_confirmation_dialog.rs`) | 各种模态确认框 |
| `app/src/workspace/native_modal.rs` | 原生模态 |
| `app/src/cloud_object/grab_edit_access_modal.rs` | 模态 |
| `app/src/auth/needs_sso_link_view.rs` | 登录引导 |
| `app/src/resource_center/**/*.rs` | Resource Center / Tips / Keybindings page（排除 `*_test*.rs`） |
| `app/src/tips/**/*.rs` | 内联提示 |
| `app/src/ui_components/**/*.rs` | tab_selector 等组件实例化处的标签 |
| `app/src/settings_view/agent_assisted_environment_modal.rs`, `transfer_ownership_confirmation_modal.rs` | 模态 |
| `crates/ui_components/src/*.rs` | 通用按钮/对话框组件**实现**（多为基础设施，但 placeholder 默认值仍可能是 UI；权重 +1） |
| `about.toml`, `about.hbs` | 关于页模板（非 .rs，单独处理） |

### 黑名单（几乎不可能是 UI，权重 -5，直接跳过）

| 路径模式 | 理由 |
|---|---|
| `**/tests/**`, `**/*_test.rs`, `**/*_tests.rs`, `**/test_*.rs`, `**/mod_test.rs` | 测试代码 |
| 函数体或 mod 块带 `#[cfg(test)]` / `#[test]` | 测试代码 (需 AST 判断，见下) |
| `**/build.rs` | 构建脚本 |
| `crates/warp_cli/**` | CLI 工具，输出走 stdout，可能含面向开发者的英文，但非 GUI UI |
| `crates/simple_logger/**`, `crates/tracing*/**` | 日志基础设施 |
| `crates/jsonrpc/**`, `crates/ipc/**`, `crates/graphql/**`, `crates/lsp/**`, `crates/managed_secrets*/**`, `crates/firebase/**` | 协议/网络/序列化层 |
| `crates/persistence/**`, `crates/virtual_fs/**`, `crates/string-offset/**`, `crates/sum_tree/**`, `crates/syntax_tree/**` | 存储/数据结构 |
| `crates/integration/**`, `**/integration_testing/**` | 集成测试 |
| `app/src/ai/agent_sdk/**`, `app/src/ai/agent_events/**`, `app/src/ai/agent_management/**` | AI SDK：含 system prompt、tool schema、协议字符串。默认全部不译，少量 UI 文本（如设置页旁路）走调用点白名单单独命中 |
| `app/src/server/**`, `app/src/auth/**` (除 `needs_sso_link_view.rs`) | 网络/鉴权 |
| `app/src/persistence/**` | 数据库 |
| `app/src/util/**` (除 `bindings.rs` 的 description 字段) | 工具函数 |
| `app/src/tracing.rs`, `app/src/profiling.rs`, `app/src/crash_reporting/**`, `app/src/server/telemetry.rs`, `**/telemetry.rs` | 日志/遥测 |
| `app/src/integration_testing/**`, `app/src/test_util/**` | 测试支持 |
| `app/src/keyboard.rs`, `app/src/keymap*.rs`, `crates/warpui_core/src/keymap.rs` | 键名常量（"cmd-n", "shift" 等是协议标识符，不译） |
| `**/build.rs`, `**/.cargo/**`, `Cargo.toml` | 构建配置 |
| `target/**`, `**/__generated__/**` | 产物 |

### 灰名单（需要看调用点上下文，权重 0）

| 路径 | 说明 |
|---|---|
| `app/src/lib.rs`, `app/src/workspace/mod.rs`, `app/src/workspace/view.rs` | 注册大量 action 描述 (`BindingDescription::new("...")`) → UI；但也有大量 action ID (`workspace:toggle_command_palette`) → 不译 |
| `app/src/util/bindings.rs` | `BindingDescription::new(...)` UI；`name: String` 通常是 action id，不译 |
| `app/src/settings/*.rs` | 设置项定义；含 `command_palette_description()`、显示标题；与配置 key 名共存 |
| `app/src/ai/agent_tips.rs` | agent 提示文本，部分 UI 部分 prompt，需逐条判断 |

---

## (b) 排除性正则列表（直接拷贝使用）

字符串 `s`（不含外层引号）若匹配以下任一正则，**强制判定为非 UI**（除非调用点强 UI，见 §(c) 覆盖规则）。

```python
# 推荐顺序：从最强信号到弱信号，命中即返回 not-UI
NON_UI_REGEX = [
    # 1. 资源路径 / 文件名 / 扩展名
    r'^[A-Za-z0-9_\-./]+\.(svg|png|jpg|jpeg|gif|webp|ico|ttf|otf|woff2?|wasm|json|toml|yaml|yml|hbs|md|txt|csv|sql|db|sqlite|so|dylib|dll|exe)$',
    r'^bundled/.*',                 # bundled/svg/* 等内部资源
    r'^(\.\./|\./|/)?([\w\-.]+/)+[\w\-.]+$',  # 多级路径
    r'^\$?[A-Z_][A-Z0-9_]*$',       # 环境变量名 / 全大写常量

    # 2. URL / scheme
    r'^(https?|ftp|ssh|warp|file|mailto|data):',
    r'^//[^\s]+$',
    r'^[a-z]+://',

    # 3. UUID / Hash / Base64-ish
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
    r'^[0-9a-fA-F]{32,}$',
    r'^[A-Za-z0-9+/=]{40,}$',

    # 4. 标识符 / action id / event name
    r'^[a-z][a-z0-9_]*(:[a-z][a-z0-9_]*)+$',  # workspace:toggle_command_palette
    r'^[a-z][a-z0-9_]*$',                     # snake_case 单 token
    r'^[A-Z][A-Za-z0-9]*$',                   # CamelCase 单 token (CSS 类名 / view 名 "AboutPage")
    r'^[A-Z][A-Z0-9_]+$',                     # SCREAMING_CASE
    r'^[a-z]+(-[a-z]+)+$',                    # kebab-case (cmd-n / shift-up 这种是按键)

    # 5. 按键组合 / 快捷键
    r'^(cmd|ctrl|alt|shift|meta|super|fn)([\-+](cmd|ctrl|alt|shift|meta|super|fn|[a-z0-9]|f\d{1,2}|tab|enter|space|escape|backspace|delete|up|down|left|right))+$',
    r'^f\d{1,2}$',                  # f1..f20

    # 6. 正则 / 格式串 / 占位符
    r'^[\^$].*[$\^]?$',             # 正则：^...$
    r'^\{[^}]*\}$',                 # 单个 {placeholder}
    r'^%[sdoxbf%]$',                # printf 单个占位符
    r'^\{:?[\w.<>?+\-#0]*\}$',      # Rust format spec

    # 7. SQL / GraphQL keywords-only / 协议片段
    r'^(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|FROM|WHERE)\b',
    r'^\s*query\s+\w+',
    r'^\s*mutation\s+\w+',

    # 8. MIME / Content-Type
    r'^[a-z]+/[a-z0-9.+\-]+$',

    # 9. 单字符 / 标点 / 空白
    r'^.{0,1}$',
    r'^[\s\p{P}\p{S}]+$',           # 仅标点/符号

    # 10. 数字字符串 / 版本号
    r'^\d+(\.\d+)*$',
    r'^v?\d+\.\d+\.\d+(-[\w.]+)?$',

    # 11. 时间格式 / strftime
    r'^%[YmdHMSpfzZ]([:\-/]%[YmdHMSpfzZ])+$',

    # 12. 内部命名空间 (com.warpdotdev.*, dev.warp.*)
    r'^[a-z]+\.[a-z]+(\.[a-z][a-z0-9]*)+$',

    # 13. shell flag / cli arg
    r'^--?[a-z][a-z0-9-]*$',

    # 14. 颜色
    r'^#[0-9a-fA-F]{3,8}$',
    r'^rgba?\(',
    r'^hsla?\(',

    # 15. ANSI / 控制序列
    r'^\x1b\[',
    r'\\x[0-9a-fA-F]{2}',
]
```

**长度兜底**：长度 < 2（去除空格后）→ 非 UI；长度 > 1024 → 非 UI（很可能是 prompt / template / 嵌入文档）。

---

## (c) UI 调用模式白名单（强 UI 信号，权重 +5，可覆盖正则黑名单除非调用点本身处于黑名单目录）

通过实测 grep（详见末尾"采样证据"），归纳出以下父节点 → 子字面量为 UI 的模式：

### 方法调用 (`receiver.METHOD("...")`)

```
.label(...)            .with_label(...)
.tool_tip(...)         .with_tooltip(...)        .set_tooltip(...)
.placeholder(...)      .with_placeholder(...)
.title(...)            .with_title(...)
.subtitle(...)         .with_subtitle(...)
.description(...)      .with_description(...)
.message(...)          .with_message(...)
.text(...)             .with_text(...)
.with_text_label(...)  .with_text_and_icon_label(...)
.span(...)             .with_span(...)         // ui_builder.span("Copyright 2026 Warp")
.heading(...)
.body(...)
.cta(...)              .with_cta_label(...)
.confirm_label(...)    .cancel_label(...)
.button_label(...)
.error_text(...)       .empty_text(...)
.aria_label(...)
.search_terms()        // 返回值类型；声明体内字面量是 UI 搜索词
```

### 关联函数构造器（强 UI）

```
SettingActionPair::new("Show X", "Hide X", ...)
ToggleSettingActionPair::new("AI", action, context, flag)
SettingActionPairDescriptions::new(...)
MenuItem::Custom(CustomMenuItem::new("New Window", ...))   // 第 1 参数
CustomMenuItem::new_with_submenu("Preferences", ...)
Dialog::new("Download Warp Desktop?".to_string(), ...)     // 第 1 参数
Span::new("Don't show again.", style)                      // 第 1 参数
BindingDescription::new("Toggle project explorer")
Tooltip::new(...)
Notification::new(title, body, ...)                        // 前 2 参数
Banner::new(...)
```

### Trait 实现签名（声明本身就是 UI 文本契约）

```rust
fn ui_name() -> &'static str { "AboutPage" }                // 注意：CSS/标识符意义，不译
fn search_terms(&self) -> &str { "about warp version" }     // **这是 UI 搜索词，要译**
fn label(&self) -> &str { ... }
fn title(&self) -> &str { ... }
fn description(&self) -> &str { ... }
fn command_palette_description(&self) -> &'static str { ... }
fn ui_label(&self) -> String { ... }
```

**注意 `ui_name()` 反例**：`"AboutPage"` 是组件类型名/分析事件 key，**不译**；用正则 `^[A-Z][A-Za-z0-9]*$` 命中黑名单。这印证了"调用点白名单不能裸覆盖所有黑名单正则；要分级"。

### 字段构造（`StructLit { field: "..." }`）

字段名属于以下集合时其字符串值为 UI：

```
{ title, subtitle, description, label, message, body, heading,
  placeholder, tooltip, hint, summary, cta, confirm_text, cancel_text,
  empty_text, error_text, search_terms, ui_label, button_label,
  primary_label, secondary_label }
```

### 关键观察 — 灰区：常量字符串 (`const X: &str = "..."`)

Warp 大量使用：
```rust
const ENABLE_SHELL_DEBUG_MODE_MENU_ITEM_NAME: &str = "Enable Shell Debug Mode (-x) for New Sessions";
const SETTINGS_CSV_FILE_NAME: &str = "warp_default_settings.csv";  // 非 UI
```
判定规则：**常量名后缀**决定，比如：
- 后缀 `_NAME` / `_LABEL` / `_TITLE` / `_DESCRIPTION` / `_TEXT` / `_MESSAGE` / `_PLACEHOLDER` / `_TOOLTIP` / `_HEADING` / `_CTA` / `_BANNER` / `_PROMPT` (UI prompt) → UI
- 后缀 `_FILE_NAME` / `_PATH` / `_URL` / `_KEY` / `_ID` / `_FLAG` / `_EVENT` → 非 UI
- 字符串内容再走正则黑名单复核

### 反向白名单（强 NON-UI，权重 -5）

调用点出现在以下，无论字符串内容如何，都不译：

#### 宏调用（详见 §d）

#### 普通函数调用

```
ctx.dispatch_global_action("workspace:save_app", &())     // 第 1 参 = action id
ctx.dispatch_typed_action(...)
Keystroke::parse("cmd-n")                                  // 按键定义
parse_*("...") / from_str("...")
include_str!("...") / include_bytes!("...")               // 路径
PathBuf::from("..."), Path::new("..."), File::open(...)    // 路径
env::var("..."), std::env::set_var(...)                   // 环境变量名
Url::parse("...")
Regex::new("...")                                          // 正则
serde_json::from_str / to_string
json!({"...": ...})
HashMap::from([("up", ...), ...])                          // 静态查表 (按键映射)
```

#### 字段写入

```
event_name: "...", id: "...", key: "...", action: "...",
schema: "...", path: "..."
```

---

## (d) 排除宏列表（宏内字面量直接判定为非 UI，权重 -5）

完整清单，按命中频率：

```
// 日志 / tracing
tracing::trace!         tracing::debug!     tracing::info!
tracing::warn!          tracing::error!     tracing::event!
tracing::span!          tracing::instrument
log::trace!             log::debug!         log::info!
log::warn!              log::error!
slog::*!

// 调试输出
println!  eprintln!  print!  eprint!
dbg!      todo!      unimplemented!  unreachable!
panic!    debug_panic!

// 断言
assert!  assert_eq!  assert_ne!
debug_assert!  debug_assert_eq!  debug_assert_ne!
static_assert*!

// 错误格式化（默认非 UI；上层若包装为 toast 再二次判定）
anyhow!  bail!  ensure!  thiserror::Error 派生
format!  // 仅看格式串本身常含 {}, 通常通过其他启发式过滤

// 编译期文件加载
include_str!  include_bytes!  concat!  env!  option_env!
file!  line!  module_path!  cfg!

// 测试
#[test]  #[cfg(test)]  #[tokio::test]  #[rstest]
mod tests { ... }

// telemetry / metrics
metric!  counter!  histogram!  gauge!
telemetry::record!  send_event!

// SQL/JSON 字面
sql!  query!  query_as!  json!  serde_json::json!

// GraphQL
graphql_query!  cynic::QueryFragment

// 嵌入式资源（含路径）
asset!  asset_path!  embed!

// CLI/clap
clap::*  Parser/Args 派生（短/长 flag、help 文本本是 UI 但 CLI 范围已被排除）

// 标识符 / 命名空间
sel!  // objc selector
msg_send!
```

特殊：`format!("text {var}")` 出现在 UI 上下文（嵌套于 `.label(...)` 内层）时仍要译；判定时把宏调用展开成"字面量片段 + 占位符"，对每个片段单独走完整流程。

---

## (e) 评分 / 决策算法草案

```python
def classify_lit(lit: LitStr, ctx: Context) -> Verdict:
    """
    返回 {"ui", "not_ui", "uncertain"} 三态。
    Verdict 同时携带 score, reasons[]，写入翻译表的 audit 列。
    """
    score = 0
    reasons = []

    # ---- Step 1: 路径优先 ----
    if ctx.file_in_blacklist():
        return Verdict("not_ui", -5, ["path_blacklist"])
    if ctx.file_in_whitelist():
        score += 3
        reasons.append("path_whitelist")
    # 灰名单不加分

    # ---- Step 2: AST 父节点：黑名单宏 / 反向函数 ----
    parent_macro = ctx.enclosing_macro()
    if parent_macro in EXCLUDED_MACROS:           # tracing::*, println!, assert!*, format! (顶层), include_str!...
        return Verdict("not_ui", score - 5, ["excluded_macro:" + parent_macro])

    parent_call = ctx.enclosing_call()             # MethodCall or Call expression
    if parent_call.is_anti_ui():                   # dispatch_global_action, Keystroke::parse, Regex::new, ...
        return Verdict("not_ui", score - 5, ["anti_ui_call:" + parent_call.name])

    # ---- Step 3: AST 父节点：UI 调用白名单 ----
    if parent_call.matches(UI_METHODS):           # .label / .tooltip / .placeholder / .title / ...
        score += 5
        reasons.append("ui_method:" + parent_call.method)
    if parent_call.matches(UI_CONSTRUCTORS):      # MenuItem::new[1], Dialog::new[1], BindingDescription::new[1], ...
        score += 5
        reasons.append("ui_ctor:" + parent_call.path)
    if ctx.enclosing_struct_field() in UI_FIELDS:
        score += 4
        reasons.append("ui_field:" + ctx.enclosing_struct_field())

    # ---- Step 4: const/static 命名 ----
    if ctx.is_const_static():
        suffix = ctx.const_name_suffix()
        if suffix in UI_CONST_SUFFIX:             # _NAME, _LABEL, _TITLE, _MESSAGE, _PLACEHOLDER, _TOOLTIP, _CTA
            score += 3
        if suffix in NON_UI_CONST_SUFFIX:         # _PATH, _URL, _KEY, _ID, _EVENT, _FLAG
            score -= 3

    # ---- Step 5: 测试上下文 ----
    if ctx.in_test_module() or ctx.in_test_fn():  # mod tests / #[cfg(test)] / #[test]
        return Verdict("not_ui", score - 5, ["in_test"])

    # ---- Step 6: 内容形态正则 ----
    s = lit.value
    if len(s.strip()) < 2 or len(s) > 1024:
        return Verdict("not_ui", score - 4, ["length_extremum"])
    for rx in NON_UI_REGEX:
        if rx.match(s):
            # 调用点强 UI 时仅扣 2，否则直接判 not_ui
            if score >= 5:
                score -= 2
                reasons.append("regex_warning:" + rx.pattern)
            else:
                return Verdict("not_ui", score - 3, ["regex:" + rx.pattern])

    # ---- Step 7: 内容启发：是否含空格 + 大小写混用 + 标点（典型自然语言句子）----
    if has_sentence_shape(s):                      # 含空格 + 含小写字母 + 不全大写 + 不是 path-like
        score += 2
        reasons.append("sentence_shape")
    if has_terminal_punct(s):                      # 以 . ? ! : … 结尾
        score += 1
        reasons.append("terminal_punct")
    if starts_with_capital_word(s) and word_count(s) >= 2:
        score += 1
        reasons.append("title_case_phrase")

    # ---- Step 8: 决策 ----
    if score >= 6:
        return Verdict("ui", score, reasons)
    if score >= 3:
        return Verdict("uncertain", score, reasons)   # 进入人工审核队列
    return Verdict("not_ui", score, reasons)
```

### 阈值策略

- score ≥ 6 → 自动加入翻译表 `decision=auto_ui`
- 3 ≤ score < 6 → 加入翻译表 `decision=needs_review`，缺省不译，等待人工标注
- score < 3 → 不加入翻译表
- 任意阶段 hard return → 不加入翻译表，但日志保留 reason 便于回查

### 翻译表 schema 建议

```
file, line, col, raw_string, score, reasons, decision[auto_ui|needs_review|skip|forced_ui|forced_skip],
context_callee, context_macro, source_kind[const|literal|attr],
zh_translation, translator_note
```

`forced_ui` / `forced_skip` 是人工覆盖位，确保算法升级不会丢失已审核的判定。

---

## (f) 属性/注释标记策略

源码不可改的前提下：

1. **不要求开发者改源码**。所有覆盖位放翻译表 `decision` 列。
2. 如果未来需要增量翻译（patch upstream merges），可在 fork 中允许增量地写：
   ```rust
   // i18n: ui     - 强制译
   // i18n: skip   - 强制不译
   // i18n: ui-ref - 引用别处已译条目
   ```
   提取器在该字面量所在行 / 上一行扫描这些注释做覆盖。零运行时影响。
3. 不引入 `#[ui_string]` 派生属性（需要源码侵入 + 自定义 macro 编译）。

---

## (g) 外部参考（启发式来源）

| 工具 | 启发式 | 借鉴点 |
|---|---|---|
| **xtr** (Rust → POT) | 仅识别 `tr!()` / `tr_n!()` / `gettext()` 等显式宏，**不做内容启发** | 反例：纯白名单宏在我们场景太严苛（无 i18n 框架，没有标记） |
| **cargo-i18n / tr-rs** | 同上，依赖 `tr!` 宏标记 | — |
| **gettext-rs** | 显式 `gettext("...")` | — |
| **i18next-parser** (前端) | 解析 `t("...")`、`<Trans>...</Trans>`；可配置 `keepSeparator`, `pluralSeparator`，支持 keyAsDefaultValue。**有 functions 数组**：`['t', 'i18next.t']`，AST 父函数白名单 | 直接借鉴：UI 方法白名单 |
| **lingui-extract** | macro 化 `t``...``` 模板字面量；CI 提取 | 标记型方案，不适用 |
| **fluent-rs** | 运行时 FTL 文件，提取依赖工具 | 不直接适用 |
| **Mozilla pontoon / l10n** | 大量手工标注 + AST `data-l10n-id` | 与本项目相反思路 |
| **学术：Strudel (UI string detection via static analysis, 2018)**, **DroidLingual (Android)** | 用类型流：字符串 → 是否 sink 进 `setText()` / `Toast.makeText()` | 直接对应到我们的 "UI methods white list" |
| **GitHub `oxc-project/oxlint` / `eslint-plugin-i18n-text`** | 警告任何裸字符串字面量出现在 JSX 文本节点中 | 在 Rust 等价：警告 UI 调用白名单内的非 i18n 字面量 |

---

## (h) 采样证据（节选自 grep 实测）

```
# 强 UI 调用样例
app/src/settings_view/about_page.rs:78        ui_builder.span(version.to_string())
app/src/settings_view/about_page.rs:121       ui_builder.span("Copyright 2026 Warp")
app/src/settings_view/show_blocks_view.rs:309 .label("You don't have any shared blocks yet.")
app/src/settings_view/show_blocks_view.rs:316 .label("Failed to load blocks. Please try again.")
app/src/settings_view/show_blocks_view.rs:663 .label("Unshare block")
app/src/settings_view/appearance_page.rs:3978 .label("Font weight".to_string())
app/src/input_suggestions.rs:888              .tool_tip("Ignore this suggestion".to_string())
app/src/workspace/view/right_panel.rs:402     .with_tooltip("Maximize")
app/src/auth/needs_sso_link_view.rs:57        .with_text_label("Link SSO".to_string())
app/src/workspace/native_modal.rs:140         Span::new("Don't show again.", Default::default())
app/src/wasm_nux_dialog.rs:168                Dialog::new("Download Warp Desktop?".to_string(), ...)
app/src/app_menus.rs:84                       CustomMenuItem::new("New Window", ...)
app/src/app_menus.rs:169                      CustomMenuItem::new_with_submenu("Preferences", ...)
app/src/app_menus.rs:190                      link_menu_item("Privacy Policy...", links::PRIVACY_POLICY_URL.into())
app/src/app_menus.rs:42                       const ENABLE_SHELL_DEBUG_MODE_MENU_ITEM_NAME: &str = "Enable Shell Debug Mode (-x) for New Sessions"
app/src/settings_view/ai_page.rs:171          ToggleSettingActionPair::new("AI", builder(...), ...)
app/src/settings_view/ai_page.rs:182          ToggleSettingActionPair::new("Active AI", ...)
app/src/settings_view/ai_page.rs:194-196      "terminal command autodetection in agent input" / "natural language detection"
app/src/workspace/mod.rs:466                  BindingDescription::new("Toggle project explorer")
app/src/workspace/mod.rs:606-665              BindingDescription::new("Create a new team notebook" ...)
app/src/settings_view/about_page.rs:57        fn search_terms(&self) -> &str { "about warp version" }

# 反例：调用点明显 UI 但内容是标识符（要走正则黑名单否决）
app/src/settings_view/about_page.rs:39        fn ui_name() -> &'static str { "AboutPage" }    // CSS/component name
app/src/app_menus.rs:87                       ctx.dispatch_global_action("root_view:open_new", &())
app/src/app_menus.rs:91                       Keystroke::parse("cmd-n")
app/src/settings_view/about_page.rs:69-72     "bundled/svg/warp-logo-with-light-title.svg" // 路径
app/src/settings_view/about_page.rs:75        "v#.##.###" // 版本占位

# 强非 UI 宏调用
app/src/settings_view/keybindings.rs:676      log::error!("Modifying row should exist");
app/src/settings_view/teams_page.rs:980       log::error!("Failed to fetch discoverable teams: {e:?}");
app/src/settings_view/settings_page.rs:90     log::info!("No updates for the selected view handle.");
```

---

## Caveats / Not Found

- **错误消息边界模糊**：`log::error!("Failed to load blocks")` 不译，但同样文案在 `.label("Failed to load blocks. Please try again.")` 出现时是 UI（user-visible toast/banner）。算法靠调用点正确区分，但具体是否暴露给用户需开发者审核 → 默认 `decision=needs_review`。
- **`format!()` 的处理**：`format!("Hello, {}", name)` 上下文若是 `.label(format!(...))` 则需译；若直接 `tracing::info!(format!(...))` 则不译。算法须递归到外层调用 / 宏。
- **assoc fn 的位置敏感性**：`Dialog::new(title, body, styles)` 仅前两个参数可能是 UI；其他构造器需要参数索引白名单。建议为每个构造器手工写参数 mask（如 `MenuItem::Custom(CustomMenuItem::new(label@1, fn, fn, opt))`），第一次扫描后导出未知构造器列表给开发者补全。
- **AI prompt 文件**：`crates/ai/`、`app/src/ai/`、`OZ_SYSTEM_PROMPT.md` 默认全部黑名单。若有人想译"AI 设置页里展示的 prompt 模板字段"，仍能通过 `app/src/settings_view/ai_page.rs` 白名单单独命中。
- **`about.toml` / `about.hbs`** 是模板文件，需要单独的 handlebars/toml 提取器，不在本研究范围。
- **未实地验证**：`crates/ui_components/src/` 内部默认 placeholder 是否自动出现在 UI（取决于 wrapper 是否传入用户文案）。建议初版按 `路径=灰名单 + 调用点+1` 处理，再根据实际命中量调整。
- **跨 crate 的方法名冲突**：`label()` 在很多 trait 上有定义（`enum BillingUsageTab { fn label() }` 也是 UI，但 `LabelExt::label()` 也可能是数据访问）。算法要降级处理：仅当方法签名返回 `String` / `&str` / `Cow<str>` / `Span` 等显示类型时加分。需要 syn + 类型推断或先静态收集已知 UI trait 列表。
