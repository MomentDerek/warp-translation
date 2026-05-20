---
name: Review fuzzy entries after upstream sync fdd74928
description: 复核 sync fdd74928 后 5 条带 target 的 fuzzy 条目，按上游新原文调整翻译并转回 translated
---

# Review fuzzy entries after upstream sync fdd74928

## Goal

`05-20-sync-upstream-to-fdd74928` 同步后 `strings.json` 出现 57 条 fuzzy，其中 5 条带原翻译（原 `translated`）。本任务对这 5 条逐条核对上游新原文，按 [[glossary]] 与既有翻译惯例调整 target，状态转回 `translated`，避免编译产物里这部分字符串回退到英文。

> 上轮 sync journal 写的"8 条 fuzzy"是粗略统计错误：实际本轮新增 fuzzy 27 条（30→57），其中 6 条来自 translated 回退，但只有 5 条原本带 target —— 第 6 条 `01KQXQV12J2T28M0CZMGZQVDY7`（ai_page changelog 长文）原本 target=None / do_not_translate，无需处理。

## What I already know

5 条待复核 fuzzy：

| # | id | file | 上游变化 | 旧翻译 |
|---|---|---|---|---|
| 1 | 01KQXQV12A4VD0XRF4PANHY73M | settings_view/billing_and_usage_page_v2.rs | `purchase add-on credits` → `enable add-on credits` | `请联系团队管理员购买附加积分。` |
| 2 | 01KQXQV12A9ZE927EKG8AKDRPW | terminal/view/shared_session/conversation_ended_tombstone_view.rs | `Continue this cloud conversation locally` → `Continue this cloud conversation` | `在本地继续此云端会话` |
| 3 | 01KQXQV12AHGDT7Q1STK2BR8EA | settings_view/teams_page.rs | `Contact sales` → `Contact Sales`（仅大小写） | `联系销售` |
| 4 | 01KQXQV12DDZ9SGBBTCZ8F5Q7Z | settings_view/teams_page.rs | 加 `Restrict by domain —` 前缀 | `仅允许使用特定域名邮箱的用户通过邀请链接加入您的团队。` |
| 5 | 01KQXQV12GXTSEVFQ6Q1FY71VQ | settings_view/teams_page.rs | `subscription payment issue` → `past-due payment` | `由于订阅付款问题，团队邀请已被限制。` |

每条都属于"原意基本保留、措辞微调"，复核成本低。

## Approach

1. 对每条 fuzzy entry：根据上游新原文调整 target（或确认原翻译直接可用）。
2. 写 `tools/scratch/fuzzy-review-batch.json`：`{flag, translations: {<id>: {target: "..."}}}`。
3. 跑 `warp-zh-builder apply-batch`，状态 → translated，flag 标 `pr-fuzzy-review-fdd74928`。
4. 跑 extractor `--check` 验证幂等。
5. journal + commit + finish-work。

## Per-entry decisions（草案）

1. **`enable add-on credits`** — `购买` → `启用`：
   `请联系团队管理员启用附加积分。`
2. **`Continue this cloud conversation`**（去掉 `locally`）：
   `继续此云端会话`
3. **`Contact Sales`**（仅 S 大小写改动）：
   `联系销售`（中文不变）
4. **`Restrict by domain — only allow ...`** —— 前缀加 `按域名限制`，[[glossary]] 中既有；保留破折号：
   `按域名限制 — 仅允许使用特定域名邮箱的用户通过邀请链接加入您的团队。`
5. **`past-due payment`** — `订阅付款问题` → `付款逾期`：
   `由于付款逾期，团队邀请已被限制。`

## Acceptance Criteria

- [ ] 5 条 fuzzy entries 全部转 `translated`，target 与上游新原文匹配
- [ ] `extract --check` exit 0（幂等）
- [ ] fuzzy 计数 57 → 52（-5）；translated 1184 → 1189（+5）
- [ ] 新 flag `pr-fuzzy-review-fdd74928` 出现在 5 条 entries 的 flags 上
- [ ] commit message 注明跨度（fuzzy review after sync fdd74928）

## Definition of Done

- 5 条目状态翻为 translated、target 与新原文契合
- `extract --check` 通过
- journal 记录每条决策
- commit + finish-work

## Out of Scope

- 其它 52 条 fuzzy（多无 target，属于 new/uncertain 范畴，等后续按页面切分时一起翻译）
- 51 条 obsolete（自然落入，三轮未回归才硬删，无需干预）
- 145 条新增 new 条目（独立后续任务，按页面切分）
- 重 build `build/warp-zh`、`cargo check`（gitignore + 本轮无源码逻辑改动）
- glossary 更新

## Technical Notes

- 工具：`warp-zh-builder apply-batch --table ../translations/strings.json --input ... --now <ts> --flag pr-fuzzy-review-fdd74928`
- 表：`translations/strings.json`
- 流程文档：README「4. 翻译条目（PR3 翻译流）」
- 上游 commit：`fdd74928de30add61f15b7cc60c316f2da98a555`
- 临时 batch JSON 文件：`tools/scratch/fuzzy-review-batch.json`（gitignore；用完即删）

## Implementation Plan

### Step 1：写 batch JSON

把 5 条 `{id: {target: "..."}}` 写到 `tools/scratch/fuzzy-review-batch.json`，按上面的 Per-entry decisions 填。

### Step 2：apply-batch

```bash
cd tools
cargo run -p warp-zh-builder --release -- apply-batch \
    --table ../translations/strings.json \
    --input scratch/fuzzy-review-batch.json \
    --now 2026-05-20T11:00:00Z
```

### Step 3：幂等校验

```bash
cargo run -p warp-zh-extractor --release -- extract \
    --source ../../warp --table ../translations/strings.json --check
```

### Step 4：journal + commit + finish-work
