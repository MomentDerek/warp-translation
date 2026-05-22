#!/usr/bin/env python3
"""Apply 60 remote_server + resource_center + notebooks/editor auto_ui translations.

Scope (Strategy 1 — Top-3 hotspot files):
  - app/src/remote_server/server_model.rs       (23)
  - app/src/resource_center/sections.rs         (22)
  - app/src/notebooks/editor/view.rs            (15, sorted-by-id head cut)

Special handling:
  * Named placeholders preserved verbatim:
      {err} / {e} / {error} / {file_id:?} / {session_id:?}
      / {dir_path} / {repo_path}
  * Positional placeholders {} / {:?} preserved with count + order.
  * protobuf protocol field/type names preserved literal:
      ClientMessage / message / DiscardFiles / DiscardFilesRequest
      / GetDiffState / mode / repo_path / dir_path.
  * Brand / acronym literals: Warp / IDE / PS1.
  * 'shell' lowercase preserved (固定写法).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
CANDIDATES = pathlib.Path(__file__).resolve().parent / "candidates.json"
BATCH_FLAG = "pr-remote-server-resource-center-notebooks-editor-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_PREFIXES = (
    "app/src/remote_server/server_model.rs",
    "app/src/resource_center/sections.rs",
    "app/src/notebooks/editor/view.rs",
)

TRANSLATIONS = {
    # ============================================================
    # app/src/remote_server/server_model.rs (23)
    # ============================================================
    # L757
    "01KQXQV129DAJB5Q49MYY4X8GB": "ClientMessage 未设置 message 字段",
    # L1880
    "01KQXQV12BF9FECWH1XTQQ5BPG": "无法发起写入：{err}",
    # L1923
    "01KQXQV12BHFZYBXX5W0GJP0DP": "无法发起删除：{err}",
    # L1823
    "01KQXQV12BQP6G2BBEFSRA56HC": "加载目录失败：{e}",
    # L1613
    "01KQXQV12BVFFD5SD28B1XJMC9": "执行命令失败：{e}",
    # L1789
    "01KQXQV12C4T5XHVWBR2ESEB42": "repo_path 无效：{e}",
    # L1799
    "01KQXQV12CA5B7QDR41HHVQR6V": "dir_path 无效：{e}",
    # L1652
    "01KQXQV12CTA3S9V5A9ES6N7EK": "路径无效：{e}",
    # L2757
    "01KQXQV12CW9E4YAFTASHY256M": "文件不存在或无法读取",
    # L1551
    "01KQXQV12DECSP36TKA66KT9AH": "会话 {session_id:?} 没有可用的执行器",
    # L1809
    "01KQXQV12J2KY0M1BQK79RDN0F": "dir_path {dir_path} 不是 repo_path {repo_path} 的子目录",
    # L397
    "01KRNVK98997K44JR1Z3H83ED4": "缓冲区已加载，但文件 {file_id:?} 的内容或同步时钟不可用",
    # L2073
    "01KRNVK98KDYFZBYEYHTVJ39W2": "缓冲区已加载，但没有文件内容",
    # L2088
    "01KRNVK98W263ZRDHJQQ3C8GMF": "缓冲区已加载，但没有同步时钟",
    # L2161
    "01KRNVK997ZCG12YNVVJAVAV8V": "缓冲区未打开：{}",
    # L531
    "01KRNVK9PV3EFC2BY8AWTVB8ZS": "加载缓冲区失败：{error}",
    # L2241
    "01KRNVK9RVGJCMWXCKA9AX1QF8": "解决冲突失败：{err}",
    # L2186
    "01KRNVK9SNGTX3DXHED6NZX9J7": "保存失败：{err}",
    # L2553
    "01KRNVK9Z55GBBCT0MKGE5TP0F": "DiscardFiles 缺少 mode 字段",
    # L2275
    "01KRNVK9ZA1Z3EG7ACKFPWB66E": "GetDiffState 缺少 mode 字段",
    # L2570
    "01KRNVKA05R5MKM5BVFK1Q0CB2": "未找到活动的 diff 状态模型：repo={} mode={:?}",
    # L2582
    "01KRNVKA1HF3TBAJQAS2DC7Q28": "DiscardFilesRequest 未指定任何文件",
    # L2604
    "01KRNVKA2S0991RPRNGWKV57PX": "路径验证后没有有效的文件",

    # ============================================================
    # app/src/resource_center/sections.rs (22)
    # ============================================================
    # L39
    "01KQXQV128AQBVB4Z0H24227M7": "通过键盘访问 Warp 的所有功能。",
    # L27
    "01KQXQV129C9DHQBSS8G6W9WFE": "点击以选中命令块，并使用方向键在其间移动。",
    # L70
    "01KQXQV12AD39WNKYHDNA75HES": "配置 Warp 让您能从最常用的开发工具中启动它",
    # L20
    "01KQXQV12AYDMTHHJYCXQS4NVW": "创建您的第一个命令块",
    # L92
    "01KQXQV12C5527GXQXM6RWZ370": "查找并运行此前执行过的命令、工作流等。",
    # L69
    "01KQXQV12C69RNQ1RF2T3C009E": "将 Warp 与您的 IDE 集成",
    # L75
    "01KQXQV12CFTDDZ6H67VE9H5W4": "Warp 团队如何使用 Warp",
    # L76
    "01KQXQV12D4DR0N4J8RHAHPWPC": "了解 Warp 工程团队如何使用他们最爱的功能",
    # L115
    "01KQXQV12D7WYHZCAWQ367TMYG": "启动配置",
    # L45
    "01KQXQV12D9YR6VNBPNZ1ENMEQ": "通过选择主题，让 Warp 成为您专属的工具。",
    # L26
    "01KQXQV12DYNZC1700Z5HXRY4J": "浏览命令块",
    # L78
    "01KQXQV12E6QS51BKQ7CHX23MK": "阅读文章",
    # L38
    "01KQXQV12E7BC8QYENFND3438D": "打开命令面板",
    # L44
    "01KQXQV12F09EWC1HQ8SG8T46Z": "设置您的主题",
    # L116
    "01KQXQV12FBJ2SEVRYK7FC54CA": "保存您当前的窗口、标签页与面板配置。",
    # L64
    "01KQXQV12FC0G2W2V0A4JSCKAA": "配置 Warp 以遵循您的 PS1 设置",
    # L21
    "01KQXQV12FEKZW144XGZTSZRSW": "运行一条命令，您将看到该命令与其输出被组合到一起。",
    # L33
    "01KQXQV12FQ1TGWJ35D74PW83N": "右键点击命令块即可复制 / 粘贴、分享等更多操作。",
    # L106
    "01KQXQV12GBD6TCYS0YR2JFNEZ": "拆分面板",
    # L32
    "01KQXQV12GQRBNSDGSF40G94DV": "对命令块执行操作",
    # L63
    "01KQXQV12H1S0VX0CY165JVDT2": "使用您的自定义 shell 提示符",
    # L66
    "01KQXQV12HBZR54842AX1BC34B": "查看文档",

    # ============================================================
    # app/src/notebooks/editor/view.rs (15)
    # ============================================================
    # L397
    "01KQXQV12A0WG966STTN65H689": "复制富文本选区",
    # L678
    "01KQXQV12A5XA7FJ64WPF08B1C": "创建或编辑链接",
    # L318
    "01KQXQV12A60QRZBM4PJ6R944N": "取消选中 shell 命令",
    # L390
    "01KQXQV12AEZCGXD6QRZFFD7TH": "复制富文本缓冲区",
    # L714
    "01KQXQV12C789ZKVKADRXWRXX4": "在笔记本中查找",
    # L471
    "01KQXQV12DCAAJRSGTF6T5H1SM": "移动到段落开头",
    # L404
    "01KQXQV12DG2RN2PFB2YSQ6863": "记录编辑器状态",
    # L487
    "01KQXQV12DT9W8CE5Q0HZMWB2R": "移动到段落末尾",
    # L336
    "01KQXQV12F35W520BV3FM2GC4X": "选择上一条命令",
    # L325
    "01KQXQV12F3MRGTVVZBNN0D1E0": "选中光标处的 shell 命令",
    # L560
    "01KQXQV12F4ESNNSR3Q11FFY56": "选择到段落末尾",
    # L350
    "01KQXQV12FESMXGE27Z0PP9MW8": "运行选中的命令",
    # L553
    "01KQXQV12FMNKGH61P4C7PNP4F": "选择到段落开头",
    # L343
    "01KQXQV12FQD38ZXZBGXWKRJBJ": "选择下一条命令",
    # L740
    "01KQXQV12G5EEWMBRBRAWJSGKR": "切换大小写敏感搜索",
}


def check_invariants():
    """Punctuation + literal preservation checks."""
    # Half-width punct adjacent to CJK — forbidden (unless followed by Latin/digit/slash/brace).
    forbidden = re.compile(r"[一-鿿][,.!?:;](?![\w/{])")
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

    # ---- Placeholder + protobuf-field-name literal assertions ----

    # protobuf protocol literals to preserve.
    proto_literals = {
        "01KQXQV129DAJB5Q49MYY4X8GB": ["ClientMessage", "message"],
        "01KQXQV12C4T5XHVWBR2ESEB42": ["repo_path"],
        "01KQXQV12CA5B7QDR41HHVQR6V": ["dir_path"],
        "01KQXQV12J2KY0M1BQK79RDN0F": ["dir_path", "repo_path"],
        "01KRNVK9Z55GBBCT0MKGE5TP0F": ["DiscardFiles", "mode"],
        "01KRNVK9ZA1Z3EG7ACKFPWB66E": ["GetDiffState", "mode"],
        "01KRNVKA05R5MKM5BVFK1Q0CB2": ["repo=", "mode="],
        "01KRNVKA1HF3TBAJQAS2DC7Q28": ["DiscardFilesRequest"],
    }
    for eid, lits in proto_literals.items():
        t = TRANSLATIONS[eid]
        for lit in lits:
            if lit not in t:
                print(f"ERROR {eid}: protobuf literal {lit!r} missing, got {t!r}")
                sys.exit(1)

    # Resource center brand / acronym literals.
    rc_brand_checks = [
        ("01KQXQV128AQBVB4Z0H24227M7", "Warp"),
        ("01KQXQV12AD39WNKYHDNA75HES", "Warp"),
        ("01KQXQV12C69RNQ1RF2T3C009E", "Warp"),
        ("01KQXQV12C69RNQ1RF2T3C009E", "IDE"),
        ("01KQXQV12CFTDDZ6H67VE9H5W4", "Warp"),
        ("01KQXQV12D4DR0N4J8RHAHPWPC", "Warp"),
        ("01KQXQV12D9YR6VNBPNZ1ENMEQ", "Warp"),
        ("01KQXQV12FC0G2W2V0A4JSCKAA", "Warp"),
        ("01KQXQV12FC0G2W2V0A4JSCKAA", "PS1"),
    ]
    for eid, lit in rc_brand_checks:
        t = TRANSLATIONS[eid]
        if lit not in t:
            print(f"ERROR {eid}: brand literal {lit!r} missing, got {t!r}")
            sys.exit(1)

    # 'shell' lowercase preservation (notebooks/editor + resource_center).
    shell_ids = [
        "01KQXQV12A60QRZBM4PJ6R944N",  # notebooks L318
        "01KQXQV12F3MRGTVVZBNN0D1E0",  # notebooks L325
        "01KQXQV12H1S0VX0CY165JVDT2",  # rc L63 (shell 提示符)
    ]
    for eid in shell_ids:
        t = TRANSLATIONS[eid]
        if "shell" not in t:
            print(f"ERROR {eid}: literal 'shell' missing, got {t!r}")
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
    assert len(TRANSLATIONS) == 60, f"Expected 60 translations, got {len(TRANSLATIONS)}"
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
    assert len(pre_snapshot) == 1620, f"Expected 1620 prior translated, got {len(pre_snapshot)}"

    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        if e["status"] != "new":
            print(f"ERROR {eid}: expected status=new, got {e['status']}")
            sys.exit(1)
        if e.get("audit", {}).get("verdict") != "auto_ui":
            print(f"ERROR {eid}: expected verdict=auto_ui")
            sys.exit(1)
        files = {o.get("file") for o in e.get("occurrences", [])}
        if not any(f == p or f.startswith(p) for f in files for p in TARGET_PREFIXES):
            print(f"ERROR {eid}: occurrences not in target files: {files}")
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
    print("Glossary delta: none (term_count stays at 93)")


if __name__ == "__main__":
    main()
