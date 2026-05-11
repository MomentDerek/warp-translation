---
name: Fix menu bar translation gap
description: 修复 build/warp-zh 实际运行时菜单栏与菜单内大量条目未翻译的问题
---

# Fix Menu Bar Translation Gap

## Goal

PR1+PR2+PR3 流水线交付后，用户运行 `build/warp-zh` 应用，发现 macOS 菜单栏（File/View/Window/Help/Session/Drive/Blocks/Agent/Tabs 等顶级标题）全部还是英文，且子菜单内大量条目也未译。本 task 收紧 heuristic + 补译第二批，使菜单栏整体中文化。

## What I already know (诊断结果)

用户截图覆盖 9 个菜单（File / Edit / View / Tabs & Panes / Blocks / Agent / Drive / Window / Help），对照 `translations/strings.json` 后将未译条目分四类：

### A 类：39 条在表里、heuristic 已认 UI、PR3 batch 漏译
全部 `status=new`，audit `auto_ui`(8) 或 `uncertain`(31)。代表条目：

- `Open Left Panel` / `Command Palette` / `Navigation Palette` / `Toggle Files Palette`
- `Split Pane Right/Left/Down/Up` / `Close Window` / `Toggle Maximize Active Pane` / `Close Tabs Below`
- `Move Tab Up/Down` / `Show History` / `Command Search`
- `Zoom In` / `Zoom Out` / `Reset Zoom`
- `Clear Blocks` / `View Shared Blocks...`
- `New Agent Pane` / `Attach Selection as Agent Context` / `Open AI Command Suggestions` / `Open AI Rules` / `Open MCP Servers`
- `New Personal Workflow/Notebook/Prompt/Environment Variables` ×4 + Team ×4 = 8
- `Search Warp Drive` / `Open Team Settings`
- `New File` / `Open Repository` / `Close Current Session` / `Find in Terminal`

→ **修复路径**：直接翻译。无需动 heuristic。

### B 类：10 个顶级菜单标题被 heuristic 切到 not_ui，根本没进表

`File / View / Window / Help / Session / Drive / Blocks / Agent / Tabs / Tabs & Panes` 等。
唯一存活的 `Edit` 是因为它命中了非 Menu::new 上下文的加分。

**根因**：`Menu::new("File", file_menu_options)` 调用，但 `Menu::new[0]` 不在 `UI_CONSTRUCTORS` 列表里。所以 `"File"` 只能拿到 `path_whitelist +3`，被 `regex:camel_case -2` 减后 score=1 < 3 → `not_ui` → 不入表。

→ **修复路径**：把 `Menu::new[0]` 加入 `UI_CONSTRUCTORS`（拿 +5），分数升到 6 → `auto_ui` → 入表 → 翻译。

### D 类：~30 条菜单内项目同样被 heuristic 误杀（不在表里）

代表条目：
- 单词 CamelCase / 短动名：`Workflows` / `Share Pane` / `GitHub Issues`
- 带冒号的 panel 路径：`Left Panel: Agent Conversations` / `Project Explorer` / `Global Search` — 命中 `colon_ident` 黑名单
- 短句无 UI 上下文：`Rename the Current Tab` / `Switch to Next/Previous Tab` / `Activate Next/Previous Pane` / `Close the Current Tab` / `Close Other Tabs` / `Clear Command Editor` / `Add Selection for Next Occurrence` / `Add Cursor Above/Below` / `Go to Line` / `Focus Terminal Input` / `Launch Configuration Palette` / `Select Previous/Next Block` / `Select All Blocks` / `Scroll to Top/Bottom of Selected Block` / `Share/Bookmark/Find Within Selected Block` / `Copy Command and Output` / `Copy Command` / `Copy Command Output`

源码上下文：这些字符串多数走 `CustomMenuItem::new(&default_name(action, ctx), ...)` 路径——但 `default_name` 从 `description_for_custom_action` 读，**真正的字面量在哪里需要进一步确认**（可能在某个 `match action => "Foo"` 表或 keymap 配置里）。

→ **修复路径**：定位字面量源 → 评估 heuristic 是否需要再放宽（如 `colon_ident` 在 UI 路径下不命中、或 short_phrase 在 UI 路径下保底进 uncertain）。

### C 类：6 条系统菜单（Cut/Copy/Paste/Undo/Redo/Select All）—— **超出本 task 范围**

