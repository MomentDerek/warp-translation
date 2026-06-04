# tag 自动 release + README 补充 Mac 运行产物说明

## 目标

1. 在 `build-translation.yml` 中：push 任意 tag 时自动构建并发布一个**正式** GitHub Release，附带全部平台安装包（macOS 未签名 `.dmg` + Linux deb/rpm/AppImage）。
2. 在 `README.md` / `README.en.md` 补充「如何在 Mac 上运行 action 产物」的说明（下载 `.dmg`、绕过 Gatekeeper）。

## 决策（已与用户确认）

- **触发**：任意 tag（`tags: ['*']`），与上游 Warp 的发版习惯一致。
- **产物**：全部平台（macOS + Linux）。
- **状态**：正式发布（published，非 draft / prerelease）。

## 关键事实

- 现有 `package` job 已产出 `warp-zh-installer-macos-latest` / `warp-zh-installer-ubuntu-latest` 两组 artifact，正是要发布的内容。
- GitHub Actions：`push` 触发器里 `branches` + `paths` + `tags` 三者共存时为 OR 逻辑——分支推送按 paths 触发 CI，tag 推送按 tags 触发（paths 不作用于 tag）。当前已有 `branches: [main]`，故只需追加 `tags: ['*']`，**无需新建 workflow 文件**。来源：github community discussion #26821。
- macOS 产物：`--channel oss --dmg-name-suffix arm64` → 文件名 `WarpOss-arm64.dmg`，内含 `WarpOss.app`（bundle id `dev.warp.WarpOss`），arm64 / Apple Silicon。未签名 → 首次打开被 Gatekeeper 拦截。

## 实现要点

- push 触发器追加 `tags: ['*']`。
- `package` job 的 `GIT_RELEASE_TAG`：tag 推送时用真实 tag（`github.ref_name`），否则保留 `v0.0.${{ github.run_number }}` 回退。
- 新增 `release` job：`needs: package`，`if: startsWith(github.ref, 'refs/tags/')`，job 级 `permissions: contents: write`，下载 `warp-zh-installer-*` artifact，用 `gh release` 在该 tag 上创建正式 release（已存在则 `upload --clobber`，幂等可重跑）。
- 同步更新 `.github/workflows/README.md`（触发器 + release job 说明）与两份顶层 README（Mac 运行产物章节）。

## 验收

- `act -n` / yaml 解析通过（结构有效）。
- README 含 Mac 运行 `.dmg` 的完整步骤（下载来源、拖入 Applications、`xattr -dr com.apple.quarantine`）。
