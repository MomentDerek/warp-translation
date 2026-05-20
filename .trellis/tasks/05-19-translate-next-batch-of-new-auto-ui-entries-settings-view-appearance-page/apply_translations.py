#!/usr/bin/env python3
"""Apply 83 appearance_page.rs auto_ui translations + 5 glossary additions.

Defers 1 entry (L4341 `Cursor does not exist`) — it's an .expect() panic msg
that should not be translated per translation-contract; the heuristic should
ideally exclude it upstream.
"""
import json
import datetime
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-appearance-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TRANSLATIONS = {
    # L166 cursor blink
    "01KQXQV12JH7F3EVAKR7DWV13W": "光标闪烁",
    # L182 jump to bottom of block button
    "01KQXQV12JXDRVEW01YSVWV03Q": "跳转到命令块底部按钮",
    # L198 block dividers
    "01KQXQV12JX69CJYCC2KBK07MD": "命令块分隔符",
    # L213 dim inactive panes
    "01KQXQV12J6486X7YV7CXWVDJB": "暗化非活动窗格",
    # L222 Start Input at the Top
    "01KQXQV12G9D78JJY42K0GWTT8": "将输入框置于顶部",
    # L234 Pin Input to the Top
    "01KQXQV12E2EQNBE2ZWPVAJABC": "将输入框固定到顶部",
    # L246 Pin Input to the Bottom
    "01KQXQV12ECBW60MX0DZYFWYCC": "将输入框固定到底部",
    # L258 Toggle Input Mode (Warp/Classic)
    "01KQXQV12G8H8GDMGVYZMFBEES": "切换输入模式（Warp/Classic）",
    # L268 tab indicators
    "01KQXQV12J5K0WZ7MPECCW39DV": "标签页指示器",
    # L286 Show code review button in tab bar
    "01KQXQV12FZ5ZZXRB9Q7TB4TH6": "在标签页栏中显示代码审查按钮",
    # L287 Hide code review button in tab bar
    "01KQXQV12CTW6TZ22ZZ6X4TTET": "在标签页栏中隐藏代码审查按钮",
    # L308 focus follows mouse
    "01KQXQV12JSQ8E2JS1SJZ0W1A6": "焦点跟随鼠标",
    # L326 Always show tab bar
    "01KQXQV129YDF6CXPT0250SE92": "始终显示标签页栏",
    # L336 Hide tab bar if fullscreen
    "01KQXQV12C211QEZPT3A31YMFE": "全屏时隐藏标签页栏",
    # L346 Only show tab bar on hover
    "01KQXQV12DFBXAWQ090Q053HS2": "仅在悬停时显示标签页栏",
    # L360 zen mode
    "01KQXQV12JJN89PCZMMXTC892Z": "禅模式",
    # L377 vertical tab layout
    "01KQXQV12JNQDWP6H2YAS9NGAQ": "垂直标签页布局",
    # L385 show vertical tabs panel in restored windows
    "01KQXQV12J91KXMZZ8KV7DPC56": "在恢复的窗口中显示垂直标签页面板",
    # L396 ligature rendering
    "01KQXQV12J1PB61YENV5CB1ZKD": "连字渲染",
    # L1412 Full-screen Apps
    "01KQXQV12C31QDPX2XHMS9ZYD0": "全屏应用",
    # L1521 Pin to the bottom (Warp mode)
    "01KQXQV12EX547F4HT5BC8A0BN": "固定到底部（Warp 模式）",
    # L1522 Pin to the top (Reverse mode)
    "01KQXQV12E1MBXH516E48ZNAE4": "固定到顶部（反向模式）",
    # L1523 Start at the top (Classic mode)
    "01KQXQV12GGRNZ53Y116GTPSJK": "从顶部开始（Classic 模式）",
    # L1552 On low-DPI displays
    "01KQXQV12D8P156W6WAJTNN0FQ": "在低 DPI 显示器上",
    # L1553 On high-DPI displays
    "01KQXQV12DK49CMR7YHJ1GMPJJ": "在高 DPI 显示器上",
    # L1561 Only for named colors
    "01KQXQV12DF5JYZKNYZ0AV9YCZ": "仅限命名颜色",
    # L1571 When windowed
    "01KQXQV12HJQTW2TFHJ959YWAF": "在窗口化时",
    # L1572 Only on hover
    "01KQXQV12DJ63V29XDFYPEJ57G": "仅在悬停时",
    # L2606 Create your own custom theme
    "01KQXQV12AEQS9RDE6H386NT8N": "创建您的自定义主题",
    # L2643 Current theme
    "01KQXQV12AK86NMRNFS6TD0AH7": "当前主题",
    # L2762 Sync with OS
    "01KQXQV12G84NEKE87M7AHPP87": "与系统同步",
    # L2790 Automatically switch between light and dark themes when your system does.
    "01KQXQV12948NM47VCR9FFANQV": "当系统切换浅色与深色主题时自动跟随。",
    # L2846 Customize your app icon
    "01KQXQV12AMSDDMXWHS8KDCTNC": "自定义您的应用图标",
    # L2847 Changing the app icon requires the app to be bundled.
    "01KQXQV12965VK2E4JT7G7M2EN": "更改应用图标需要应用以打包形式运行。",
    # L2871 You may need to restart Warp for MacOS to apply the preferred icon style.
    "01KQXQV12JYS71HMCDZ6AWC9CF": "您可能需要重启 Warp，MacOS 才会应用所选的图标样式。",
    # L2916 Open new windows with custom size
    "01KQXQV12E0Q3V1Y3HDYWZRDCG": "以自定义大小打开新窗口",
    # L3041 Window Opacity:
    "01KQXQV12JFX2CPVSESQWWXKJF": "窗口不透明度：",
    # L3068 Window Opacity: {opacity_value}
    "01KQXQV12J9CWC2D4XSGHW215S": "窗口不透明度：{opacity_value}",
    # L3105 The selected graphics settings may not support rendering transparent windows.
    "01KQXQV12GPAN9CTZRR1BNRKXA": "所选图形设置可能不支持渲染透明窗口。",
    # L3117 " Try changing the settings for the graphics backend or integrated GPU in Features > System."
    "01KQXQV11QAPKVAEG24WVNG5YC": " 请尝试在 功能 > 系统 中更改图形后端或集成 GPU 设置。",
    # L3173 Window Blur Radius: {blur_value}
    "01KQXQV12JNJZ8CR5P6VMPCBBZ": "窗口模糊半径：{blur_value}",
    # L3230 Use Window Blur (Acrylic texture)
    "01KQXQV12HHYVWK4462DNP4HS9": "使用窗口模糊（亚克力质感）",
    # L3294 Tools panel visibility is consistent across tabs
    "01KQXQV12HHJCP4FKT5Y9ZKHE9": "工具面板可见性在标签页之间保持一致",
    # L3350 Shell (PS1)
    "01KQXQV12FTGBGGDQQKGY7CHR5": "Shell（PS1）",
    # L3370 Input type
    "01KQXQV12C4YEJ5JBS6KS4KX3W": "输入类型",
    # L3399 Input position
    "01KQXQV12CDHZESRETGZB5YSSN": "输入位置",
    # L3521 Dim inactive panes
    "01KQXQV12AAPTTHPKEWKHXVDR1": "暗化非活动窗格",
    # L3564 Focus follows mouse
    "01KQXQV12C6SMAH15A56PCY23V": "焦点跟随鼠标",
    # L3612 Compact mode
    "01KQXQV12AB6SS8JH4YAZ2ZQJ1": "紧凑模式",
    # L3659 Show Jump to Bottom of Block button
    "01KQXQV12FJS9E6MZCHCWHCY2J": "显示跳转到命令块底部按钮",
    # L3706 Show block dividers
    "01KQXQV12F2ZZ5THQK7SP1JXN2": "显示命令块分隔符",
    # L3752 Agent font
    "01KQXQV129QBQAEDB9Q5REZ5D3": "Agent 字体",
    # L3788 Match terminal
    "01KQXQV12D610AYQQWADWBZ6WB": "匹配终端",
    # L3816 Line height
    "01KQXQV12DRFVH64PNRBPEN4W1": "行高",
    # L3883 Reset to default
    "01KQXQV12EVP9V93AK2KD9GBHV": "重置为默认",
    # L3914 Terminal font
    "01KQXQV12G68RVTH8WNTRM1P7E": "终端字体",
    # L3957 View all available system fonts
    "01KQXQV12HV8P9ET02Y6BWJRRS": "查看所有可用的系统字体",
    # L3978 Font weight
    "01KQXQV12CGHWBBJGTKTTWA8VV": "字重",
    # L4001 Font size (px)
    "01KQXQV12CVN49YB1QVCYS9H56": "字号 (px)",
    # L4085 Notebook font size
    "01KQXQV12D5RANF6VJCZV68MEA": "笔记本字号",
    # L4169 Use thin strokes
    "01KQXQV12HDY0JB7VW607GYDZ1": "使用细笔画",
    # L4202 Enforce minimum contrast
    "01KQXQV12BJ55VF6B4GA7Y6CT0": "强制最小对比度",
    # L4240 Show ligatures in terminal
    "01KQXQV12GZWTX0TJW6M4FZHGF": "在终端中显示连字",
    # L4245 Ligatures may reduce performance
    "01KQXQV12DQBZ3EW82E28EZNPE": "连字可能会降低性能",
    # L4305 Cursor type
    "01KQXQV12AS21DMBYKMFQPZ9AG": "光标类型",
    # L4320 Cursor type is disabled in Vim mode
    "01KQXQV12AVF8RTCNEXGMYECVX": "Vim 模式下禁用光标类型",
    # L4341 Cursor does not exist  — DEFERRED (panic msg under .expect())
    # L4374 Blinking cursor
    "01KQXQV129Q1H4TA2V6W4366D2": "闪烁光标",
    # L4416 Tab close button position
    "01KQXQV12GGV7KA652YTT7XDSN": "标签页关闭按钮位置",
    # L4452 Show tab indicators
    "01KQXQV12GVCJ1YZWBWBB1SRW8": "显示标签页指示器",
    # L4497 Show code review button
    "01KQXQV12FJ9JSDYP51JZGT4JG": "显示代码审查按钮",
    # L4542 Preserve active tab color for new tabs
    "01KQXQV12E0410EXW10R8MTQHH": "为新标签页保留当前标签页颜色",
    # L4587 Use vertical tab layout
    "01KQXQV12HVW7Y530ZH5NPB1F8": "使用垂直标签页布局",
    # L4632 Show vertical tabs panel in restored windows
    "01KQXQV12GAGTJ8EBS2EDSAE3M": "在恢复的窗口中显示垂直标签页面板",
    # L4654 When enabled, reopening or restoring a window opens the vertical tabs panel even if it was closed when the window was last saved.
    "01KQXQV12HAA4SJVD53AV352Z0": "启用后，即使窗口上次保存时关闭了垂直标签页面板，重新打开或恢复窗口时也会重新打开该面板。",
    # L4682 Use latest user prompt as conversation title in tab names
    "01KQXQV12H1V0P49HPVQG5G16E": "在标签页名称中使用最新的用户提示词作为会话标题",
    # L4707 Show the latest user prompt instead of the generated conversation title for Oz and third-party agent sessions in vertical tabs.
    "01KQXQV12GVKY421FZZDCBEQ1D": "在垂直标签页中，为 Oz 和第三方 Agent 会话显示最新的用户提示词，而不是生成的会话标题。",
    # L4731 Header toolbar layout
    "01KQXQV12CG8VWKZ6E9Q1NB0QB": "标题栏工具栏布局",
    # L4838 Directory tab colors
    "01KQXQV12A8275V3F55X195PM8": "目录标签页颜色",
    # L4848 Automatically color tabs based on the directory or repo you're working in.
    "01KQXQV129S95VJZCJENRABWB7": "根据您当前所在的目录或仓库自动为标签页着色。",
    # L4985 Show the tab bar
    "01KQXQV12G79M58V64EB6MEWJ3": "显示标签页栏",
    # L5022 Use custom padding in alt-screen
    "01KQXQV12HK11BGC8XYFNYD70F": "在替代屏幕中使用自定义内边距",
    # L5083 Uniform padding (px)
    "01KQXQV12HPXCBWM9C5EQ6BV0P": "统一内边距 (px)",
    # L5142 Adjusts the default zoom level across all windows
    "01KQXQV129E5Y16H57K9ZPBFJC": "调整所有窗口的默认缩放级别",
}

