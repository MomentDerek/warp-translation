#!/usr/bin/env python3
"""Apply 29 mcp_servers/{list_page.rs, server_card.rs} auto_ui translations and glossary additions
for the settings-mcp-servers-list-card batch (8th in settings_view series).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-mcp-servers-list-card-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_FILES = {
    "app/src/settings_view/mcp_servers/list_page.rs",
    "app/src/settings_view/mcp_servers/server_card.rs",
}

# 29 entries: status=new + audit.verdict=auto_ui + occurrence in list_page.rs or server_card.rs
TRANSLATIONS = {
    # ============================================================
    # list_page.rs (17 entries)
    # ============================================================
    # L78 long description (note trailing space preserved)
    "01KQXQV128ZMEQG25ZTK98W3AD": "添加 MCP 服务器以扩展 Warp Agent 的能力。MCP 服务器通过标准化接口向 Agent 暴露数据源或工具，本质上类似插件。您可以添加自定义服务器，或使用预设快速接入流行服务器。您也可以在此处找到他人与您共享的团队服务器。 ",
    # L1146 long description (auto-detect; example file path preserved + trailing space)
    "01KQXQV12915TBPC7WFZ07XGH5": "自动从全局范围的第三方 AI agent 配置文件（例如位于您的主目录中）检测并启动 MCP 服务器。仓库内检测到的服务器不会自动启动，必须在下方“检测自”分组中单独启用。 ",
    # L376 group header
    "01KQXQV129HHQTZST3947G59BK": "可供安装",
    # L1304 source label with positional placeholder
    "01KQXQV12A2K7AAFM5SQKWTZ3H": "检测自 {}",
    # L1641 source label
    "01KQXQV12AA95KN0GQ7KVA37Z2": "检测自配置文件",
    # L1779 source label
    "01KQXQV12C4AE65A1WDP4H9XPK": "来自其他设备",
    # L1187 inline "Learn more."
    "01KQXQV12D5Q7KNASDBNZBGD0G": "了解更多。",
    # L844 toast
    "01KQXQV12D82NH18XCSCCK2MQP": "MCP 服务器已更新",
    # L105 empty state
    "01KQXQV12DAJ8C5NZK8CFZDWZN": "未找到搜索结果",
    # L1271 group header
    "01KQXQV12DH5NCS98FXJ8HJMCS": "我的 MCP",
    # L104 empty state
    "01KQXQV12DPG5B6HB3G4WME61T": "添加 MCP 服务器后，将在此处显示。",
    # L1295 source label
    "01KQXQV12F758X1YV9590XNX79": "由 Warp 共享",
    # L1284 source label
    "01KQXQV12F9T3TXEWMCCA4RGSD": "由 Warp 与其他设备共享",
    # L230 search placeholder
    "01KQXQV12FA1S6MSD3VG8VB716": "搜索 MCP 服务器",
    # L1283 source label with named placeholder
    "01KQXQV12FKJQKEF14EE84849S": "由 Warp 与 {name} 共享",
    # L1775 source label with named placeholder
    "01KQXQV12FWTYXGSM6J37Q2035": "共享者：{creator}",
    # L1776 source label
    "01KQXQV12FZAE5X8MCAGTD2WS4": "由团队成员共享",

    # ============================================================
    # server_card.rs (12 entries)
    # ============================================================
    # L641 error
    "01KQXQV12AC7TYPTD4W8E3QNZA": "找不到云端模板",
    # L848 button
    "01KQXQV12B2DYY1425DT93ESPK": "编辑配置",
    # L633 metadata with named placeholder
    "01KQXQV12CGBZVWZ9CG7ZEEJ67": "模板库 ID：{uuid}",
    # L634 metadata "Gallery Id: None"
    "01KQXQV12CRQ4RTZJ7XCT4F6MM": "模板库 ID：无",
    # L494 empty state
    "01KQXQV12D2QTYE03TZ0B11307": "暂无可用工具",
    # L864 button
    "01KQXQV12F1HFAKE26B7C87DFT": "设置",
    # L795 button
    "01KQXQV12FPX4YWB966JRWV7RK": "共享服务器",
    # L912 update notice
    "01KQXQV12FRB41RGNKVAW2TGWH": "服务器有可用更新",
    # L317 toast (... -> ……)
    "01KQXQV12GRH1FP5FYH4MBQK9K": "正在关闭……",
    # L765 button
    "01KQXQV12GXKZB1746HW3BABEG": "显示日志",
    # L257 toast (... -> ……)
    "01KQXQV12GXPE5PH4C18VWTJSS": "正在启动服务器……",
    # L623 metadata with positional placeholder
    "01KQXQV12GZSA9V42Q5JPB50TB": "模板同步 ID：{}",
}

NEW_GLOSSARY_TERMS = {
    "mcp_server": {
        "en": "MCP server",
        "zh": "MCP 服务器",
        "notes": "Model Context Protocol 服务器，作为 Agent 与数据源/工具之间的桥梁。'MCP server' → 'MCP 服务器'；'MCP servers' → 'MCP 服务器'；'Search MCP Servers' → '搜索 MCP 服务器'；'MCP server updated' → 'MCP 服务器已更新'。'MCP' 保留英文，'server' 统一译 '服务器'。",
        "do_not_translate": False,
    },
    "tool": {
        "en": "tool",
        "zh": "工具",
        "notes": "MCP / Agent 上下文中的工具能力。'No tools available' → '暂无可用工具'；'tools' 译 '工具'。区别于通用 '工具栏 / toolbar' 等 UI 用语。",
        "do_not_translate": False,
    },
    "gallery": {
        "en": "Gallery",
        "zh": "模板库",
        "notes": "MCP server 模板库（cloud-hosted gallery of MCP templates）。'Gallery Id' → '模板库 ID'；'Gallery Id: None' → '模板库 ID：无'。沿用 'cloud template / 云端模板' 词族。",
        "do_not_translate": False,
    },
    "template": {
        "en": "template",
        "zh": "模板",
        "notes": "MCP / Workflow 模板。'Template sync id' → '模板同步 ID'；'cloud template' → '云端模板'。",
        "do_not_translate": False,
    },
}


def check_invariants():
    """Enforce full-width punctuation invariant + placeholder integrity."""
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

    for eid, target in TRANSLATIONS.items():
        if "..." in target:
            print(f"ERROR {eid}: bare '...' detected; use '……' instead")
            sys.exit(1)


def check_placeholders(src_entry, target):
    src = src_entry.get("source", "")
    src_phs = re.findall(r"\{[^{}]*\}", src)
    tgt_phs = re.findall(r"\{[^{}]*\}", target)
    if sorted(src_phs) != sorted(tgt_phs):
        return f"placeholder mismatch: source={src_phs} target={tgt_phs}"
    return None


def check_whitespace_preservation(src_entry, target):
    src = src_entry.get("source", "")
    if src.startswith(" ") and not target.startswith(" "):
        return "leading-space lost"
    if src.endswith(" ") and not target.endswith(" "):
        return "trailing-space lost"
    return None


def main():
    check_invariants()

    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"
    assert len(TRANSLATIONS) == 29, f"Expected 29 entries, got {len(TRANSLATIONS)}"

    for eid, target in TRANSLATIONS.items():
        err = check_placeholders(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)
        err = check_whitespace_preservation(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        files = {o.get("file") for o in e.get("occurrences", [])}
        assert files & TARGET_FILES, f"{eid} no mcp_servers occurrence: {files}"
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

    status_counts = {"new": 0, "translated": 0, "fuzzy": 0, "approved": 0, "obsolete": 0, "uncertain": 0}
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

    g = json.loads(GLOSSARY.read_text())
    added = 0
    for k, v in NEW_GLOSSARY_TERMS.items():
        if k not in g["terms"]:
            g["terms"][k] = v
            added += 1
        else:
            print(f"Glossary term '{k}' already exists, skipping")
    g["metadata"]["term_count"] = len(g["terms"])
    GLOSSARY.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} glossary terms (total: {g['metadata']['term_count']})")


if __name__ == "__main__":
    main()
