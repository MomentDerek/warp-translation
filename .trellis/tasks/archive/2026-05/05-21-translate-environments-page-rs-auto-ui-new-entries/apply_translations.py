#!/usr/bin/env python3
"""Apply 30 environments_page.rs auto_ui translations and glossary additions
for the settings-environments batch (5th in settings_view series).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-environments-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# 30 entries: status=new + audit.verdict=auto_ui + occurrence in environments_page.rs
TRANSLATIONS = {
    # ---- Overview / onboarding ----
    # L86 PAGE_DESCRIPTION_TEXT
    "01KQXQV12BBQ7PD189XE7V2PV9": (
        "环境定义了您的 ambient agent 的运行位置。"
        "您可以在几分钟内通过 GitHub（推荐）、Warp 辅助设置或手动配置完成创建。"
    ),
    # L1488 empty-state header
    "01KQXQV12JWPG0TY05ZJHHYSNK": "您还未设置任何环境。",
    # L1497 empty-state subheader
    "01KQXQV129VN85MZSZMW0ASK36": "请选择您希望设置环境的方式：",
    # L1411 GitHub button label "Get started"
    "01KQXQV12CDRX10CX97RME1KQD": "开始使用",

    # ---- List item metadata ----
    # L194 "Last edited: {}"
    "01KQXQV12DJ1WCSF8JEPQECJ00": "上次编辑：{}",
    # L200 "Last used: {}"
    "01KQXQV12DY661EVSRZDFTRZFC": "上次使用：{}",
    # L203 "Last used: never"
    "01KQXQV12D03ECB6SWHXDG8YRZ": "上次使用：从未",
    # L1762 "Env ID: {}"
    "01KQXQV12B0RPQ20DA6FDDT8ME": "环境 ID：{}",
    # L1817 "Image: {}"
    "01KQXQV12CNJQDS6PH6WFB86KB": "镜像：{}",
    # L1825 "Repos: {}"
    "01KQXQV12ENS7YK95T29X8VY4G": "仓库：{}",
    # L1830 "Setup commands: {}"
    "01KQXQV12FD0J545R3N7S19EM7": "设置命令：{}",
    # L1320 "Shared by Warp and {}"
    "01KQXQV12FXH7K19HZ0GK0FXPT": "由 Warp 与 {} 共享",
    # L1321 "Shared by Warp and your team"
    "01KQXQV12F56ZKFKMNRK7M4KVP": "由 Warp 与您的团队共享",

    # ---- Search / empty state ----
    # L376 search placeholder
    "01KQXQV12FJ9ZYDJ30874Z05VA": "搜索环境……",
    # L1290 "No environments match your search."
    "01KQXQV12D45HZP7VTK4AXY38G": "没有与您的搜索匹配的环境。",

    # ---- CRUD success toasts ----
    # L639
    "01KQXQV12G1Y1XYSKJNQ3SSDF1": "已成功更新环境",
    # L657
    "01KQXQV12GR4W43HDFQ5BR2HYE": "已成功创建环境",
    # L674
    "01KQXQV12BXPV6YJYH0BASDXZ0": "环境已成功删除",
    # L697
    "01KQXQV12GKPH3AB5XKJPQ24KF": "已成功共享环境",

    # ---- Errors / warnings ----
    # L699
    "01KQXQV12B69ZA21TYJJA9Q5X4": "向团队共享环境失败",
    # L769
    "01KQXQV12HRQ5DF89EQGA9T3GT": "无法创建环境：未登录。",
    # L796
    "01KQXQV12H1TMGY7BW7ABJY5Q8": "无法保存：环境已不存在。",
    # L965
    "01KQXQV12HYP00A53GYZMNCH65": "无法共享环境：您当前不在任何团队中。",
    # L973
    "01KQXQV12HKGKQXTNPZ97VQDF1": "无法共享环境：环境尚未同步完成。",

    # ---- Quick setup / Use the agent ----
    # L1452 row title
    "01KQXQV12E9SMK0J6VTZDB234R": "快速设置",
    # L1455 row subtitle
    "01KQXQV12F4ZYWTW7YT0B154ZV": (
        "选择您希望使用的 GitHub 仓库，我们将为您推荐基础镜像与配置"
    ),
    # L1466 row title
    "01KQXQV12H4D4VKWBWR6XZMKQD": "使用 Agent",
    # L1469 row subtitle
    "01KQXQV1294CHCGQGNZ56XE9EB": (
        "选择一个本地已设置的项目，我们将协助您基于它创建环境"
    ),
    # L1433 button "Launch agent"
    "01KQXQV12DKDMEV0TQDGEB36A4": "启动 Agent",
    # L1862 link "View my runs"
    "01KQXQV12H6Y8QK05QVRZBXR43": "查看我的运行记录",
}

NEW_GLOSSARY_TERMS = {
    "environment": {
        "en": "environment",
        "zh": "环境",
        "notes": "Environments 设置页中的核心概念：ambient agent 的运行环境。'environment' → '环境'；'Environments' (页面/区域标题) → '环境'；'environment variables' → '环境变量' (与本术语并存，按上下文区分)；'create environment' → '创建环境'；'shared environment' → '共享环境'。",
        "do_not_translate": False,
    },
    "ambient_agent": {
        "en": "ambient agent",
        "zh": "ambient agent",
        "notes": "Warp 的云端常驻 Agent 概念，与本地交互式 Agent 区分。保留英文小写形式 'ambient agent'，避免 '环境 Agent'/'常驻 Agent' 等译名摇摆；与 'Agent' 术语并列出现时不会产生歧义。",
        "do_not_translate": True,
    },
    "repository": {
        "en": "repository",
        "zh": "仓库",
        "notes": "代码仓库（通常指 GitHub repository）。'repository' / 'repo' / 'repos' → '仓库'；'GitHub repositories' → 'GitHub 仓库'。与 'codebase/代码库' 区分：repository 强调存储/版本系统单位。",
        "do_not_translate": False,
    },
    "base_image": {
        "en": "base image",
        "zh": "基础镜像",
        "notes": "Environment 配置中的容器基础镜像（Docker base image）。'base image' → '基础镜像'；'Image: {}' → '镜像：{}'。短 'image' 在 environment 上下文同译为 '镜像'。",
        "do_not_translate": False,
    },
    "setup_commands": {
        "en": "setup commands",
        "zh": "设置命令",
        "notes": "Environment 启动时执行的初始化命令序列。'Setup commands: {}' → '设置命令：{}'。与 'Initialization Block / 初始化命令块' 区分：setup commands 是 environment 容器级别的预置命令。",
        "do_not_translate": False,
    },
    "launch_agent": {
        "en": "launch agent",
        "zh": "启动 Agent",
        "notes": "Environments 页 'Use the agent' 流程中的动作按钮。'Launch agent' → '启动 Agent'。与 'Use the agent / 使用 Agent' 配对：前者描述功能类别，后者是触发按钮。",
        "do_not_translate": False,
    },
}


def check_invariants():
    """Enforce full-width punctuation invariant + placeholder integrity."""
    # Forbid half-width sentence punctuation (,.!?:;) immediately after a CJK character
    # — allowed inside placeholders {}, URLs, regex, ASCII identifiers.
    forbidden = re.compile(r"[一-鿿][,.!?:;](?![\w/])")
    problems = []
    for eid, target in TRANSLATIONS.items():
        for m in forbidden.finditer(target):
            problems.append((eid, m.group(0), m.start()))
    if problems:
        print("ERROR: half-width punctuation adjacent to Chinese characters:")
        for eid, frag, pos in problems:
            print(f"  {eid} at pos {pos}: {frag!r}")
        sys.exit(1)


def check_placeholders(src_entry, target):
    """Confirm placeholder count and names match between source and target."""
    src = src_entry.get("source", "")
    src_phs = re.findall(r"\{[^{}]*\}", src)
    tgt_phs = re.findall(r"\{[^{}]*\}", target)
    if sorted(src_phs) != sorted(tgt_phs):
        return f"placeholder mismatch: source={src_phs} target={tgt_phs}"
    return None


def main():
    check_invariants()

    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"
    assert len(TRANSLATIONS) == 30, f"Expected 30 entries, got {len(TRANSLATIONS)}"

    # Placeholder integrity check before write
    for eid, target in TRANSLATIONS.items():
        err = check_placeholders(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        # Confirm occurrence file
        files = {o.get("file") for o in e.get("occurrences", [])}
        assert "app/src/settings_view/environments_page.rs" in files, (
            f"{eid} no environments_page occurrence: {files}"
        )
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

    # Recompute stats
    stats = data.get("stats") or {}
    status_counts = {"new": 0, "translated": 0, "fuzzy": 0, "obsolete": 0}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    stats.update({
        "entry_count": len(entries),
        "translated": status_counts["translated"],
        "fuzzy": status_counts["fuzzy"],
        "new": status_counts["new"],
        "obsolete": status_counts.get("obsolete", 0),
    })
    data["stats"] = stats

    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {updated} entries in strings.json")
    print(f"New stats: {stats}")

    g = json.loads(GLOSSARY.read_text())
    added = 0
    for k, v in NEW_GLOSSARY_TERMS.items():
        if k not in g["terms"]:
            g["terms"][k] = v
            added += 1
        else:
            print(f"Glossary term '{k}' already exists, skipping")
    g["metadata"]["term_count"] = len(g["terms"])
    GLOSSARY.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} glossary terms (total: {g['metadata']['term_count']})")


if __name__ == "__main__":
    main()
