#!/usr/bin/env python3
"""Apply 51 ai/blocklist auto_ui translations — Agent input/control cluster.

Files: agent_input_footer/mod.rs (19) + environment_selector.rs (1) +
       inline_agent_view_header.rs (6) + orchestration_pill_bar.rs (2) +
       zero_state_block.rs (2) + block/view_impl/common.rs (4) +
       block/view_impl/orchestration.rs (1) + requested_command.rs (12) +
       orchestration_controls.rs (4).
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
BATCH_FLAG = "pr-ai-blocklist-agent-control-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_FILES = {
    "app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs",
    "app/src/ai/blocklist/agent_view/agent_input_footer/environment_selector.rs",
    "app/src/ai/blocklist/agent_view/inline_agent_view_header.rs",
    "app/src/ai/blocklist/agent_view/orchestration_pill_bar.rs",
    "app/src/ai/blocklist/agent_view/zero_state_block.rs",
    "app/src/ai/blocklist/block/view_impl/common.rs",
    "app/src/ai/blocklist/block/view_impl/orchestration.rs",
    "app/src/ai/blocklist/inline_action/requested_command.rs",
    "app/src/ai/blocklist/inline_action/orchestration_controls.rs",
}

# Translation map keyed by entry id.
TRANSLATIONS = {
    # ============================================================
    # agent_input_footer/mod.rs (19)
    # ============================================================
    # L451 — toast/banner
    "01KQXQV128PWB53MZD7361S155": "Warp 插件有新版本可用",
    # L341 — button tooltip
    "01KQXQV1292YHX77G9CQJ1V4YY": "附加文件",
    # L133 — toggle tooltip (current state: on → action to enable for task)
    "01KQXQV1299Z0FEMXTX31WTQ46": "为此任务自动批准所有 Agent 操作",
    # L603 — context window label
    "01KQXQV12ABGVS72CF13CK58R0": "上下文窗口用量",
    # L130 — toggle tooltip (off → action to disable autodetect)
    "01KQXQV12AF9KJKPDD358TR2ZY": "停用终端命令自动检测",
    # L129 — toggle tooltip (on → action to enable autodetect)
    "01KQXQV12B53GKD5QQNMPWZ89J": "启用终端命令自动检测",
    # L424 — install prompt
    "01KQXQV12CBT6YK4CA3Y5VJT77": "安装 Warp 插件以在 Warp 内启用丰富的 Agent 通知",
    # L380 — button label
    "01KQXQV12CZV0G33NHMTWKABXR": "文件浏览器",
    # L397 — button tooltip
    "01KQXQV12D2PE32AQ6AHS8MTA3": "打开富文本输入",
    # L136 — auth gate label; preserve /remote-control literal
    "01KQXQV12DME5MT1WTGN4Q8AKQ": "登录以使用 /remote-control",
    # L1285 — error
    "01KQXQV12DZGTQ7YWBMQAW18VD": "无可用的插件管理器",
    # L412 — button tooltip
    "01KQXQV12E8FT85ZW9DRVXH4SM": "打开代码 Agent 设置",
    # L382 — button tooltip
    "01KQXQV12EMWX7AGAE9YMP5QCY": "打开文件浏览器",
    # L135 — button label
    "01KQXQV12GNWPKPDN4M2987SVS": "启动远程控制",
    # L463 — link/button label
    "01KQXQV12H1X6MCDXYF4Y55M9F": "查看更新 Warp 插件的说明",
    # L305 — button tooltip
    "01KQXQV12H9RP2MPWR01NJBWWB": "语音输入",
    # L132 — toggle tooltip (off auto-approve)
    "01KQXQV12HBVGXVQTRJ9K8J70A": "关闭自动批准所有 Agent 操作",
    # L437 — link/button label
    "01KQXQV12HSMATTEGWCXJ20TC9": "查看安装 Warp 插件的说明",
    # L369 — input chip; preserve & literal as half-width
    "01KS2GEQ79W7Z5BTQXS7VRYC52": "移交至云端（或键入 &）",

    # ============================================================
    # agent_input_footer/environment_selector.rs (1)
    # ============================================================
    # L210
    "01KQXQV129K3RCYTD9Y8NC17SX": "选择一个环境",

    # ============================================================
    # inline_agent_view_header.rs (6)
    # ============================================================
    # L28
    "01KQXQV129B7GJ5X9XEVAXMJR6": "Agent 正在控制",
    # L25
    "01KQXQV129KXEYPTB9YMSNE3PH": "Agent 正在等待指令",
    # L27
    "01KQXQV129KYSYWSZ6VXKHGC51": "Agent 需要您的许可才能继续",
    # L26
    "01KQXQV129NFSYMEC1JM4QGHPE": "Agent 正在等待命令退出",
    # L24
    "01KQXQV12EJ0XE2YY1CPQN598C": "提示 Agent 进行交互",
    # L29
    "01KQXQV12HVB76STNHVMBGFCRP": "您正在控制",

    # ============================================================
    # orchestration_pill_bar.rs (2)
    # ============================================================
    # L448
    "01KQXQV12E9CYB7SVR0N9MREX0": "在新标签页中打开",
    # L443
    "01KQXQV12EWAE3QAB303S76YHC": "在新窗格中打开",

    # ============================================================
    # zero_state_block.rs (2)
    # ============================================================
    # L425 — Oz codename preserved
    "01KQXQV12D4V7N8JX6XPXHSDC1": "新建 Oz Agent 会话",
    # L409 — Oz codename preserved
    "01KQXQV12DBHY90DM6XJTTW0MW": "新建 Oz 云端 Agent 会话",

    # ============================================================
    # block/view_impl/common.rs (4)
    # ============================================================
    # L971 — tooltip
    "01KQXQV1292BMXZR4M3ZS48398": "请 Agent 立即检查此命令，跳过其计时器。",
    # L127 — status; ASCII ... → ……
    "01KQXQV129QW4VSYTKAN7WFN14": "Agent 正在等待指令……",
    # L3131 — button label; API uppercase
    "01KQXQV12B6BMHPM78CH99ATZQ": "编辑 API 密钥",
    # L130 — error message
    "01KQXQV12C1JV0QKRDSTQ7WVB0": "抱歉，我无法完成该请求。",

    # ============================================================
    # block/view_impl/orchestration.rs (1)
    # ============================================================
    # L48
    "01KQXQV12CZN9H5HBPRXW7CSXH": "正在生成标题……",

    # ============================================================
    # requested_command.rs (12)
    # ============================================================
    # L93
    "01KQXQV1297EB0P4DK2QDYQ9PV": "Agent 遇到问题。请接管控制权。",
    # L89
    "01KQXQV129C35Q4GDEA83K3WEP": "Agent 需要您的输入才能继续",
    # L88
    "01KQXQV129DEK0YWVGJMC3BK5V": "Agent 正在监控命令……",
    # L161
    "01KQXQV12BSDCXJNWXG23AMQ5M": "编辑请求的命令",
    # L85
    "01KQXQV12CSEB58PF860SKZDC8": "正在生成命令……",
    # L87
    "01KQXQV12D036XXR8M50PAT4T6": "允许我调用此 MCP 工具吗？",
    # L86
    "01KQXQV12D0DVSW9D1WSP880Q9": "允许我运行此命令并读取输出吗？",
    # L91
    "01KQXQV12E2FKM0QJ84C7NB318": "已暂停 Agent。您正在控制。",
    # L92 — concise status pill
    "01KQXQV12H3SV1JKJFEFBRTB2M": "您正在控制",
    # L95
    "01KQXQV12HDD11WBRGN1X8080X": "查看 MCP 工具调用详情",
    # L90
    "01KQXQV12HDGD4MYTE180CA703": "您正在控制。",
    # L94
    "01KQXQV12HXE2J3C81F6G115Q6": "查看命令详情",

    # ============================================================
    # orchestration_controls.rs (4)
    # ============================================================
    # L1866
    "01KQXQV129M23QZR4QCQNFM8SQ": "Agent 执行环境",
    # L70
    "01KQXQV12AG7Y6ASSS5A35T2AB": "默认模型",
    # L74
    "01KS2GEQN05YWQ8W476E2484V0": "跳过（高级）",
    # L77 — preserve U+2026 ellipsis at end (already in source)
    "01KS2GEQCDHKRTZFXJ6CZ9ZSKW": "新建 API 密钥…",
}


def check_invariants():
    """Full-width punctuation invariant + special-literal preservation."""
    # Half-width punct adjacent to CJK (excluding intentional code/path literals).
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

    # No bare ASCII ellipsis.
    for eid, target in TRANSLATIONS.items():
        if "..." in target:
            print(f"ERROR {eid}: bare '...' detected; use '……' instead")
            sys.exit(1)

    # Special literal preservation.
    # L369 must contain '&' (half-width).
    t = TRANSLATIONS["01KS2GEQ79W7Z5BTQXS7VRYC52"]
    if "&" not in t or "＆" in t:
        print(f"ERROR L369: '&' must be half-width, got {t!r}")
        sys.exit(1)
    # L136 must contain '/remote-control' literal.
    t = TRANSLATIONS["01KQXQV12DME5MT1WTGN4Q8AKQ"]
    if "/remote-control" not in t:
        print(f"ERROR L136: '/remote-control' literal missing, got {t!r}")
        sys.exit(1)
    # L409 / L425 must retain 'Oz'.
    for eid in ("01KQXQV12D4V7N8JX6XPXHSDC1", "01KQXQV12DBHY90DM6XJTTW0MW"):
        if "Oz" not in TRANSLATIONS[eid]:
            print(f"ERROR {eid}: 'Oz' codename missing, got {TRANSLATIONS[eid]!r}")
            sys.exit(1)
    # L3131 must contain 'API' uppercase.
    t = TRANSLATIONS["01KQXQV12B6BMHPM78CH99ATZQ"]
    if "API" not in t:
        print(f"ERROR L3131: 'API' uppercase missing, got {t!r}")
        sys.exit(1)
    # L77 must contain U+2026 (single char ellipsis).
    t = TRANSLATIONS["01KS2GEQCDHKRTZFXJ6CZ9ZSKW"]
    if "…" not in t:
        print(f"ERROR L77: U+2026 ellipsis missing, got {t!r}")
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

    cands = json.loads(CANDIDATES.read_text())
    cand_ids = {c["id"] for c in cands}

    # Coverage sanity.
    assert len(TRANSLATIONS) == 51, f"Expected 51 translations, got {len(TRANSLATIONS)}"
    assert set(TRANSLATIONS.keys()) == cand_ids, (
        "Translation keys do not match candidates.json: "
        f"missing={cand_ids - TRANSLATIONS.keys()}, "
        f"extra={TRANSLATIONS.keys() - cand_ids}"
    )

    check_invariants()

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs in strings.json: {missing}"

    # Pre-mutation snapshot: existing translated entries' (id, target, status).
    pre_snapshot = {
        e["id"]: (e.get("target"), e["status"])
        for e in entries
        if e["status"] == "translated"
    }
    assert len(pre_snapshot) == 1417, f"Expected 1417 prior translated, got {len(pre_snapshot)}"

    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        if e["status"] != "new":
            print(f"ERROR {eid}: expected status=new, got {e['status']}")
            sys.exit(1)
        if e.get("audit", {}).get("verdict") != "auto_ui":
            print(f"ERROR {eid}: expected verdict=auto_ui")
            sys.exit(1)
        files = {o.get("file") for o in e.get("occurrences", [])}
        if not (files & TARGET_FILES):
            print(f"ERROR {eid}: occurrences not in target files: {files}")
            sys.exit(1)
        err = check_placeholders(e, target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)
        err = check_whitespace_preservation(e, target)
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
    # Preserve prior uncertain count (audit-bucket, not entry-status).
    prior_uncertain = data.get("metadata", {}).get("stats", {}).get("uncertain", 0)
    status_counts["uncertain"] = prior_uncertain

    md = data.setdefault("metadata", {})
    md["entry_count"] = len(entries)
    md["stats"] = status_counts
    md["last_changed_at"] = NOW

    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {updated} entries in strings.json")
    print(f"New stats: {status_counts}")
    print("No new glossary terms needed (Rich Input + Agent + MCP + API + API key already present)")


if __name__ == "__main__":
    main()
