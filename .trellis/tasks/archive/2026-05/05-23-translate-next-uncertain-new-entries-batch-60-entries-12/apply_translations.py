#!/usr/bin/env python3
"""Apply batch-12 translations to translations/strings.json.

Strategy: first batch from the `uncertain` verdict pool now that `auto_ui-new`
hotspot is zeroed (4398 `new` entries all `verdict=uncertain`). Triage carefully
between user-facing UI strings (translate) and internal log / doc-comment /
extractor-false-positive content (flag `do_not_translate`).

Files touched (4 translate + 3 do_not_translate):
  - app/src/settings_view/features_page.rs               (11 toggle UI labels)
  - app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs (21 UI strings)
  - app/src/ai/execution_profiles/editor/ui_helpers.rs   (20 UI labels/descs)
  - app/src/terminal/model/secrets.rs                    (15 secret name UI
                                                          labels + 4 doc-cmt)
  - app/src/util/bindings.rs                             (19 doc-cmt false pos)
  - app/src/experiments/mod.rs                           (14 doc-cmt false pos)

Translated: 67. Flagged do_not_translate (extractor_false_positive_doc_comment): 38.

Special handling:
  - `Installing Warp plugin...` / `Updating Warp plugin...` -> ASCII `...` to
    `……` per project convention.
  - Voice-input long help: backtick `{}` placeholder + `Settings > AI > Voice`
    navigation path preserved verbatim.
  - secrets.rs Acronyms (IPv4, IPv6, MAC, AWS, OAuth, etc.) and brand names
    (GitHub, Slack, Stripe, Firebase, Fireworks, Warp) retained verbatim;
    common-noun parts translated.

Invariants:
  - placeholders preserved exactly (positional {} and named {uuid}/{agent}/
    {now}/{log}/{char_count}/etc.).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/literal verbatim (Warp, Oz, MCP, Agent, Warp Drive, PTY, Settings
    paths, `{}` backtick wrappers).
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

BATCH_FLAG = "pr-uncertain-pool-features-agent-input-profile-editor-secrets-batch-12"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str | None] = {
    # ====== app/src/settings_view/features_page.rs (11) ======
    "01KQXQV12J1VD2NJ5FTSRG4N31": "Linux 选择剪贴板",
    "01KQXQV12J2CTVE0DB6RQJBM7H": "错误下划线",
    "01KQXQV12J34WMS5YR03JX442F": "输入时自动打开补全",
    "01KQXQV12J76CQKJ9DVRG25VZ9": "语法高亮",
    "01KQXQV12J9W3W9MKVWX3XJVTB": "自动建议快捷键提示",
    "01KQXQV12JCJCGRFCNSXXXGQHX": "启动时恢复窗口、标签页和窗格",
    "01KQXQV12JDMCCM6JD4N3063S2": "自动补全引号、圆括号和方括号",
    "01KQXQV12JEEGWNXSDD9MFY426": "滚动上报",
    "01KQXQV12JMYYRH4TCN11RW83Y": "命令纠错",
    "01KQXQV12JWZN15AZVXMV98ZN6": "终端内选中即复制",
    "01KQXQV12JXNXJPH5Y4DZME8F4": "终端响铃",

    # ====== app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs (21) ======
    "01KQXQV12A87P6BP6ZB8VM2EGN": "无法自动安装插件。请再次点击 chip 查看手动安装步骤。",
    "01KQXQV12B4FC1PF06E59A1K0D": "启用 {} 通知",
    "01KQXQV12B7QV42G3JNSA1TF93": "转写语音输入失败",
    "01KQXQV12B9613WM7JYZ6PXQ7B": "Warp 插件安装失败",
    "01KQXQV12BF4R2FQ7W0WF8SH65": "Warp 插件更新失败",
    "01KQXQV12BH2FXHVKE75ZVAY10": "启用通知",
    "01KQXQV12BHBPBMQKRZ93H2FZ5": "关闭",
    "01KQXQV12BYCC1XY73G9DMEQPB": "启动语音输入失败（您可能需要启用麦克风访问权限）",
    "01KQXQV12CHRHKTX69F601RDVP": "隐藏富文本输入",
    "01KQXQV12CV9JNMNGWMS5W1PAP": "正在安装 Warp 插件……",
    "01KQXQV12D9CF1JKM42A91VF9B": "现已使用 Full Terminal Agent 的默认模型。",
    "01KQXQV12DVPN5GW70YEKC8QJ6": "通知设置说明",
    "01KQXQV12EYAPK3KHWGPCF2TRB": "插件更新说明",
    "01KQXQV12F5GWREY5TS3ZHBQGN": "查看日志了解详情",
    "01KQXQV12FX5BN5WV9YA9YDXWJ": "富文本输入",
    "01KQXQV12H51MCY67D9JT6V25N": "更新 Warp 插件",
    "01KQXQV12H7E8T0ZSB5V9KQ2DN": "语音输入已启用。您也可以按住 `{}` 键来激活语音输入（在 Settings > AI > Voice 中配置）",
    "01KQXQV12H96ZBKZ3720R7S9QZ": "Warp 插件已安装。请重启会话以激活。",
    "01KQXQV12HGSCZCEHQRD0NSZ28": "语音输入额度已达上限",
    "01KQXQV12HHGP6YRDPW7TF4WF0": "Warp 插件已更新。请重启会话以激活。",
    "01KQXQV12HS0GJ3QC23VZRF8Q6": "正在更新 Warp 插件……",

    # ====== app/src/ai/execution_profiles/editor/ui_helpers.rs (20) ======
    "01KQXQV12936790QJE18S5NT3V": "调用网页工具",
    "01KQXQV129RDMZC21M63CAGKCW": "提问",
    "01KQXQV12A2NT4N6DD5G82SDPG": "计算机使用",
    "01KQXQV12A5FSER1N5MRP6XJGE": "计算机使用模型",
    "01KQXQV12AH02DR5MWRPG706AE": "上下文窗口",
    "01KQXQV12APA1KYZRT9HMA3M02": "默认 Profile 名称无法修改。",
    "01KQXQV12BV5A1E6AX2PTHD6HP": "编辑 Profile",
    "01KQXQV12CR8WKF4SRQ6AJY5VX": "完整终端能力模型",
    "01KQXQV12D1G1H3CZ5Z1Q8BRM2": "MCP 服务器 {uuid}",
    "01KQXQV12DB4PCF4N84QBTNJ14": "Oz 不允许调用的 MCP 服务器。",
    "01KQXQV12DWT6CF5E8D4MJY2V2": "Oz 允许调用的 MCP 服务器。",
    "01KQXQV12E0G3EP5FPY0AFFDKW": "用于匹配 Oz 在执行前总是询问权限的命令的正则表达式。",
    "01KQXQV12E138QCRQ5MB9YK82R": "计划自动同步",
    "01KQXQV12EJZJ85TGD43DYDYPF": "用于匹配可由 Oz 自动执行的命令的正则表达式。",
    "01KQXQV12G1Y865VV0M359GB8J": "Agent 可在有助于完成任务时使用网页搜索。",
    "01KQXQV12G822RT3ZDK0TWGYJR": "Agent 通过鼠标移动、点击和键盘输入接管您的计算机以操作图形化应用时所使用的模型。",
    "01KQXQV12G8AQBFGKEY9A91DKH": "Agent 在数据库 shell、调试器、REPL 或开发服务器等交互式终端应用中运行时所使用的模型——读取实时输出并向 PTY 写入命令。",
    "01KQXQV12GB7PBAG3ESTFBZ6MN": "此 Agent 创建的计划将自动添加并同步到 Warp Drive。",
    "01KQXQV12GF1W2TVQ4R6MFSGMQ": "基础模型的工作记忆——它可同时考虑的对话、代码与文档的 token 数量。窗口越大，越能支持更长的对话以及在更大代码库上更连贯的响应，代价是更高的延迟与计算开销。",
    "01KQXQV12GFEE5XT1NFPBYR6MK": "此模型作为 Agent 背后的主引擎。它支持大多数交互，并在需要时调用其他模型来完成规划或代码生成等任务。Warp 可能会根据模型可用性，或为对话摘要等辅助任务自动切换到备用模型。",

    # ====== app/src/terminal/model/secrets.rs (15 secret name UI labels) ======
    "01KQXQV128P4TWH95VBS9521FE": "AWS 访问 ID",
    "01KQXQV12C69WBW49RJ8JSD5Q9": "IPv4 地址",
    "01KQXQV12C74W327ZMWRCBG40R": "GitHub 经典个人访问令牌",
    "01KQXQV12C85QY0YDJJ7Z1XBNR": "GitHub 细粒度个人访问令牌",
    "01KQXQV12CA4A18X36TKACP25K": "GitHub 服务器对服务器令牌",
    "01KQXQV12CADVG525BZM47C2CB": "通用 SK API 密钥",
    "01KQXQV12CEFGTB6M2R0E15XT5": "GitHub OAuth 访问令牌",
    "01KQXQV12CF3FKC4N9E5VCVY8V": "IPv6 地址",
    "01KQXQV12CGK53GZGYZ2GRXMWR": "GitHub 用户对服务器令牌",
    "01KQXQV12CX0CPDAZRY2H2JWWG": "Fireworks API 密钥",
    "01KQXQV12CXP9EMM8RJ9VQZ1KK": "Firebase 认证域名",
    "01KQXQV12D97R2ZRTTXNT170YV": "MAC 地址",
    "01KQXQV12E5NTEPW2JBFG5D765": "电话号码",
    "01KQXQV12G1B95JANM219ESM36": "Stripe 密钥",
    "01KQXQV12GG0WQ98Y9ANQQFE99": "Slack 应用令牌",
}

# do_not_translate buckets ----------------------------------------------------

# Doc comments inside lazy_static!/macro bodies — extractor false positive.
# All target=None + status=translated + flags=[batch_flag, do_not_translate,
# extractor_false_positive_doc_comment].
EXTRACTOR_FALSE_POSITIVE_DOC_COMMENT_IDS: set[str] = {
    # app/src/util/bindings.rs (19)
    "01KQXQV10NHR482QB0QBHMF8HP",
    "01KQXQV112PE61M4406QEDR3F5",
    "01KQXQV1151REV1B3JEZT4EVA1",
    "01KQXQV116QDKJRVDWADZT3EA8",
    "01KQXQV11DHGFPJJYBMFV4X1A9",
    "01KQXQV11DM39176D6C9BXVRD1",
    "01KQXQV11DWEVPW9B29C7DK37S",
    "01KQXQV11JS8PYQD59EQK5KB9Y",
    "01KQXQV11PW8CN4GF9QQKY0K6Q",
    "01KQXQV11Q4H5DP2W5QDXBVMRB",
    "01KQXQV11QQFYEZ6Z85VR7PVA9",
    "01KQXQV11W30R9JKTJHNXWED4P",
    "01KQXQV11WP69TH8GTST7PHFT4",
    "01KQXQV11YJ36F8QATCX5ZA9C7",
    "01KQXQV11YP1R6K6V7FJ2MFVRE",
    "01KQXQV11YYSP9B5YJ3838RWXT",
    "01KQXQV1250MS0AWHQCJHGDZTW",
    "01KQXQV1250N3W9XXJB3Y23K7P",
    "01KQXQV1260VRQHHZEXH8FF2HR",
    "01KQXQV126QRFKQ8H0R35GP99M",
    # app/src/experiments/mod.rs (14)
    "01KQXQV10KXCW3VT178EQXQVF7",
    "01KQXQV10M4QSCSA3PF97K7BPQ",
    "01KQXQV10V8KKC8PS04GS8YFY7",
    "01KQXQV10XS3KTD9PM4G1KVRXC",
    "01KQXQV110PT4A9Q1FPVTXB9QV",
    "01KQXQV110RNKMCM7T04DTWCPY",
    "01KQXQV111Y0GFP4W1Z8832485",
    "01KQXQV112PZAFQ8KVKCNX2JH6",
    "01KQXQV11X2JTFAGHD7HZ8RFBG",
    "01KQXQV120M51MVYJB9JJBESTG",
    "01KQXQV121BX7B585MFZGS5MWZ",
    "01KQXQV122098HK8Z6M6JDHVCS",
    "01KQXQV122KRH5AM1FXJW29M50",
    "01KQXQV1275TT0NHFQ6D7ARBB7",
    # app/src/terminal/model/secrets.rs (4) — doc cmts in `regexes` mod scope
    "01KQXQV11199NJE5M1HQ8XKK3E",
    "01KQXQV11QFWT1WSY1K81E4GVJ",
    "01KQXQV11RG4FZ4KPTDDGRK28W",
    "01KQXQV11RVV6ZZ3NCAASDSQSG",
}

DO_NOT_TRANSLATE_IDS: set[str] = set(EXTRACTOR_FALSE_POSITIVE_DOC_COMMENT_IDS)

# Map each do_not_translate id -> list of sub-flags (besides batch_flag and
# do_not_translate).
DO_NOT_TRANSLATE_SUBFLAGS: dict[str, list[str]] = {
    eid: ["extractor_false_positive_doc_comment"]
    for eid in EXTRACTOR_FALSE_POSITIVE_DOC_COMMENT_IDS
}

# Set None target for do_not_translate ids in TRANSLATIONS dict.
for eid in DO_NOT_TRANSLATE_IDS:
    TRANSLATIONS[eid] = None

# Sanity: every do_not_translate id is in TRANSLATIONS with None.
assert all(
    TRANSLATIONS[eid] is None for eid in DO_NOT_TRANSLATE_IDS
), "DO_NOT_TRANSLATE_IDS must all map to None in TRANSLATIONS"

EXPECTED_TOTAL = 67 + 38  # 105
assert len(TRANSLATIONS) == EXPECTED_TOTAL, (
    f"expected {EXPECTED_TOTAL}, got {len(TRANSLATIONS)}"
)

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

BRAND_LITERALS = [
    "Warp Drive",
    "Warp",
    "Oz",
    "MCP",
    "Agent",
    "PTY",
    "REPL",
    "shell",
    "GitHub",
    "Slack",
    "Stripe",
    "Firebase",
    "Fireworks",
    "AWS",
    "IPv4",
    "IPv6",
    "MAC",
    "OAuth",
    "JWT",
    "SK",
    "Linux",
    "Profile",
    "Full Terminal Agent",
    "Settings > AI > Voice",
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
        problems.append(f"strftime differs: src={src_strf} vs tgt={tgt_strf}")

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

    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")

    if "..." in tgt:
        problems.append("'...' still in target (should be '……')")

    return problems


def main() -> int:
    with STRINGS_PATH.open() as f:
        data = json.load(f)

    cands = json.loads(CANDIDATES.read_text())
    cand_ids = {c["id"] for c in cands}
    assert set(TRANSLATIONS.keys()) == cand_ids, (
        f"keys != candidates: missing={cand_ids - TRANSLATIONS.keys()}, "
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
        # idempotent: skip if already translated to this exact target
        if entry["status"] == "translated" and entry.get("target") == tgt:
            already += 1
            continue
        if entry["status"] != "new":
            errors.append(f"{eid}: status not 'new' (got {entry['status']!r})")
            continue
        verdict = entry.get("audit", {}).get("verdict")
        if verdict not in {"auto_ui", "uncertain"}:
            errors.append(
                f"{eid}: verdict not 'auto_ui'|'uncertain' (got {verdict!r})"
            )
            continue
        src = entry["source"]

        if eid in DO_NOT_TRANSLATE_IDS:
            if tgt is not None:
                errors.append(
                    f"{eid}: DO_NOT_TRANSLATE_IDS must have None target, got {tgt!r}"
                )
                continue
            entry["target"] = None
            entry["status"] = "translated"
            flags = entry.get("flags") or []
            for flag in (
                BATCH_FLAG,
                "do_not_translate",
                *DO_NOT_TRANSLATE_SUBFLAGS.get(eid, []),
            ):
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
    print(
        f"applied {applied}/{EXPECTED_TOTAL} translations (already={already})"
    )
    print(f"stats: {dict(status_counter)}")
    print(
        f"pre_translated={pre_translated} -> post_translated={status_counter.get('translated', 0)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
