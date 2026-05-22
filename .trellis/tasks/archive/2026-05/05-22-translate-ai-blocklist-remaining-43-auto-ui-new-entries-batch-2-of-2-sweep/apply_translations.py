#!/usr/bin/env python3
"""Apply 43 ai/blocklist auto_ui translations — long-tail sweep (batch 2 of 2).

Files: 20 leaf files across ai/blocklist subtree:
  - action_model/execute/{get_files,read_files,search_codebase}.rs
  - block.rs / block/cli.rs / block/toggleable_items.rs / block/view_impl/output.rs
  - codebase_index_speedbump_banner.rs / history_model.rs
  - inline_action/{ask_user_question_view, code_diff_view, host_picker, search_codebase}.rs
  - prompt/prompt_alert.rs / suggested_rule_modal.rs / summarization_cancel_dialog.rs
  - task_status_sync_model.rs / telemetry_banner.rs / usage/conversation_usage_view.rs
  - view_util.rs

Special handling:
  * L253 read_files.rs: preserve {missing_files} placeholder verbatim.
  * L569 block.rs: 'GitHub' literal in target.
  * L26 prompt_alert: target end with ASCII ", " (concat fragment).
  * L32 prompt_alert: target end with ASCII " - " (concat fragment).
  * L180 toggleable_items: target STARTS with " " (half-width space prefix).
  * Credit (glossary 已存在 → '积分') used instead of PRD's draft '额度'.
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
BATCH_FLAG = "pr-ai-blocklist-sweep-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Target files: 20 ai/blocklist leaf files for this batch.
TARGET_FILES = {
    "app/src/ai/blocklist/action_model/execute/get_files.rs",
    "app/src/ai/blocklist/action_model/execute/read_files.rs",
    "app/src/ai/blocklist/action_model/execute/search_codebase.rs",
    "app/src/ai/blocklist/block.rs",
    "app/src/ai/blocklist/block/cli.rs",
    "app/src/ai/blocklist/block/toggleable_items.rs",
    "app/src/ai/blocklist/block/view_impl/output.rs",
    "app/src/ai/blocklist/codebase_index_speedbump_banner.rs",
    "app/src/ai/blocklist/history_model.rs",
    "app/src/ai/blocklist/inline_action/ask_user_question_view.rs",
    "app/src/ai/blocklist/inline_action/code_diff_view.rs",
    "app/src/ai/blocklist/inline_action/host_picker.rs",
    "app/src/ai/blocklist/inline_action/search_codebase.rs",
    "app/src/ai/blocklist/prompt/prompt_alert.rs",
    "app/src/ai/blocklist/suggested_rule_modal.rs",
    "app/src/ai/blocklist/summarization_cancel_dialog.rs",
    "app/src/ai/blocklist/task_status_sync_model.rs",
    "app/src/ai/blocklist/telemetry_banner.rs",
    "app/src/ai/blocklist/usage/conversation_usage_view.rs",
    "app/src/ai/blocklist/view_util.rs",
}

# Translation map keyed by entry id.
TRANSLATIONS = {
    # ============================================================
    # action_model/execute/get_files.rs (1)
    # ============================================================
    # L173 — Agent action error
    "01KQXQV12G0728CH3CQMT2V08K": "搜索失败。请尝试用其他方式定位相关文件。",

    # ============================================================
    # action_model/execute/read_files.rs (1)
    # ============================================================
    # L253 — Agent action error; {missing_files} placeholder MUST survive
    "01KQXQV12GHRB9WC07DNCS2612": "以下文件不存在：{missing_files}",

    # ============================================================
    # action_model/execute/search_codebase.rs (1)
    # ============================================================
    # L237 — Agent action error
    "01KQXQV12GJB5SEX6RWTJEDX0Q": "搜索失败，因为代码库不可用。请尝试用其他方式定位相关文件。",

    # ============================================================
    # block.rs (4) — command block top-level actions
    # ============================================================
    # L569 — button; GitHub literal preserved
    "01KQXQV12E48R5BG6FHCPY8V5K": "在 GitHub 中打开",
    # L1301 — button
    "01KQXQV12E7DS7EXV4FFFRZP9B": "审阅变更",
    # L1327 — checkbox label
    "01KQXQV12BYE7HTMXEFX8PW4P3": "不再显示",
    # L1340 — button (block → 命令块)
    "01KQXQV12EKF26J0TX4W29M9R7": "回退至此命令块之前",

    # ============================================================
    # block/cli.rs (1)
    # ============================================================
    # L181 — control semantics aligned with batch 1 L93 「接管控制权」
    "01KQXQV12GA9V4K6SXXZFSVQZX": "接管运行中的命令",

    # ============================================================
    # block/toggleable_items.rs (1)
    # ============================================================
    # L180 — concat suffix; preserve leading half-width space
    "01KQXQV12J2BY125KRQ0774SA7": " 切换选中",

    # ============================================================
    # block/view_impl/output.rs (6) — output bar actions
    # ============================================================
    # L2095
    "01KQXQV12E4TA3XX4ZT1N26JND": "恢复会话",
    # L3100 — feedback
    "01KQXQV12CBV8ZM3FZWH7D1FAV": "好的回复",
    # L3121 — feedback
    "01KQXQV12944FTP80VKGJJGS6W": "差的回复",
    # L3193 — button
    "01KQXQV12A1XNRCFJSM8YZHTB0": "继续会话",
    # L3217 — fork (new glossary term)
    "01KQXQV12CFQ6JKTWK9XH74KD1": "派生会话",
    # L3393 — credit usage (glossary `credit → 积分`)
    "01KQXQV12F064RGSRQVZB297TK": "显示积分使用详情",

    # ============================================================
    # codebase_index_speedbump_banner.rs (4) — codebase indexing onboarding
    # ============================================================
    # L21 — long description (... → ……)
    "01KQXQV12C02FP5ZYJHY91E1T9": "索引能帮助 Agent 快速理解上下文并提供针对性的解决方案。代码永远不会存储在服务器上。",
    # L25 — button
    "01KQXQV12CXJA6EDFESEX11YPJ": "索引代码库",
    # L26 — toggle label
    "01KQXQV1298873MRTHYJ5T0377": "允许自动索引",
    # L30 — link/button
    "01KQXQV12HVBX03QKTQ4XYBRVF": "查看状态",

    # ============================================================
    # history_model.rs (1)
    # ============================================================
    # L2622 — status
    "01KQXQV129H31SZBXYD5HYTBKE": "已被用户取消",

    # ============================================================
    # inline_action/ask_user_question_view.rs (1)
    # ============================================================
    # L1368 — status
    "01KQXQV12ERWC85VMHAYSABGY1": "已跳过提问",

    # ============================================================
    # inline_action/code_diff_view.rs (5) — code diff review
    # ============================================================
    # L132 — button
    "01KQXQV1287FDC313QYNG54JCT": "接受并继续与 Agent 协作",
    # L133 — button
    "01KQXQV12D5CHGREEZAH40M473": "与 Agent 迭代",
    # L214 — action label
    "01KQXQV12B6KXFP6NKMJTWK4GK": "编辑代码差异",
    # L2543 — checkbox / option
    "01KQXQV12B3NHG5DTQ4JPX4EEY": "不再向我显示建议代码横幅",
    # L3148 — label
    "01KQXQV12EDT3MXSBTXJW0QM3F": "请求的编辑",

    # ============================================================
    # inline_action/host_picker.rs (1)
    # ============================================================
    # L53 — picker option; U+2026 single-char ellipsis preserved
    "01KS2GEQ2S2MMVRFYAY8GZ0KGP": "自定义主机…",

    # ============================================================
    # inline_action/search_codebase.rs (1)
    # ============================================================
    # L244 — empty state
    "01KQXQV12DHSMYZ5NV2GW4A95R": "未找到结果",

    # ============================================================
    # prompt/prompt_alert.rs (8) — AI billing/alerts
    # ============================================================
    # L26 — concat prefix; preserve trailing ASCII ", "
    "01KQXQV12GBYJ3ZMZ24TMT2PJW": "要使用 AI 功能, ",
    # L30 — alert
    "01KQXQV12DK67EYY3RVR51PQ3G": "无网络连接",
    # L32 — concat prefix; preserve trailing ASCII " - "
    "01KQXQV1292EHGACR4T8JHQPKQ": "已达上限 - ",
    # L33 — alert
    "01KQXQV12EZSYX37Z750ENH8K0": "因付款问题受限",
    # L34 — alert (credit → 积分)
    "01KQXQV12ES14AQWY1W857RKG7": "积分不足",
    # L36 — link/button (credit → 积分)
    "01KQXQV12G1WE20V680GNWPMWA": "注册以获取更多 AI 积分",
    # L38 — link/button
    "01KQXQV12B4NA0N3F0C3NH6XA9": "启用超额付费",
    # L39 — link/button (spending_limit → 支出限额)
    "01KQXQV12CP5S88KXT7P5TEFTC": "提升每月支出限额",

    # ============================================================
    # suggested_rule_modal.rs (1)
    # ============================================================
    # L48 — dialog title (rule → 规则)
    "01KQXQV12GHJKK27R8XCAF5334": "建议的规则",

    # ============================================================
    # summarization_cancel_dialog.rs (1)
    # ============================================================
    # L173 — dialog title
    "01KQXQV129C3YQ0E0R21A9FAAG": "取消摘要？",

    # ============================================================
    # task_status_sync_model.rs (1)
    # ============================================================
    # L277 — error
    "01KQXQV12H7YTGQQRTVMXXM47J": "Warp 暂时过载。请稍后再试。",

    # ============================================================
    # telemetry_banner.rs (1)
    # ============================================================
    # L136 — button
    "01KQXQV12D2EWMKD1SZS4HF1AK": "管理隐私设置",

    # ============================================================
    # usage/conversation_usage_view.rs (1)
    # ============================================================
    # L671 — button
    "01KQXQV12CCBDM50YPXEMRRESR": "隐藏详情",

    # ============================================================
    # view_util.rs (2)
    # ============================================================
    # L39 — menu item
    "01KQXQV129WHK8JYJ41SNCT74C": "作为 Agent 上下文附加",
    # L93 — menu item
    "01KQXQV12CWN9WZ2RAJ9GVNZP1": "跟进现有会话",
}


def check_invariants():
    """Full-width punctuation invariant + special-literal preservation."""
    # IDs of concat-fragment entries where ASCII punctuation at boundary is intentional.
    CONCAT_FRAGMENT_IDS = {
        "01KQXQV12GBYJ3ZMZ24TMT2PJW",  # L26 prompt_alert "..., "
        "01KQXQV1292EHGACR4T8JHQPKQ",  # L32 prompt_alert "... - "
        "01KQXQV12J2BY125KRQ0774SA7",  # L180 toggleable_items " ..."
    }
    # Half-width punct adjacent to CJK (excluding intentional concat fragments).
    forbidden = re.compile(r"[一-鿿][,.!?:;](?![\w/])")
    problems = []
    for eid, target in TRANSLATIONS.items():
        if eid in CONCAT_FRAGMENT_IDS:
            continue
        for m in forbidden.finditer(target):
            problems.append((eid, m.group(0), m.start()))
    if problems:
        print("ERROR: half-width punctuation adjacent to Chinese characters:")
        for eid, frag, pos in problems:
            print(f"  {eid} at pos {pos}: {frag!r}")
        sys.exit(1)

    # No bare ASCII ellipsis (... three dots). The single-char U+2026 is OK.
    for eid, target in TRANSLATIONS.items():
        if "..." in target:
            print(f"ERROR {eid}: bare '...' detected; use '……' instead")
            sys.exit(1)

    # ---- Special literal preservation ----

    # L253: {missing_files} placeholder MUST appear exactly once.
    t = TRANSLATIONS["01KQXQV12GHRB9WC07DNCS2612"]
    if t.count("{missing_files}") != 1:
        print(f"ERROR L253: '{{missing_files}}' must appear exactly once, got {t!r}")
        sys.exit(1)

    # L569: 'GitHub' must appear literally.
    t = TRANSLATIONS["01KQXQV12E48R5BG6FHCPY8V5K"]
    if "GitHub" not in t:
        print(f"ERROR L569: 'GitHub' literal missing, got {t!r}")
        sys.exit(1)

    # L26 (prompt_alert): target MUST end with ASCII ", " (half-width comma + space).
    t = TRANSLATIONS["01KQXQV12GBYJ3ZMZ24TMT2PJW"]
    if not t.endswith(", "):
        print(f"ERROR L26 prompt_alert: target must end with ASCII ', ', got {t!r}")
        sys.exit(1)

    # L32 (prompt_alert): target MUST end with ASCII " - " (space-hyphen-space).
    t = TRANSLATIONS["01KQXQV1292EHGACR4T8JHQPKQ"]
    if not t.endswith(" - "):
        print(f"ERROR L32 prompt_alert: target must end with ASCII ' - ', got {t!r}")
        sys.exit(1)

    # L180 (toggleable_items): target MUST start with half-width space.
    t = TRANSLATIONS["01KQXQV12J2BY125KRQ0774SA7"]
    if not t.startswith(" "):
        print(f"ERROR L180 toggleable_items: target must start with half-width space, got {t!r}")
        sys.exit(1)

    # L277: 'Warp' brand preserved.
    t = TRANSLATIONS["01KQXQV12H7YTGQQRTVMXXM47J"]
    if "Warp" not in t:
        print(f"ERROR L277: 'Warp' brand missing, got {t!r}")
        sys.exit(1)

    # L53: U+2026 single-char ellipsis preserved.
    t = TRANSLATIONS["01KS2GEQ2S2MMVRFYAY8GZ0KGP"]
    if "…" not in t:
        print(f"ERROR L53: U+2026 ellipsis missing, got {t!r}")
        sys.exit(1)

    # Agent brand: any target mentioning Agent must have it capitalized as 'Agent'.
    for eid, target in TRANSLATIONS.items():
        # Detect lowercase 'agent' as standalone English word in target — forbidden.
        if re.search(r"\bagent\b", target):
            print(f"ERROR {eid}: lowercase 'agent' in target; use 'Agent'. Got {target!r}")
            sys.exit(1)


def check_placeholders(src_entry, target):
    src = src_entry.get("source", "")
    src_phs = re.findall(r"\{[^{}]*\}", src)
    tgt_phs = re.findall(r"\{[^{}]*\}", target)
    if sorted(src_phs) != sorted(tgt_phs):
        return f"placeholder mismatch: source={src_phs} target={tgt_phs}"
    return None


def check_whitespace_preservation(src_entry, target, eid):
    """One-way preservation: if source has leading/trailing ws, target must too.
    Target may have extra leading/trailing ws (concat fragment cases) — that is
    asserted separately in check_invariants for the specific IDs.
    """
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
    assert len(TRANSLATIONS) == 43, f"Expected 43 translations, got {len(TRANSLATIONS)}"
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
    assert len(pre_snapshot) == 1468, f"Expected 1468 prior translated, got {len(pre_snapshot)}"

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
        err = check_whitespace_preservation(e, target, eid)
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
    print("Glossary delta: +fork +rule (credit already existed as '积分')")


if __name__ == "__main__":
    main()
