#!/usr/bin/env python3
"""Apply batch-6 translations (60 entries) to translations/strings.json.

Files cleared (20 files, 18 fully zeroed; 2 retain 1 cross-file shared entry each):
  - app/src/auth/auth_override_warning_body.rs (3)
  - app/src/auth/login_slide.rs (3)
  - app/src/auth/needs_sso_link_view.rs (3)
  - app/src/cloud_object/grab_edit_access_modal.rs (3)
  - app/src/drive/cloud_object_naming_dialog.rs (3)
  - app/src/drive/empty_trash_confirmation_dialog.rs (3)
  - app/src/drive/sharing/dialog/mod.rs (4)
  - app/src/notebooks/file/mod.rs (3)
  - app/src/settings_view/billing_and_usage/billing_cycle_usage_rows.rs (3)
  - app/src/settings_view/billing_and_usage/billing_cycle_usage_team_totals.rs (3)
  - app/src/settings_view/features/working_directory.rs (3) [retains 'New tab']
  - app/src/settings_view/privacy/add_regex_modal.rs (3)
  - app/src/workspace/close_session_confirmation_dialog.rs (3) [retains "Don't show again."]
  - app/src/workspace/delete_conversation_confirmation_dialog.rs (3)
  - app/src/workspace/rewind_confirmation_dialog.rs (3)
  - app/src/workspace/view/conversation_list/view.rs (3)
  - crates/warpui/src/platform/mac/menus.rs (3) [1 doc-comment FP + 2 menu items]
  - crates/warpui/src/rendering/wgpu/renderer.rs (3) [all wgpu debug labels]
  - crates/warpui/src/rendering/wgpu/resources/quad.rs (2) [all wgpu debug labels]
  - crates/warpui/src/rendering/wgpu/resources/uniforms.rs (3) [all wgpu debug labels]

Invariants:
  - placeholders preserved exactly ({} count + named placeholders).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/path/JSON-literal verbatim (Warp, Warp Drive, Notebook, SSO, Agent, Fork, shell).
  - ASCII `...` -> `……` (none in this batch).
  - DO_NOT_TRANSLATE_IDS: target=None, status=translated, flags add do_not_translate (+ specialized flag).

Special handling:
  - WGPU_DEBUG_LABEL_IDS (8): wgpu debug labels (developer-only). target=None +
    flags=[batch_flag, do_not_translate, wgpu_debug_label].
  - DOC_COMMENT_FP_IDS (1): extractor false positive on /// doc-comment. target=None +
    flags=[batch_flag, do_not_translate, extractor_false_positive_doc_comment].
"""

from __future__ import annotations
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STRINGS_PATH = ROOT / "translations" / "strings.json"
CANDIDATES = Path(__file__).resolve().parent / "candidates.json"

