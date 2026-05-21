#!/usr/bin/env python3
"""Apply 32 privacy_page.rs (+ auth_view_shared_helpers.rs) auto_ui translations
and privacy-domain glossary additions."""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-privacy-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

EXCLUDED = "01KQXQV12JH96FDFWJWAJSESV0"  # "secret redaction" search-keyword tag

TRANSLATIONS = {
    # ---- Secret redaction (privacy_page.rs) ----
    # L76 SAFE_MODE_TITLE
    "01KQXQV12F99311QNESCQ8JEPH": "保密信息脱敏",
    # L77-82 SAFE_MODE_DESCRIPTION
    "01KQXQV12HH9QW56Y0YKYQ5T3Y": (
        "启用此设置后，Warp 将扫描命令块、Warp Drive 对象内容以及 Oz prompts，"
        "查找潜在的敏感信息，并阻止将这些数据保存或发送至任何服务器。"
        "您可以通过 regex 自定义该列表。"
    ),
    # L83 USER_SECRET_REGEX_TITLE
    "01KQXQV12AXR3MQJC8RMQJ2FSN": "自定义保密信息脱敏",
    # L84-87 USER_SECRET_REGEX_DESCRIPTION
    "01KQXQV12HX9Y5NRVF21WX6D0G": (
        "使用 regex 定义您希望脱敏的其他保密信息或数据。"
        "下一条命令运行时即生效。"
        "您可以在 regex 前缀加上内联标记 (?i)，使其不区分大小写。"
    ),
    # L171 modal title "Add regex pattern"
    "01KQXQV129D7Z6CYPM93BF9QS0": "添加 regex 模式",
    # privacy/add_regex_modal.rs:220 "Add regex"
    "01KQXQV129GEHDT94T7DC8DRBJ": "添加 regex",
    # L1031 "Add all"
    "01KQXQV129HYTGFHNBNYFQSBMJ": "全部添加",
    # L802 "Enterprise secret redaction cannot be modified."
    "01KQXQV12BQWMSKFKV1BQTJXWH": "企业保密信息脱敏无法修改。",
    # L921 "No enterprise regexes have been configured by your organization."
    "01KQXQV12D1X17TFA7Q3GXFQZF": "您所在的组织尚未配置任何企业 regex。",
    # L1197 "Enabled by your organization."
    "01KQXQV12BK6JY8NPWNKE4GG91": "已由您所在的组织启用。",
    # L1250 "Secret visual redaction mode"
    "01KQXQV12FXRZBEYKY83Q7WNJA": "保密信息显示模式",
    # L1264 long description for secret display mode
    "01KQXQV1291AV34E36MH47VD6B": (
        "选择保密信息在命令块列表中的展示方式，同时保持其可搜索。"
        "此设置仅影响您在命令块列表中看到的内容。"
    ),

    # ---- App analytics / telemetry ----
    # auth_view_shared_helpers.rs:459 "Help improve Warp"
    "01KQXQV12CA2P3PP47DGM9TP59": "帮助改进 Warp",
    # privacy_page.rs:89 TELEMETRY_DESCRIPTION_OLD
    "01KQXQV1296NP48AQ3B4K7Z1JY": (
        "App 使用分析能帮助我们为您打造更好的产品。"
        "我们只收集 App 使用元数据，从不收集命令行输入或输出。"
    ),
    # privacy_page.rs:93 TELEMETRY_DESCRIPTION (new)
    "01KQXQV12915JH7EHNT3RKZF62": (
        "App 使用分析能帮助我们为您打造更好的产品。"
        "我们可能会收集特定的命令行交互，用于改进 Warp 的 AI 能力。"
    ),
    # privacy_page.rs:96 TELEMETRY_FREE_TIER_NOTE
    "01KQXQV12DRQA85P26SV3Q8SV0": "在免费套餐下，必须启用使用分析才能使用 AI 功能。",
    # L1524 "This setting is managed by your organization."
    "01KQXQV12G8KKV4FBTQP2C59TW": "此设置由您所在的组织管理。",
    # L1583 link text
    "01KQXQV12EG6VTTHRAAHWYQ0Z8": "了解更多关于 Warp 数据使用的信息",
    # L1413 zero data retention tooltip
    "01KQXQV12JM8MHRVXDQZ9D9PTG": (
        "您的管理员已为团队启用零数据保留。"
        "用户生成的内容将永不被收集。"
    ),

    # ---- Crash reports ----
    # auth_view_shared_helpers.rs:504 toggle label
    "01KQXQV12FRY5RQZVZ4P5990CH": "发送崩溃报告",
    # L1652 description
    "01KQXQV12AT1H3ASX4YB57A21K": "崩溃报告有助于调试与稳定性改进。",

    # ---- Cloud conversation storage (Agent) ----
    # auth_view_shared_helpers.rs:534 toggle label
    "01KQXQV12GGSK1K2SYR7796HJ0": "将 AI 会话存储到云端",
    # auth_view_shared_helpers.rs:557 description (when enabled)
    "01KQXQV129CHT8XAP12EXDDGS4": (
        "Agent 会话可与他人共享，并在您在其他设备登录时保留。"
        "此数据仅用于产品功能，Warp 不会将其用于使用分析。"
    ),
    # auth_view_shared_helpers.rs:559 description (when disabled)
    "01KQXQV12944328J8P1GHQ563V": (
        "Agent 会话仅存储在您本机，登出后即丢失，且无法共享。"
        "注意：ambient agent 的会话数据仍存储在云端。"
    ),

    # ---- Network log console ----
    # L1811 "Network log console"
    "01KQXQV12DR1RPQAJZDKGZB1W1": "网络日志控制台",
    # L1823 description
    "01KQXQV12HJQ3FXJZCPQSP3334": (
        "我们构建了一个原生控制台，您可以查看 Warp 与外部服务器之间的所有通信，"
        "确保您可以放心，您的工作始终安全无虞。"
    ),
    # L1849 link "View network logging"
    "01KQXQV12H96CWR8Z6TV01KRF3": "查看网络日志",

    # ---- Data management ----
    # L100 "Manage your data"
    "01KQXQV12DG0PDXATD3S4XCGM9": "管理您的数据",
    # L102 description
    "01KQXQV129887F3VZHZPNS15V0": (
        "您可以随时选择永久删除您的 Warp 账户。"
        "此后您将无法继续使用 Warp。"
    ),
    # L104 link text
    "01KQXQV12H1FV1DXSCK066QQ01": "前往数据管理页面",

    # ---- Privacy policy ----
    # L106 section title
    "01KQXQV12ESE67ZH46BYYTYRQ5": "隐私政策",
    # L107 link text
    "01KQXQV12EEMC11E4Q9GCFCMNG": "阅读 Warp 的隐私政策",
}

