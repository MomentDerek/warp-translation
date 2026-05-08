# warp_translation

把 [Warp](https://github.com/warpdotdev/Warp) 终端的 UI 字符串翻译为中文，**不修改源仓库**。

## 概览

```
源仓库 ../warp (只读)
        │
        ▼
warp-zh-extractor   ──┐
                      ├──>  translations/strings.json (主表，入 git)
                      │
                      ▼
warp-zh-builder    ───>  build/warp-zh/  (完整可编译的中文化 Warp 源码副本)
```

- 源仓库 `../warp` 全程只读；翻译以**外置覆盖**形式存放在本仓库
- 翻译表是单一事实来源；缺失/失效条目自动回退英文，编译永远成立
- 工具增量更新：源仓库变化时只重译新增/变更条目

## 目录结构

| 路径 | 说明 |
|---|---|
| `tools/` | Rust 翻译工具（cargo workspace）|
| `tools/extractor/` | `warp-zh-extractor`：抽取源码字符串字面量 |
| `translations/strings.json` | 翻译主表（PR2 起生成）|
| `translations/glossary.json` | 术语表（PR3 起生成）|
| `build/warp-zh/` | 翻译后的源码副本（gitignore，可重生成）|
| `reports/` | 抽取/构建诊断（gitignore）|
| `.trellis/` | 任务管理与规范（Trellis）|

## 用法

### 1. 抽取并合并到翻译表（PR2 主入口）

```bash
cd tools
cargo run -p warp-zh-extractor -- extract \
    --source ../../warp \
    --table ../translations/strings.json \
    --lock ../translations/.lock.json
```

完整流水线：
1. 遍历 `../warp` 所有 `.rs`，用 `syn` 抽出字面量（含 AST 父调用、所在 const 名、是否在测试模块等上下文，PR2 由 `extract.rs` 内联记录）
2. 对每条字面量跑 D3 启发式（路径白/黑名单、UI 方法/构造器、const 后缀、15 类内容正则、句式特征），算出 `score`/`verdict`/`reasons`
3. 评分 ≥6 → `auto_ui`，3-5 → `uncertain`，<3 → 丢弃
4. 增量合并到 `translations/strings.json`：
   - 原文一字不差 → 复用旧条目（status/target 保留）
   - normalized Levenshtein ≥ 0.7 → 认领旧条目，旧原文入 `history`，状态置 `fuzzy`
   - 全新原文 → 新条目，状态 `new`
   - 旧条目本轮未被认领 → 状态 `obsolete`；3 次抽取仍未回归 → 硬删
5. 重排 entries（按 `id` 字典序）+ 重算 `metadata.stats` → 写盘

幂等性：源仓库 HEAD 不变时连跑两次，`strings.json` 字节级一致（`updated_at` 仅在条目实际变化时刷新；`obsoleted_at_run` 仅在条目从 alive→obsolete 转移时写入）。

#### 检查模式（CI）

```bash
cargo run -p warp-zh-extractor -- extract \
    --source ../../warp --table ../translations/strings.json --check
```

不写盘；若 `strings.json` 不在 canonical 形态（排序错误 / stats 没重算 / 字段顺序变了）则非零退出。CI 用 `extract` 跑一次再跑 `--check`，避免人工编辑破坏 diff 友好性。

### 2. 原始抽取（PR1 模式，调试/审计用）

```bash
cargo run -p warp-zh-extractor -- raw-extract \
    --source ../../warp \
    --out ../reports/raw-extract.json
```

输出 `reports/raw-extract.json`，列出全部字面量（不应用启发式过滤），便于回查 PR2 漏抽 / 误判。

### 3. 生成中文化副本（PR3）

```bash
cd tools
cargo run -p warp-zh-builder -- build \
    --source ../../warp \
    --table ../translations/strings.json \
    --out ../build/warp-zh \
    --report ../reports/build-pr3.json
```

行为：
1. 把 `../warp` 整棵目录树镜像到 `build/warp-zh/`（跳过 `target/`、`.git/`、`node_modules/`、`.cargo/`、`build/`、`dist/`，与抽取器同一份 `is_ignored_dir` 列表）。非 `.rs` 文件按字节复制；`Cargo.lock`、`rust-toolchain.toml`、资源文件、点文件全部保留。
2. 对每个 `.rs` 重新 `syn::parse_file` 并复用抽取器的 `Visit` 走法收集字面量字节区间。`syn` parse 失败的文件按字节复制并记入 `parse_failures`，永不 panic。
3. 对每条字面量按原文查 `translations/strings.json` 索引（`HashMap<&str, &Entry>`）。仅当 entry 的 `target` 非空且 `status ∈ {translated, approved, fuzzy}` 时替换；否则保留英文（编译永远成立）。
4. 替换按 byte_range 倒序应用，保证早区间不会被晚区间的字节偏移失效。输出引号风格优先 `"..."` 并按 Rust 转义规则处理 `\\`、`\"`、`\n` 等；当目标含较多反斜杠/引号时回退 `r#"..."#`。`b"..."` 字节串字面量不替换。
5. 建立时机标记 `.warp-zh-build-marker`：再次构建若 out 目录不存在或带此标记则覆盖；否则拒绝写入，避免误删用户数据。
6. 可选 `--report` 写出 `reports/build-pr3.json`：`files_copied/files_modified/files_parse_failed/literals_replaced/literals_kept_english`、`parse_failures[]`、`untranslated_files[]` 前 50。

幂等性：源仓库 + 翻译表不变时连跑两次，`build/warp-zh/` 字节级一致。

#### 编译验证

```bash
cd build/warp-zh
MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp
```

`-p warp` 是 app crate（见 `app/Cargo.toml` 的 `name = "warp"`）。

> macOS 上 warp 自身的 `app/build.rs` 要求设置 `MACOSX_DEPLOYMENT_TARGET`，与翻译无关；翻译质量本身不会影响编译（前提是 builder 字面量替换正确）。

### 4. 翻译条目（PR3 翻译流）

`warp-zh-builder` 内置两个辅助子命令，用于增量翻译条目：

```bash
# 列出某些文件中所有 status=new 的条目
cargo run -p warp-zh-builder -- list-batch \
    --table ../translations/strings.json \
    --filter app/src/app_menus.rs \
    --filter app/src/settings_view/about_page.rs \
    --filter app/src/settings_view/ai_page.rs \
    --status new > /tmp/candidates.json

# 应用一批翻译。input 形如：
# { "flag": "pr3_first_batch",
#   "translations": {
#     "<id>": { "target": "中文" },
#     "<id>": { "target": null, "do_not_translate": true }
#   } }
cargo run -p warp-zh-builder -- apply-batch \
    --table ../translations/strings.json \
    --input /tmp/batch.json \
    --now 2026-05-08T00:00:00Z
```

`apply-batch`：把映射写入条目的 `target`、把 `status` 改成 `translated`、附加 `flag`（默认 `pr3_first_batch`）和可选 `do_not_translate` flag、刷新 `updated_at`，最后按规范化形态（按 id 排序、重算 stats）写盘。

PR3 已完成第一批 227 条翻译：`app/src/app_menus.rs`（43）+ `app/src/settings_view/about_page.rs`（3）+ `app/src/settings_view/ai_page.rs`（181）。其中 45 条标 `do_not_translate`（产品名 / `expect()` panic 文 / 搜索关键词 / 占位符），182 条带中文 target。

术语决策见 `translations/glossary.json`：32 条术语 + 翻译哲学说明（产品名保留英文；行为概念给中文；占位符与快捷键修饰符原样保留）。

> **本 PR 范围**：MVP，227/6327 条已翻译。后续 PR 会继续扩张到其它 settings page、command palette、对话框等。

## 设计文档

- 总体决策：[`.trellis/tasks/05-04-translate-warp-project-to-chinese/prd.md`](.trellis/tasks/05-04-translate-warp-project-to-chinese/prd.md)
- 抽取器内核：[`research/syn-string-extraction.md`](.trellis/tasks/05-04-translate-warp-project-to-chinese/research/syn-string-extraction.md)
- UI 字符串判定：[`research/ui-string-heuristics.md`](.trellis/tasks/05-04-translate-warp-project-to-chinese/research/ui-string-heuristics.md)
- 翻译表格式：[`research/translation-table-format.md`](.trellis/tasks/05-04-translate-warp-project-to-chinese/research/translation-table-format.md)

## 工具链

`tools/rust-toolchain.toml` 锁定 Rust 1.92.0，与 `../warp` 一致，避免 `cargo check` 工具版本错位。