BATCH_FLAG = "pr-drive-auth-workspace-warpui-billing-batch"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str | None] = {
    # ====== app/src/auth/auth_override_warning_body.rs (3) ======
    "01KQXQV12DYHB1JYEZY64PBG3W": "检测到您已通过浏览器登录 Warp 账户。如果继续，此匿名会话中的所有个人 Warp Drive 对象和偏好设置都将被永久删除。",
    "01KQXQV12BX5F2BHDM3YY4148Z": "导出您的数据",
    "01KQXQV127223FBVARD86DQQMT": " 以便后续导入。",  # leading space preserved

    # ====== app/src/auth/login_slide.rs (3) ======
    "01KQXQV12CY723VVKF8RS22MPG": "如需选择退出数据分析,您可以调整您的 ",  # placeholder for full-width comma check below
    "01KQXQV11XDPA63Q5CES42MENF": " 并手动打开",  # leading space preserved, no trailing
    "01KQXQV12JKQ2308RBVNNW8D46": "该页面。",

    # ====== app/src/auth/needs_sso_link_view.rs (3) ======
    "01KQXQV12D7WG3VZKSEVPM8C8Z": "关联 SSO",
    "01KQXQV12J4EM1HV0EQTA43XCY": "您所在的组织已为您的账户启用 SSO",
    "01KQXQV12942ERGYGFHE8F2GDE": "点击下方按钮,将您的 Warp 账户关联到您的 SSO 提供商。",

    # ====== app/src/cloud_object/grab_edit_access_modal.rs (3) ======
    "01KQXQV12B6PN1T9QFPDV1KN8K": "仍然编辑",
    "01KQXQV12CAXJWZR5Z2BPGE662": "如果您接管编辑权,当前编辑者将被强制切换到查看模式",
    "01KQXQV12G03W29SRR7AK0PA72": "此 Notebook 正在被编辑",

    # ====== app/src/drive/cloud_object_naming_dialog.rs (3) ======
    "01KQXQV12D45F4FBCBHBMJDJ9R": "Notebook 名称",
    "01KQXQV12C0GTVH82SHJ1EJMTE": "文件夹名称",
    "01KQXQV12AWFBFNRW28MS236MS": "集合名称",

    # ====== app/src/drive/empty_trash_confirmation_dialog.rs (3) ======
    "01KQXQV129A95591A60H6ZGYYY": "确定要清空回收站吗？",
    "01KQXQV12G9P8C77RT5J7NADYY": "此操作无法撤销。",
    "01KQXQV12JAWWKWPEEXPX1Q3V1": "是,清空回收站",

    # ====== app/src/drive/sharing/dialog/mod.rs (4) ======
    "01KQXQV12D2RBHV39FWV7HTTKY": "无访问权限",
    "01KQXQV12JADQ6Z191DXT389PS": "谁有访问权限",
    "01KQXQV12DRPMKAFQS2P2MFXXX": "仅限受邀的团队成员",
    "01KQXQV12GX5M5KBJPVBYBDSBG": "拥有链接的团队成员",

    # ====== app/src/notebooks/file/mod.rs (3) ======
    "01KQXQV12CVTCAW72890PSRYXP": "从文件聚焦终端输入",
    "01KQXQV12EKQ2PRFHVFXTQX10Q": "重新加载文件",
    "01KQXQV12E11K8EKAE415X13NM": "刷新文件",

    # ====== billing_and_usage/billing_cycle_usage_rows.rs (3) ======
    "01KS2GEQDT3RJHEPFPH6BN6KJ0": "其他成员",
    "01KS2GEQNVE139ZHZDKJ26W49T": "这是您团队中的自动化 Agent。",
    "01KS2GEQRA6MKG7EFGFEMMHWYY": "您的用量",

    # ====== billing_and_usage/billing_cycle_usage_team_totals.rs (3) ======
    "01KS2GEQE9F18FAJQCCM8PQSEC": "整体用量",
    "01KS2GEQBA0JJWTXZ5HB3HTC65": "本地 Agent 用量",
    "01KS2GEQA89VHY1S55KCRVZHM6": "上限:{}",  # placeholder check below; full-width colon

    # ====== settings_view/features/working_directory.rs (3) ======
    "01KQXQV12DT0NM0EKP3X6V9XPA": "新建窗口",
    "01KQXQV12GPGPE6SA2436H22RC": "拆分窗格",
    "01KQXQV12ATMXSBBHCHYPRYRNS": "目录路径",

    # ====== settings_view/privacy/add_regex_modal.rs (3) ======
    "01KQXQV12DBHJ42PRG0YWPXKVT": "名称(可选)",  # full-width parens applied below
    "01KQXQV12EBRY3AY2KXCAZRNDP": "正则表达式模式",
    "01KQXQV12C25HBXT5WA7Z5Z5Q1": "无效的正则表达式",

    # ====== workspace/close_session_confirmation_dialog.rs (3) ======
    "01KQXQV129EYGQ2D4FJ8JY0YKW": "关闭会话",
    "01KQXQV129DYGPVTBHVF6RR4NW": "关闭会话？",
    "01KQXQV12J3SV3CZESK93GN0VX": "您即将关闭一个正在共享的会话。关闭后,所有参与者的共享都将终止。",

    # ====== workspace/delete_conversation_confirmation_dialog.rs (3) ======
    "01KQXQV12ATG9DV1DCXJ57S53D": "删除 '{}'？",  # placeholder + ASCII quote preserved + full-width ?
    "01KQXQV12AC2RGSJTQ39THPP56": "删除对话？",
    "01KQXQV12GVBQZ9F6Q9TNKVEDT": "此对话将被永久删除。此操作无法撤销。",

    # ====== workspace/rewind_confirmation_dialog.rs (3) ======
    "01KQXQV12E2JCG7BF6Q3JPVHC6": "倒带操作不会影响通过手动编辑或 shell 命令修改的文件。",
    "01KQXQV12E7BCH9C5P1RKMRXRC": "倒带",
    "01KQXQV129GFC4A82CCE36854Y": "确定要倒带吗?此操作会将您的代码和对话恢复到此节点之前,并取消 Agent 当前正在运行的所有命令。原对话的副本将保存在您的对话历史中。",

    # ====== workspace/view/conversation_list/view.rs (3) ======
    "01KQXQV12HA3S3G62QPXMTWWVF": "查看全部",
    "01KQXQV12CN3TKVXJH7MSBJCXE": "在新窗格中派生",
    "01KQXQV12CNA9Q14EPDF9SCV36": "在新标签页中派生",

    # ====== crates/warpui/src/platform/mac/menus.rs (3) ======
    # L31 is doc-comment FP -> target=None (set below)
    "01KQXQV10K08VKM1PTG55SSRGM": None,
    "01KQXQV12FC5SBSAXZ4GY98E09": "显示全部",
    "01KQXQV129YDKRM2XKH2AY5XPC": "全部窗口前置",

    # ====== crates/warpui/src/rendering/wgpu/renderer.rs (3) wgpu debug labels ======
    "01KQXQV12AP6S38RJP1W8AKSY9": None,
    "01KQXQV12C8BKH2Q9W1GQD5YMY": None,
    "01KQXQV12CSGCKT3VYQ3HT8YC6": None,

    # ====== crates/warpui/src/rendering/wgpu/resources/quad.rs (2) ======
    "01KQXQV12EG44FXM3F1C25N0GX": None,
    "01KQXQV12E35NPKXJ1SWMXXMR2": None,

    # ====== crates/warpui/src/rendering/wgpu/resources/uniforms.rs (3) ======
    "01KQXQV12EG48VSPTAX8RZ997G": None,
    "01KQXQV12H6RT5M0NY1GBXSFYQ": None,
    "01KQXQV12H9WNMRS299SQ5FR7G": None,
}

