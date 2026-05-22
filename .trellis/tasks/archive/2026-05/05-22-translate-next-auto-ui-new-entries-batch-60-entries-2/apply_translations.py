#!/usr/bin/env python3
"""Apply 60 settings_view sweep auto_ui translations.

Scope (Strategy B — settings_view configuration UI sweep):
  - app/src/settings_view/execution_profile_view.rs        (18)
  - app/src/settings_view/main_page.rs                     (14)
  - app/src/settings_view/mod.rs                           (14)
  - app/src/settings_view/agent_assisted_environment_modal.rs (13)
  - app/src/settings_view/warpify_page.rs                  (1)

Special handling:
  * Named placeholders preserved verbatim: {description_suffix}, {path}.
  * Feature flag identifier `Same_Line_Prompt_Enabled` is preserved as-is
    (target = source) since it's an internal const value mis-classified
    as auto_ui — pure ASCII, no Chinese chars introduced.
  * ASCII '...' → '……' (U+2026 doubled). Source U+2026 preserved verbatim.
  * Brand / product literals preserved: Warp, Warp Drive, MCP, Oz Cloud,
    API, Git, SSH.
  * 'shell' / 'diff' lowercase preserved (固定写法).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
CANDIDATES = pathlib.Path(__file__).resolve().parent / "candidates.json"
BATCH_FLAG = "pr-settings-view-sweep-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_PREFIXES = (
    "app/src/settings_view/execution_profile_view.rs",
    "app/src/settings_view/main_page.rs",
    "app/src/settings_view/mod.rs",
    "app/src/settings_view/agent_assisted_environment_modal.rs",
    "app/src/settings_view/warpify_page.rs",
    # Shared occurrences also touch these — accept entries whose ANY occurrence
    # is in our primary list (above).
    "app/src/ai/execution_profiles/editor/mod.rs",
    "app/src/ai/execution_profiles/mod.rs",
    "app/src/workspace/view.rs",
    "app/src/settings_view/platform_page.rs",
    "app/src/settings_view/show_blocks_view.rs",
)

PRIMARY_PREFIXES = (
    "app/src/settings_view/execution_profile_view.rs",
    "app/src/settings_view/main_page.rs",
    "app/src/settings_view/mod.rs",
    "app/src/settings_view/agent_assisted_environment_modal.rs",
    "app/src/settings_view/warpify_page.rs",
)

TRANSLATIONS = {
    # ============================================================
    # app/src/settings_view/execution_profile_view.rs (18)
    # ============================================================
    # L301
    "01KQXQV1294SJYA4BHZEK96BJE": "提问：",
    # L163
    "01KQXQV1299SQKF7F5JK05STFE": "基础模型：",
    # L355
    "01KQXQV12923JXHA3EHXY1FPAA": "调用网页工具：",
    # L311
    "01KQXQV129E1CXPXZ83DXWENJZ": "调用 MCP 服务器：",
    # L739
    "01KQXQV129GND90HDFJ080ZV5Y": "除非自动批准否则询问",
    # L211
    "01KQXQV129MX3NZBYP0BN10EG3": "应用代码 diff：",
    # L366
    "01KQXQV129QKG9E377RQ7JVPZF": "自动同步计划至 Warp Drive：",
    # L764
    "01KQXQV12A6BPC67G5VQ2TGX4A": "目录白名单：",
    # L778
    "01KQXQV12ACFJB9KY0H8QPBS31": "命令白名单：",
    # L182
    "01KQXQV12AH4B2RZDK5VAB5F2C": "计算机使用：",
    # L792
    "01KQXQV12AYYXW0288A2ABKN1B": "命令黑名单：",
    # L240
    "01KQXQV12B1VV84DZS932QNY2C": "执行命令：",
    # L279
    "01KQXQV12CR7TV3FD4TN32X1CD": "与运行中的命令交互：",
    # L172
    "01KQXQV12CTVMHTJV38EQ13SQ3": "完整终端使用：",
    # L737
    "01KQXQV12D4FX1WTJW2HSGGSWJ": "从不询问",
    # L807
    "01KQXQV12D6VR3M1DVNSBPRDC1": "MCP 白名单：",
    # L823
    "01KQXQV12DC7DAFTPT804R1KJE": "MCP 黑名单：",
    # L220
    "01KQXQV12EVAARTTG38JKYVMZZ": "读取文件：",

    # ============================================================
    # app/src/settings_view/main_page.rs (14)
    # ============================================================
    # L59
    "01KQXQV12BKV2WVXPZQ7HMWWYT": "与亲朋好友及同事分享 Warp 即可获得奖励",
    # L93
    "01KQXQV12JRNY42E1Q850ZF289": "设置同步",
    # L153
    "01KQXQV12GHVXM3NSB5GEFJ248": "切换设置同步",
    # L706
    "01KQXQV12F6NEKWMWV40AFA3CW": "设置同步",
    # L790
    "01KQXQV12EPA026PJKS4BSYBM5": "推荐朋友",
    # L840
    "01KQXQV12H8018GM5Z90XKZHCQ": "已是最新版本",
    # L850
    "01KQXQV12J1CBQFWWKX9WF7EBH": "正在检查更新……",
    # L857
    "01KQXQV12JZ7MW66KDEAJC29ZQ": "正在下载更新……",
    # L864
    "01KQXQV12HM1K9BVGK0X0JPYZ2": "有可用更新",
    # L868
    "01KQXQV12E833RN1JM1M1S4RVX": "重新启动 Warp",
    # L881
    "01KQXQV12CSMMN5ZFGS6MR947R": "已安装更新",
    # L891
    "01KQXQV128PFQ5AFK0FESE8YFG": "Warp 有新版本可用，但无法完成安装",
    # L895
    "01KQXQV12HV8X3WGHXS07HE802": "手动更新 Warp",
    # L902
    "01KQXQV128PXP78HN1KFKG6GSY": "Warp 新版本已安装，但无法启动。",

    # ============================================================
    # app/src/settings_view/mod.rs (14)
    # ============================================================
    # L272
    "01KQXQV12DR7QS44JSSM5P20XX": "键盘快捷键",
    # L273
    "01KQXQV12FJN1QQ78F5PZ9MF7X": "共享命令块",
    # L278
    "01KQXQV12DP2QY1C1NEDH0F18D": "MCP 服务器",
    # L281
    "01KQXQV12CJ738FSDJX95KQGTR": "索引与项目",
    # L284
    "01KQXQV12E293FNJGNZ32F0CGR": "Oz Cloud API 密钥",
    # L442 — feature flag identifier, preserved verbatim
    "01KQXQV12F5NDPA97S8WW9V9RT": "Same_Line_Prompt_Enabled",
    # L554
    "01KQXQV12CJSMSASBC8SG41W76": "隐藏初始化命令块",
    # L567
    "01KQXQV12GX4TCE2XTY78X1N6P": "显示带内命令块",
    # L568
    "01KQXQV12C9V5VEQP0S9QAES32": "隐藏带内命令块",
    # L706
    "01KQXQV12BR15VM7NRA5GR7DQV": "启用 {description_suffix}",
    # L707
    "01KQXQV12AYE4MHP2ZZNQ323DG": "禁用 {description_suffix}",
    # L1243
    "01KQXQV129XYDGWMD5FS8MK60R": "云端平台",
    # L2280
    "01KQXQV12DP37CKVX2AY8V0846": "没有匹配您搜索条件的设置。",
    # L2288
    "01KQXQV12JQCP6BMWT8JPAX1V5": "您可以尝试使用其他关键词，或检查是否存在拼写错误。",

    # ============================================================
    # app/src/settings_view/agent_assisted_environment_modal.rs (13)
    # ============================================================
    # L104
    "01KQXQV129FY142Y3RKVV23R2D": "添加仓库",
    # L336
    "01KQXQV12FZ8DGXSKV3901AR9M": "已选仓库",
    # L341
    "01KQXQV12D4MQ8KC17WSW1MHEA": "尚未选择任何仓库",
    # L417
    "01KQXQV1297SK5MV3Z7CNFJ0QT": "可用的已索引仓库",
    # L437 (source has U+2026)
    "01KQXQV12DBR65M54B5Y2DHCK1": "正在加载本地已索引的仓库……",
    # L439
    "01KQXQV12D40VG9SQ0RYSF6YDA": "尚未找到本地已索引的仓库。请先索引一个仓库后再试。",
    # L442
    "01KQXQV12DX2EG8CTZW4T0H7EP": "当前构建版本不支持本地仓库选择。",
    # L512
    "01KQXQV129PA1ANEG2JBCT6T84": "所有本地已索引的仓库均已被选中。",
    # L555
    "01KQXQV12FN53SNC6M29ZJ6F6R": "所选文件夹不是 Git 仓库：{path}",
    # L599
    "01KQXQV12DQZE9GVM3T9S3ZRF7": "未选择任何目录",
    # L617
    "01KQXQV12F3HS6GQP4F8MFWBHM": "选择本地已索引的仓库，为环境创建 Agent 提供上下文。",
    # L619
    "01KQXQV12FBFFMWXRJZ3T43KAB": "选择仓库，为环境创建 Agent 提供上下文。",
    # L643
    "01KQXQV12FXMRX59C2MTR1NAR6": "为您的环境选择仓库",

    # ============================================================
    # app/src/settings_view/warpify_page.rs (1)
    # ============================================================
    # L605
    "01KQXQV1292BJYESSV75ZAXMDP": "已添加的命令",
}


# Entries that intentionally have target == source (identifiers).
# These get a `do_not_translate` flag in addition to BATCH_FLAG.
IDENTITY_IDS = {
    "01KQXQV12F5NDPA97S8WW9V9RT",  # Same_Line_Prompt_Enabled
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

    # ---- Brand / acronym literal assertions ----
    brand_checks = [
        # execution_profile_view
        ("01KQXQV129E1CXPXZ83DXWENJZ", "MCP"),
        ("01KQXQV129QKG9E377RQ7JVPZF", "Warp Drive"),
        ("01KQXQV12D6VR3M1DVNSBPRDC1", "MCP"),
        ("01KQXQV12DC7DAFTPT804R1KJE", "MCP"),
        # main_page
        ("01KQXQV12BKV2WVXPZQ7HMWWYT", "Warp"),
        ("01KQXQV12E833RN1JM1M1S4RVX", "Warp"),
        ("01KQXQV128PFQ5AFK0FESE8YFG", "Warp"),
        ("01KQXQV12HV8X3WGHXS07HE802", "Warp"),
        ("01KQXQV128PXP78HN1KFKG6GSY", "Warp"),
        # mod.rs
        ("01KQXQV12DP2QY1C1NEDH0F18D", "MCP"),
        ("01KQXQV12E293FNJGNZ32F0CGR", "Oz Cloud"),
        ("01KQXQV12E293FNJGNZ32F0CGR", "API"),
        # modal
        ("01KQXQV12FN53SNC6M29ZJ6F6R", "Git"),
        ("01KQXQV12F3HS6GQP4F8MFWBHM", "Agent"),
        ("01KQXQV12FBFFMWXRJZ3T43KAB", "Agent"),
    ]
    for eid, lit in brand_checks:
        t = TRANSLATIONS[eid]
        if lit not in t:
            print(f"ERROR {eid}: brand literal {lit!r} missing, got {t!r}")
            sys.exit(1)

    # 'shell'/'diff' lowercase preservation.
    if "diff" not in TRANSLATIONS["01KQXQV129MX3NZBYP0BN10EG3"]:
        print("ERROR: 'diff' literal missing in Apply code diffs")
        sys.exit(1)

    # Identifier identity check: target must equal source for IDENTITY_IDS.
    cands = json.loads(CANDIDATES.read_text())
    by_id = {c["id"]: c for c in cands}
    for eid in IDENTITY_IDS:
        if TRANSLATIONS[eid] != by_id[eid]["source"]:
            print(f"ERROR {eid}: IDENTITY_IDS requires target == source, "
                  f"got {TRANSLATIONS[eid]!r} vs {by_id[eid]['source']!r}")
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
    assert len(pre_snapshot) == 1680, f"Expected 1680 prior translated, got {len(pre_snapshot)}"

    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        if e["status"] != "new":
            print(f"ERROR {eid}: expected status=new, got {e['status']}")
            sys.exit(1)
        if e.get("audit", {}).get("verdict") != "auto_ui":
            print(f"ERROR {eid}: expected verdict=auto_ui")
            sys.exit(1)
        files = {o.get("file") for o in e.get("occurrences", [])}
        # at least one occurrence must be in primary settings_view files
        if not any(f == p or f.startswith(p) for f in files for p in PRIMARY_PREFIXES):
            print(f"ERROR {eid}: no occurrence in primary settings_view files: {files}")
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
        if eid in IDENTITY_IDS and "do_not_translate" not in flags:
            flags.append("do_not_translate")
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
