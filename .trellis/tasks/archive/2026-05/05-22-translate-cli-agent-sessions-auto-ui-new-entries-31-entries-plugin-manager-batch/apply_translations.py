#!/usr/bin/env python3
"""Apply 31 cli_agent_sessions plugin_manager auto_ui translations.

Scope:
  - app/src/terminal/cli_agent_sessions/mod.rs (1)
  - app/src/terminal/cli_agent_sessions/plugin_manager/claude.rs (10)
  - app/src/terminal/cli_agent_sessions/plugin_manager/codex.rs (4)
  - app/src/terminal/cli_agent_sessions/plugin_manager/gemini.rs (5)
  - app/src/terminal/cli_agent_sessions/plugin_manager/mod.rs (4)
  - app/src/terminal/cli_agent_sessions/plugin_manager/opencode.rs (7)

Special handling:
  * {display_cmd} placeholder + surrounding ASCII single quotes preserved.
  * File-path literals preserved verbatim: ~/.codex/config.toml, opencode.json.
  * JSON literals preserved verbatim (with double quotes):
      "always" / "plugin" / "@warp-dot-dev/opencode-warp".
  * Brand literals preserved: Warp / Claude Code / Codex / Gemini CLI / OpenCode / jq.
  * Gemini-specific wording: source uses 'extension' (not 'plugin'); translate
    as '扩展' to match source choice and the new glossary term.
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
CANDIDATES = pathlib.Path(__file__).resolve().parent / "candidates.json"
BATCH_FLAG = "pr-cli-agent-sessions-plugin-manager-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_PREFIXES = (
    "app/src/terminal/cli_agent_sessions/",
)

# Translation map keyed by entry id.
TRANSLATIONS = {
    # ============================================================
    # cli_agent_sessions/mod.rs (1)
    # ============================================================
    # L207
    "01KQXQV12HYG74G91P81QF3ZC6": "等待您的回复",

    # ============================================================
    # plugin_manager/claude.rs (10)
    # ============================================================
    # L117
    "01KQXQV12E59XTZMWNJMMBMMQR": "插件更新未生效",
    # L166
    "01KQXQV12CQ0FNF23JJFN1V9NZ": "为 Claude Code 安装 Warp 插件",
    # L167 — jq literal preserved
    "01KQXQV12B8MM7QMB2X905YC2W": "请确保您的机器上已安装 jq。然后运行以下命令。",
    # L170
    "01KQXQV129FFV60ZGCNSNDAY6M": "添加 Warp 插件市场仓库",
    # L176
    "01KQXQV12C604BA0EWG44TK58H": "安装 Warp 插件",
    # L191
    "01KQXQV12HBW4841JZQVK6RB5S": "为 Claude Code 更新 Warp 插件",
    # L192
    "01KQXQV12FS80SZGBB398NERME": "运行以下命令。",
    # L195
    "01KQXQV12E28NPEM6VVP6KX7Q8": "移除现有插件市场（若存在）",
    # L201
    "01KQXQV12EFN2RF3423Z91AWP9": "重新添加插件市场",
    # L207 (claude.rs)
    "01KQXQV12CZM9SG0KCP7ZQ0Z6W": "安装最新版本的插件",

    # ============================================================
    # plugin_manager/codex.rs (4)
    # ============================================================
    # L34 — Codex literal preserved
    "01KQXQV12BDCN4B1GE3K7XTSJ9": "为 Codex 启用 Warp 通知",
    # L35 — long sentence
    "01KQXQV12HRBYNMB9NCVXEMFH3": "请将 Codex 更新至最新版本，然后启用前台通知，以便 Warp 在您工作时进行展示。",
    # L38
    "01KQXQV12H7A3XM2Z93QSXE2VK": "将 Codex 更新至最新版本。",
    # L44 — "always" and ~/.codex/config.toml literals preserved verbatim (with quotes)
    "01KQXQV12FZKCV68H4ZY5TY3KS": "在您的 Codex 配置中将通知条件设为 \"always\"。打开或创建 ~/.codex/config.toml 并添加：",

    # ============================================================
    # plugin_manager/gemini.rs (5)
    # ============================================================
    # L127 — Gemini CLI literal preserved
    "01KQXQV12CXMCYSD4B5WT54M3T": "为 Gemini CLI 安装 Warp 插件",
    # L128
    "01KQXQV12FVTB8HB8ZQRE5D7AD": "运行以下命令，然后重启 Gemini CLI。",
    # L130 — source uses 'extension' (not plugin); translate as 扩展
    "01KQXQV12CWQ13HKHYJP3YPQT4": "安装 Warp 扩展",
    # L140
    "01KQXQV12HWCA7EZQKNGH9NR49": "为 Gemini CLI 更新 Warp 插件",
    # L143 — source uses 'extension'
    "01KQXQV12HYY33P2VNCCW1RRQH": "更新 Warp 扩展",

    # ============================================================
    # plugin_manager/mod.rs (4)
    # ============================================================
    # L124 — '{display_cmd}' (with single quotes) preserved
    "01KQXQV128Z5122440P1FG89Z2": "'{display_cmd}' 执行失败",
    # L131 — '{display_cmd}' (with single quotes) preserved
    "01KQXQV12JAMSJJSXBAPVT5BZ3": "无法运行 '{display_cmd}'",
    # L167
    "01KQXQV129EZX54YTP1NANQVSX": "此 Agent 不支持自动安装",
    # L176
    "01KQXQV129K0Q1HY8ZGWT5EB2E": "此 Agent 不支持自动更新",

    # ============================================================
    # plugin_manager/opencode.rs (7)
    # ============================================================
    # L36 — OpenCode literal preserved
    "01KQXQV12CGSHC5ZMCCM64WZE8": "为 OpenCode 安装 Warp 插件",
    # L38
    "01KQXQV129P101081EVWKSS4Y9": "将 Warp 插件添加到您的 OpenCode 配置中，然后重启 OpenCode。",
    # L41 — opencode.json literal preserved
    "01KQXQV12EFPWFASWBW6VA524V": "打开或创建您的 opencode.json。它可以位于您的项目根目录，或全局配置路径下：",
    # L47 — "@warp-dot-dev/opencode-warp" + "plugin" JSON literals preserved (with double quotes)
    "01KQXQV128DVVFHJ3Y1GN47B05": "将 \"@warp-dot-dev/opencode-warp\" 添加到顶层 JSON 对象的 \"plugin\" 数组中：",
    # L59
    "01KQXQV12HMGGG6BFRYJYBAFHE": "为 OpenCode 更新 Warp 插件",
    # L60 — long sentence; opencode.json literal preserved
    "01KQXQV12ESZYEXKJXH4E52YRX": "在您的 opencode.json 中将插件固定到最新版本。OpenCode 按版本规格缓存插件，因此修改固定版本会强制其在重启时重新拉取。",
    # L69 — "@warp-dot-dev/opencode-warp" + "plugin" JSON literals preserved
    "01KQXQV12EAFR46CAZAG0Q1FXX": "将 \"plugin\" 数组中现有的 \"@warp-dot-dev/opencode-warp\" 条目替换为显式版本：",
}


def check_invariants():
    """Punctuation + special-literal preservation."""
    # Half-width punct adjacent to CJK — forbidden unless followed by Latin/digit/slash.
    forbidden = re.compile(r"[一-鿿][,.!?:;](?![\w/])")
    problems = []
    for eid, target in TRANSLATIONS.items():
        for m in forbidden.finditer(target):
            problems.append((eid, m.group(0), m.start()))
    if problems:
        print("ERROR: half-width punctuation adjacent to Chinese characters:")
        for eid, frag, pos in problems:
            print(f"  {eid} at pos {pos}: {frag!r}")
        sys.exit(1)

    # No bare ASCII ellipsis "..." anywhere.
    for eid, target in TRANSLATIONS.items():
        if "..." in target:
            print(f"ERROR {eid}: bare '...' detected; use '……' instead")
            sys.exit(1)

    # Lowercase 'agent' as standalone English word — forbidden.
    for eid, target in TRANSLATIONS.items():
        if re.search(r"\bagent\b", target):
            print(f"ERROR {eid}: lowercase 'agent' in target; use 'Agent'. Got {target!r}")
            sys.exit(1)

    # ---- Placeholder + literal assertions ----

    # {display_cmd} with surrounding single quotes preserved on L124 / L131.
    for eid in ("01KQXQV128Z5122440P1FG89Z2", "01KQXQV12JAMSJJSXBAPVT5BZ3"):
        t = TRANSLATIONS[eid]
        if "{display_cmd}" not in t:
            print(f"ERROR {eid}: missing {{display_cmd}} placeholder, got {t!r}")
            sys.exit(1)
        if "'{display_cmd}'" not in t:
            print(f"ERROR {eid}: surrounding ASCII single quotes lost, got {t!r}")
            sys.exit(1)

    # codex.rs L44: "always" + ~/.codex/config.toml literals.
    t = TRANSLATIONS["01KQXQV12FZKCV68H4ZY5TY3KS"]
    if '"always"' not in t:
        print(f'ERROR L44: \'"always"\' literal missing, got {t!r}')
        sys.exit(1)
    if "~/.codex/config.toml" not in t:
        print(f"ERROR L44: '~/.codex/config.toml' literal missing, got {t!r}")
        sys.exit(1)

    # opencode.rs file/JSON literals.
    opencode_json_ids = (
        "01KQXQV12EFPWFASWBW6VA524V",  # L41
        "01KQXQV12ESZYEXKJXH4E52YRX",  # L60
    )
    for eid in opencode_json_ids:
        t = TRANSLATIONS[eid]
        if "opencode.json" not in t:
            print(f"ERROR {eid}: 'opencode.json' literal missing, got {t!r}")
            sys.exit(1)

    pkg_ids = (
        "01KQXQV128DVVFHJ3Y1GN47B05",  # L47
        "01KQXQV12EAFR46CAZAG0Q1FXX",  # L69
    )
    for eid in pkg_ids:
        t = TRANSLATIONS[eid]
        if '"@warp-dot-dev/opencode-warp"' not in t:
            print(f'ERROR {eid}: \'"@warp-dot-dev/opencode-warp"\' literal missing, got {t!r}')
            sys.exit(1)
        if '"plugin"' not in t:
            print(f'ERROR {eid}: \'"plugin"\' JSON key missing, got {t!r}')
            sys.exit(1)

    # jq literal in claude.rs L167.
    t = TRANSLATIONS["01KQXQV12B8MM7QMB2X905YC2W"]
    if "jq" not in t:
        print(f"ERROR L167: 'jq' literal missing, got {t!r}")
        sys.exit(1)

    # Brand-literal sweep.
    brand_checks = [
        ("01KQXQV12CQ0FNF23JJFN1V9NZ", "Claude Code"),  # L166 claude
        ("01KQXQV12CQ0FNF23JJFN1V9NZ", "Warp"),
        ("01KQXQV12HBW4841JZQVK6RB5S", "Claude Code"),  # L191 claude
        ("01KQXQV12HBW4841JZQVK6RB5S", "Warp"),
        ("01KQXQV12BDCN4B1GE3K7XTSJ9", "Codex"),        # L34 codex
        ("01KQXQV12BDCN4B1GE3K7XTSJ9", "Warp"),
        ("01KQXQV12HRBYNMB9NCVXEMFH3", "Codex"),        # L35 codex
        ("01KQXQV12HRBYNMB9NCVXEMFH3", "Warp"),
        ("01KQXQV12H7A3XM2Z93QSXE2VK", "Codex"),        # L38 codex
        ("01KQXQV12FZKCV68H4ZY5TY3KS", "Codex"),        # L44 codex
        ("01KQXQV12CXMCYSD4B5WT54M3T", "Gemini CLI"),   # L127 gemini
        ("01KQXQV12CXMCYSD4B5WT54M3T", "Warp"),
        ("01KQXQV12FVTB8HB8ZQRE5D7AD", "Gemini CLI"),   # L128 gemini
        ("01KQXQV12CWQ13HKHYJP3YPQT4", "Warp"),         # L130 gemini extension
        ("01KQXQV12HWCA7EZQKNGH9NR49", "Gemini CLI"),   # L140 gemini
        ("01KQXQV12HWCA7EZQKNGH9NR49", "Warp"),
        ("01KQXQV12HYY33P2VNCCW1RRQH", "Warp"),         # L143 gemini
        ("01KQXQV12CGSHC5ZMCCM64WZE8", "OpenCode"),     # L36 opencode
        ("01KQXQV12CGSHC5ZMCCM64WZE8", "Warp"),
        ("01KQXQV129P101081EVWKSS4Y9", "OpenCode"),     # L38 opencode
        ("01KQXQV129P101081EVWKSS4Y9", "Warp"),
        ("01KQXQV12HMGGG6BFRYJYBAFHE", "OpenCode"),     # L59 opencode
        ("01KQXQV12HMGGG6BFRYJYBAFHE", "Warp"),
        ("01KQXQV12ESZYEXKJXH4E52YRX", "OpenCode"),     # L60 opencode
        ("01KQXQV129EZX54YTP1NANQVSX", "Agent"),        # L167 mod (Agent capitalized)
        ("01KQXQV129K0Q1HY8ZGWT5EB2E", "Agent"),        # L176 mod
    ]
    for eid, lit in brand_checks:
        t = TRANSLATIONS[eid]
        if lit not in t:
            print(f"ERROR {eid}: brand literal {lit!r} missing, got {t!r}")
            sys.exit(1)

    # Gemini-specific: L130 + L143 must use '扩展', not '插件' (source uses 'extension').
    for eid in ("01KQXQV12CWQ13HKHYJP3YPQT4", "01KQXQV12HYY33P2VNCCW1RRQH"):
        t = TRANSLATIONS[eid]
        if "扩展" not in t:
            print(f"ERROR {eid}: gemini extension entry must use '扩展', got {t!r}")
            sys.exit(1)
        if "插件" in t:
            print(f"ERROR {eid}: gemini extension entry must NOT use '插件', got {t!r}")
            sys.exit(1)


def check_placeholders(src_entry, target):
    src = src_entry.get("source", "")
    src_phs = re.findall(r"\{[^{}]*\}", src)
    tgt_phs = re.findall(r"\{[^{}]*\}", target)
    if sorted(src_phs) != sorted(tgt_phs):
        return f"placeholder mismatch: source={src_phs} target={tgt_phs}"
    return None


def main():
    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    cands = json.loads(CANDIDATES.read_text())
    cand_ids = {c["id"] for c in cands}

    # Coverage sanity.
    assert len(TRANSLATIONS) == 31, f"Expected 31 translations, got {len(TRANSLATIONS)}"
    assert set(TRANSLATIONS.keys()) == cand_ids, (
        "Translation keys do not match candidates.json: "
        f"missing={cand_ids - TRANSLATIONS.keys()}, "
        f"extra={TRANSLATIONS.keys() - cand_ids}"
    )

    check_invariants()

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs in strings.json: {missing}"

    # Pre-mutation snapshot of all existing translated entries.
    pre_snapshot = {
        e["id"]: (e.get("target"), e["status"])
        for e in entries
        if e["status"] == "translated"
    }
    assert len(pre_snapshot) == 1589, f"Expected 1589 prior translated, got {len(pre_snapshot)}"

    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        if e["status"] != "new":
            print(f"ERROR {eid}: expected status=new, got {e['status']}")
            sys.exit(1)
        if e.get("audit", {}).get("verdict") != "auto_ui":
            print(f"ERROR {eid}: expected verdict=auto_ui")
            sys.exit(1)
        files = {o.get("file") for o in e.get("occurrences", [])}
        if not any(f.startswith(p) for f in files for p in TARGET_PREFIXES):
            print(f"ERROR {eid}: occurrences not in target dirs: {files}")
            sys.exit(1)
        err = check_placeholders(e, target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)

    # Apply mutation.
    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

    # Post-mutation: verify pre_snapshot entries are byte-identical.
    for eid, (prev_target, prev_status) in pre_snapshot.items():
        e = by_id[eid]
        if e.get("target") != prev_target or e["status"] != prev_status:
            print(f"ERROR: prior translated entry mutated: {eid}")
            sys.exit(1)

    # Recompute stats.
    status_counts = {"new": 0, "translated": 0, "fuzzy": 0, "approved": 0,
                     "obsolete": 0, "uncertain": 0}
    for e in entries:
        s = e["status"]
        status_counts[s] = status_counts.get(s, 0) + 1
    prior_uncertain = data.get("metadata", {}).get("stats", {}).get("uncertain", 0)
    status_counts["uncertain"] = prior_uncertain

    md = data.setdefault("metadata", {})
    md["entry_count"] = len(entries)
    md["stats"] = status_counts
    md["last_changed_at"] = NOW

    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {updated} entries in strings.json")
    print(f"New stats: {status_counts}")
    print("Glossary delta: +plugin +extension +marketplace +notification (4 new)")


if __name__ == "__main__":
    main()
