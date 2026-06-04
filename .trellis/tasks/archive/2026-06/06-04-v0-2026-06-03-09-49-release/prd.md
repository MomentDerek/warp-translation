# 同步上游 v0.2026.06.03.09.49 并发布 release

## 目标

把翻译覆盖层对齐到上游最新 stable 版本，并用纯版本号 tag 触发自动 release。

- 发布版本：`v0.2026.06.03.09.49`（无 channel 后缀；上游对应 tag 为 `v0.2026.06.03.09.49.stable_00`，commit `2249469e5d24e472cee6ce97d3d324293f67db71`）。

## 关键发现（已验证）

- `../warp` 的 HEAD 已经正好在 `2249469e`（目标 stable tag），工作树干净。
- 对 `2249469e` 重新抽取 `translations/strings.json`：`added=0 changed=0 obsoleted=0`，`git diff` 为空，`--check passed`。
  → **翻译表早已与上游 `2249469e` 完全同步**（6874 条全部 translated，fuzzy=0）。无需重译。
- 唯一过时项：`build-translation.yml` 的 `DEFAULT_WARP_REF` 仍指向旧 commit `2566f54af7c3e71facfe1865f2c492549b14248a`（= v0.2026.05.27.09.22），落后 130 个 commit。

## 实现要点

1. 更新 `DEFAULT_WARP_REF`：`2566f54...` → `2249469e5d24e472cee6ce97d3d324293f67db71`，并更新其上方注释指明对应 stable tag。
2. 同步两份 README 的状态行（旧值「6,794 条 / 64 fuzzy / 7 obsolete」已过时 → 实际 6,874 条全部已翻译，fuzzy 0）。
3. 提交（pin + 文档）。
4. 打 tag `v0.2026.06.03.09.49` 并 push → 触发 release job 自动构建并发布。

## 验收

- `DEFAULT_WARP_REF` == `2249469e5d24e472cee6ce97d3d324293f67db71`。
- `strings.json` 对该 commit `--check passed`（已验证）。
- tag `v0.2026.06.03.09.49` 推送后，Actions 的 *Build Chinese Warp* run 跑出 `release` job 并在该 tag 上发布带全平台安装包的正式 release。
