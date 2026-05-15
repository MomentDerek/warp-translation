---
name: Sync upstream to b9ec4f39
description: 把翻译表 strings.json 重新锚定到上游 warp master b9ec4f39（25652d73 → b9ec4f39，357 commits）
---

# Sync upstream to b9ec4f39

## Goal

`../warp` 已 fast-forward 到 `b9ec4f39`（原锚 `25652d73`，357 个新提交），现 `translations/strings.json` 中 `source_commit` 与实际不符，`extract --check` 失败。需要重跑 extractor，把新增字符串纳入表中、被改动的旧条目转 `fuzzy`、消失的转 `obsolete`，让翻译表回到规范态，作为后续翻译工作的基线。

## What I already know

- 上游变更：`25652d73 → b9ec4f39`，357 commits。重点新功能：
  - Cloud Agent 重命名（tab menu item）
  - Custom inference endpoints for third-party API models (#10781)
  - Billing & Usage 新页（autoreload credit behavior）
  - Auth secret dropdown picker for non-Oz orchestration
  - 多个 orchestration / NLD / cloud mode UX 改动
- 当前翻译表（commit 25652d73 时刻快照）：
  - entry_count: **6391**
  - status：`new=5655`, `translated=735`, `fuzzy=1`
  - 已 translated 的 735 条主要集中在菜单栏 + 部分设置页（来自上一轮 task 05-11）
- 新源码 extractor scoring：**8295 kept**（vs 当前 6391），预估约 **1900+ 条新字符串**入表
- `extract --check` 当前失败，确认必须重跑
- 工具链已稳定（PR1-PR3），直接调用 extractor / builder 子命令即可
- 历史从未做过纯 sync 任务（archive 里没有同类前例），但 README 描述的增量合并语义清楚：
  - 原文不变 → 复用旧条目（保留 status / target）
  - normalized Levenshtein ≥ 0.7 → 认领旧条目，旧原文入 `history`，状态置 `fuzzy`
  - 全新 → 新条目，status=`new`
  - 旧条目未被认领 → status=`obsolete`，三轮未回归才硬删
- 当前已 translated 的 735 条中，理论上不会被无脑打成 `fuzzy`（原文未变才会保留 translated）

## Approaches (Diverge)

### Approach A — 纯表同步（MVP，推荐）

- 只跑 `extractor extract`，更新 `strings.json`：
  - `source_commit` 从 25652d73 → b9ec4f39
  - 新增字符串入表（`status=new`），约 ~1900 条
  - 修改字符串打 `fuzzy`
  - 消失字符串打 `obsolete`
- 验证 `extract --check` 通过（幂等）
- 不动 builder、不重 build、不翻译任何新条目
- 提交 commit `chore: sync upstream to b9ec4f39`
- **优点**：scope 最小、风险低、给后续翻译任务一个干净基线
- **缺点**：build/warp-zh 与最新 strings.json 错位（builder 仍是 25652d73 时刻的产物，但 build/ 是 gitignore，无影响）

### Approach B — 同步 + 翻 fuzzy 回归

- A 的全部工作 +
- 列出所有 status=`fuzzy` 条目，复核翻译（原文小改动通常翻译可沿用，确认即转 `translated`）
- 列出 obsolete 条目（不动，让自然消亡）
- **优点**：把上一轮 735 已译条目里因为上游小改动被打 fuzzy 的恢复，避免回退到英文
- **缺点**：fuzzy 条目数量未知，可能很少（1 → ?），但 review 流程拉长

### Approach C — 同步 + 翻新页面 + 全量重 build

- A + B + 把新增的大块功能（Custom inference endpoints / Billing & Usage / Cloud Mode 等新页）也一并翻译
- 重 build `warp-zh` 并跑 `cargo check`
- **优点**：用户拿到的中文版本随上游同步推进
- **缺点**：scope 急剧膨胀（~1900 新条目里挑哪些翻？翻译质量门槛？build 时间长），更像下一阶段的迭代任务

## Recommended: **Approach A**（纯表同步）

理由：
- sync 本身和"翻译新增内容"是两件事，混到一个 task 容易失焦
- 上一轮 task 05-11 是按"覆盖菜单栏 + 部分设置页"路径推进，本次同样应该交给后续任务按页面 / 模块为单位推进
- 让 strings.json 先回到规范态，是后续任何翻译工作的前置条件
- fuzzy 数量未知，如果跑完发现只有个位数，可以在本 task 内顺手处理；如果很多，转独立 task

## Requirements (evolving)

1. 跑 `cargo run -p warp-zh-extractor -- extract --source ../../warp --table ../translations/strings.json` 完成增量合并
2. 验证 `extract --check` 通过（幂等）
3. 比对前后 metadata.stats，记入 journal
4. （Approach B 增项，待用户确认）翻 fuzzy 条目
5. commit + finish-work

## Acceptance Criteria

- [x] `strings.json` 的 `metadata.source_commit` = `b9ec4f39` ✓
- [x] `extract --check` exit 0（幂等保持）✓
- [x] translated 回退 ≤ 1%（735 → 728，回退 7 条 / 0.95%，全部为上游真实改动）✓
  - 4 条转 fuzzy（原文小改动：`Copy git branch`→`Copy branch`、`Rename the current tab`→`...pane`、`Scroll...up one line`→`...down one page`、`Oz`→`Orchestration`）
  - 2 条转 obsolete（上游删除：`Add new MCP server`、AI page API key 说明长句）
  - 1 条边界差异
- [x] obsolete 条目数 30（自然落入，无需处理）✓
- [ ] commit message 包含 commit hash 跨度 25652d73..b9ec4f39

## Definition of Done

- `extract --check` 通过
- strings.json 重排 + stats 重算到位
- journal 记录前后对比
- commit + finish-work

## Out of Scope

- 翻译任何 `status=new` 的新增条目（独立后续任务，按页面 / 模块切分）
- 重 build `build/warp-zh`（build/ 是 gitignore，无影响）
- 改 heuristic / extractor 工具逻辑（本轮纯数据同步）
- C 类 macOS 系统菜单本地化（依旧 out）
- glossary 更新（无 PRD 变化）

## Technical Notes

- 工具：`tools/extractor` (`warp-zh-extractor`)
- 表：`translations/strings.json`
- 锁文件：`translations/.lock.json`（如果存在）
- 流程文档：项目 README.md「1. 抽取并合并到翻译表」
- 上游 commit 跨度：25652d73 (旧) → b9ec4f39 (新)，357 commits
- 新源码 scoring kept：8295（vs 旧 6391）

## Implementation Plan

### Step 1：跑 extract（写盘）

```bash
cd tools
cargo run -p warp-zh-extractor --release -- extract \
    --source ../../warp \
    --table ../translations/strings.json
```

### Step 2：验证

```bash
# 幂等检查
cargo run -p warp-zh-extractor --release -- extract \
    --source ../../warp --table ../translations/strings.json --check
```

读取 strings.json metadata.stats，对比同步前后：
- entry_count: 6391 → ?
- new: 5655 → ?
- translated: 735 → ?
- fuzzy: 1 → ?
- obsolete: 0 → ?

### Step 3：journal 记录 + commit

- 把前后 stats 写入 journal
- `git add translations/strings.json` + commit
