---
name: Sync upstream to fdd74928
description: 把翻译表 strings.json 重新锚定到上游 warp master fdd74928（b9ec4f39 → fdd74928，179 commits）
---

# Sync upstream to fdd74928

## Goal

`../warp` 上游已推进 179 commits（`b9ec4f39 → fdd74928`），本地 `../warp` 仍在 `b9ec4f39`。需要先把源仓库 fast-forward 到 `fdd74928`，再重跑 extractor，把新增字符串纳入表中、被改动的旧条目转 `fuzzy`、消失的转 `obsolete`，让翻译表回到规范态，作为后续翻译工作的基线。

## What I already know

- 源仓库当前 HEAD：`b9ec4f39`（与 `strings.json.metadata.source_commit` 一致）
- `origin/master` HEAD：`fdd74928`，本地落后 179 commits，可 fast-forward
- 当前翻译表基线（`b9ec4f39` 时刻）：
  - entry_count: **6640**
  - status: `new=5400`, `translated=1210`, `fuzzy=30`, `obsolete=0`, `uncertain=4484`
- 上游 179 commits 中的部分 UI 改动：
  - `Move feature flag initialization logic out of lib.rs` (#11380)
  - `Fix agent dropdown rendering in new API key modal` (#11187)
  - `Enable cmd-O and @ context on remote SSH session` (#11295)
  - `Clean up TMUX SSH warpification setting` (#11365)
  - `REV-1595 [5/n] Render per-user/team/own rows in cycle usage section` (#11123)
  - `Update add-on credits billing v2 UI` (#11346)
  - `feat(ai): add feedback skill setting` (#11341)
  - `Custom model TOS hyperlink coloring` (#11240)
  - `Skip AgentTips with unresolved keybinding placeholders` (#9509)
  - `fix(feedback): confirm before filing issues` (#11308)
  - `Reset pane flex when double-clicking on a pane divider` (#11293)
  - 其它 orchestration / pane / terminal 行为类改动
- 增量合并语义（README）：原文不变→复用旧条目（保留 status/target）；normalized Levenshtein ≥ 0.7 → 认领旧条目，旧原文入 history，置 `fuzzy`；全新→新条目 `new`；旧条目未认领 → `obsolete`，三轮未回归才硬删
- 上次同样的 sync 任务（`05-15-sync-upstream-b9ec4f39`）流程已固化：仅 extractor，不动 builder、不重译

## Approach: 纯表同步（沿用 05-15 的 Approach A）

1. fast-forward `../warp` 到 `fdd74928`
2. 跑 `cargo run -p warp-zh-extractor --release -- extract` 完成增量合并
3. `extract --check` 验证幂等
4. 对比前后 `metadata.stats` 写入 journal
5. commit + finish-work

**不做**：翻译任何新 `status=new` 条目、重 build `build/warp-zh`、改 heuristic / extractor 工具逻辑、glossary 更新。这些都拆给后续按页面 / 模块切分的翻译任务。

## Acceptance Criteria

- [ ] `../warp` HEAD = `fdd74928`
- [ ] `strings.json.metadata.source_commit` = `fdd74928`
- [ ] `extract --check` exit 0（幂等保持）
- [ ] translated 回退 ≤ 1%（基线 1210，回退条目记入 journal）
- [ ] obsolete 数（自然落入）、新增 new 数 都记入 journal
- [ ] commit message 包含 commit hash 跨度 `b9ec4f39..fdd74928`

## Definition of Done

- `../warp` 已 fast-forward 到 `fdd74928`
- `strings.json` source_commit / stats 同步、`extract --check` 通过
- journal 记录前后 stats 对比、translated 回退明细
- commit + finish-work

## Out of Scope

- 翻译 `status=new` 的新增条目（拆给后续 page/module 任务）
- 重 build `build/warp-zh`（gitignore，无影响）
- extractor heuristic 调整
- glossary 更新
- macOS 系统菜单本地化

## Technical Notes

- 工具：`tools/extractor` (`warp-zh-extractor`)
- 表：`translations/strings.json`
- 锁文件：`translations/.lock.json`
- 流程文档：README 「1. 抽取并合并到翻译表」
- 上游 commit 跨度：`b9ec4f39` (旧) → `fdd74928` (新)，179 commits

## Implementation Plan

### Step 1：fast-forward 源仓库

```bash
cd ../warp
git pull --ff-only origin master
git rev-parse HEAD  # 应为 fdd74928
```

### Step 2：跑 extract（写盘）

```bash
cd tools
cargo run -p warp-zh-extractor --release -- extract \
    --source ../../warp \
    --table ../translations/strings.json
```

### Step 3：幂等校验

```bash
cargo run -p warp-zh-extractor --release -- extract \
    --source ../../warp --table ../translations/strings.json --check
```

### Step 4：对比前后 stats + journal

读取 `strings.json` metadata.stats，对比 `b9ec4f39` 时刻基线：

| 字段 | 基线（b9ec4f39） | 同步后（fdd74928） |
|---|---|---|
| entry_count | 6640 | ? |
| new | 5400 | ? |
| translated | 1210 | ? |
| fuzzy | 30 | ? |
| obsolete | 0 | ? |
| uncertain | 4484 | ? |

### Step 5：commit

```
chore(translations): sync upstream b9ec4f39..fdd74928 (179 commits)
```
