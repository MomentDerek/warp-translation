---
name: Refresh 4 fuzzy translations after upstream sync
description: 上一轮 sync (05-15) 把 4 条已译条目转 fuzzy，本任务复核并恢复 translated
---

# Refresh 4 fuzzy translations

## Goal

`05-15-sync-upstream-b9ec4f39` 把 4 条带翻译的条目从 `translated` 转 `fuzzy`（原文小改动），翻译需要根据新原文小修。完成后这 4 条回到 `translated`，幂等保持。

## What I already know

参考类目（来自当前表）：
- `pane` → `窗格`（5+ 条一致：`Activate next pane` → `激活下一个窗格`、`Close pane` → `关闭窗格`、`Maximize pane` → `最大化窗格` 等）
- `Copy X` → `复制 X`（无引导虚词：`Copy command` → `复制命令`、`Copy URL` → `复制 URL`）
- `[Debug] V O` 整体翻译，但产品代号保留英文：`[Debug] Open Oz Launch Modal` → `[Debug] 打开 Oz 启动弹窗`、`OpenWarp` 同样保留
- `multi-agent orchestration` → `多 Agent 编排`（已有 translated 条目用 `编排` 翻译 `orchestration` 作为概念名）
- Scroll 行/页 模式：`Scroll terminal output down one line` → `终端输出向下滚动一行`（已存在）

## 4 条 fuzzy 复核方案

| ID | 旧原文 | 新原文 | 旧译 | 新译 | 改动逻辑 |
|---|---|---|---|---|---|
| `01KQXQV12A4A8RZ6NYZ0TNQAAE` | `Copy git branch` | `Copy branch` | `复制 git 分支` | `复制分支` | 原文去 `git`，译文同步去 |
| `01KQXQV12E0PATFSDTE8XW7XDB` | `Rename the current tab` | `Rename the current pane` | `重命名当前标签页` | `重命名当前窗格` | tab → pane，按 glossary 映射 |
| `01KQXQV12F7KVGS0GAMRWJMFQT` | `Scroll terminal output up one line` | `Scroll terminal output down one page` | `终端输出向上滚动一行` | `终端输出向下滚动一页` | 方向 + 行 / 页双改，与已有兄弟条目结构对齐 |
| `01KRBDMFVW2SWZBF0GCV6W6H3C` | `[Debug] Reset Oz Launch Modal State` | `[Debug] Reset Orchestration Launch Modal State` | `[Debug] 重置 Oz 启动弹窗状态` | `[Debug] 重置编排启动弹窗状态` | Oz 是旧内部代号，上游对外重命名为 Orchestration 概念，按 glossary 用法译 `编排` |

### Orchestration 处理决策（ADR-lite）

**Context**: 上游 PR #10887 起把 `Oz` 内部代号统一替换为对外 `Orchestration`。`Oz` 在旧 [Debug] 调试项里保留英文（因为它是代号）。

**Decision**: 现 `Orchestration` 是公开概念名（非代号），按表内已有 `multi-agent orchestration` → `多 Agent 编排` 的处理，翻译为 `编排`。

**Consequences**: 后续大批量 Cloud Mode / Orchestration 相关新条目（279 条新增里有相当数量）也按 `编排` 统一翻；若发现 UI 文案中 `Orchestration` 作为产品名（如标题级 "Orchestration" 按钮）则需独立判断。

## Requirements

1. 用编辑器（不是工具）直接改 strings.json：将 4 条 fuzzy 条目的 `target` 改为上表新译，`status` 改为 `translated`
2. 跑 `extract --check` 确认幂等（不动 source_commit）
3. 跑 builder 验证（可选 — out of scope）

## Acceptance Criteria

- [ ] strings.json 中这 4 个 id 的 status = `translated`
- [ ] target 与上表新译一致
- [ ] `extract --check` exit 0
- [ ] stats: `translated` 728 → 732、`fuzzy` 34 → 30

## Out of Scope

- 翻译剩余 30 条无 target 的 fuzzy（自然 `new`，归入下批新条目翻译）
- 翻译 30 条 obsolete
- 重 build `warp-zh`
- 翻译 279 条新增条目（按模块独立 task）

## Technical Notes

- `translations/strings.json` 直接 JSON 编辑（小改动，无需走 builder 子命令）
- 复核来源：`.trellis/workspace/moment/journal-1.md` 2026-05-15 段落
- 翻译契约：`.trellis/spec/guides/translation-contract.md`