NEW_GLOSSARY_TERMS = {
    "cursor": {
        "en": "cursor",
        "zh": "光标",
        "notes": "终端/输入区域的光标。'cursor blink' → '光标闪烁'；'Cursor type' → '光标类型'；'Blinking cursor' → '闪烁光标'。",
        "do_not_translate": False,
    },
    "font": {
        "en": "font",
        "zh": "字体",
        "notes": "字体相关 UI 标签。'Terminal font' → '终端字体'；'Agent font' → 'Agent 字体'；'Font weight' → '字重'；'Font size' → '字号'。size 译为 '字号'，weight 译为 '字重'，更贴合中文排版用语。",
        "do_not_translate": False,
    },
    "opacity": {
        "en": "opacity",
        "zh": "不透明度",
        "notes": "窗口/UI 的不透明度。'Window Opacity' → '窗口不透明度'。",
        "do_not_translate": False,
    },
    "blur": {
        "en": "blur",
        "zh": "模糊",
        "notes": "窗口背景模糊效果。'Window Blur' → '窗口模糊'；'Window Blur Radius' → '窗口模糊半径'。",
        "do_not_translate": False,
    },
    "padding": {
        "en": "padding",
        "zh": "内边距",
        "notes": "UI 元素内边距设置。'custom padding' → '自定义内边距'；'Uniform padding' → '统一内边距'。",
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

    # Update stats
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

    # Update glossary
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
