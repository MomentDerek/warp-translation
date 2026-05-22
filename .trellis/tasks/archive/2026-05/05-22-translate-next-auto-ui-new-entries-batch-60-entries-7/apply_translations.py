#!/usr/bin/env python3
"""Apply batch-7 translations (60 entries) to translations/strings.json.

Files cleared (13 files, all zeroed to auto_ui-new=0):
  - crates/warpui/src/rendering/wgpu/renderer/image.rs (5) [wgpu debug labels]
  - crates/warpui/src/rendering/wgpu/renderer/glyph.rs (4) [wgpu debug labels]
  - crates/warpui/src/rendering/wgpu/renderer/rect.rs (4) [wgpu debug labels]
  - crates/ui_components/examples/library.rs (8)
  - crates/onboarding/src/callout/view.rs (6)
  - crates/onboarding/src/slides/customize_slide.rs (3)
  - app/src/settings/app_icon.rs (5)
  - app/src/resource_center/section_views/feature_section.rs (5)
  - app/src/resource_center/keybindings_page.rs (4)
  - app/src/themes/theme_creator_body.rs (4)
  - app/src/context_chips/display_chip.rs (4)
  - app/src/terminal/input/models/model_spec_scores.rs (4)
  - app/src/settings_view/mcp_servers/mod.rs (4)

Side-effect cross-file clearings:
  - app/src/settings_view/appearance_page.rs (-5)
  - app/src/terminal/profile_model_selector.rs (-3)
  - app/src/workspace/view/right_panel.rs (-1)

Invariants:
  - placeholders preserved exactly ({} count + named placeholders).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/path/JSON-literal verbatim (Warp, MCP, Agent, Gallery, git, Pull Request).
  - ASCII `...` -> `……` (1 occurrence: 'Selecting image...').
  - DO_NOT_TRANSLATE_IDS: target=None, status=translated, flags add do_not_translate (+ wgpu_debug_label).

Special handling:
  - WGPU_DEBUG_LABEL_IDS (13): wgpu debug labels (developer-only). target=None +
    flags=[batch_flag, do_not_translate, wgpu_debug_label].
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

BATCH_FLAG = "pr-warpui-wgpu-onboarding-ui-examples-resource-center-batch"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str | None] = {
    # ====== crates/warpui/src/rendering/wgpu/renderer/image.rs (5) ======
    "01KQXQV12C9T9YCDNB9C09ANRQ": None,  # Image Shader
    "01KQXQV12CYQBQT5J5XKXDDSHW": None,  # Image pipeline layout
    "01KQXQV12C5PD6VQ2E8N7168WR": None,  # Image render pipeline
    "01KQXQV12C6DS6GF9VB3XYFEWE": None,  # Image instance buffer
    "01KQXQV12CWBYYYHJNYDMDD3ZJ": None,  # Image texture

    # ====== crates/warpui/src/rendering/wgpu/renderer/glyph.rs (4) ======
    "01KQXQV12CZ2E3Z32C083P9T4F": None,  # Glyph Shader
    "01KQXQV12CFK12FTD49TP8BHXE": None,  # Glyph pipeline layout
    "01KQXQV12CCXC28ACBQD7TYPEK": None,  # Glyph Render pipeline
    "01KQXQV12CMW2H6QXNSBKFEJPC": None,  # Glyph instance buffer

    # ====== crates/warpui/src/rendering/wgpu/renderer/rect.rs (4) ======
    "01KQXQV12EHYCE096TDE762WRW": None,  # Rect Shader
    "01KQXQV12EN1R207VXGECMQ60J": None,  # Rect pipeline layout
    "01KQXQV12EZZA8H2H82VHK76WB": None,  # Rect render pipeline
    "01KQXQV12EG5SFZHRRNBQRXPH8": None,  # Rect instance buffer

    # ====== crates/ui_components/examples/library.rs (8) ======
    "01KQXQV12HP9GQEM8DSH2QMP6D": "工具提示标签",                  # Tooltip label
    "01KQXQV12EVY74SVMEZ7DKZTS9": "主要 / 默认",                   # Primary / Default
    "01KQXQV12F4QZ24AGJBPTZB3HP": "次要 / 默认",                   # Secondary / Default
    "01KQXQV12BT624KA7W9P4KNC3E": "禁用 / 默认",                   # Disabled / Default
    "01KQXQV12E7BHT4K6Q32RPNPSR": "主要 / 小型",                   # Primary / Small
    "01KQXQV12FH78FBKPH4TSZZHGS": "次要 / 小型",                   # Secondary / Small
    "01KQXQV12BN7NPBRA40FKW32ZV": "禁用 / 小型",                   # Disabled / Small
    "01KQXQV12AV4DWGVXP35C2YJWY": "对话框标题",                    # Dialog Title

    # ====== crates/onboarding/src/callout/view.rs (6) ======
    "01KQXQV12DS2S5S98KPQ8H3RJ5": "认识 Warp 输入框",              # Meet the Warp input
    "01KQXQV12G14692SJMYKNJWJZG": "与 Agent 对话",                 # Talk to the agent
    "01KS2GEQPT9EPFMY0MF14ETFHF": "欢迎使用终端模式",              # Welcome to terminal mode
    "01KS2GEQRBWDSBPT1NBV40YT49": "您正处于终端模式",              # You're in terminal mode (U+2019)
    "01KQXQV12BGSPZV4G35275SEXV": "启用自然语言检测",              # Enable Natural Language Detection
    "01KS2GEQQE7EZTCPM1C68A9P73": "您正处于 Agent 模式",           # You're in agent mode (ASCII ')

    # ====== crates/onboarding/src/slides/customize_slide.rs (3) ======
    "01KQXQV12GYA6HSB3RTKNZJE34": "标签页样式",                    # Tab styling
    "01KQXQV12A336C8B2AKQAA1FD2": "对话历史",                      # Conversation history
    "01KQXQV129X24N8Y3CHG0FRG0J": "代码审查",                      # Code review

    # ====== app/src/settings/app_icon.rs (5) ======
    "01KQXQV129EMX64ARZNHHPMB7Q": "经典 1",                        # Classic 1
    "01KQXQV12963N6Y7BHKFQJ0R07": "经典 2",                        # Classic 2
    "01KQXQV12929FE9119VXJVRWDP": "经典 3",                        # Classic 3
    "01KQXQV12C572J0YNHZMNKFE23": "玻璃天空",                      # Glass Sky
    "01KQXQV12HA8QDY151P3TTT988": "Warp 1",                        # Warp 1 (brand+version kept)

    # ====== app/src/resource_center/section_views/feature_section.rs (5) ======
    "01KQXQV12HS80GB87ADA8XXZYF": "新功能？",                      # What's New?
    "01KQXQV12C924X9AXRHEZ0F90H": "快速入门",                      # Getting Started
    "01KQXQV12D1YS80AH7NB4NM9EF": "用足 Warp",                     # Maximize Warp
    "01KQXQV129YFCJEAF4FPK98DAX": "高级设置",                      # Advanced Setup
    "01KQXQV12BY7N9Z5FEHFQAB3T4": "应为有效的鼠标状态",            # Expected valid mouse state (.expect panic)

    # ====== app/src/resource_center/keybindings_page.rs (4) ======
    "01KQXQV12F54CX3039EVN9QZ9C": "应有命令绑定向量",              # Should have command bindings vector (.expect panic)
    "01KQXQV12G2D6X6EKEGV6SHX18": "切换此面板",                    # To toggle this panel
    "01KQXQV12CRJN06NPE2YRY55PV": "前往「设置 > 键盘快捷键」配置自定义快捷键",  # Go to settings > keyboard shortcuts ...
    "01KQXQV12CJEE825FXPHGR2JTD": "输入编辑器",                    # Input Editor

    # ====== app/src/themes/theme_creator_body.rs (4) ======
    "01KQXQV12FR51ZYHA71E2CC9VH": "选择图片",                      # Select an image
    "01KQXQV12FYYA8P2D3GTVC1P95": "正在选择图片……",                # Selecting image... -> ……
    "01KQXQV12FPYDEDEYCXHV532QV": "重新选择图片",                  # Select a new image
    "01KQXQV12AMF66QMG4ZVGR7QKK": "创建主题",                      # Create theme

    # ====== app/src/context_chips/display_chip.rs (4) ======
    "01KQXQV129Q7FVW4JTAN9RK948": "切换 git 分支",                 # Change git branch
    "01KQXQV12HRT7YPZ5AGHANHJ4P": "查看 Pull Request",             # View pull request
    "01KQXQV129TJH7WHKY2MRAWWR8": "切换工作目录",                  # Change working directory
    "01KQXQV12J5QMZ3GR9JB3D0Q03": "工作目录",                      # Working directory

    # ====== app/src/terminal/input/models/model_spec_scores.rs (4) ======
    "01KQXQV12DXX99614GYH8SDJ7F": "模型规格",                      # Model Specs
    "01KQXQV12HZ5S50MNVBDA0YYF2": "Warp 对模型在我们测试框架中的表现、消耗 credit 速率及任务速度的基准测试。",
    "01KQXQV12EK33PHJH7XPJ10QEW": "推理强度",                      # Reasoning level
    "01KQXQV12C6A9S0RPMW1FAR9ZN": "提高推理强度会消耗更多 credit 并增加延迟，但在复杂任务上的表现更佳。",

    # ====== app/src/settings_view/mcp_servers/mod.rs (4) ======
    "01KQXQV12G0N1SN2NBGFWMFBHZ": "可模板化 MCP Id：{template_uuid}",
    "01KQXQV12GCYCTMKAPZC2XAK8V": "可模板化 MCP 安装 Id：{uuid}",
    "01KQXQV12CJ917PS9ZCTDPEA33": "Gallery MCP Id：{uuid}",
    "01KQXQV12CDCGTMNJNR49Q493Y": "基于文件的 MCP Id：{uuid}",
}

# DO_NOT_TRANSLATE classifications
WGPU_DEBUG_LABEL_IDS = {
    # image.rs
    "01KQXQV12C9T9YCDNB9C09ANRQ",
    "01KQXQV12CYQBQT5J5XKXDDSHW",
    "01KQXQV12C5PD6VQ2E8N7168WR",
    "01KQXQV12C6DS6GF9VB3XYFEWE",
    "01KQXQV12CWBYYYHJNYDMDD3ZJ",
    # glyph.rs
    "01KQXQV12CZ2E3Z32C083P9T4F",
    "01KQXQV12CFK12FTD49TP8BHXE",
    "01KQXQV12CCXC28ACBQD7TYPEK",
    "01KQXQV12CMW2H6QXNSBKFEJPC",
    # rect.rs
    "01KQXQV12EHYCE096TDE762WRW",
    "01KQXQV12EN1R207VXGECMQ60J",
    "01KQXQV12EZZA8H2H82VHK76WB",
    "01KQXQV12EG5SFZHRRNBQRXPH8",
}
DO_NOT_TRANSLATE_IDS = WGPU_DEBUG_LABEL_IDS

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

BRAND_LITERALS = [
    "Warp Drive",
    "Warp",
    "MCP",
    "Agent",
    "Gallery",
    "Pull Request",
    "credit",
    "git",
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
    # Special handling for case-sensitive brand 'git' (only check word-boundary form).
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target unless source already had it.
    # If source has '...' -> target should have '……' (per project convention).
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
            if eid in WGPU_DEBUG_LABEL_IDS and "wgpu_debug_label" not in flags:
                flags.append("wgpu_debug_label")
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
