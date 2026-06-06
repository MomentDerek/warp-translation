# 同步上游 06.05.dev 并发布翻译版 release

## 目标

把翻译覆盖层对齐到上游 dev 版 `v0.2026.06.05.09.22.dev_00`（commit `327445ee8506bcf77656eaeafc7bc046e3105cfa`），翻译增量条目，并用纯版本号 tag `v0.2026.06.05.09.22` 触发 CI 自动 release。

## 背景

- 当前 pin：stable `v0.2026.06.03.09.49.stable_00`（commit `2249469e`），6,874 条全部 translated，0 fuzzy / 0 obsolete。
- 上游 stable 无新版；dev 已到 06.06。用户选择基于 **06.05.dev** 出一个翻译版。
- `../warp` 当前 HEAD 在 `2249469e`，工作树干净。

## 步骤

1. **Sync & Extract**（工作流 E 的第一阶段，手动指定 tag）：
   - 快照 `strings.json` → before。
   - `cd ../warp && git checkout 327445ee`（只读，detached）。
   - 从 `tools/` 跑 `warp-zh-extractor extract`。
   - 用 `COMPARE_PY` diff before/after，得到 new/fuzzy/obsolete/deleted 计数。
2. **翻译增量**：对 new/fuzzy 条目按翻译契约翻译（量小则手动 apply-batch；量大则并行批量工作流）。委派 trellis-implement。
3. **同步文档**：更新两份 README 的状态行与 pin 引用；更新 `DEFAULT_WARP_REF` → `327445ee...`。
4. **提交**。
5. **打 tag** `v0.2026.06.05.09.22` 并 push → 触发 CI `release` job 构建并发布全平台安装包。

## 验收

- `strings.json` 对 `327445ee` `--check passed`，0 fuzzy / 0 obsolete。
- `DEFAULT_WARP_REF == 327445ee8506bcf77656eaeafc7bc046e3105cfa`。
- README 状态行准确反映新条目数。
- tag `v0.2026.06.05.09.22` 推送后 Actions 跑出 release。

## 决策点（需用户确认）

- 翻译完成后是否立即 push tag 触发正式 release（发布动作不可逆，需用户确认）。
