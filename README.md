# warp_translation

> 📖 **English version / 英文版**: [README.en.md](README.en.md)

[Warp](https://github.com/warpdotdev/Warp) 终端的中文本地化项目 —— **不修改上游源码**。

这是一个纯粹的"覆盖层"方案：从 `../warp` 中抽取每一条 Rust 字符串字面量，把译文存进本仓库的 `translations/strings.json`，再构建出一份本地化的源码副本，像平常一样 `cargo build` 即可。上游始终保持原样。

```
上游 Warp (../warp，只读)
        │
        ▼ 抽取
warp-zh-extractor ──► translations/strings.json   (唯一事实来源)
                                  │
                                  ▼ 构建
                       warp-zh-builder ──► build/warp-zh/   (可编译的中文源码)
```

缺失或过期的条目会自动回退到英文，因此构建永远成功。增量式：上游变动时，只有新增/改动的字符串需要重新翻译。

**状态**（表快照，对齐上游 `v0.2026.06.03.09.49.stable_00`）：6,874 条 —— 全部已翻译，0 条 fuzzy，0 条 obsolete。

## 快速开始

```bash
# 0. 克隆本仓库，并把 Warp 放在它旁边
git clone https://github.com/warpdotdev/Warp.git ../warp

# 1. 从上游重新抽取（幂等；只有新增/改动的条目会翻转状态）
cd tools && cargo run -p warp-zh-extractor -- extract \
    --source ../../warp \
    --table ../translations/strings.json \
    --lock ../translations/.lock.json

# 2. 构建本地化源码树
cd tools && cargo run -p warp-zh-builder -- build \
    --source ../../warp \
    --table ../translations/strings.json \
    --out ../build/warp-zh \
    --report ../reports/build.json

# 3. 编译本地化后的 Warp
cd build/warp-zh && MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp
```

就这么简单。本地化后的二进制产物位于 `build/warp-zh/target/`。

## 在 Mac 上运行 action 编译产物

不想本地编译，也可以直接用 GitHub Actions 构建好的安装包。

### 获取 `.dmg`

- **正式版本（推荐）**：仓库 [Releases](../../releases) 页面 —— 每个 tag 都会自动发布一个 release，里面附带 macOS 的 `WarpOss-arm64.dmg`（以及 Linux 的 deb/rpm/AppImage）。
- **任意一次构建**：进入 [Actions](../../actions) → 选择某次 *Build Chinese Warp* 运行 → 页面底部 **Artifacts** → 下载 `warp-zh-installer-macos-latest`（解压后即为 `.dmg`）。

> 产物为 **Apple Silicon（arm64）** 架构；Intel Mac 不适用，请改用上面「快速开始」自行编译。

### 安装并绕过 Gatekeeper

该 `.dmg` 用 `script/bundle --nosign` 构建，**未经签名 / 公证**，首次打开会被 macOS Gatekeeper 拦截（提示「无法打开，因为无法验证开发者」）。步骤：

```bash
# 1. 双击挂载 WarpOss-arm64.dmg，把 WarpOss.app 拖入「应用程序」
# 2. 清除隔离属性（二选一）：

#  a) 命令行一次解决：
xattr -dr com.apple.quarantine /Applications/WarpOss.app

#  b) 或在「访达」里右键 WarpOss.app → 打开 → 在弹窗里再次点「打开」
```

之后即可正常启动。`WarpOss.app` 是 Warp 的 OSS 自包含构建（`oss` channel，bundle id `dev.warp.WarpOss`），与官方签名版互不冲突，可并存。

## 仓库结构

| 路径 | 用途 |
|---|---|
| `tools/extractor/` | `warp-zh-extractor` —— 扫描 `.rs` 文件，应用 UI 字符串启发式规则，合并进翻译表 |
| `tools/builder/` | `warp-zh-builder` —— 复制源码树并替换已翻译的字面量；产出可构建的中文版 Warp |
| `tools/translations/kit/` | `build_batch.py`、`apply_batch.py` —— 批量翻译的 Python 辅助脚本 |
| `translations/strings.json` | 翻译表（唯一事实来源） |
| `translations/glossary.json` | 术语决策（约 32 个术语）与翻译理念 |
| `.claude/workflows/` | [Claude Code](https://claude.com/claude-code) Workflow 脚本，用于并行批量翻译与上游同步 |
| `.trellis/` | 任务日志与规范 —— 开发本项目所用的 [Trellis](https://github.com/) 工作流。仅供参考；运行工具时并不需要 |
| `build/warp-zh/` | `warp-zh-builder` 的产物（已 gitignore） |
| `reports/` | 抽取/构建诊断信息（已 gitignore） |

## 五大工作流

### A. 从上游重新抽取

`../warp` 变动后重新运行。幂等：HEAD 稳定的输入 → 字节级一致的 `strings.json`。

```bash
cd tools
cargo run -p warp-zh-extractor -- extract \
    --source ../../warp \
    --table ../translations/strings.json \
    --lock ../translations/.lock.json
```

它做了什么：用 `syn` 遍历 `../warp` 中每个 `.rs` 文件，应用 UI 字符串启发式规则（路径允许/拒绝列表、UI 方法/构造器识别、内容正则、句式结构特征），为每条字面量赋予 `score`/`verdict`，并增量合并进 `strings.json`。已有译文会被保留；上游文本变更会把条目翻转为 `fuzzy`；消失的条目翻转为 `obsolete`（连续 3 次抽取缺失后硬删除）。

**检查模式**（CI / 预提交）：

```bash
cargo run -p warp-zh-extractor -- extract --source ../../warp \
    --table ../translations/strings.json --check
```

若 `strings.json` 不是规范形态（排序顺序 / 统计数据 / 字段顺序），则以非零状态退出。

**原始模式**（调试 —— 转储启发式过滤前的全部字面量）：

```bash
cargo run -p warp-zh-extractor -- raw-extract \
    --source ../../warp --out ../reports/raw-extract.json
```

### B. 构建本地化源码

```bash
cd tools
cargo run -p warp-zh-builder -- build \
    --source ../../warp \
    --table ../translations/strings.json \
    --out ../build/warp-zh \
    --report ../reports/build.json
```

镜像源码树（跳过 `target/`、`.git/`、`node_modules/` 等），用 `syn` 重新解析每个 `.rs`，并替换 `target` 非空且 `status ∈ {translated, approved, fuzzy}` 的字面量。替换按字节逆序进行以保持偏移量；引号风格根据内容自动在 `"..."` 与 `r#"..."#` 之间选择。未翻译的字面量保持英文 —— 构建始终能编译通过。

**编译验证**（macOS）：

```bash
cd build/warp-zh
MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp
```

`-p warp` 是应用 crate（见 `app/Cargo.toml`）。`MACOSX_DEPLOYMENT_TARGET` 的要求来自 Warp 自身的 `app/build.rs`，并非本项目所加。

### C. 翻译单条目

`warp-zh-builder` 上的两个辅助子命令，用于增量翻译：

```bash
# 列出某个/某些文件的 status=new 条目
cargo run -p warp-zh-builder -- list-batch \
    --table ../translations/strings.json \
    --filter app/src/app_menus.rs \
    --status new > /tmp/candidates.json

# 写入一批译文
# 输入: { "flag": "<你的-flag>",
#          "translations": {
#            "<id>": { "target": "中文" },
#            "<id>": { "target": null, "do_not_translate": true }
#          } }
cargo run -p warp-zh-builder -- apply-batch \
    --table ../translations/strings.json \
    --input /tmp/batch.json \
    --now 2026-05-08T00:00:00Z
```

`apply-batch` 写入 target，把 status 翻转为 `translated`，附上 flag，并重新规范化整张表。

### D. 并行批量翻译（进阶 —— 需要 Claude Code）

对于较大的批次（约 75–600 条），有一个 Claude Code Workflow 会并行分发 N 个子代理：

```
1. 构建候选集 → tools/translations/kit/build_batch.py
2. 翻译       → .claude/workflows/translate_batch.mjs   (N 个 implementer 子代理)
3. 应用       → tools/translations/kit/apply_batch.py   (违反不变量时硬失败)
4. 检查       → trellis-check 子代理
```

完整的端到端步骤：见 [`tools/translations/kit/RUNBOOK.md`](tools/translations/kit/RUNBOOK.md)。
文件/API 参考：见 [`tools/translations/kit/README.md`](tools/translations/kit/README.md)。

此流程依赖 Claude Code 的 `Workflow` 工具，以及 `.claude/agents/` 下提供的 `trellis-implement` / `trellis-check` 子代理。没有 Claude Code 时，改用工作流 C（手动 `apply-batch`）—— 表格式与不变量完全一致。

### E. 上游同步（当上游 Warp 发生变动时）

一个 Claude Code Workflow，它会快进 `../warp`、重新抽取、对比变更前后的 `strings.json`、按源码区域分类变更，并写出一份 Markdown 报告：

```js
Workflow({
  scriptPath: ".claude/workflows/sync-upstream-translations.ts",
  args: {
    repoRoot: "<本仓库的绝对路径>",
    srcRepo:  "<上游 warp 克隆的绝对路径>",
  }
})
```

输出：`reports/sync-translation-changes.{json,md}`。报告会按源码区域列出新增 / fuzzy / obsolete / 删除的内容，并推荐下一批要翻译的条目。

对 `../warp` 只读（仅快进 —— 绝不强推、绝不做非快进合并）。若上游发生分叉，合并步骤会中止。

## 翻译策略

翻译时的逐条目决策流程（首个命中者优先）：

1. **文档注释误报**（`/// …` 片段）—— 打 flag `extractor_false_positive_doc_comment`，无 target。
2. **`.expect()` / `panic!` / `unreachable!`** 消息 —— 打 flag `panic_message`，无 target。
3. **遥测 / 仅日志** 字面量（`tracing::*`、日志文件 —— 非 UI）—— 打 flag `telemetry_payload`，无 target。
4. **`fn search_terms()`** 关键词 —— 双语追加：`target = "<source> <中文>"`（保留英文搜索，叠加中文）。
5. **wgpu 调试标签 / 测试夹具 / 协议键**（serde/YAML 字段名、特性/模型标识符）—— 打对应的子 flag，无 target。
6. **常规 UI 文本** —— 按契约翻译为中文。

子 flag 白名单（每个被标记的条目恰好一个）：`panic_message`、`telemetry_payload`、`extractor_false_positive_doc_comment`、`test_fixture`、`wgpu_debug_label`、`protocol_key`。

`apply_batch.py` 强制执行的翻译不变量：

- 占位符（`{}`、`{name}`、`{0}`）与 strftime 代码（`%b`、`%d`、…）原样保留
- 首尾空白与换行形态保留
- 品牌字面量逐字保留（Warp、MCP、AI、OAuth、GitHub、…）
- 中文标点用全角（`，。；！？`）；拒绝 ASCII `...`（必须是 `……`）
- 双语 target 以 `"<source> "` 开头（一个 ASCII 空格，无标点）

完整契约：[`.trellis/spec/guides/translation-contract.md`](.trellis/spec/guides/translation-contract.md)。

## 工具链

`tools/rust-toolchain.toml` 锁定 Rust 1.92.0，与 `../warp` 保持一致。工具链不匹配会导致 `cargo check` 在不同的 rustc 下重新编译大量重型依赖。

## 设计文档

- [翻译表格式](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/research/translation-table-format.md)
- [`syn` 字符串抽取](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/research/syn-string-extraction.md)
- [UI 字符串启发式规则](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/research/ui-string-heuristics.md)
- [初始 PRD](.trellis/tasks/archive/2026-05/05-04-translate-warp-project-to-chinese/prd.md)

## 许可证

MIT —— 见 [`LICENSE`](LICENSE)。

请注意，构建产物 `build/warp-zh/` 是上游 Warp（AGPLv3 + MIT）的衍生作品，仍受上游许可证约束。本仓库的 MIT 许可证仅覆盖本项目原创的工具代码与翻译数据。
