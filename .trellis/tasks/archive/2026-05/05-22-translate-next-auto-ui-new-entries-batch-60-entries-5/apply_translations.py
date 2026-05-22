#!/usr/bin/env python3
"""Apply batch-5 translations (60 entries) to translations/strings.json.

Files cleared (all auto_ui-new):
  - app/src/drive/workflows/modal.rs (7)
  - app/src/settings_view/features/external_editor.rs (7)
  - app/src/code/file_tree/view.rs (7)
  - app/src/settings_view/billing_and_usage/billing_cycle_usage_section.rs (7)
  - app/src/code/view.rs (6)
  - app/src/ai_assistant/transcript.rs (6)
  - app/src/drive/cloud_action_confirmation_dialog.rs (6)
  - app/src/ai/ai_document_view.rs (6)
  - app/src/settings_view/keybindings.rs (6)
  - app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs (2)

Invariants:
  - placeholders preserved exactly ({} count + named placeholders).
  - strftime format directives (%b/%d/%-I/%M/%p) preserved verbatim.
  - whitespace single-direction (no new leading/trailing space; preserve if src has it).
  - brand/path/JSON-literal verbatim (Warp, Warp AI, Warp Drive, Markdown, WSL, MCP, Git,
    Business, credit, cd).
  - ASCII `...` -> `……` (U+2026 doubled) where present.
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STRINGS_PATH = ROOT / "translations" / "strings.json"

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str] = {
    # ------ drive/workflows/modal.rs (7) ------
    "01KQXQV12HSGVFPE2QRFK8FHE6": "未命名工作流",
    "01KQXQV1281ZWHHWZF7BPR5MMA": "添加描述",
    "01KQXQV12D2HZ9YKHQCW5SBTKC": "新建参数",
    "01KQXQV12A6AZPG0305YYCPF0N": "默认值（可选）",
    "01KQXQV12FT6BJ59B1Q2GWNZHZ": "保存工作流",
    "01KQXQV12J87PQNW8QNA5XFXRS": "您有未保存的更改。",
    "01KQXQV12DNC2K24X9Q844YX7D": "继续编辑",

    # ------ settings_view/features/external_editor.rs (7) ------
    "01KQXQV12CXVG5KN85CVS19XFM": "将文件分组到同一编辑器窗格",
    "01KQXQV12H98VQ8VHZ2D69E567": "开启此设置后，同一标签页中打开的任何文件都将自动分组到同一编辑器窗格。",
    "01KQXQV12AKP15Q77BX3B1TC31": "默认应用",
    "01KQXQV1292ZEWS1JA2ZFSD8NQ": "选择用于打开文件链接的编辑器",
    "01KQXQV129F49S92XA0VHCFDA5": "选择用于从代码评审面板、项目浏览器和全局搜索打开文件的编辑器",
    "01KQXQV129SV75C8035770V94J": "选择在 Warp 中打开文件的布局",
    "01KQXQV12D7EH88EJQQA0NMXY6": "默认使用 Warp 的 Markdown 查看器打开 Markdown 文件",

    # ------ code/file_tree/view.rs (7) ------
    "01KQXQV12G6ZKB2CYEPTV5X14Z": "项目浏览器需要访问您的本地工作区，这在远程会话中不受支持。",
    "01KQXQV12GHQ0RRKWYPVX4ZA4M": "项目浏览器需要访问您的本地工作区。请打开新会话或切换到活动会话查看。",
    "01KQXQV12GS082X8GXFBTKN84Y": "项目浏览器目前在 WSL 中不可用。",
    "01KQXQV12DMH981WWXM3M23B7P": "新建文件",
    "01KRBDMFW6WXRTD2HWA7DT2GB1": "cd 到目录",
    "01KQXQV1294KDXV6CDXSSPXHPQ": "作为上下文附加",
    "01KQXQV12AY1P143VX80C5CYZB": "复制相对路径",

    # ------ settings_view/billing_and_usage/billing_cycle_usage_section.rs (7) ------
    # strftime format directives preserved verbatim.
    "01KS2GEQJRYS4Z9459JS6FDMT6": "%b %d %-I:%M %p 重置",
    "01KS2GEQS0C7FHH4N1WGTTD2PB": "查看团队级 credit 用量。",
    "01KS2GEQPK7KCYT8MRMY4JZC3K": "升级到 Business",
    "01KS2GEQRZRDD94EET1BZ5ZWEC": "查看每位用户的 credit 归属。",
    "01KS2GEQRYV1T4NQ8JQ3M69V3K": "查看细粒度 credit 归属并设置每位用户的支出上限。",
    "01KS2GEQS17KEK10MJ368CYH3Q": "设置每位用户的支出上限。",
    "01KS2GEQE6HWJRJ0CBCEMJAZRJ": "其他团队成员在附加包、按量付费和云端专属 credit 上的用量。",

    # ------ code/view.rs (6) ------
    "01KQXQV12FE27129PB0GHKSD95": "保存文件",
    "01KQXQV12F3HMZSHZDZW1XVWWZ": "文件另存为",
    "01KQXQV129WFPMXK2XMK8JZ2X6": "关闭所有标签页",
    "01KQXQV129BHXPQ0JJ8P7DFGMB": "关闭已保存的标签页",
    "01KQXQV128DBE6DHP7HKX7Z59G": "接受并保存",
    "01KQXQV12H2B0SEKFBAJ9M4DGW": "查看 Markdown 预览",

    # ------ ai_assistant/transcript.rs (6) ------
    "01KQXQV12CF92SBBMP1Q4795XE": "我该如何修复这个问题？",
    "01KQXQV12FEKDF16JG7WRRDANS": "展示一些示例。",
    "01KQXQV12H4ZCJ2DFAKCHA1324": "接下来我该做什么？",
    "01KQXQV12CB22K3WDC4KH5W4SR": "正在生成回复……",
    "01KQXQV128EYTNG5GEM6KABSRM": "AI 的回复可能不准确。",
    "01KQXQV12HJQ8JQTWJCE6XR2XC": "当对话变长时，Warp AI 可能会遗忘早期的回答。",

    # ------ drive/cloud_action_confirmation_dialog.rs (6) ------
    "01KQXQV129XN6ZCDWSCQDZR6K7": "确定要删除此团队吗？",
    "01KQXQV129PS980CXV1ZZF3N15": "确定要离开此团队吗？",
    "01KQXQV12A7J40EGJMA10YEAK8": "删除此团队将永久删除该团队及其所有相关内容，包括账单信息和 credit。删除后将无法恢复。",
    "01KQXQV12J5X827743SAS7TRG0": "如需重新加入，您需要被再次邀请。",
    "01KQXQV12JZD3VJVK14963H941": "是，删除",
    "01KQXQV12JQ9Q4MXX7M0YAT33F": "是，离开",

    # ------ ai/ai_document_view.rs (6) ------
    "01KQXQV12EBP82BPC0XBDS31X1": "规划文档",
    "01KQXQV12G0V0BPPHWAD4ZCVT9": "显示版本历史",
    "01KQXQV12FMW5EGKZ6BPHCE3PY": "保存并自动同步此规划到您的 Warp Drive",
    "01KQXQV12G6WQ76XWX56V8K3X4": "在 Warp Drive 中显示",
    "01KQXQV12FRDE6N9N39Z0G8ZJA": "另存为 Markdown 文件",
    "01KQXQV12AWMXQ3W55AASYZYWX": "复制规划 ID",

    # ------ settings_view/keybindings.rs (6) ------
    "01KQXQV12FF2YDGK2QQ3YMNG0D": "按名称或按键搜索（例如 \"cmd d\"）",
    "01KQXQV12GZNS8K1SH5EEQBY1F": "此快捷键与其他键位冲突",
    "01KQXQV129ZEF1W5T9CJXNG960": "为下方现有操作添加您的自定义键位。",
    "01KQXQV12J4ZP4SNXWQCW51RAQ": "即可随时在侧边面板查阅这些键位。",
    "01KQXQV12D2B3807CY030V11B3": "键盘快捷键不会同步到云端",
    "01KQXQV12AKE5CXQ0KT2HREYMM": "配置键盘快捷键",

    # ------ settings_view/billing_and_usage/billing_cycle_usage_common.rs (2) ------
    "01KS2GEQN6CFV21S1T1XEDC350": "建议的代码差异",
    "01KS2GEQP1QSVQW6RBH1DFPR99": "总用量",
}

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
# chrono / strftime format directives we must preserve verbatim.
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

BRAND_LITERALS = [
    "Warp Drive",
    "Warp Agent",
    "Warp AI",
    "Warp",
    "Markdown",
    "MCP",
    "WSL",
    "Git",
    "Business",
    "credit",
    "cd",
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

    # brand literals: each brand literal that appears in source must remain
    # somewhere in target (case-insensitive accepted).
    tgt_lower = tgt.lower()
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            if brand.lower() in tgt_lower:
                continue
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target unless source already had it.
    if "..." in tgt and "..." not in src:
        problems.append("introduced ASCII '...' (should be '……')")

    return problems


# --- apply ------------------------------------------------------------------


def main() -> int:
    with STRINGS_PATH.open() as f:
        data = json.load(f)

    by_id = {e["id"]: e for e in data["entries"]}
    missing = [eid for eid in TRANSLATIONS if eid not in by_id]
    if missing:
        print("missing ids:", missing, file=sys.stderr)
        return 1

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
        problems = check_invariants(src, tgt, eid)
        if problems:
            errors.append(f"{eid}: {problems}\n  src={src!r}\n  tgt={tgt!r}")
            continue
        entry["target"] = tgt
        entry["status"] = "translated"
        applied += 1

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    # update aggregate stats
    from collections import Counter
    status_counter = Counter(e["status"] for e in data["entries"])
    if "stats" in data:
        data["stats"]["translated"] = status_counter.get("translated", 0)
        data["stats"]["new"] = status_counter.get("new", 0)
        data["stats"]["fuzzy"] = status_counter.get("fuzzy", 0)

    with STRINGS_PATH.open("w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"applied {applied}/60 translations")
    print(f"stats: {dict(status_counter)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