不在 warp Rust 源里，由 macOS AppKit 提供。需要走 `Info.plist` `CFBundleLocalizations` + `zh-Hans.lproj/MainMenu.strings`，技术路径完全不同。开独立 task `macos-system-menu-localization` 处理。

## Open Questions

~~已研究并锁定。见 Decision 下方。~~

## Approaches (Diverge)

### Approach A — 最小改动：只解决 B 类 + 翻 A 类，D 类 fall-through 到下一轮

- **改 heuristic**：仅加 `Menu::new[0]` 到 `UI_CONSTRUCTORS`
- **重跑 extract**：B 类 10 条入表 → 翻译
- **翻 A 类 39 条**
- **预估第二批译表**：~50 条
- **优点**：风险低，改 1 行 const，效果立竿见影（菜单栏顶部全中文）
- **缺点**：D 类 ~30 条仍英文，子菜单仍多处英文

### Approach B — 中等改动：解决 B + D，全面收紧 heuristic

- **改 heuristic**：
  - 加 `Menu::new[0]` 到 `UI_CONSTRUCTORS`
  - 在 `app/src/app_menus.rs` 路径下，对短句 / 单词 CamelCase / 含冒号 panel 标签降低惩罚或保底进 uncertain
  - 评估是否给 `app_menus.rs` 路径 +5（而不是当前的 +3）
- **重跑 extract**：B 类 10 + D 类 ~30 = ~40 条新入表
- **翻 A + B + D 共 ~80 条**
- **预估第二批译表**：~80 条
- **优点**：菜单栏 + 子菜单整体中文化
- **缺点**：heuristic 改动面较大，需新增 unit tests 覆盖；可能误收一些非 UI 字符串

### Approach C — 激进改动：放宽 camel_case 全局，让所有 UI 路径下单词 CamelCase 进 uncertain

- 修改 `regex:camel_case` 规则：仅当不在 UI 路径白名单下时才扣分
- 重跑 extract 估计大幅增加 uncertain 数量（全 repo 范围影响）
- **缺点**：影响范围太大、回归测试成本高；不推荐 MVP 选用

## Decision (locked 2026-05-11，基于 `research/menu-literal-trace.md`)

**Approach B 中等改动**。研究结论让方案落地非常聚焦：

### Heuristic 改动（D5）
在 `tools/extractor/src/heuristic.rs::UI_CONSTRUCTORS` 加 8 个 `(call_path, arg_index)` 条目：

| Call path | Arg index | 覆盖 | 备注 |
|---|---|---|---|
| `Menu::new` | 0 | B 类 10 条顶级菜单 | 改 1 行即可 |
| `EditableBinding::new` | 1 | D 类主力（200+ 绑定描述，~40-60 进菜单） | 主要工作量 |
| `FixedBinding::custom` | 2 | D 类 ~10 条（Switch tab / Zoom / New File 等） | |
| `BindingDescription::new` | 0 | 处理嵌套：`EditableBinding::new(X, BindingDescription::new("Y"), Z)` 里 `Y` 的 `parent_call` 是 `BindingDescription::new` | 关键收容 |
| `BindingDescription::new_preserve_case` | 0 | 同上变体 | |
| `BindingDescription::with_custom_description` | 1 | 自定义描述：`.with_custom_description(MAC_MENUS_CONTEXT, "...")` | |
| `MenuItemFields::new` | 0 | 菜单项 fields 构造器 | |
| `link_menu_item` | 0 | `app_menus.rs` 内置 helper：`link_menu_item("GitHub Issues...", url)` | |

### 已知 caveat（已确认不影响翻译流水线）

**Titlecase 二次处理**：`BindingDescription::new` 在 runtime 对 input 调 `titlecase()`（`crates/warpui_core/src/keymap.rs:115`）。源里 `"Activate next pane"` 显示为 `"Activate Next Pane"`。但：
- 我们的 builder 用**源字面量本身**做 key 替换 → 替换为中文 `"激活下一个面板"`
- runtime titlecase() 在中文字符上是 no-op → 显示 `"激活下一个面板"`，正常
- **无需特殊处理**

### Group 5 (Expr::If / Match 分支字面量)
推迟到下一轮——研究估计 < 5 条，可手工补 override 或下一 task 再做。

## Recommended: **Approach B**（中等改动）

理由：
- B 类不修是没法看的（菜单栏顶部 80% 英文，用户已 flag）
- D 类如果不修，单菜单的英文混杂状态仍很糟糕，用户体验差
- ~80 条翻译规模可控（PR3 已做 227 条，再做 80 是熟练工）
- heuristic 改动用 unit test 锁定，回归风险可控

