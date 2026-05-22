#!/usr/bin/env python3
"""Apply batch-9 translations (60 entries) to translations/strings.json.

Files cleared (29 files, all zeroed to auto_ui-new=0):
  - crates/onboarding/src/slides/agent_slide.rs (3)
  - app/src/workflows/workflow_view/argument_editor.rs (3)
  - app/src/resource_center/view.rs (3) [1 panic + 1 SHARED]
  - app/src/settings_view/directory_color_add_picker.rs (2)
  - app/src/editor/accept_autosuggestion_keybinding_view.rs (2) [SHARED]
  - app/src/drive/mod.rs (2) [SHARED]
  - app/src/workspace/view/launch_modal/oz_launch.rs (2)
  - app/src/env_vars/view/env_var_collection.rs (2) [1 SHARED]
  - app/src/settings_view/transfer_ownership_confirmation_modal.rs (2)
  - app/src/settings_view/delete_environment_confirmation_dialog.rs (2)
  - app/src/settings_view/settings_page.rs (2)
  - app/src/search/command_search/warp_ai.rs (2)
  - app/src/settings_view/features/undo_close.rs (2)
  - app/src/ai/skills/resolve_skill_spec.rs (2)
  - app/src/ui_components/dialog.rs (2) [2 panics]
  - app/src/terminal/ssh/install_tmux.rs (2)
  - app/src/code_review/git_dialog/commit.rs (2)
  - app/src/terminal/warpify/success_block.rs (2)
  - app/src/notebooks/editor/find_bar.rs (2) [SHARED]
  - app/src/uri/mod.rs (2)
  - app/src/terminal/block_filter.rs (2)
  - app/src/launch_configs/save_modal.rs (2)
  - app/src/settings/import/view.rs (2)
  - app/src/ui_components/red_notification_dot.rs (2) [2 panics]
  - app/src/resource_center/section_views/changelog_section.rs (2)
  - app/src/code_review/comment_list_view.rs (2)
  - app/src/settings_view/warp_drive_page.rs (2)
  - app/src/workspace/view/global_search/view.rs (2)
  - app/src/themes/theme_deletion_body.rs (1)

Side-effect cross-file zeroings (SHARED occurrences also flipped to translated):
  - app/src/settings_view/features_page.rs (-2: Accept Autosuggestion + Change keybinding)
  - app/src/settings_view/billing_and_usage_page.rs (-2: A to Z + Z to A)
  - app/src/workflows/workflow_view.rs (-1: Add a title)
  - app/src/workspace/view.rs (-1: Warp Essentials)
  - app/src/settings_view/billing_and_usage_page_v2.rs (no — billing_and_usage_page is *not* v2)
  - app/src/notebooks/editor/view.rs (-2: Focus next / previous match)
(Net new auto_ui-new entries cleared: 60 main + 8 cross-file = 68; but the SHARED
  entries are only counted once in the registry.)

Invariants:
  - placeholders preserved exactly (positional {} and named {e} / {package_manager}).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/path/JSON-literal verbatim (Warp, Warp Drive, Agent, Warp AI, MCP, GitHub,
    YAML, RedNotificationDot, FamilyId).
  - ASCII `...` -> `……` (1 occurrence: 'Looking for settings to import...').
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

BATCH_FLAG = "pr-workflow-resource-center-warp-drive-launch-modals-batch"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str] = {
    # ====== crates/onboarding/src/slides/agent_slide.rs (3) ======
    # Inline spans glued around link chips:
    #   "If your browser hasn't launched, " + [Copy URL link] +
    #   " and open the page manually. " + [Click here link] +
    #   " to paste your token from the browser."
    # Preserve leading/trailing whitespace exactly.
    "01KQXQV11XYQABRZQ4D93W92AZ": " 并手动打开页面。 ",
    "01KQXQV127FAV6VBFE25X67P3D": " 以粘贴来自浏览器的令牌。",
    "01KQXQV12ECK18X04M2X5MC9BB": "套餐已成功激活。所有高级模型均已可用。",

    # ====== app/src/workflows/workflow_view/argument_editor.rs (3) ======
    "01KQXQV129RJ5FHZPPG57RF85F": "添加工作流参数",
    "01KQXQV12CBYYERR41832VYPF2": "填写此工作流中的参数并复制到您的终端会话中运行",
    "01KQXQV12HPPKKV7W1GPMNF4CY": "值（可选）",

    # ====== app/src/resource_center/view.rs (3) ======
    "01KQXQV12DPG4EWFR6WW4792X1": "键盘快捷键",
    # `.expect("Should have a valid page")` — internal panic on resource center page state.
    "01KQXQV12F7V39Q83KS16MNGQX": "应有一个有效的页面",
    "01KQXQV12H13BSTEQ1T1NG3TY0": "Warp 入门精要",

    # ====== app/src/settings_view/directory_color_add_picker.rs (2) ======
    "01KQXQV128795HD9Y1RTAPYN8W": "+ 添加目录…",
    "01KQXQV1295KZN6K5N88K92TE0": "添加目录颜色",

    # ====== app/src/editor/accept_autosuggestion_keybinding_view.rs (2) ======
    "01KQXQV1288YA2VRN0K94DMEEB": "接受自动建议",
    "01KQXQV1291DG3EMESBRVPB372": "修改快捷键",

    # ====== app/src/drive/mod.rs (2) ======
    "01KQXQV128MYXRDJ77F0NETEDA": "A 到 Z",
    "01KQXQV12JEX64PJSW1S7ZZPTB": "Z 到 A",

    # ====== app/src/workspace/view/launch_modal/oz_launch.rs (2) ======
    "01KQXQV1292KS1XH52EB2393Q6": "存储在云端的 Agent 会话只需一键即可与任何人分享，并支持跨设备和登出后继续对话。",
    "01KQXQV12GV6SR8S1NSFWT8YSS": "将会话同步至云端",

    # ====== app/src/env_vars/view/env_var_collection.rs (2) ======
    "01KQXQV1295MKB31WX5JNVZ5C7": "添加机密信息或命令。Warp 永远不会存储外部机密信息",
    "01KQXQV129R3KK8TA76DV1HG52": "添加标题",

    # ====== app/src/settings_view/transfer_ownership_confirmation_modal.rs (2) ======
    "01KQXQV1298ZJXC3JE4NZXW0PK": "确定要将团队所有权转让给 {} 吗？您将不再是所有者，也无法对此团队执行任何管理操作。",
    "01KQXQV12HTQWVMTYHVED4NWHV": "转让",

    # ====== app/src/settings_view/delete_environment_confirmation_dialog.rs (2) ======
    "01KQXQV1299G1QQQ11ZRE8X732": "确定要移除环境 {} 吗？",
    "01KQXQV12ADE5CCXQ3WSMRBX12": "删除环境？",

    # ====== app/src/settings_view/settings_page.rs (2) ======
    "01KQXQV129SB4G1381FMC8ACFK": "点击在文档中了解更多",
    "01KQXQV12GF6T8MGNDT00TPD4J": "此设置不会同步至您的其他设备",

    # ====== app/src/search/command_search/warp_ai.rs (2) ======
    "01KQXQV129XQE3T9X77F1P0RAB": "向 Warp AI 询问命令建议",
    "01KQXQV12HSQSG7ZM7CZQYNVPG": "使用 Warp AI 翻译为 shell 命令",

    # ====== app/src/settings_view/features/undo_close.rs (2) ======
    "01KQXQV12B65N8GJEVNKWZMXAK": "启用重新打开已关闭的会话",
    "01KQXQV12CFV16K20FE5Z88JHQ": "宽限期（秒）",

    # ====== app/src/ai/skills/resolve_skill_spec.rs (2) ======
    "01KQXQV12BH5BB2KGD84P8GR4M": "执行 git clone 失败：{e}",
    "01KQXQV12GD1ZQ6D9JNH5WSSC2": "目标目录 {} 已存在但不是 git 仓库",

    # ====== app/src/ui_components/dialog.rs (2) ======
    # Both are `.expect(...)` panic messages on Option<...> unwrap.
    "01KQXQV12BWHCWANGH2SAEYS91": "FamilyId 已设置",
    "01KQXQV12C94X07P38ED0YA7XK": "字号已设置",

    # ====== app/src/terminal/ssh/install_tmux.rs (2) ======
    "01KQXQV12C1DM1C6G5D67JQ7Z8": "使用 {package_manager} 安装",
    "01KQXQV12CJ05PK5XPRR99CFWF": "安装到 ~/.warp",

    # ====== app/src/code_review/git_dialog/commit.rs (2) ======
    # NOTE: source already uses unicode ellipsis '…' (U+2026), preserve it verbatim.
    "01KQXQV12C2428FHA0E5YSA32P": "正在生成提交信息…",
    "01KQXQV12H72EA4W15E9AC28RC": "输入提交信息",

    # ====== app/src/terminal/warpify/success_block.rs (2) ======
    "01KQXQV12C7ZP4DJKD092N2BMS": "在远程子 shell 中，Warp 会在后台运行命令以支持补全、语法高亮等功能。",
    "01KQXQV12FJSPACWM6PN6XVY6C": "运行以下命令以在将来自动 Warpify：",

    # ====== app/src/notebooks/editor/find_bar.rs (2) ======
    "01KQXQV12C8HR63KT0AM6VXK1R": "聚焦上一个匹配项",
    "01KQXQV12CPTH0YSQ9TV20P6CK": "聚焦下一个匹配项",

    # ====== app/src/uri/mod.rs (2) ======
    "01KQXQV12CE79C0FF9EBHBV2XB": "前往 Warp 查看您的新标签页。",
    "01KQXQV12D9B7ARH10MWBAFRJ0": "已创建新标签页",

    # ====== app/src/terminal/block_filter.rs (2) ======
    "01KQXQV12CTM18YDM0DXJMC9PX": "反转过滤器",
    "01KQXQV12FATG2W881N8J0379R": "在匹配项周围显示上下文行",

    # ====== app/src/launch_configs/save_modal.rs (2) ======
    "01KQXQV12D7H1Y8CPAF9F62SB4": "打开 YAML 文件",
    "01KQXQV12FVKV9WA97AT280CJJ": "保存配置",

    # ====== app/src/settings/import/view.rs (2) ======
    # ASCII '...' -> '……' per project convention.
    "01KQXQV12DSPRFAWTM2H6Z5H9S": "正在查找可导入的设置……",
    "01KQXQV12FJKN2DMQ7R7KYPG83": "选择要导入的设置配置：",

    # ====== app/src/ui_components/red_notification_dot.rs (2) ======
    # Both are `.expect(...)` panic strings on missing layout dimensions.
    "01KQXQV12E7832S4J9DYTBY9PC": "RedNotificationDot 需要 width",
    "01KQXQV12EEMQ80P7ZD85AASHA": "RedNotificationDot 需要 height",

    # ====== app/src/resource_center/section_views/changelog_section.rs (2) ======
    "01KQXQV12EJQSQ2XDV81N2W8QQ": "阅读全部更新日志",
    "01KQXQV12HYC0AGWGXV96BBN8D": "无法获取最新的更新日志。",

    # ====== app/src/code_review/comment_list_view.rs (2) ======
    "01KQXQV12FVG8M9S7WJ93FAC2F": "发送给 Agent",
    "01KQXQV12H137VMVYJ5V0PDK0J": "在 GitHub 中查看",

    # ====== app/src/settings_view/warp_drive_page.rs (2) ======
    "01KQXQV12GV98JWH1XJ5GJDN3W": "要使用 Warp Drive，请创建账户。",
    "01KQXQV12HWY53Z9CPN3A6NJSF": "Warp Drive 是您终端中的工作区，可用于保存工作流、笔记本、提示词与环境变量，供个人使用或与团队共享。",

    # ====== app/src/workspace/view/global_search/view.rs (2) ======
    "01KQXQV12GKJ8CCZ0GHTHPDFFV": "切换大小写敏感",
    "01KQXQV12GT9XNKF39ZES7R2CT": "切换正则表达式",

    # ====== app/src/themes/theme_deletion_body.rs (1) ======
    "01KQXQV12ADK90JYEGZ1CD1FG1": "删除主题",
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
    "Warp AI",
    "Warp",
    "MCP",
    "Agent",
    "GitHub",
    "YAML",
    "RedNotificationDot",
    "FamilyId",
    "git clone",
    "git",
    "shell",
    "~/.warp",
    "Warpify",
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
