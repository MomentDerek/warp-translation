#!/usr/bin/env python3
"""Apply batch-3 translations (60 entries) to translations/strings.json.

Files cleared (all auto_ui-new):
  - app/src/settings_view/warpify_page.rs (11)
  - app/src/settings_view/show_blocks_view.rs (9)
  - app/src/settings_view/platform_page.rs (9)
  - app/src/settings_view/platform/create_api_key_modal.rs (9)
  - app/src/workspace/hoa_onboarding/welcome_banner.rs (8)
  - app/src/wasm_nux_dialog.rs (8)
  - app/src/notebooks/editor/view.rs (5)
  - app/src/ai_assistant/mod.rs (1) [+1 pad]

Invariants:
  - placeholders preserved exactly ({name} count + spelling)
  - whitespace single-direction (no new leading/trailing space)
  - brand/path/JSON-literal verbatim (Warp, MCP, SSH, Git, API, Oz Cloud, Claude Code, Codex, OpenCode, tmux, bash, zsh, fish)
  - ASCII `...` -> `……` (U+2026 doubled) where present
  - identifier-as-source false positives (none in this batch)
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
    # ------ warpify_page.rs (11) ------
    "01KQXQV12A0QVMZPECAQ5KQ4FR": "黑名单主机",
    "01KQXQV12A63Z0AP7X3R8F8C9A": "控制远程主机未安装 Warp SSH 扩展时的安装行为。",
    "01KQXQV12AKPEZ2XAK7MY3X8Y2": "黑名单命令",
    # NOTE: source has trailing space — must preserve.
    "01KQXQV12APT990HJ9QC8TSAJ2": "配置 Warp 是否尝试对某些 shell 进行 “Warpify”（添加对命令块、输入模式等的支持）。 ",
    "01KQXQV12C2BKYKX1Z2KHTF51B": "安装 SSH 扩展",
    "01KQXQV12FKG10XFG7TN8AZCEA": "SSH 会话的 Warpification 检测",
    "01KQXQV12GHQXP2CB4RB5XDN8Y": "tmux ssh 包装器在许多默认包装器无法工作的场景下仍可正常运行，但可能需要您点击按钮才能完成 warpify。新标签页生效。",
    "01KQXQV12GPXCC8BFSN5DNSYP0": "支持的子 shell：bash、zsh 和 fish。",
    "01KQXQV12H6RHXQGZDMWBHXNS7": "为交互式 SSH 会话启用 Warpify。",
    "01KQXQV12H7ZGBDP07J8QHQNT6": "使用 Tmux Warpification",
    "01KQXQV12HPG683H3RK81F2KX9": "Warpify SSH 会话",

    # ------ show_blocks_view.rs (9) ------
    # chrono strftime format string. Keep specifiers, translate "at" -> 「于」-pattern via 「年/月/日」 structure.
    # Source: "%a, %b %-d %Y at %-I:%M %p"
    # Translation keeps numeric date + 12h time. Drop %a/%b (English locale tokens) in favor of numeric Chinese form.
    "01KQXQV1286B8Q8WPKVHHMYT6Y": "%Y 年 %-m 月 %-d 日 %-I:%M %p",
    "01KQXQV129WZVNVZKD9KE2CJ5F": "确定要取消分享此命令块吗？\n\n它将无法再通过链接访问，并将从 Warp 服务器永久删除。",
    "01KQXQV129ZR47KG5XC6Z3CWYD": "命令块已成功取消分享。",
    "01KQXQV12AXS3W4P5NJDXJRKKS": "正在删除……",
    "01KQXQV12BSK3WHYKZTCH1Y04P": "执行于：{}",
    "01KQXQV12CQXYBJ0Z8DZ2NF4N9": "正在获取命令块……",
    "01KQXQV12HA4JDYS5TZQC7S564": "取消分享",
    "01KQXQV12HF6EY8HPTWBH2BABV": "取消分享命令块",
    "01KQXQV12J87DHB67B5PA6GNNG": "您还没有任何已分享的命令块。",

    # ------ platform_page.rs (9) ------
    "01KQXQV128B5TXF8V5RR2QJ5CT": "+ 创建 API 密钥",
    "01KQXQV128PGXE7SYFTK2NTTQ6": "API 密钥已删除",
    "01KQXQV12A931HZTN58F1HF6QD": "创建密钥以管理对 Warp 的外部访问",
    # Source has trailing space and \n inside.
    "01KQXQV12AFMXXE6YRZ9A36X5H": "创建和管理 API 密钥，允许其他 Oz Cloud Agent 访问您的 Warp 账户。\n如需了解更多信息，请访问 ",
    "01KQXQV12BSZSP23M2F6NDM421": "过期时间",
    "01KQXQV12DBEXNTRFATG0RS7B5": "新建 API 密钥",
    "01KQXQV12DRZJXRKSJ9N11Q436": "上次使用",
    "01KQXQV12DV31TTWCAZA4K7PTV": "暂无 API 密钥",
    "01KQXQV12F1GYA968XRC8SSJ9B": "保存您的密钥",

    # ------ create_api_key_modal.rs (9) ------
    "01KQXQV12A7WJDDVFQNCHRPE9B": "创建密钥",
    # Source uses U+2026 already; preserve verbatim.
    "01KQXQV12AA5HFSP8A2E90ZSGD": "正在创建…",
    "01KQXQV12BHEPA72MWPXQ4EZDX": "完成",
    "01KQXQV12BQK83WR2B1AJD0SRQ": "创建 API 密钥失败。请重试。",
    "01KQXQV12F1SPQHXKS9BDFSJDR": "密钥已复制。",
    "01KQXQV12GGBV8HR8JK1TEB6K8": "此密钥仅显示一次，请复制并妥善保存。",
    "01KQXQV12GQ6TKPBD7Y8394RZR": "此 API 密钥与您的用户绑定，可用于向您的 Warp 账户发起请求。",
    "01KQXQV12HBD36ZG3TH3S4ET0Z": "无法创建团队 API 密钥，因为当前没有团队。",
    "01KQXQV12HCFDFAD1QAWBH4FAH": "Warp API 密钥",

    # ------ welcome_banner.rs (8) ------
    "01KQXQV129316WW0W2VTSS8E39": "Agent 收件箱",
    "01KQXQV12D2H8V771GZP5RVX1Y": "任何 Agent 需要您关注时发出的通知，也可在统一收件箱中查看",
    "01KQXQV12DFES18YEDDS5XWPCA": "原生代码评审",
    "01KQXQV12FCBVERKF8DT3A7RJ0": "将 Warp 代码评审中的行内评论直接发送至 Claude Code、Codex 或 OpenCode",
    "01KQXQV12FMDZ005X1VVFCWT5Q": "丰富的标签页标题与元数据，例如 Git 分支、worktree 和 PR。完全可自定义。",
    "01KQXQV12GNPS9HA9T01RTJP76": "标签页配置",
    "01KQXQV12GQQV67RVC3ACEAQWT": "标签页级别的模板，一键设定您的目录、启动命令、主题和 worktree",
    "01KQXQV12H8XXMJ1F989V4CKW5": "垂直标签页",

    # ------ wasm_nux_dialog.rs (8) ------
    # {object_kind} placeholder concatenates English plurals ("Warp Drive objects" / "shared sessions" / "Warp links").
    "01KQXQV129S50CY44D1SF9J90C": "始终在网页上打开 {object_kind}？",
    "01KQXQV12BSSMZ1EW4SM59JDKD": "下载 Warp 桌面端？",
    "01KQXQV12CTXF3JNFJA2CBAMFQ": "未来打开链接时将自动在桌面端打开。",
    "01KQXQV12ENPCYVT3Y24N6EYWX": "在 Warp 桌面端打开？",
    "01KQXQV12HAE5T5F4JCCSWXNX5": "Warp 是一款智能终端，内置 AI 与您的开发团队知识。",
    "01KQXQV12HFJB5FT6QJ682MR2A": "Warp 链接",
    "01KQXQV12HMZ6GYMTEZ3Y15VSM": "Warp Drive 对象",
    "01KQXQV12JH0ZE1CWNDRGYS0H9": "您可以随时在设置中更改此项。",

    # ------ notebooks/editor/view.rs (5) ------
    "01KQXQV12H1V42P6CGWAFDK4EA": "切换删除线样式",
    "01KQXQV12HNPJGADJ4023478BH": "切换行内代码样式",
    "01KQXQV12HV3QY5TDYC45QR7RT": "切换正则表达式搜索",
    "01KQXQV12HVG1TESJQBG7E6AHP": "切换富文本调试模式",
    "01KQXQV12HXY3S33XH8N05X2X6": "切换下划线样式",

    # ------ ai_assistant/mod.rs (1, brand pad) ------
    "01KQXQV12H80E93FRQ5RK6JVYY": "Warp AI",
}

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
BRAND_LITERALS = [
    "Warp Drive",
    "Warp AI",
    "Warp",
    "MCP",
    "SSH",
    "API",
    "Git",
    "Oz Cloud",
    "Claude Code",
    "Codex",
    "OpenCode",
    "tmux",
    "bash",
    "zsh",
    "fish",
    "Tmux",
    "Warpify",
    "Warpification",
    "warpify",
]


def placeholders(s: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(s))


def check_invariants(src: str, tgt: str, eid: str) -> list[str]:
    problems: list[str] = []
    src_ph = placeholders(src)
    tgt_ph = placeholders(tgt)
    if src_ph != tgt_ph:
        problems.append(f"placeholders differ: src={src_ph} vs tgt={tgt_ph}")

    # whitespace single-direction: if source has no leading/trailing whitespace,
    # target must not introduce any. Conversely, if source HAS it, target must keep.
    if src.startswith(" ") != tgt.startswith(" "):
        problems.append("leading whitespace mismatch")
    if src.endswith(" ") != tgt.endswith(" "):
        problems.append("trailing whitespace mismatch")
    if src.startswith("\n") != tgt.startswith("\n"):
        problems.append("leading newline mismatch")
    if src.endswith("\n") != tgt.endswith("\n"):
        problems.append("trailing newline mismatch")

    # brand literals: each brand literal that appears in source must remain
    # somewhere in target (case-sensitive). Skip case-variants where target uses
    # a different brand surface form (e.g. "tmux"/"Tmux" both legit).
    src_lower = src.lower()
    tgt_lower = tgt.lower()
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            # accept case-insensitive presence
            if brand.lower() in tgt_lower:
                continue
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target unless source already had a
    # specific pattern we want to preserve. (None in this batch besides the
    # `...` -> `……` rule.)
    if "..." in tgt and "..." not in src:
        problems.append("introduced ASCII '...' (should be '……')")

    # placeholders with literal '\n' inside source must keep their relative
    # ordering — already covered by sorted compare above.
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
