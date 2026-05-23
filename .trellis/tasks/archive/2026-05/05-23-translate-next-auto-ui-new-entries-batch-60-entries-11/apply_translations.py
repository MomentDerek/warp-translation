#!/usr/bin/env python3
"""Apply batch-11 translations (64 entries) to translations/strings.json.

Strategy: finish 21 auto_ui-new leaves + expand into 22 code/footer.rs LSP
labels + 21 notebooks/editor/view.rs a11y action labels = 64 entries.
auto_ui-new hotspot zeroed after this batch.

Files cleared (23 unique files; 64 entries):
  - 22 entries in app/src/code/footer.rs (LSP/language server mgmt UI labels)
  - 21 entries in app/src/notebooks/editor/view.rs (a11y action descriptions
    + 1 `.expect` panic at L2103)
  - 21 single-entry leaves across util/onboarding/terminal/workspace/
    workflows/editor/ui_components/warpui_core etc.

Special handling:
  - No DO_NOT_TRANSLATE in this batch.
  - 2 .expect panic strings translated (native_modal L163, view.rs L2103).
  - ASCII '...' -> '……' (1 occurrence: 'Installing {}...').
  - `'/'` -> `『/』` (1 occurrence: paragraph.rs L15).

Invariants:
  - placeholders preserved exactly (positional {} and named {root_name}/
    {code_block_type}).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/path/literal verbatim (Warp, Warp on Web, Oz, Agent, MCP, Markdown,
    Xwayland, Profile, chip, worktree, /update-tab-config).
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

BATCH_FLAG = "pr-long-tail-ui-leaves-code-footer-notebook-editor-batch-11"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str | None] = {
    # ====== app/src/util/tooltips.rs (1) ======
    "01KQXQV128JN2JRX0BYNZV0B9S": "*机密信息不会发送至 Warp 服务器。",

    # ====== crates/onboarding/src/slides/third_party_slide.rs (1) ======
    "01KQXQV129M97YSH8GF78FRBAZ": "CLI Agent 工具栏",

    # ====== app/src/terminal/input/conversations/view.rs (1) ======
    "01KQXQV12AS0865E39T56FM7P4": "当前目录",

    # ====== app/src/terminal/shared_session/role_change_modal/sharer_grant_body.rs (1) ======
    "01KQXQV12B71JN4J8FYR2SAQMM": "不再显示。",

    # ====== app/src/workspace/header_toolbar_editor.rs (1) ======
    "01KQXQV12BBZABG9EX7CJ1G757": "编辑工具栏",

    # ====== app/src/terminal/input/models/view.rs (1) ======
    "01KQXQV12CCJQ8ZWXH2XX6YDXH": "完整终端能力",

    # ====== app/src/view_components/find.rs (1) ======
    "01KQXQV12CW7VPTP38A0BJJN80": "在选中命令块中查找",

    # ====== crates/onboarding/examples/callout.rs (1) ======
    "01KQXQV12DB8AVGNF99AKWQZNZ": "认识您的 Warp 输入",

    # ====== app/src/workspace/view/build_plan_migration_modal.rs (1) ======
    "01KQXQV12DBGSZW0210MK25N47": "糟糕，出错了；未能找到您团队的数据。",

    # ====== app/src/workspace/native_modal.rs (1) - .expect panic ======
    "01KQXQV12DR2R2QYFB7EFQWFCD": "模态按钮应已设置鼠标状态",

    # ====== app/src/terminal/input/profiles/search_item.rs (1) ======
    "01KQXQV12DV0KBS22B01725PKC": "管理 Profile",

    # ====== app/src/tab_configs/session_config.rs (1) ======
    "01KQXQV12DY82VRSRV726VYXKT": "新建 worktree 分支名",

    # ====== crates/ui_components/src/lightbox.rs (1) ======
    "01KQXQV12DYXPJJM484CRV3TZ4": "没有图片",

    # ====== app/src/terminal/shared_session/share_modal/body.rs (1) ======
    "01KQXQV12FT2BFZVMW8NACFB8B": "从选中命令块开始分享",

    # ====== app/src/terminal/shared_session/sharer/network.rs (1) ======
    "01KQXQV12FVH966QDG3WH3YCQQ": "今日会话分享用量已用完。请稍后重试。",

    # ====== app/src/workflows/local_workflows.rs (1) ======
    "01KQXQV12GZVF44C24JS1S2MQ2": "显示提示词上下文 chip 运行的 shell 命令诊断日志（仅限内部测试）",

    # ====== crates/editor/src/render/element/paragraph.rs (1) ======
    "01KQXQV12H2YXM451D0MCNZS56": "键入文本或 Markdown，或输入 『/』 以插入内容",

    # ====== app/src/workspace/view/crash_recovery.rs (1) ======
    "01KQXQV12H3PHF5THXE9BRGJ3R": "我们检测到应用启动时发生了崩溃，已调整您的设置改用 Xwayland 进行窗口管理。如果您正在使用分数缩放，这可能导致文本模糊。",

    # ====== app/src/workspace/view/vertical_tabs.rs (1) ======
    "01KQXQV12H7YBWXR56KZ4Q64HV": "视图选项",

    # ====== crates/warpui_core/src/core/app.rs (1) ======
    "01KQXQV12HJKGBMP0EY7RRC3SH": "视图树调试器",

    # ====== app/src/workspace/home.rs (1) ======
    "01KQXQV12HQZAW4PS4Z87DVANT": "欢迎使用 Warp on Web",

    # ====== app/src/code/footer.rs (22) ======
    "01KQXQV12BNGHWDFE4B49YAD7K": "启用服务器",
    "01KQXQV12BRZ68XRATEWWFGEQC": "允许 AI 使用 /update-tab-config 技能",
    "01KQXQV12BSHTS1PH6M74KY7PV": "启用 {}",
    "01KQXQV12C61KWYKWMEGAS3922": "正在安装 {}……",
    "01KQXQV12CDC500EDAPPTJE31N": "安装服务器",
    "01KQXQV12CGHH5BNS3055Y45AQ": "安装 {}",
    "01KQXQV12D0QZ2EYGD6P5STFBV": "{root_name} 没有可用的语言支持",
    "01KQXQV12D38BV4S4CG5WZAY0V": "管理服务器",
    "01KQXQV12DB2FPQTKNDX2NM1KH": "{} 当前未启用语言支持",
    "01KQXQV12DG4T2AQB4D9YDJB5Z": "此代码库没有可用的语言服务器",
    "01KQXQV12DJYRT6000GJKNW1B5": "{root_name} 当前未启用语言支持",
    "01KQXQV12DP7BDAZGYY0DS8JFZ": "此文件类型没有可用的语言支持",
    "01KQXQV12E1BWXJJ6S64NPG107": "重启所有服务器",
    "01KQXQV12EH3BY4XWTVSJ3KA1D": "打开日志",
    "01KQXQV12ENYZHN0VMM2MJ464F": "使用 /update-tab-config 技能打开 Agent 输入",
    "01KQXQV12EYWK584GRN3X0SHTP": "移除服务器",
    "01KQXQV12G3GMVHPJN979CKVY3": "启动所有已停止的服务器",
    "01KQXQV12GCY62C8BAXYDP3JRQ": "停止所有服务器",
    "01KQXQV12GEKM8K6VWV6VYM8V7": "停止服务器",
    "01KQXQV12GRJNJ102A44ZQXPS5": "启动所有服务器",
    "01KQXQV12GRRRCHFSXKVP44T83": "启动服务器",
    "01KQXQV12HWCEMYF6TFGDZ51DN": "用 Oz 更新此配置",

    # ====== app/src/notebooks/editor/view.rs (21) ======
    "01KQXQV129YS0P2BPCBK4K6EDH": "将代码块语言切换为 {code_block_type}",
    "01KQXQV12A1ZMWYR17S9FY6RHA": "删除左侧整行",
    "01KQXQV12A6CVNCN3S0XFG5QF8": "剪切左侧整行",
    "01KQXQV12AE1P84YPW3JHEGX81": "复制代码块",
    "01KQXQV12AG0HQ8QD6EVSRJ2W2": "取消选中命令",
    "01KQXQV12ANKTQQWEE623CM7D3": "复制链接",
    "01KQXQV12ARM95N3SDAGGFV77A": "删除右侧整行",
    "01KQXQV12AX4FC87Q5XZ8KQWB9": "剪切右侧整行",
    "01KQXQV12BZV7PTD470RXQY5Z5": "编辑链接",
    "01KQXQV12C1N173BJ4TA04Z4HB": "插入 {} 命令块",
    "01KQXQV12D219137720CXV0ZB9": "上方刚刚检查过",
    "01KQXQV12DCJ1V9QZ39WJE5F0M": "链接已复制",
    "01KQXQV12E5H16FRVFP3J0NX5M": "打开命令块插入菜单",
    "01KQXQV12E77KCFF82TZ3HFZ06": "打开嵌入对象搜索菜单",
    "01KQXQV12EA2QXCD68T69GA7T1": "打开文件夹",
    "01KQXQV12EB92XBTVY6BQGMASY": "打开链接：{}",
    "01KQXQV12F26VTYD04PPVQC8XZ": "显示查找栏",
    "01KQXQV12FPPYRQ9VY2CYZDFS6": "显示字符面板",
    "01KQXQV12FSEEQ7DRXK027SBWB": "在 {} 上右键单击",
    "01KQXQV12GRHY9YSZBKVFC8V0Y": "从选中命令切换到选中文本",
    "01KQXQV12HK69JYGVCPKDSM4C9": "切换任务列表",
}

DO_NOT_TRANSLATE_IDS: set[str] = set()  # none this batch

assert len(TRANSLATIONS) == 64, f"expected 64, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

# Brand/literals that must remain verbatim if present in source.
BRAND_LITERALS = [
    "Warp on Web",
    "Warp",
    "Oz",
    "MCP",
    "Agent",
    "Markdown",
    "Xwayland",
    "/update-tab-config",
    "shell",
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
    if src.count("\n") != tgt.count("\n"):
        problems.append(
            f"newline count differs: src={src.count(chr(10))} tgt={tgt.count(chr(10))}"
        )

    # brand literals must remain in target if present in source.
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target (project convention: convert to '……').
    if "..." in tgt:
        problems.append("'...' still in target (should be '……')")

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
    already = 0
    for eid, tgt in TRANSLATIONS.items():
        entry = by_id[eid]
        # idempotent: skip if already translated to this target
        if entry["status"] == "translated" and entry.get("target") == tgt:
            already += 1
            continue
        if entry["status"] != "new":
            errors.append(f"{eid}: status not 'new' (got {entry['status']!r})")
            continue
        verdict = entry.get("audit", {}).get("verdict")
        if verdict not in {"auto_ui", "uncertain"}:
            errors.append(f"{eid}: verdict not 'auto_ui'|'uncertain' (got {verdict!r})")
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
    if "uncertain" in status_counter:
        stats["uncertain"] = status_counter.get("uncertain", 0)
    md["entry_count"] = len(entries)
    md["last_changed_at"] = NOW

    STRINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"applied {applied}/64 translations (already={already})")
    print(f"stats: {dict(status_counter)}")
    print(f"pre_translated={pre_translated} -> post_translated={status_counter.get('translated', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
