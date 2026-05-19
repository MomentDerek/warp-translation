#!/usr/bin/env python3
"""
Apply pr-settings-features-batch translations to translations/strings.json.

Scope:
- 114 auto_ui status=new entries in app/src/settings_view/features_page.rs.
- Excluded: 4 internal `.expect("...")` panic-msg entries on L1491/1500/1509/3082.

Behavior:
- Match by (source-text + file). Source text is the authoritative key because
  the same string at different lines is the same entry in strings.json.
- For each matched entry: set target, status=translated, append flag,
  bump updated_at. Leave history empty (consistent with prior batches).
- Idempotent: re-running over an already-translated entry is a no-op
  (only re-applies if status==new).
- Asserts: every TRANSLATIONS key must match exactly one new auto_ui
  entry under features_page.rs, and after the run, all 114 are flipped.
"""

import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
STRINGS = ROOT / "translations" / "strings.json"

TARGET_FILE = "app/src/settings_view/features_page.rs"
BATCH_FLAG = "pr-settings-features-batch"

# Lines of internal panic/assert messages to SKIP (must stay status=new).
SKIP_LINES = {1491, 1500, 1509, 3082}

# Mapping: English source -> Chinese target.
# Sources copied verbatim from strings.json (including any leading newline).
TRANSLATIONS = {
    # Modifier keys (macOS / non-macOS)
    "Left Option key is Meta": "左 Option 键作为 Meta",
    "Right Option key is Meta": "右 Option 键作为 Meta",
    "Left Alt key is Meta": "左 Alt 键作为 Meta",
    "Right Alt key is Meta": "右 Alt 键作为 Meta",

    # Toggle-pair labels (lower-case sentence fragments used in toggle list)
    "Warp SSH wrapper": "Warp SSH 包装器",
    "show tooltip on click on links": "点击链接时显示提示",
    "quit warning modal": "退出确认对话框",
    "alias expansion": "别名展开",
    "middle-click paste": "鼠标中键粘贴",
    "code as default editor": "将 VS Code 设为默认编辑器",
    "input hint text": "输入提示文本",
    "editing commands with Vim keybindings": "使用 Vim 快捷键编辑命令",
    "Vim unnamed register as system clipboard": "Vim 无名寄存器作为系统剪贴板",
    "Vim status bar": "Vim 状态栏",
    "focus reporting": "焦点上报",
    "smart select": "智能选择",
    "terminal input message line": "终端输入提示行",
    "slash commands in terminal mode": "终端模式下的斜杠命令",
    "integrated GPU rendering (low power)": "集成 GPU 渲染（低功耗）",
    "Wayland for window management": "使用 Wayland 进行窗口管理",
    "Configure Global Hotkey": "配置全局快捷键",
    "Make Warp the default terminal": "将 Warp 设为默认终端",

    # Maximum rows / block limits
    "Setting the limit above 100k lines may impact performance. Maximum rows supported is {max_rows}.":
        "上限超过 10 万行可能影响性能。最大支持 {max_rows} 行。",
    "Maximum rows in a block": "命令块最大行数",
    "Allowed Values: 1-20": "可选范围：1–20",
    "Lines scrolled by mouse wheel interval": "鼠标滚轮单次滚动的行数",
    "Supports floating point values between 1 and 20.": "支持 1 到 20 之间的浮点值。",

    # Active screen / pin (split layout)
    "Active Screen": "活动屏幕",
    "Pin to top": "固定到顶部",
    "Pin to bottom": "固定到底部",
    "Pin to left": "固定到左侧",
    "Pin to right": "固定到右侧",
    "Width %": "宽度 %",
    "Height %": "高度 %",
    "Autohides on loss of keyboard focus": "失去键盘焦点时自动隐藏",

    # Tabs
    "After all tabs": "所有标签页之后",
    "After current tab": "当前标签页之后",
    "New tab placement": "新标签页位置",

    # Categories
    "Text Editing": "文本编辑",
    "Terminal Input": "终端输入",

    # Notifications
    "When a command takes longer than": "命令运行时长超过",
    "Receive desktop notifications from Warp": "接收来自 Warp 的桌面通知",
    "Notify when an agent completes a task": "Agent 完成任务时通知",
    "Notify when a command or agent needs your attention to continue":
        "命令或 Agent 需要您的关注才能继续时通知",
    "Play notification sounds": "播放通知声音",
    "Show in-app agent notifications": "显示应用内 Agent 通知",
    "Toast notifications stay visible for": "提示通知持续显示时长",

    # Hotkey / shortcuts
    "Click to set global hotkey": "点击以设置全局快捷键",
    "Press new keyboard shortcut": "按下新的快捷键",
    "Global hotkey:": "全局快捷键：",
    "Not supported on Wayland. ": "在 Wayland 上不受支持。 ",
    "See docs.": "查看文档。",

    # Window / startup behavior
    "Open links in desktop app": "在桌面应用中打开链接",
    "Automatically open links in desktop app whenever possible.":
        "在可能时自动用桌面应用打开链接。",
    "Restore windows, tabs, and panes on startup": "启动时恢复窗口、标签页和窗格",
    "Window positions won't be restored on Wayland. ": "在 Wayland 上窗口位置不会被恢复。 ",
    "Show sticky command header": "显示固定命令头",
    "Show tooltip on click on links": "点击链接时显示提示",
    "Show warning before quitting/logging out": "退出或登出前显示警告",
    "Start Warp at login (requires macOS 13+)": "登录时启动 Warp（需要 macOS 13+）",
    "Start Warp at login": "登录时启动 Warp",
    "Quit when all windows are closed": "关闭所有窗口时退出",
    "Show changelog toast after updates": "更新后显示更新日志提示",
    "Warp is the default terminal": "Warp 已是默认终端",

    # SSH wrapper section header
    "Warp SSH Wrapper": "Warp SSH 包装器",
    "This change will take effect in new sessions": "此更改将在新会话中生效",

    # Shell defaults
    "Default shell for new sessions": "新会话的默认 shell",
    "Working directory for new sessions": "新会话的工作目录",
    "Confirm before closing shared session": "关闭共享会话前确认",

    # Completions / autosuggestions
    "Autocomplete quotes, parentheses, and brackets": "自动补全引号、圆括号和方括号",
    "Error underlining for commands": "为命令添加错误下划线",
    "Syntax highlighting for commands": "命令语法高亮",
    "Open completions menu as you type": "输入时自动打开补全菜单",
    "Suggest corrected commands": "建议更正后的命令",
    "Expand aliases as you type": "输入时展开别名",
    "Middle-click to paste": "鼠标中键粘贴",
    "→ accepts autosuggestions.": "→ 接受自动建议。",
    "{} accepts autosuggestions.": "{} 接受自动建议。",
    "Completions open as you type.": "输入时自动打开补全。",
    "Completions open as you type (or {}).": "输入时自动打开补全（或按 {}）。",
    "Opening the completion menu is unbound.": "打开补全菜单的快捷键未绑定。",
    "{} opens completion menu.": "{} 打开补全菜单。",
    "Open Completions Menu": "打开补全菜单",
    "Tab key behavior": "Tab 键行为",
    "Ctrl+Tab behavior:": "Ctrl+Tab 行为：",

    # Vim
    "Edit code and commands with Vim keybindings": "使用 Vim 快捷键编辑代码和命令",
    "Set unnamed register as system clipboard": "将无名寄存器设为系统剪贴板",
    "Show Vim status bar": "显示 Vim 状态栏",

    # Terminal input context menus
    "Enable '@' context menu in terminal mode": "在终端模式下启用 “@” 上下文菜单",
    "Enable slash commands in terminal mode": "在终端模式下启用斜杠命令",
    "Outline codebase symbols for '@' context menu": "为 “@” 上下文菜单列出代码符号",
    "Show terminal input message line": "显示终端输入提示行",
    "Show autosuggestion keybinding hint": "显示自动建议的快捷键提示",
    "Show autosuggestion ignore button": "显示自动建议的忽略按钮",

    # Mouse / scroll / focus reporting + bell
    "Enable Mouse Reporting": "启用鼠标上报",
    "Enable Scroll Reporting": "启用滚动上报",
    "Enable Focus Reporting": "启用焦点上报",
    "Use Audible Bell": "启用响铃",

    # Selection / copy
    "Characters considered part of a word": "视作单词组成部分的字符",
    "Double-click smart selection": "双击智能选择",
    "Show help block in new sessions": "新会话中显示帮助命令块",
    "Copy on select": "选中即复制",
    "Default mode for new sessions": "新会话的默认模式",
    "Show Global Workflows in Command Search (ctrl-r)":
        "在命令搜索（ctrl-r）中显示全局工作流",

    # Linux clipboard
    "Honor linux selection clipboard": "遵循 Linux 选择剪贴板",
    "Whether the Linux primary clipboard should be supported.":
        "是否支持 Linux 主剪贴板。",

    # GPU / Wayland
    "Prefer rendering new windows with integrated GPU (low power)":
        "优先使用集成 GPU（低功耗）渲染新窗口",
    "Changes will apply to new windows.": "更改将应用于新打开的窗口。",
    "Use Wayland for window management": "使用 Wayland 进行窗口管理",
    "Enables the use of Wayland": "启用 Wayland",
    "Enabling this setting disables global hotkey support. When disabled, text may be blurry if your Wayland compositor is using fraction scaling (ex: 125%).":
        "启用此设置会禁用全局快捷键支持。关闭后，如果 Wayland 合成器使用了分数缩放（如 125%），文本可能会模糊。",
    "\n\nRestart Warp for changes to take effect.": "\n\n重启 Warp 以使更改生效。",
    "Preferred graphics backend": "首选图形后端",
    "Current backend: {}": "当前后端：{}",
}


