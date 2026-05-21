#!/usr/bin/env python3
"""Apply 39 code_page.rs auto_ui translations + code-area glossary additions."""
import json
import datetime
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-code-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TRANSLATIONS = {
    # ---- top-of-file constants (L94-L104, Initialization Settings cluster) ----
    # L94 INITIALIZATION_SETTINGS_HEADER
    "01KQXQV12CKJCS6AXX7E5XP35C": "初始化设置",
    # L95 CODEBASE_INDEXING_LABEL
    "01KQXQV12A8ZFVEH0QFACPTK3M": "代码库索引",
    # L96 CODEBASE_INDEX_DESCRIPTION
    "01KQXQV12HQH5P7AGF9FVA0DND": "Warp 可在您浏览代码仓库时自动建立索引，帮助 Agent 快速理解上下文并提供方案。代码绝不会存储到服务器。若代码库无法被索引，Warp 仍可通过 grep 与 find 工具调用浏览您的代码库并获取信息。",
    # L97 WARP_INDEXING_IGNORE_DESCRIPTION
    "01KQXQV12GM07YVZEJZ04C887N": "若要将特定文件或目录排除在索引之外，请在仓库目录中将其添加到 .warpindexingignore 文件。这些文件仍可被 AI 功能访问，但不会包含在代码库嵌入中。",
    # L98 AUTO_INDEX_FEATURE_NAME
    "01KQXQV12C9X3V186A49T6RGP3": "默认索引新文件夹",
    # L99 AUTO_INDEX_DESCRIPTION
    "01KQXQV12HAK6KAH5K66N1RKH2": "启用此设置后，Warp 将在您浏览代码仓库时自动建立索引——帮助 Agent 快速理解上下文并提供针对性方案。",
    # L100 INDEXING_DISABLED_ADMIN_TEXT
    "01KQXQV12GCG3TE0CMA53F03PE": "团队管理员已停用代码库索引。",
    # L101 INDEXING_WORKSPACE_ENABLED_ADMIN_TEXT
    "01KQXQV12GK8GX5K8N0ZQHAQ4P": "团队管理员已启用代码库索引。",
    # L103 INDEXING_DISABLED_GLOBAL_AI_TEXT
    "01KQXQV128NTCKVDA15KPCGR1W": "必须启用 AI 功能才能使用代码库索引。",
    # L104 CODEBASE_INDEX_LIMIT_REACHED
    "01KQXQV12JK1PTAJ8S53D8BFW5": "您已达到当前套餐允许的代码库索引数量上限。请删除已有索引以自动索引新的代码库。",

    # ---- subpage titles & category labels ----
    # L129 CodeSubpage::Indexing.title()
    "01KQXQV12AYQF3CCKX04C75Y85": "代码库索引",
    # L130 CodeSubpage::EditorAndCodeReview.title()
    "01KQXQV12BWE8EVN19P1GYY0R8": "编辑器与代码审查",
    # L425 Category::new("Code Editor and Review", ...)
    "01KQXQV129Q8PQ5AZ15NKNB109": "代码编辑器与审查",

    # ---- buttons / header in indexed-folders section ----
    # L380 ActionButton::new("Index new folder")
    "01KQXQV12CMY3VMR6GKQ68S5YN": "索引新文件夹",
    # L1319 section header "Initialized / indexed folders"
    "01KQXQV12C6JF6V5EYRHQ6XTGJ": "已初始化 / 已索引的文件夹",
    # L1443 empty-state "No folders have been initialized yet."
    "01KQXQV12DAJ7EACF2VS12NF61": "尚未初始化任何文件夹。",
    # L1510 TextAndIcon "Open project rules"
    "01KQXQV12EG05XW3KR3H9J6Q3E": "打开项目规则",

    # ---- INDEXING section labels & status text ----
    # L1674 "INDEXING" section header
    "01KQXQV12CYWA30QN4WN64GCFN": "索引",
    # L1713 "No index created" (NotEnabled state)
    "01KQXQV12DQX981CNMZPPHYWQZ": "未创建索引",
    # L1724 "Discovered {total_nodes} chunks"
    "01KQXQV12BVX2850N6MWPW146Y": "已发现 {total_nodes} 个分块",
    # L1729 "Syncing - {completed_nodes} / {total_nodes}"
    "01KQXQV12GAD36TMY1DH0YQJ1S": "同步中 - {completed_nodes} / {total_nodes}",
    # L1751 "Codebase too large"
    "01KQXQV12AKZFZKRXKG5NNQYGG": "代码库过大",
    # L1776 "No index built" (warn path when no index state)
    "01KQXQV12D82376P7P93DXKKS1": "未建立索引",
    # L1839 "Indexing - {completed} / {total}"
    "01KS2GEQ7Y9H7PNQ0ES28BZ8M4": "索引中 - {completed} / {total}",
    # L1841 "Indexing - {completed}"
    "01KS2GEQ7R905AVPWT78X19QF3": "索引中 - {completed}",
    # L1842 "Indexing - 0 / {total}"
    "01KS2GEQ7KMTQERMJ36GWBH7KS": "索引中 - 0 / {total}",

    # ---- LSP SERVERS section ----
    # L2024 "LSP SERVERS" section header
    "01KQXQV12DVAEWF6KGAFD88AHN": "LSP 服务器",
    # L2140 suggested LSP description "Available for download"
    "01KQXQV1297B6BQ5AMCTGTZXR1": "可供下载",
    # L2353 button "View logs"
    "01KQXQV12HYREXARS2NE9C2XVW": "查看日志",
    # L2428 status text "Not running" (no server model)
    "01KQXQV12DNDSHAQD6KBP9FSFF": "未运行",

    # ---- Editor and Code Review section (toggles + descriptions) ----
    # L2626 "Auto open code review panel"
    "01KQXQV129M36GBE7KYQ7SB2T3": "自动打开代码审查面板",
    # L2640 description for auto-open code review
    "01KQXQV12HBB5YAMZ6VCVG153R": "启用此设置后，代码审查面板将在对话中首次接受 diff 时打开",
    # L2718 description "Show a button in the top right..."
    "01KQXQV12F2M5A4RCWE5C7NJK2": "在窗口右上角显示按钮，用于切换代码审查面板。",
    # L2746 toggle label "Show diff stats on code review button"
    "01KQXQV12FV164QQWWBYTTY1Y6": "在代码审查按钮上显示 diff 统计",
    # L2762 description "Show lines added and removed counts..."
    "01KQXQV12G808CF3874AE87X9C": "在代码审查按钮上显示新增和删除的行数。",
    # L2788 toggle label "Project explorer"
    "01KQXQV12EGF38BG0S9A46PSPP": "项目浏览器",
    # L2803 description "Adds an IDE-style project explorer..."
    "01KQXQV129CTG51EFQQ365SREA": "在左侧工具面板添加 IDE 风格的项目浏览器 / 文件树。",
    # L2831 toggle label "Global file search"
    "01KQXQV12CQZWY3KB5863C4430": "全局文件搜索",
    # L2845 description "Adds global file search..."
    "01KQXQV129F0VQBY4198ZETFRM": "在左侧工具面板添加全局文件搜索。",
}

