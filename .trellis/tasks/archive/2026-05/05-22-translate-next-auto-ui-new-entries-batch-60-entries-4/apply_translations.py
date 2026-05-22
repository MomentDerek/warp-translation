#!/usr/bin/env python3
"""Apply batch-4 translations (60 entries) to translations/strings.json.

Files cleared (all auto_ui-new):
  - app/src/workspace/view.rs (17)
  - app/src/quit_warning/mod.rs (16)
  - app/src/ai_assistant/panel.rs (10)
  - app/src/auth/auth_view_body.rs (8)
  - app/src/pane_group/mod.rs (8)
  - app/src/workspace/view/left_panel.rs (1) [pad]

Invariants:
  - placeholders preserved exactly ({} count + named placeholders such as {version}, {scope_suffix})
  - whitespace single-direction (no new leading/trailing space; preserve if source has it)
  - brand/path/JSON-literal verbatim (Warp, Warp AI, Warp Agent, MCP, Git, AWS, EC2, worktree)
  - ASCII `...` -> `……` (U+2026 doubled) where present
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
    # ------ workspace/view.rs (17) ------
    "01KQXQV128X02B566DEG5G692P": "在此访问您的标签页配置。",
    "01KQXQV12AEXSNW2MXMYTA1W0A": "当前版本为 {version}",
    "01KQXQV12CCQ7M2ENMDZYBB463": "安装更新（{}）",
    "01KQXQV12CXTS869VN5NFC0BE6": "邀请好友",
    "01KQXQV12DJK6HZMSEXMZX05RT": "新建标签页配置",
    "01KQXQV12DQ7CE410CG9EK27PV": "新建 worktree 配置",
    "01KQXQV12ERYY4NW1GVXPZC2P0": "请重新登录以恢复对云端功能的访问。",
    "01KQXQV12G09JYFD9W5TBDH2B9": "部分 Warp 功能在未立即更新时可能无法按预期工作，但 Warp 无法执行此次更新。",
    "01KQXQV12HBVS7DATJMHYT07FE": "正在更新至（{}）",
    "01KQXQV12HDNQAXWM6MY7J3WMX": "工具面板",
    "01KQXQV12HVC242QKJ7511HJ0C": "更新 Warp",
    "01KQXQV12HW07YW7RJC7Z3K76N": "更新并重启 Warp",
    "01KQXQV12HZ6N0JD4ZQAKM3EMJ": "新功能",
    "01KQXQV12J0MFA5NBATN92M6VB": "您的登录已过期。",
    "01KQXQV12J6TT5MZQ6A82DHSHT": "应用已过期，部分功能可能无法按预期工作。请立即更新。",
    "01KQXQV12JYMEDV8JZZAC7PXJ3": "应用已过期，需要更新。",
    "01KS2GEQ04DAXQX46KH3M3FDVZ": "从当前会话状态在云端继续此本地 Warp Agent 任务。",

    # ------ quit_warning/mod.rs (16) ------
    # 3 scope_suffix entries: source has LEADING ASCII space + trailing ASCII period.
    # Target preserves leading space (single-direction rule) and converts period to 。
    "01KQXQV1214YS0CEYDTVSRMY0K": " （位于此窗格）。",
    "01KQXQV1218WA166R3H2J2GQR2": " （位于此标签页）。",
    "01KQXQV1219N114H9S3RBQGXTD": " （位于此窗口）。",
    "01KQXQV12925HR740VRWK5AJ78": "关闭窗格？",
    "01KQXQV129AK83JY7SDE5M8D0H": "关闭标签页？",
    "01KQXQV129B2PS6DRWYKVRTH41": "关闭窗口？",
    "01KQXQV129X5H48ERD6BQ7FTWD": "关闭标签页？",
    "01KQXQV12BENEB9F66SD21PTEN": "不保存",
    "01KQXQV12BQA1F5QJRWM4RK3NN": "是否保存对 {} 所做的更改？如不保存，您的更改将被丢弃。",
    "01KQXQV12EMNR98FHHNCHEY8Y4": "退出 Warp？",
    "01KQXQV12FJQ0ZK9J5HHG6S6WJ": "保存更改？",
    "01KQXQV12J0PQZVBFH3DQ2722R": "您正在分享 {} {}{scope_suffix}",
    "01KQXQV12J7KY0GS918HEK548F": "是，关闭",
    "01KQXQV12JC2PRPCA2759RC9R8": "您有未保存的文件更改{scope_suffix}",
    "01KQXQV12JEGPQCCRDJFP56J6F": "您有 {} 个 {} 正在运行",
    "01KQXQV12JR7NCZBTWYP95A19R": "是，退出",

    # ------ ai_assistant/panel.rs (10) ------
    # Two entries have LEADING ASCII space (placeholder text cushion).
    "01KQXQV10N8SEYP4AK21K7JH87": " 提问……",
    "01KQXQV11RY5TZDZC609BR8PZZ": " 输入回复或点击上方任一选项……",
    "01KQXQV129PBQSABCH6PCP0D15": "关闭 Warp AI",
    "01KQXQV12AV1ZXW9WG7SC66JH1": "复制对话记录到剪贴板",
    "01KQXQV12C1N3119STH7GVT0M0": "从 Warp AI 聚焦到终端输入",
    "01KQXQV12C89VWPZMG13WCNF6V": "如何查找包含特定文本的所有文件？",
    "01KQXQV12CNPXDTB8AGHBBKNTD": "如何撤销 Git 中最近的提交？",
    "01KQXQV12EZWW21FZF0C6S6BMB": "重启 Warp AI",
    "01KQXQV12FW7Q2QGQDNC215Q23": "选中命令块或文本后按 Shift + ctrl + space 即可向 Warp AI 提问。",
    "01KQXQV12JS3KGSTC6VKT00EKY": "编写一个连接 AWS EC2 实例的脚本。",

    # ------ auth/auth_view_body.rs (8) ------
    # 5 entries with TRAILING ASCII space (link prefix glue).
    "01KQXQV1290B2BXXHGAW9NJ3BT": "继续即表示您同意 Warp 的 ",
    "01KQXQV1292TSY727D48NX2B0X": "已有账户？ ",
    "01KQXQV129D8BRAV7D4JNGAGDR": "认证令牌",
    "01KQXQV12B4F2C86ZTHRCA527D": "暂时不想登录？ ",
    "01KQXQV12CY05JA1GFN0TRPNY9": "如果浏览器未启动， ",
    "01KQXQV12ETVKKPMD9RWW4GEQ7": "隐私设置",
    "01KQXQV12J5C5PW6HDC6PXGMB0": "仅对已登录用户开放。 ",
    "01KQXQV12JEED5P4BERYQ53CQ4": "并手动打开页面。",

    # ------ pane_group/mod.rs (8) ------
    "01KQXQV12E5NBF8QGVAVWFA1H0": "调整窗格大小 > 向上移动分隔条",
    "01KQXQV12EJRJKTMXRVW3QNTG3": "调整窗格大小 > 向下移动分隔条",
    "01KQXQV12EPRHFYEY7H5KRBW9Y": "调整窗格大小 > 向左移动分隔条",
    "01KQXQV12EW9MTGTB8A4MKFMZJ": "调整窗格大小 > 向右移动分隔条",
    "01KQXQV12G799CZN2BB2CV0JF3": "切换到右侧窗格",
    "01KQXQV12G8Z673T24F40VTWC1": "切换到上方窗格",
    "01KQXQV12GADARX32XQW4452RY": "切换到下方窗格",
    "01KQXQV12GV9FBN6S4FC692C5R": "切换到左侧窗格",

    # ------ workspace/view/left_panel.rs (1, pad) ------
    "01KQXQV12937TNH3NRP95VRDQ9": "关闭面板",
}

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
BRAND_LITERALS = [
    "Warp Drive",
    "Warp Agent",
    "Warp AI",
    "Warp",
    "MCP",
    "Git",
    "AWS",
    "EC2",
    "worktree",
    "Shift",
    "ctrl",
    "space",
]


def placeholders(s: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(s))


def check_invariants(src: str, tgt: str, eid: str) -> list[str]:
    problems: list[str] = []
    src_ph = placeholders(src)
    tgt_ph = placeholders(tgt)
    if src_ph != tgt_ph:
        problems.append(f"placeholders differ: src={src_ph} vs tgt={tgt_ph}")

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
    # somewhere in target (case-insensitive accepted; e.g. "git" -> "Git" allowed).
    src_lower = src.lower()
    tgt_lower = tgt.lower()
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            if brand.lower() in tgt_lower:
                continue
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target unless source already had it AND we
    # decided to preserve verbatim (none in this batch — all converted to '……').
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
