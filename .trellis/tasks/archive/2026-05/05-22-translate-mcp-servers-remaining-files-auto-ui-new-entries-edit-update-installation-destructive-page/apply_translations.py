#!/usr/bin/env python3
"""Apply 32 mcp_servers remaining auto_ui translations for the
settings-mcp-servers-remaining batch (closes mcp_servers subdirectory).

Files: edit_page.rs (9) + update_modal.rs (6) + installation_modal.rs (5) +
       destructive_mcp_confirmation_dialog.rs (7) + mcp_servers_page.rs (5).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-mcp-servers-remaining-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_FILES = {
    "app/src/settings_view/mcp_servers/edit_page.rs",
    "app/src/settings_view/mcp_servers/update_modal.rs",
    "app/src/settings_view/mcp_servers/installation_modal.rs",
    "app/src/settings_view/mcp_servers/destructive_mcp_confirmation_dialog.rs",
    "app/src/settings_view/mcp_servers_page.rs",
}

# IDs whose target MUST equal source byte-for-byte (no invariant pass).
DO_NOT_TRANSLATE_LITERAL = {
    "01KQXQV12JTN7Z6JZPRJMAAQDD",  # edit_page.rs L67 — JSON config template literal
}

TRANSLATIONS = {
    # ============================================================
    # edit_page.rs (9)
    # ============================================================
    # L67 — JSON template literal; target == source (set below from source).
    "01KQXQV12JTN7Z6JZPRJMAAQDD": "__LITERAL_FROM_SOURCE__",
    # L147 button
    "01KQXQV12BCAMXZJGVJD96M0MN": "编辑变量",
    # L194 description
    "01KQXQV12D7PS6F6WY5ABRM46F": "只有团队管理员和该 MCP 服务器的创建者可以编辑此 MCP 服务器。",
    # L318 dialog title
    "01KQXQV128ZPDX66GJHXKA5PHP": "添加新的 MCP 服务器",
    # L320 dialog title (named placeholder)
    "01KQXQV12BFZGM9FKHWGHFH06S": "编辑 {name} MCP 服务器",
    # L322 dialog title
    "01KQXQV12BZ206KEE2B2T6ZZBH": "编辑 MCP 服务器",
    # L544 warning — preserve "Settings > Privacy" path with > as half-width separator
    "01KQXQV12G28W0T421HS6J024F": "此 MCP 服务器包含密钥。请前往「设置」 > 「隐私」 修改您的密钥脱敏设置。",
    # L604 error
    "01KQXQV12DD0HDV62DQ7F9TP2P": "未指定 MCP 服务器。",
    # L618 error
    "01KQXQV129SXQP0F72PXJP8EBS": "编辑单个服务器时无法添加多个 MCP 服务器。",

    # ============================================================
    # update_modal.rs (6)
    # ============================================================
    # L116 modal title
    "01KQXQV12HG52HFR7T8ADQQ040": "更新 {name}",
    # L184 prompt
    "01KQXQV12G5X3KAZNX5JP2S2WH": "此服务器有 {} 个可用更新，您希望执行哪一项？",
    # L230 label
    "01KQXQV12HC9NVA4WFHW9BGH8M": "来自 {publisher_string} 的更新",
    # L237 label
    "01KQXQV12H562AJD00Y3E6VPDR": "来自 {name} 的更新",
    # L238 label
    "01KQXQV12H4MJ4TKQ93VVWTQ51": "版本 {new_version}",
    # L430 empty state
    "01KQXQV12DDY4GT4JDD3T9BGAA": "暂无可用更新",

    # ============================================================
    # installation_modal.rs (5)
    # ============================================================
    # L256 modal title
    "01KQXQV12CDQD7K5J3S1T7PKV2": "安装 {name}",
    # L348 error — preserve {e:?} Rust Debug placeholder
    "01KQXQV12BMEJ25RC7T5488M0P": "解析 markdown 失败：{e:?}",
    # L422 label
    "01KQXQV12FVWAM2STENFTEC1RN": "由团队共享",
    # L448 button
    "01KQXQV129RB0ZREA1PJP60MPV": "取消",
    # L617 status
    "01KQXQV12D1VA501NVC1YFXYZ1": "未选择 MCP 服务器",

    # ============================================================
    # destructive_mcp_confirmation_dialog.rs (7)
    # ============================================================
    # L62 title
    "01KQXQV12ABBX934V6TGGRFRP2": "删除 MCP 服务器？",
    # L63 description
    "01KQXQV12G71RQ4CQX6MZ2S2XD": "这将从您的所有设备卸载并移除此 MCP 服务器。",
    # L64 button
    "01KQXQV12AA5FKYENG5V9S94X7": "删除 MCP",
    # L68 title
    "01KQXQV12ANMZ6VE25NQ9E1W3S": "删除共享的 MCP 服务器？",
    # L69 description (full sentence — verified no trailing-space concatenation)
    "01KQXQV12GSCJ6V87EWPRHAHHT": "这不仅会为您自己删除此 MCP 服务器，还会从 Warp 中卸载并从您所有团队成员的设备上移除此 MCP 服务器。",
    # L74 title
    "01KQXQV12EHD81WE8MFEVA3MX1": "从团队中移除共享的 MCP 服务器？",
    # L75 description
    "01KQXQV12GHH8J2XDRQCJCWA17": "这将从 Warp 中卸载并从您所有团队成员的设备上移除此 MCP 服务器。",

    # ============================================================
    # mcp_servers_page.rs (5)
    # ============================================================
    # L149 toast
    "01KQXQV12G93KV8EQATYHB5E4N": "已成功从 {name} MCP 服务器登出",
    # L150 toast
    "01KQXQV12G5YJ2D54DKCAQ4CSS": "已成功从 MCP 服务器登出",
    # L317 error
    "01KQXQV12C65CRAJ57EERXYRKZ": "请先完成当前 MCP 安装，再打开另一个安装链接。",
    # L332 error (named placeholder)
    "01KQXQV12H3ASMMB3K20K0ZNWG": "未知 MCP 服务器“{autoinstall_param}”",
    # L360 error (named placeholder)
    "01KQXQV12DR6SCN8ADVFE40ZND": "MCP 服务器“{gallery_title}”无法通过此链接安装。",
}

NEW_GLOSSARY_TERMS = {}  # all required terms already present from prior batch


def check_invariants(by_id):
    """Enforce full-width punctuation invariant + placeholder integrity.

    Skip the invariant pass for DO_NOT_TRANSLATE_LITERAL ids (e.g. JSON templates).
    """
    forbidden = re.compile(r"[一-鿿][,.!?:;](?![\w/])")
    problems = []
    for eid, target in TRANSLATIONS.items():
        if eid in DO_NOT_TRANSLATE_LITERAL:
            continue
        for m in forbidden.finditer(target):
            problems.append((eid, m.group(0), m.start()))
    if problems:
        print("ERROR: half-width punctuation adjacent to Chinese characters:")
        for eid, frag, pos in problems:
            print(f"  {eid} at pos {pos}: {frag!r}")
        sys.exit(1)

    for eid, target in TRANSLATIONS.items():
        if eid in DO_NOT_TRANSLATE_LITERAL:
            continue
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
    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    # Resolve literal-passthrough targets from source bytes (post-load, pre-check).
    for eid in DO_NOT_TRANSLATE_LITERAL:
        TRANSLATIONS[eid] = by_id[eid]["source"]

    check_invariants(by_id)

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"
    assert len(TRANSLATIONS) == 32, f"Expected 32 entries, got {len(TRANSLATIONS)}"

    for eid, target in TRANSLATIONS.items():
        err = check_placeholders(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)
        err = check_whitespace_preservation(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)

    # Sanity: literal entries must be byte-equal to source.
    for eid in DO_NOT_TRANSLATE_LITERAL:
        assert TRANSLATIONS[eid] == by_id[eid]["source"], \
            f"{eid}: literal target diverged from source"

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

    if NEW_GLOSSARY_TERMS:
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
    else:
        print("No new glossary terms (all MCP-area terms reused from prior batch)")


if __name__ == "__main__":
    main()