def main() -> int:
    with STRINGS.open() as f:
        data = json.load(f)

    # Index features_page auto_ui new entries by source.
    candidates = {}
    skipped_panics = []
    for e in data["entries"]:
        is_new = e["status"] == "new"
        is_already_batched = (
            e["status"] == "translated"
            and BATCH_FLAG in (e.get("flags") or [])
        )
        if not (is_new or is_already_batched):
            continue
        if e["audit"]["verdict"] != "auto_ui":
            continue
        occ0 = e["occurrences"][0]
        if occ0["file"] != TARGET_FILE:
            continue
        if occ0["line"] in SKIP_LINES:
            skipped_panics.append((occ0["line"], e["source"]))
            continue
        if e["source"] in candidates:
            print(
                f"FATAL duplicate source key in features_page candidates: {e['source']!r}",
                file=sys.stderr,
            )
            return 2
        candidates[e["source"]] = e

    print(f"candidates (auto_ui new in {TARGET_FILE}, excluding panics): {len(candidates)}")
    print(f"panic-line skips: {len(skipped_panics)}")
    for line, src in skipped_panics:
        print(f"  L{line}: {src!r}")

    # Validate every translation key matches a candidate.
    missing_in_table = [s for s in TRANSLATIONS if s not in candidates]
    missing_translation = [s for s in candidates if s not in TRANSLATIONS]

    if missing_in_table:
        print(
            "FATAL: TRANSLATIONS keys not present as candidates (typo or wrong source):",
            file=sys.stderr,
        )
        for s in missing_in_table:
            print(f"  {s!r}", file=sys.stderr)
        return 3
    if missing_translation:
        print(
            "FATAL: candidates without a translation (missing rows in TRANSLATIONS):",
            file=sys.stderr,
        )
        for s in missing_translation:
            print(f"  {s!r}", file=sys.stderr)
        return 4

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    flipped = 0
    for src, target in TRANSLATIONS.items():
        e = candidates[src]
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = now
        flipped += 1

    # Update metadata stats roll-up via re-counting.
    from collections import Counter

    status_counts = Counter(e["status"] for e in data["entries"])
    verdict_new = Counter(
        e["audit"]["verdict"] for e in data["entries"] if e["status"] == "new"
    )

    meta = data.setdefault("metadata", {})
    stats = meta.setdefault("stats", {})
    stats["entry_count"] = len(data["entries"])
    stats["translated"] = status_counts.get("translated", 0)
    stats["fuzzy"] = status_counts.get("fuzzy", 0)
    stats["new"] = status_counts.get("new", 0)
    stats["obsolete"] = status_counts.get("obsolete", 0)
    stats["uncertain"] = verdict_new.get("uncertain", 0)
    stats["auto_ui"] = verdict_new.get("auto_ui", 0)

    with STRINGS.open("w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")

    print(f"flipped {flipped} entries to status=translated")
    print(f"new stats: {dict(stats)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
