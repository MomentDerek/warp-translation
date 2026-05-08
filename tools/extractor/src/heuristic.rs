//! UI string heuristic — score every extracted literal and decide whether
//! it belongs in the translation table.
//!
//! Algorithm follows `research/ui-string-heuristics.md`:
//!   1. Path white/blacklist (+3 / −5)
//!   2. Length bounds (< 2 or > 1024 → not_ui)
//!   3. Test context (−5)
//!   4. Anti-UI macro / call (−5, hard cut)
//!   5. UI method / constructor / struct field (+5 / +4)
//!   6. const/static name suffix (+3 / −3)
//!   7. Content regex blacklist (15 categories)
//!   8. Sentence-shape bonuses (small +1/+2)
//!   9. Threshold: ≥6 → auto_ui, 3..=5 → uncertain, <3 → not_ui

use once_cell::sync::Lazy;
use regex::Regex;
use serde::{Deserialize, Serialize};

use crate::model::RawString;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Verdict {
    AutoUi,
    Uncertain,
    NotUi,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Audit {
    pub score: i32,
    pub verdict: Verdict,
    pub reasons: Vec<Reason>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Reason {
    pub code: String,
    pub delta: i32,
}

impl Reason {
    fn new(code: impl Into<String>, delta: i32) -> Self {
        Self {
            code: code.into(),
            delta,
        }
    }
}

/// Path whitelist (relative to source root). Match by prefix.
const PATH_WHITELIST: &[&str] = &[
    "app/src/settings_view/",
    "app/src/app_menus.rs",
    "app/src/menu.rs",
    "app/src/command_palette.rs",
    "app/src/search/command_palette/",
    "app/src/wasm_nux_dialog.rs",
    "app/src/banner/",
    "app/src/notification.rs",
    "app/src/quit_warning/",
    "app/src/workspace/close_session_confirmation_dialog.rs",
    "app/src/workspace/rewind_confirmation_dialog.rs",
    "app/src/workspace/delete_conversation_confirmation_dialog.rs",
    "app/src/workspace/native_modal.rs",
    "app/src/cloud_object/grab_edit_access_modal.rs",
    "app/src/auth/needs_sso_link_view.rs",
    "app/src/resource_center/",
    "app/src/tips/",
    "app/src/ui_components/",
    "crates/ui_components/src/",
    "crates/warpui/src/platform/mac/menus.rs",
];

/// Path blacklist — the entries below are *strong* non-UI hints. Any literal
/// inside such a file is rejected outright.
const PATH_BLACKLIST: &[&str] = &[
    "tests/",
    "test_util/",
    "integration_testing/",
    "build.rs",
    "crates/warp_cli/",
    "crates/simple_logger/",
    "crates/jsonrpc/",
    "crates/ipc/",
    "crates/graphql/",
    "crates/lsp/",
    "crates/firebase/",
    "crates/persistence/",
    "crates/virtual_fs/",
    "crates/string-offset/",
    "crates/sum_tree/",
    "crates/syntax_tree/",
    "crates/integration/",
    "app/src/ai/agent_sdk/",
    "app/src/ai/agent_events/",
    "app/src/ai/agent_management/",
    "app/src/server/",
    "app/src/persistence/",
    "app/src/tracing.rs",
    "app/src/profiling.rs",
    "app/src/crash_reporting/",
    "app/src/server/telemetry.rs",
    "app/src/integration_testing/",
    "app/src/test_util/",
    "app/src/keyboard.rs",
    "app/src/keymap.rs",
];

const PATH_BLACKLIST_SUFFIX: &[&str] = &[
    "_test.rs",
    "_tests.rs",
    "/telemetry.rs",
    "/build.rs",
];

const PATH_BLACKLIST_CONTAINS: &[&str] = &[
    "/tests/",
    "/test_",
];

/// UI method names (`.label()`, `.tool_tip()`, `.placeholder()`, ...).
const UI_METHODS: &[&str] = &[
    "label",
    "with_label",
    "tool_tip",
    "tooltip",
    "with_tooltip",
    "set_tooltip",
    "placeholder",
    "with_placeholder",
    "title",
    "with_title",
    "subtitle",
    "with_subtitle",
    "description",
    "with_description",
    "message",
    "with_message",
    "text",
    "with_text",
    "with_text_label",
    "with_text_and_icon_label",
    "span",
    "with_span",
    "heading",
    "body",
    "cta",
    "with_cta_label",
    "confirm_label",
    "cancel_label",
    "button_label",
    "error_text",
    "empty_text",
    "aria_label",
];

/// UI constructor patterns. Tuple = `(callee_substring, allowed_arg_indices)`.
/// `None` allowed_arg_indices = any arg index counts.
const UI_CONSTRUCTORS: &[(&str, &[usize])] = &[
    ("MenuItem::new", &[0]),
    ("CustomMenuItem::new", &[0]),
    ("CustomMenuItem::new_with_submenu", &[0]),
    ("Dialog::new", &[0, 1]),
    ("BindingDescription::new", &[0]),
    ("SettingActionPair::new", &[0, 1]),
    ("ToggleSettingActionPair::new", &[0]),
    ("SettingActionPairDescriptions::new", &[0, 1]),
    ("Span::new", &[0]),
    ("Tooltip::new", &[0]),
    ("Notification::new", &[0, 1]),
    ("Banner::new", &[0]),
];

/// Anti-UI calls — when the literal is the argument of one of these, hard cut.
const ANTI_UI_CALLS: &[&str] = &[
    "dispatch_global_action",
    "dispatch_typed_action",
    "Keystroke::parse",
    "PathBuf::from",
    "Path::new",
    "File::open",
    "Url::parse",
    "Regex::new",
    "env::var",
    "set_var",
    "from_str",
    "include_str",
    "include_bytes",
    "serde_json::from_str",
    "serde_json::to_string",
];

const UI_FIELDS: &[&str] = &[
    "title",
    "subtitle",
    "description",
    "label",
    "message",
    "body",
    "heading",
    "placeholder",
    "tooltip",
    "hint",
    "summary",
    "cta",
    "confirm_text",
    "cancel_text",
    "empty_text",
    "error_text",
    "search_terms",
    "ui_label",
    "button_label",
    "primary_label",
    "secondary_label",
];

const UI_CONST_SUFFIXES: &[&str] = &[
    "_NAME",
    "_LABEL",
    "_TITLE",
    "_DESCRIPTION",
    "_TEXT",
    "_MESSAGE",
    "_PLACEHOLDER",
    "_TOOLTIP",
    "_HEADING",
    "_CTA",
    "_BANNER",
    "_PROMPT",
];

const NON_UI_CONST_SUFFIXES: &[&str] = &[
    "_FILE_NAME",
    "_PATH",
    "_URL",
    "_KEY",
    "_ID",
    "_FLAG",
    "_EVENT",
];

/// Each category is `(code, regex)`. The codes show up in `audit.reasons` so
/// reviewers can grep what fired.
static NON_UI_REGEX: Lazy<Vec<(&'static str, Regex)>> = Lazy::new(|| {
    let raw: &[(&str, &str)] = &[
        // 1. file extension / asset path
        ("regex:file_ext", r"^[A-Za-z0-9_\-./]+\.(svg|png|jpg|jpeg|gif|webp|ico|ttf|otf|woff2?|wasm|json|toml|yaml|yml|hbs|md|txt|csv|sql|db|sqlite|so|dylib|dll|exe)$"),
        ("regex:bundled_path", r"^bundled/.*"),
        ("regex:multi_seg_path", r"^(\.\./|\./|/)?([\w\-.]+/)+[\w\-.]+$"),
        ("regex:env_var", r"^\$?[A-Z_][A-Z0-9_]*$"),
        // 2. URLs
        ("regex:url_scheme", r"^(https?|ftp|ssh|warp|file|mailto|data):"),
        ("regex:proto_url", r"^[a-z]+://"),
        // 3. UUID / hash / base64
        ("regex:uuid", r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"),
        ("regex:long_hex", r"^[0-9a-fA-F]{32,}$"),
        ("regex:base64ish", r"^[A-Za-z0-9+/=]{40,}$"),
        // 4. identifier / action id / event name
        ("regex:colon_ident", r"^[a-z][a-z0-9_]*(:[a-z][a-z0-9_]*)+$"),
        ("regex:snake_case", r"^[a-z][a-z0-9_]*$"),
        ("regex:camel_case", r"^[A-Z][A-Za-z0-9]*$"),
        ("regex:screaming", r"^[A-Z][A-Z0-9_]+$"),
        ("regex:kebab_case", r"^[a-z]+(-[a-z]+)+$"),
        // 5. shortcut keys
        ("regex:keychord", r"^(cmd|ctrl|alt|shift|meta|super|fn)([\-+](cmd|ctrl|alt|shift|meta|super|fn|[a-z0-9]|f\d{1,2}|tab|enter|space|escape|backspace|delete|up|down|left|right))+$"),
        ("regex:fkey", r"^f\d{1,2}$"),
        // 6. format spec / placeholders
        ("regex:format_spec", r"^\{[^}]*\}$"),
        ("regex:printf", r"^%[sdoxbf%]$"),
        // 7. SQL / GraphQL prefix
        ("regex:sql_kw", r"^(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|FROM|WHERE)\b"),
        ("regex:graphql_query", r"^\s*query\s+\w+"),
        ("regex:graphql_mutation", r"^\s*mutation\s+\w+"),
        // 8. MIME
        ("regex:mime", r"^[a-z]+/[a-z0-9.+\-]+$"),
        // 9. punct / whitespace only
        ("regex:punct_only", r"^[\s[:punct:]]+$"),
        // 10. version / numeric
        ("regex:version", r"^v?\d+\.\d+\.\d+(-[\w.]+)?$"),
        ("regex:numeric", r"^\d+(\.\d+)*$"),
        // 11. namespace dot-id (com.foo.bar)
        ("regex:reverse_dns", r"^[a-z]+\.[a-z]+(\.[a-z][a-z0-9]*)+$"),
        // 12. shell flag
        ("regex:cli_flag", r"^--?[a-z][a-z0-9-]*$"),
        // 13. color
        ("regex:hex_color", r"^#[0-9a-fA-F]{3,8}$"),
        ("regex:css_color", r"^(rgba?|hsla?)\("),
        // 14. ANSI / control escapes
        ("regex:ansi", r"^\x1b\["),
        // 15. css class id (single CamelCase already handled). dot-prefixed class
        ("regex:css_classpath", r"^\.[a-zA-Z][\w-]*$"),
    ];
    raw.iter()
        .map(|(c, p)| (*c, Regex::new(p).expect("non-UI regex compiles")))
        .collect()
});

static SENTENCE_HAS_LETTER: Lazy<Regex> = Lazy::new(|| Regex::new(r"[A-Za-z]").unwrap());

pub fn classify(raw: &RawString) -> Audit {
    let mut score = 0i32;
    let mut reasons: Vec<Reason> = Vec::new();

    // ---- Step 1: path white/blacklist ----
    let file = raw.file.as_str();
    if path_in_blacklist(file) {
        return Audit {
            score: -5,
            verdict: Verdict::NotUi,
            reasons: vec![Reason::new("path_blacklist", -5)],
        };
    }
    if path_in_whitelist(file) {
        score += 3;
        reasons.push(Reason::new("path_whitelist", 3));
    }

    // ---- Step 2: length bounds ----
    let trimmed_len = raw.value.trim().chars().count();
    if trimmed_len < 2 {
        return Audit {
            score: score - 4,
            verdict: Verdict::NotUi,
            reasons: vec![Reason::new("length_too_short", -4)],
        };
    }
    if raw.value.len() > 1024 {
        return Audit {
            score: score - 4,
            verdict: Verdict::NotUi,
            reasons: vec![Reason::new("length_too_long", -4)],
        };
    }

    // ---- Step 3: test context ----
    if raw.in_test {
        score -= 5;
        reasons.push(Reason::new("in_test", -5));
        // No early return — overall score will likely fall below 3 and be
        // dropped, but this keeps the audit trail consistent.
    }

    // ---- Step 4: anti-UI macros / calls ----
    if let Some(macro_path) = &raw.macro_path {
        // Macro literals that survived SKIP_MACROS still might be telemetry.
        // Treat any logging-ish macro as anti-UI.
        let last = macro_path.rsplit("::").next().unwrap_or(macro_path.as_str());
        if matches!(
            last,
            "trace" | "debug" | "info" | "warn" | "error" | "log" | "metric" | "telemetry"
        ) {
            score -= 5;
            reasons.push(Reason::new(format!("anti_ui_macro:{last}"), -5));
        }
    }
    if let Some(call) = &raw.parent_call {
        if anti_ui_call_match(call) {
            score -= 5;
            reasons.push(Reason::new(format!("anti_ui_call:{call}"), -5));
        }
    }

    // ---- Step 5: UI method / constructor / struct field ----
    if let Some(call) = &raw.parent_call {
        if let Some(method) = ui_method_match(call) {
            score += 5;
            reasons.push(Reason::new(format!("ui_method:{method}"), 5));
        }
        if let Some(ctor) = ui_constructor_match(call, raw.parent_call_arg_index) {
            score += 5;
            reasons.push(Reason::new(format!("ui_ctor:{ctor}"), 5));
        }
    }
    if let Some(field) = &raw.struct_field {
        if UI_FIELDS.iter().any(|f| f == field) {
            score += 4;
            reasons.push(Reason::new(format!("ui_field:{field}"), 4));
        }
    }

    // ---- Step 6: const/static name suffix ----
    if let Some(name) = &raw.enclosing_const_name {
        if let Some(suf) = match_suffix(name, NON_UI_CONST_SUFFIXES) {
            score -= 3;
            reasons.push(Reason::new(format!("non_ui_const:{suf}"), -3));
        }
        if let Some(suf) = match_suffix(name, UI_CONST_SUFFIXES) {
            // Note: if both match (unlikely, _FILE_NAME shadows _NAME), the
            // non-UI suffix is checked first via longer match below.
            if !is_non_ui_const(name) {
                score += 3;
                reasons.push(Reason::new(format!("ui_const:{suf}"), 3));
            }
        }
    }

    // ---- Step 7: content regex blacklist ----
    let s = raw.value.as_str();
    for (code, rx) in NON_UI_REGEX.iter() {
        if rx.is_match(s) {
            // If a strong UI signal already pushed score ≥ 5, downgrade
            // instead of hard cut (per research §e Step 6).
            if score >= 5 {
                score -= 2;
                reasons.push(Reason::new(format!("{code}:warn"), -2));
            } else {
                score -= 3;
                reasons.push(Reason::new((*code).to_string(), -3));
                return decide(score, reasons);
            }
            break;
        }
    }

    // ---- Step 8: sentence-shape bonuses ----
    if has_sentence_shape(s) {
        score += 2;
        reasons.push(Reason::new("sentence_shape", 2));
    }
    if has_terminal_punct(s) {
        score += 1;
        reasons.push(Reason::new("terminal_punct", 1));
    }
    if title_case_phrase(s) {
        score += 1;
        reasons.push(Reason::new("title_case_phrase", 1));
    }

    decide(score, reasons)
}

fn decide(score: i32, reasons: Vec<Reason>) -> Audit {
    let verdict = if score >= 6 {
        Verdict::AutoUi
    } else if score >= 3 {
        Verdict::Uncertain
    } else {
        Verdict::NotUi
    };
    Audit {
        score,
        verdict,
        reasons,
    }
}

fn path_in_whitelist(path: &str) -> bool {
    PATH_WHITELIST.iter().any(|p| path.starts_with(p) || path == *p)
}

fn path_in_blacklist(path: &str) -> bool {
    if PATH_BLACKLIST.iter().any(|p| path.starts_with(p) || path == *p) {
        return true;
    }
    if PATH_BLACKLIST_SUFFIX.iter().any(|s| path.ends_with(s)) {
        return true;
    }
    if PATH_BLACKLIST_CONTAINS.iter().any(|s| path.contains(s)) {
        return true;
    }
    false
}

fn ui_method_match(callee: &str) -> Option<&'static str> {
    // Method calls are tagged as ".label", ".tool_tip", etc.
    let stripped = callee.strip_prefix('.')?;
    UI_METHODS.iter().copied().find(|m| *m == stripped)
}

fn ui_constructor_match(callee: &str, arg_idx: Option<usize>) -> Option<&'static str> {
    for (sig, allowed) in UI_CONSTRUCTORS {
        if callee.contains(sig) {
            match arg_idx {
                Some(idx) if allowed.contains(&idx) => return Some(*sig),
                None => return Some(*sig),
                _ => continue,
            }
        }
    }
    None
}