## Requirements (evolving)

1. `Menu::new[0]` 加入 `UI_CONSTRUCTORS`
2. 定位 D 类字面量真实源头，对应调整 heuristic
3. 重跑 `extractor extract`，B+D 新入表
4. 翻译第二批 ~80 条（含 A 类原有 39 条 + B/D 类新入表 ~40 条）
5. 重 build `warp-zh` 并 `cargo check -p warp` 通过
6. 用户截图覆盖的 9 个菜单 100% 中文化（除 C 类系统菜单 6 条外）

## Acceptance Criteria

- [ ] heuristic 改动新增 unit test 覆盖 `Menu::new("File", ...)` → score ≥ 6
- [ ] 第二轮 `extractor extract` 跑过 `--check`，幂等保持
- [ ] `strings.json` 含全部用户截图英文条目（除 C 类）且 status=translated
- [ ] `build/warp-zh` 重 build 后 `cargo check -p warp` exit 0
- [ ] 人工抽查 9 个菜单：顶级 + 每菜单 5 个子项 = ~50 个抽样点 100% 中文（C 类除外）
- [ ] 译表幂等（再跑一次 extract 不变化）

## Definition of Done

- 4 角度 trellis-check 通过（builder / 翻译质量 / 端到端 build / schema）
- spec 更新（heuristic 规则变化记入 `quality-guidelines.md` 或 `rust-syn-extraction.md`）
- commit + finish-work

## Out of Scope

- **C 类 macOS 系统菜单本地化**（Cut/Copy/Paste/Undo/Redo/Select All）→ 独立 task
- **AI 设置页之外**的设置页全面翻译（features_page / billing_and_usage / appearance / 等）→ 独立 task
- **terminal 主视图 / banner / notification** 翻译 → 独立 task
- 改 PRD/glossary 哲学
- 主流程外的 heuristic 大改

## Technical Notes

- `tools/extractor/src/heuristic.rs` — `UI_CONSTRUCTORS` 常量
- `app/src/app_menus.rs` — 实际菜单定义；`Menu::new(title, items)` × 11，`CustomMenuItem::new(title, ...)` × 35，`MenuBar::new` × 1
- `app/src/app_menus.rs:100` — `default_name(action, ctx)` 从 `description_for_custom_action` 读，真正的字面量需要 trace
- 上一轮 PR2 quality-check Q1 agent flag 的 "单词 CamelCase UI 标签被切断" 问题在本轮兑现
- 上一轮 PR2 quality-check Q2 agent flag 的 8 条 panic / action-id 字符串问题与本 task 无关，留下一轮

## Research References

- [`research/menu-literal-trace.md`](research/menu-literal-trace.md) — D 类字面量源码定位：主力是 `EditableBinding::new` arg 1，嵌套见 `BindingDescription::new` arg 0；推荐 8 个 `(call_path, arg_index)` 白名单；titlecase 二次处理不影响中文翻译

## Implementation Plan

### PR1：heuristic 扩 + 重 extract
- 在 `heuristic.rs::UI_CONSTRUCTORS` 加 8 个条目（见 Decision 表）
- 加 unit tests 覆盖每个新条目（mock AST snippet → 期望分数 ≥ 6）
- 跑 `extractor extract` 重生成 `strings.json`
- 校验：B+D 字符串现已进表且 status=new；A 类 39 条仍 status=new；现有 PR3 translated 227 条不动
- DoD：`--check` 通过，幂等

### PR2：翻译第二批 + 重 build
- 列出 `app_menus.rs` + `workspace/mod.rs` + `terminal/view/init.rs` + `editor/view/mod.rs` + `pane_group/pane/view/mod.rs` + `terminal/input.rs` 等菜单相关文件下，status=new 的所有条目
- 预估规模：A 39 + B 10 + D 30 + 顺带 BindingDescription 周边 = ~100 条（保守）
- 用 Claude 翻译（沿用 `guides/translation-contract.md` 规则 + glossary）
- 跑 `warp-zh-builder build`
- `cargo check -p warp` 通过
- 人工抽样 9 个菜单确认中文化

### PR3：spec + commit
- 把 `(call_path, arg_index)` 白名单维护策略写入 `spec/backend/rust-syn-extraction.md` 或 `quality-guidelines.md`
- commit + finish-work