# Patch in full-width punctuation (中文逗号 / 全角冒号 / 全角括号) using post-processing.
# I built the strings above with ASCII commas/colons/parens to keep the source readable;
# convert them now to the appropriate full-width forms (only those adjacent to CJK).
def to_full_width_chinese_punct(s: str) -> str:
    if s is None:
        return s
    # Replace ASCII comma -> 中文逗号 if preceded by CJK character.
    s = re.sub(r"(?<=[一-鿿]),(?!\s*[a-zA-Z0-9])", "，", s)
    # ASCII colon -> 中文冒号 if preceded by CJK and not followed by digit/path-like.
    # Note: '{' is NOT in exclusion — '上限:{}' should become '上限：{}'.
    s = re.sub(r"(?<=[一-鿿]):(?![0-9a-zA-Z/\\])", "：", s)
    # ASCII parens -> full-width parens when the content is CJK (i.e., the paren wraps Chinese content)
    s = re.sub(r"\(([一-鿿]+)\)", r"（\1）", s)
    # ASCII question mark -> 全角 if preceded by CJK
    s = re.sub(r"(?<=[一-鿿])\?", "？", s)
    return s


for k in list(TRANSLATIONS.keys()):
    v = TRANSLATIONS[k]
    if isinstance(v, str):
        TRANSLATIONS[k] = to_full_width_chinese_punct(v)


# DO_NOT_TRANSLATE classifications
WGPU_DEBUG_LABEL_IDS = {
    # renderer.rs
    "01KQXQV12AP6S38RJP1W8AKSY9",
    "01KQXQV12C8BKH2Q9W1GQD5YMY",
    "01KQXQV12CSGCKT3VYQ3HT8YC6",
    # quad.rs
    "01KQXQV12EG44FXM3F1C25N0GX",
    "01KQXQV12E35NPKXJ1SWMXXMR2",
    # uniforms.rs
    "01KQXQV12EG48VSPTAX8RZ997G",
    "01KQXQV12H6RT5M0NY1GBXSFYQ",
    "01KQXQV12H9WNMRS299SQ5FR7G",
}
DOC_COMMENT_FP_IDS = {
    "01KQXQV10K08VKM1PTG55SSRGM",  # mac/menus.rs L31
}
DO_NOT_TRANSLATE_IDS = WGPU_DEBUG_LABEL_IDS | DOC_COMMENT_FP_IDS

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

BRAND_LITERALS = [
    "Warp Drive",
    "Warp",
    "Notebook",
    "SSO",
    "Agent",
    "Fork",
    "shell",
    "MCP",
    "Markdown",
    "Git",
    "WSL",
]


def placeholders(s: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(s))


def strftime_codes(s: str) -> list[str]:
    return sorted(STRFTIME_RE.findall(s))