fn anti_ui_call_match(callee: &str) -> bool {
    ANTI_UI_CALLS.iter().any(|c| callee.contains(c))
}

fn match_suffix<'a>(name: &str, suffixes: &'a [&'a str]) -> Option<&'a str> {
    // Prefer longest suffix match so `_FILE_NAME` beats `_NAME`.
    suffixes
        .iter()
        .filter(|s| name.ends_with(*s))
        .max_by_key(|s| s.len())
        .copied()
}

fn is_non_ui_const(name: &str) -> bool {
    NON_UI_CONST_SUFFIXES
        .iter()
        .any(|s| name.ends_with(*s))
}

fn has_sentence_shape(s: &str) -> bool {
    s.contains(' ')
        && SENTENCE_HAS_LETTER.is_match(s)
        && !s.chars().all(|c| c.is_ascii_uppercase() || !c.is_alphabetic())
}

fn has_terminal_punct(s: &str) -> bool {
    matches!(
        s.trim_end().chars().last(),
        Some('.') | Some('?') | Some('!') | Some(':') | Some('…')
    )
}

fn title_case_phrase(s: &str) -> bool {
    let words: Vec<&str> = s.split_whitespace().collect();
    if words.len() < 2 {
        return false;
    }
    matches!(words[0].chars().next(), Some(c) if c.is_ascii_uppercase())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::{LitKind, RawString};

    fn raw(file: &str, value: &str) -> RawString {
        RawString {
            file: file.to_string(),
            line: 1,
            column: 0,
            byte_start: 0,
            byte_end: value.len() + 2,
            value: value.to_string(),
            kind: LitKind::Literal,
            macro_path: None,
            parent_call: None,
            parent_call_arg_index: None,
            enclosing_const_name: None,
            in_test: false,
            struct_field: None,
        }
    }

    #[test]
    fn whitelisted_ui_label_scores_high() {
        let mut r = raw("app/src/settings_view/ai_page.rs", "Active AI");
        r.parent_call = Some(".label".to_string());
        r.parent_call_arg_index = Some(0);
        let v = classify(&r);
        assert_eq!(v.verdict, Verdict::AutoUi, "audit={v:?}");
        assert!(v.score >= 6, "score={}", v.score);
    }

    #[test]
    fn snake_case_identifier_is_not_ui() {
        let r = raw("app/src/settings_view/ai_page.rs", "agent_input");
        let v = classify(&r);
        assert_eq!(v.verdict, Verdict::NotUi, "audit={v:?}");
    }

    #[test]
    fn url_in_ui_path_still_not_ui() {
        let r = raw(
            "app/src/settings_view/about_page.rs",
            "https://warp.dev/policy",
        );
        let v = classify(&r);
        assert_eq!(v.verdict, Verdict::NotUi, "audit={v:?}");
    }

    #[test]
    fn blacklisted_path_rejects() {
        let mut r = raw("crates/ipc/src/foo.rs", "Hello world");
        r.parent_call = Some(".label".to_string());
        let v = classify(&r);
        assert_eq!(v.verdict, Verdict::NotUi);
    }

    #[test]
    fn dialog_first_two_args_are_ui() {
        let mut r = raw(
            "app/src/wasm_nux_dialog.rs",
            "Download Warp Desktop?",
        );
        r.parent_call = Some("Dialog::new".to_string());
        r.parent_call_arg_index = Some(0);
        let v = classify(&r);
        assert_eq!(v.verdict, Verdict::AutoUi);
    }

    #[test]
    fn const_with_label_suffix_promotes() {
        let mut r = raw(
            "app/src/app_menus.rs",
            "Enable Shell Debug Mode for New Sessions",
        );
        r.enclosing_const_name = Some("ENABLE_SHELL_DEBUG_LABEL".to_string());
        let v = classify(&r);
        assert!(v.verdict == Verdict::AutoUi || v.verdict == Verdict::Uncertain);
    }

    #[test]
    fn const_path_suffix_demotes() {
        let mut r = raw("app/src/app_menus.rs", "warp_default_settings.csv");
        r.enclosing_const_name = Some("SETTINGS_CSV_FILE_NAME".to_string());
        let v = classify(&r);
        assert_eq!(v.verdict, Verdict::NotUi);
    }
}