NEW_GLOSSARY_TERMS = {
    "codebase": {
        "en": "codebase",
        "zh": "代码库",
        "notes": "源代码仓库整体。'codebase indexing' → '代码库索引'；'Codebase too large' → '代码库过大'。与 'repository/仓库' 区分：codebase 强调内容本体，repository 强调存储与版本系统。",
        "do_not_translate": False,
    },
    "code_review": {
        "en": "code review",
        "zh": "代码审查",
        "notes": "Warp 的代码审查面板与按钮。'code review panel' → '代码审查面板'；'code review button' → '代码审查按钮'；'Auto open code review panel' → '自动打开代码审查面板'。",
        "do_not_translate": False,
    },
    "project_explorer": {
        "en": "project explorer",
        "zh": "项目浏览器",
        "notes": "Code 设置中的左侧工具面板组件 (IDE-style file tree)。'Project explorer' → '项目浏览器'；'Left Panel: Project explorer' → '左侧面板：项目浏览器'。",
        "do_not_translate": False,
    },
    "file_tree": {
        "en": "file tree",
        "zh": "文件树",
        "notes": "Project explorer 的文件树视图。'IDE-style project explorer / file tree' → 'IDE 风格的项目浏览器 / 文件树'。",
        "do_not_translate": False,
    },
    "lsp": {
        "en": "LSP",
        "zh": "LSP",
        "notes": "Language Server Protocol 缩写，保留英文。'LSP servers' → 'LSP 服务器'；'LSP server' → 'LSP 服务器'。",
        "do_not_translate": True,
    },
    "diff": {
        "en": "diff",
        "zh": "diff",
        "notes": "代码差异。短语中保留英文 'diff'：'diff stats' → 'diff 统计'；'accepted diff' → '接受 diff'。带 'code' 修饰的长短语沿既有翻译 'code diffs' → '代码差异'。",
        "do_not_translate": False,
    },
}


def main():
    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

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
    g["metadata"]["term_count"] = len(g["terms"])
    GLOSSARY.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} glossary terms (total: {g['metadata']['term_count']})")


if __name__ == "__main__":
    main()