NEW_GLOSSARY_TERMS = {
    "secret_redaction": {
        "en": "secret redaction",
        "zh": "保密信息脱敏",
        "notes": "Privacy 设置中的敏感信息扫描与遮蔽功能。'Secret redaction' → '保密信息脱敏'；'Custom secret redaction' → '自定义保密信息脱敏'；'Enterprise secret redaction' → '企业保密信息脱敏'；'Secret visual redaction mode' → '保密信息显示模式'。secret 不译为 '秘密'，避免与日常含义混淆；redaction 取 '脱敏' 以贴近数据保护术语。",
        "do_not_translate": False,
    },
    "regex": {
        "en": "regex",
        "zh": "regex",
        "notes": "正则表达式术语在 UI/技术语境中保留英文 'regex'。'Add regex' → '添加 regex'；'Add regex pattern' → '添加 regex 模式'；'enterprise regexes' → '企业 regex'。开发者更熟悉英文短形式，避免 '正则' 与 '正则表达式' 译名摇摆。",
        "do_not_translate": False,
    },
    "telemetry": {
        "en": "telemetry",
        "zh": "使用分析",
        "notes": "Privacy 设置中的产品使用数据收集功能。'App analytics' / 'usage analytics' → 'App 使用分析' / '使用分析'。避免 '遥测'（过于技术化）与 '统计'（语义过宽）。'analytics' 与 'telemetry' 在该上下文同义同译。",
        "do_not_translate": False,
    },
    "crash_reports": {
        "en": "crash reports",
        "zh": "崩溃报告",
        "notes": "应用崩溃信息上报功能。'Send crash reports' → '发送崩溃报告'；'crash reporting' 同译。",
        "do_not_translate": False,
    },
    "zero_data_retention": {
        "en": "zero data retention",
        "zh": "零数据保留",
        "notes": "企业级隐私选项 (ZDR)：用户生成内容不被收集存储。'zero data retention' → '零数据保留'；徽章 'ZDR' 保留英文缩写。",
        "do_not_translate": False,
    },
    "data_management": {
        "en": "data management",
        "zh": "数据管理",
        "notes": "账户级数据管理页与入口。'Manage your data' → '管理您的数据'；'data management page' → '数据管理页面'。",
        "do_not_translate": False,
    },
    "privacy_policy": {
        "en": "privacy policy",
        "zh": "隐私政策",
        "notes": "法律文档名。'Privacy policy' → '隐私政策'；'Read Warp's privacy policy' → '阅读 Warp 的隐私政策'。",
        "do_not_translate": False,
    },
}


def check_invariants():
    """Pre-flight: enforce full-width punctuation invariant and placeholder integrity."""
    # Allow half-width punctuation only inside regex/URL/code-literal contexts
    # — for the privacy batch, the only legit half-width chars are: "(?i)" (regex inline flag),
    # ASCII ".rs" file extensions in notes, ULIDs, and ASCII identifiers.
    forbidden = re.compile(r"[一-鿿][,.!?:](?![\w/])")
    problems = []
    for eid, target in TRANSLATIONS.items():
        # Check half-width sentence punctuation adjacent to Chinese text
        for m in forbidden.finditer(target):
            problems.append((eid, m.group(0), m.start()))
    if problems:
        print("ERROR: half-width punctuation adjacent to Chinese characters:")
        for eid, frag, pos in problems:
            print(f"  {eid} at pos {pos}: {frag!r}")
        sys.exit(1)


def main():
    check_invariants()

    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"
    assert EXCLUDED not in TRANSLATIONS, f"Excluded ID {EXCLUDED} must not be in TRANSLATIONS"
    assert len(TRANSLATIONS) == 32, f"Expected 32 entries, got {len(TRANSLATIONS)}"

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

    stats = data.get("stats") or {}
    status_counts = {"new": 0, "translated": 0, "fuzzy": 0, "obsolete": 0}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    stats.update({
        "entry_count": len(entries),
        "translated": status_counts["translated"],
        "fuzzy": status_counts["fuzzy"],
        "new": status_counts["new"],
        "obsolete": status_counts.get("obsolete", 0),
    })
    data["stats"] = stats

    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {updated} entries in strings.json")
    print(f"New stats: {stats}")

    g = json.loads(GLOSSARY.read_text())
    added = 0
    for k, v in NEW_GLOSSARY_TERMS.items():
        if k not in g["terms"]:
            g["terms"][k] = v
            added += 1
    g["metadata"]["term_count"] = len(g["terms"])
    GLOSSARY.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} glossary terms (total: {g['metadata']['term_count']})")


if __name__ == "__main__":
    main()