def check_invariants(src: str, tgt: str, eid: str) -> list[str]:
    problems: list[str] = []
    src_ph = placeholders(src)
    tgt_ph = placeholders(tgt)
    if src_ph != tgt_ph:
        problems.append(f"placeholders differ: src={src_ph} vs tgt={tgt_ph}")

    src_strf = strftime_codes(src)
    tgt_strf = strftime_codes(tgt)
    if src_strf != tgt_strf:
        problems.append(f"strftime directives differ: src={src_strf} vs tgt={tgt_strf}")

    # whitespace single-direction
    if src.startswith(" ") != tgt.startswith(" "):
        problems.append("leading whitespace mismatch")
    if src.endswith(" ") != tgt.endswith(" "):
        problems.append("trailing whitespace mismatch")
    if src.startswith("\n") != tgt.startswith("\n"):
        problems.append("leading newline mismatch")
    if src.endswith("\n") != tgt.endswith("\n"):
        problems.append("trailing newline mismatch")

    # brand literals: each brand literal that appears in source must remain in target.
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target unless source already had it.
    if "..." in tgt and "..." not in src:
        problems.append("introduced ASCII '...' (should be '……')")

    # No bare ASCII ellipsis allowed.
    if "..." in tgt and "..." in src and tgt.count("...") != src.count("..."):
        problems.append("'...' count differs from source")

    return problems


def main() -> int:
    with STRINGS_PATH.open() as f:
        data = json.load(f)

    cands = json.loads(CANDIDATES.read_text())
    cand_ids = {c["id"] for c in cands}
    assert set(TRANSLATIONS.keys()) == cand_ids, (
        f"Translation keys != candidates: missing={cand_ids - TRANSLATIONS.keys()}, "
        f"extra={TRANSLATIONS.keys() - cand_ids}"
    )

    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}
    missing = [eid for eid in TRANSLATIONS if eid not in by_id]
    if missing:
        print("missing ids:", missing, file=sys.stderr)
        return 1

    pre_translated = sum(1 for e in entries if e["status"] == "translated")
    pre_snapshot = {
        e["id"]: (e.get("target"), e["status"])
        for e in entries
        if e["status"] == "translated"
    }

    errors: list[str] = []
    applied = 0
    for eid, tgt in TRANSLATIONS.items():
        entry = by_id[eid]
        if entry["status"] != "new":
            errors.append(f"{eid}: status not 'new' (got {entry['status']!r})")
            continue
        if entry.get("audit", {}).get("verdict") != "auto_ui":
            errors.append(f"{eid}: verdict not 'auto_ui'")
            continue
        src = entry["source"]

        if eid in DO_NOT_TRANSLATE_IDS:
            if tgt is not None:
                errors.append(f"{eid}: DO_NOT_TRANSLATE_IDS must have None target, got {tgt!r}")
                continue
            entry["target"] = None
            entry["status"] = "translated"
            flags = entry.get("flags") or []
            for flag in (BATCH_FLAG, "do_not_translate"):
                if flag not in flags:
                    flags.append(flag)
            if eid in WGPU_DEBUG_LABEL_IDS and "wgpu_debug_label" not in flags:
                flags.append("wgpu_debug_label")
            if eid in DOC_COMMENT_FP_IDS and "extractor_false_positive_doc_comment" not in flags:
                flags.append("extractor_false_positive_doc_comment")
            entry["flags"] = flags
            entry["updated_at"] = NOW
            applied += 1
            continue

        if tgt is None:
            errors.append(f"{eid}: tgt is None but eid not in DO_NOT_TRANSLATE_IDS")
            continue

        problems = check_invariants(src, tgt, eid)
        if problems:
            errors.append(f"{eid}: {problems}\n  src={src!r}\n  tgt={tgt!r}")
            continue

        entry["target"] = tgt
        entry["status"] = "translated"
        flags = entry.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        entry["flags"] = flags
        entry["updated_at"] = NOW
        applied += 1

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    # Post-mutation: pre_snapshot byte-identical
    for eid, (prev_target, prev_status) in pre_snapshot.items():
        e = by_id[eid]
        if e.get("target") != prev_target or e["status"] != prev_status:
            print(f"ERROR: prior translated entry mutated: {eid}", file=sys.stderr)
            return 1

    status_counter = Counter(e["status"] for e in entries)
    md = data.setdefault("metadata", {})
    stats = md.setdefault("stats", {})
    stats["new"] = status_counter.get("new", 0)
    stats["translated"] = status_counter.get("translated", 0)
    stats["fuzzy"] = status_counter.get("fuzzy", 0)
    stats["approved"] = status_counter.get("approved", 0)
    stats["obsolete"] = status_counter.get("obsolete", 0)
    # 'uncertain' is an audit verdict, not a status; preserve prior value.
    md["entry_count"] = len(entries)
    md["last_changed_at"] = NOW

    STRINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"applied {applied}/60 translations")
    print(f"stats: {dict(status_counter)}")
    print(f"pre_translated={pre_translated} -> post_translated={status_counter.get('translated', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
