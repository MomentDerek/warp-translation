#!/usr/bin/env python3
"""Apply batch-8 translations (60 entries) to translations/strings.json.

Files cleared (16 files, all zeroed to auto_ui-new=0):
  - app/src/settings_view/billing_and_usage_page_v2.rs (6)
  - app/src/settings_view/ai_page.rs (5)
  - app/src/settings_view/billing_and_usage/overage_limit_modal.rs (5)
  - app/src/terminal/profile_model_selector.rs (5)
  - app/src/workspace/view/openwarp_launch_modal/view.rs (5)
  - app/src/settings_view/features_page.rs (4) [3 panic + 1 panic]
  - app/src/terminal/share_block_modal.rs (4)
  - app/src/workflows/workflow_view.rs (4)
  - app/src/ai/auth_secret_types.rs (3)
  - app/src/ai/facts/view/rule.rs (3)
  - app/src/code_review/mod.rs (3)
  - app/src/terminal/block_list_element.rs (3)
  - app/src/terminal/shared_session/participant_avatar_view.rs (3)
  - app/src/terminal/universal_developer_input.rs (3)
  - app/src/terminal/enable_auto_reload_modal.rs (3)
  - app/src/workspace/view/right_panel.rs (1)

Side-effect cross-file clearings:
  - app/src/workspace/global_actions.rs (-3)
  - app/src/workspace/view.rs (-3)
  - app/src/workspace/view/build_plan_migration_modal.rs (-1)

Invariants:
  - placeholders preserved exactly (named {credits} {price}).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/path/JSON-literal verbatim (Warp, Agent, MCP, Oz, GitHub, AWS, /feedback,
    auto (open-weights), Kimi, MiniMax, FocusReportingEnabled, MouseReportingEnabled,
    ScrollReportingEnabled, Pin, Bearer, Secret, Session, API, PII, React).
  - ASCII `...` -> `……` (1 occurrence: 'Enter your prompt here...').
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

BATCH_FLAG = "pr-billing-ai-settings-workflow-share-code-review-agent-batch"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str] = {
    # ====== app/src/settings_view/billing_and_usage_page_v2.rs (6) ======
    "01KS2GEPRAD00RC94NVCF09D6K": "自动充值已启用",
    "01KS2GEQC5EVC4YW6D9JSY85JK": "由您的管理员管理",
    "01KS2GEQKJXXA5M7BJGZN9XRQP": "因账单问题受限。请联系团队管理员更新支付方式。",
    "01KS2GEPQVP33JYKBB3H99NN59": "因近期充值失败，自动充值已禁用。请联系团队管理员更新支付方式。",
    "01KS2GEQQT37VQQJPZFR5CNYAB": "您的管理员已为附加积分启用自动充值。当您的个人附加积分余额不足时，Warp 将自动购买附加积分并添加到您的余额中。",
    "01KS2GEQQZS6AABN0KPWFXQ430": "您的管理员已为附加积分启用自动充值。当您的个人附加积分余额不足时，Warp 将以 {price} 自动购买 {credits} 积分并添加到您的余额中。",

    # ====== app/src/settings_view/ai_page.rs (5) ======
    "01KRBDMFSV95Z6WRHX832P25B9": "其他",
    "01KS2GEPR2B1NQRKQ7P9SFD1NJ": "睡眠前自动移交",
    "01KS2GEQQ1905GTK5TEXC0YGTZ": "当 macOS 即将进入睡眠时，自动将最近聚焦且正在本地运行的 Warp Agent 对话移交至云端模式，以便继续工作。",
    "01KS2GEQ3E562RX0CHZQ9R6BEM": "启用内置反馈技能",
    "01KS2GEQA5WEEPDTH6D3H7FY1X": "允许 Oz 使用 Warp 内置技能将 Warp 产品反馈转化为 GitHub Issue。",

    # ====== app/src/settings_view/billing_and_usage/overage_limit_modal.rs (5) ======
    "01KQXQV12EYRM8N45SBRV21C6C": "请输入有效的金额",
    "01KQXQV12EHDA5VX44WRG5S1RC": "请输入 $0.01 至 $10,000,000 之间的金额",
    "01KQXQV12HM377NKCEPVFPQEJW": "当达到此美元额度时，Warp 将禁止使用高级模型。每月自动重置。",
    "01KQXQV12DD3X7KN6GSY0R0DY3": "请注意，接近所选额度的 AI 积分用量可能超出额度数美元。",
    "01KQXQV12H99WBF2WB0TDTK62Z": "更新",

    # ====== app/src/terminal/profile_model_selector.rs (5) ======
    "01KQXQV129NXPTYW2ZX419YZT6": "选择 AI 执行 Profile",
    "01KQXQV1292G1SEEB09WKC9DNS": "选择 Agent 模型",
    "01KS2GEQ6WVTDWBZNQNF0RJ48B": "后续追问使用原始运行的模型",
    "01KQXQV12ESJKCXC8VH17X4CC0": "请求编辑权限以更换模型",
    "01KQXQV12DJN9NDM0AC21XZE2W": "管理 API 密钥",

    # ====== app/src/workspace/view/openwarp_launch_modal/view.rs (5) ======
    "01KQXQV12H5WQFD8MBDRZ7AMEY": "Warp 的客户端代码现已开源。请使用 /feedback 技能提交 Issue 开始体验，并参考此处的贡献指南。",
    "01KQXQV12DTPFMQC4H7M2D7FC4": "开放自动化开发",
    "01KQXQV12G4Z3MQ0Z3CRGH49M0": "Warp 仓库采用 Agent 优先的工作流管理，由我们的云端 Agent 编排平台 Oz 提供支持。",
    "01KQXQV12CDMG6139PZME36CDR": "隆重推出『auto (open-weights)』",
    "01KQXQV12HWRB38E719TAGQHD6": "我们新增了一个 auto 模型，能为任务挑选最优的开源权重模型，例如 Kimi 或 MiniMax。",

    # ====== app/src/settings_view/features_page.rs (4) ======
    "01KQXQV12DXXQC7SEPS215WFHH": "MouseReportingEnabled 序列化失败",
    "01KQXQV12FX8XS6ETE4SEAZ41A": "ScrollReportingEnabled 序列化失败",
    "01KQXQV12C2PNMTSFT38KTSP2X": "FocusReportingEnabled 序列化失败",
    "01KQXQV12EHTWCWMMH0N5A5WK7": "Pin 位置应存在于默认尺寸百分比中",

    # ====== app/src/terminal/share_block_modal.rs (4) ======
    "01KQXQV12GT0RBYJN03R87CZK6": "标题（可选）",
    "01KQXQV12BD9NCXCPSKVRXE6M7": "嵌入代码已复制。",
    "01KQXQV12G2WCQ6G9SJK9T3G4T": "显示提示词",
    "01KQXQV12EN40A6E8KN07QGWPA": "脱敏机密信息（API 密钥、密码、IP 地址、PII 等）",

    # ====== app/src/workflows/workflow_view.rs (4) ======
    "01KQXQV12BR2H003YSFQHY3J2S": "在此输入您的提示词……（例如：『创建一个按日期对对象数组排序的函数』或『帮我调试这个 React 组件』）。",
    "01KQXQV129Q59M106JGCEJ93FG": "别名让您可以创建简短字符串以执行工作流。每个别名可以拥有不同的参数值和环境变量，且别名仅属于您个人。",
    "01KQXQV12F8478CX9WKXTTZ74D": "在 Warp 中运行",
    "01KQXQV12EHP2J9T6X1CJ6V99R": "从回收站恢复工作流",

    # ====== app/src/ai/auth_secret_types.rs (3) ======
    "01KS2GEPRFSPACWTVGS21FHV3T": "Bearer 令牌",
    "01KS2GEQMAH941Z850D71GPS4E": "Secret 访问密钥",
    "01KS2GEQMXYMSC5W9HWG8Q88FJ": "Session 令牌（仅限临时凭证）",

    # ====== app/src/ai/facts/view/rule.rs (3) ======
    "01KQXQV12F22MSZT48D1M0WRFF": "规则通过提供结构化指引来增强 Agent 能力，帮助维持一致性、落实最佳实践，并适配特定工作流，涵盖代码库或更广泛的任务场景。",
    "01KQXQV12F8RBZRA0EZDNFSCSB": "搜索规则",
    "01KQXQV12J576KNDCXA9QGQPYG": "您的规则已禁用，不会作为会话上下文使用。您可以 ",

    # ====== app/src/code_review/mod.rs (3) ======
    "01KQXQV12FTR0BMEHSJHBR9X4T": "保存代码审查中所有未保存的文件",
    "01KQXQV12GSWZQ1VT3MX084G9M": "在代码审查中显示查找栏",
    "01KS2GEQNZYXKY53YQ760DH3CS": "在代码审查中切换文件导航",

    # ====== app/src/terminal/block_list_element.rs (3) ======
    "01KQXQV12GAHH57BFV1W2VAKT3": "标记 Agent 协助",
    "01KQXQV12F58T1CPER1N3P755M": "另存为工作流",
    "01KQXQV129TMAXVMG1QN3RXSV1": "包含机密信息的命令块无法保存。",

    # ====== app/src/terminal/shared_session/participant_avatar_view.rs (3) ======
    "01KQXQV12DBWZ3Z3JSFWMBHYFR": "设为编辑者",
    "01KQXQV12DJXGZBA98P80C79YG": "设为查看者",
    "01KQXQV129119ACA14M6A60TV2": "切换角色",

    # ====== app/src/terminal/universal_developer_input.rs (3) ======
    "01KQXQV129RS9H82VPZY0SPYKW": "附加上下文",
    "01KQXQV12GQ4YJ14BBJ05GH1S9": "斜杠命令",
    "01KQXQV129CA62RTCM0AZ6R3DW": "Agent 模式",

    # ====== app/src/terminal/enable_auto_reload_modal.rs (3) ======
    "01KQXQV1292NF7H8KQJB5VXZ1Y": "自动充值设置已更新",
    "01KQXQV12B31H1V0TEX2HP3AHR": "启用自动充值失败。请尝试在「计费与用量」中更新您的设置。",
    "01KQXQV12DPNFAKTT1AY6S0QNF": "糟糕，出错了；未能找到您团队的数据。",

    # ====== app/src/workspace/view/right_panel.rs (1) ======
    "01KQXQV12GW8HDJFCH918XTJNJ": "切换代码审查面板最大化",
}

# No DO_NOT_TRANSLATE entries this batch.
DO_NOT_TRANSLATE_IDS: set[str] = set()

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

# Brand/literals that must remain verbatim if present in source.
BRAND_LITERALS = [
    "Warp Drive",
    "Warp",
    "MCP",
    "Agent",
    "Oz",
    "GitHub",
    "AWS",
    "/feedback",
    "auto (open-weights)",
    "Kimi",
    "MiniMax",
    "FocusReportingEnabled",
    "MouseReportingEnabled",
    "ScrollReportingEnabled",
    "Bearer",
    "Secret",
    "Session",
    "API",
    "PII",
    "React",
    "macOS",
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
    if "..." in src and "..." in tgt:
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
    md["entry_count"] = len(entries)
    md["last_changed_at"] = NOW

    STRINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"applied {applied}/60 translations")
    print(f"stats: {dict(status_counter)}")
    print(f"pre_translated={pre_translated} -> post_translated={status_counter.get('translated', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
