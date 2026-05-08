---
name: Translate Warp project to Chinese
description: 把 ../warp 仓库的 UI 字符串非侵入式翻译为中文，工具与产物存放在当前 warp_translation 仓库
---

# Translate Warp Project to Chinese (UI Strings)

## Goal

把 `../warp`（Warp 终端，Rust 项目）**用户界面字符串**翻译为中文。

`warp_translation` 仓库的产出包括：
- **翻译工具**（Rust 编写的 CLI：`warp-zh-extractor` + `warp-zh-builder`）
- **翻译表**（`translations/strings.json`，单一事实来源，入 git）
- **构建产物**（`build/warp-zh/`：完整可编译的中文化源码副本）
- **术语表与文档**（`translations/glossary.json`、README）

源仓库 `../warp` 全程**只读**，零修改。

## Scope

**仅翻译 UI 字符串**：
- 菜单（mac menus、app_menus）
- 设置页（`app/src/settings_view/*`）
- 命令面板 / 动作描述
- 模态框 / 对话框（NUX、退出确认、删除确认等）
- 工具提示 / 占位符
- 内联横幅 / 通知（用户可见部分）

**不翻译**：
- markdown 文档、specs/、注释、LICENSE
- 错误消息（除非加入白名单）
- AI 系统 prompt（影响 LLM 行为）
- 日志 / tracing / telemetry / panic / assert
- 测试代码 / 测试 fixture
- CLI 工具输出
- 协议字符串、action ID、按键名、URL、路径、CSS 类名

## Decisions (locked 2026-05-04)

### D1：注入机制 = 源码副本生成器（方案 A）
工具读 `../warp` → 用 `syn` 抽取字面量 → 查 `translations/strings.json` → 生成 `build/warp-zh/`（完整可编译副本）。源不动，未命中翻译保留英文 → 编译永远成立。

### D2：抽取与替换技术路径
**Surgical text replacement**（详见 `research/syn-string-extraction.md`）：
- `syn = "2"` (`features = ["full", "extra-traits", "visit"]`)
- `proc-macro2 = "1"` (`features = ["span-locations"]`)，要求 ≥ 1.0.80 以使用 `Span::byte_range()`
- 只读遍历用 `syn::visit::Visit`；按 byte range 倒序 `replace_range` 写回
- **不**用 `quote!` / `to_token_stream` 重写整文件（会丢注释和格式）
- 宏调用体（`tracing::info!`、`println!` 等）默认不深入；`format!` 等少数 UI 相关宏要做白名单深入扫描
- `parse_file` 失败时降级为 copy 原文 + 写入 `report.json` 的 `parse_failures`，绝不 skip
- `include_str!` / `env!` / `cfg!` 等 18 个宏内部字面量整体跳过

### D3：UI 字符串判定算法
**白名单优先 + 黑名单兜底 + 调用点 AST 评分**（详见 `research/ui-string-heuristics.md`）：
1. 路径白名单（如 `app/src/settings_view/`）+3，黑名单（tests / telemetry / agent_sdk / ipc）−5
2. AST 父节点：UI 调用方法（`.label/.tooltip/.placeholder/.title/.span/.heading/.cta/...`）+5；UI 构造器（`MenuItem::new[1]`、`Dialog::new[1]`、`BindingDescription::new[1]`、`SettingActionPair::new[1,2]`）+5；反向调用（`dispatch_global_action`、`Keystroke::parse`、`Regex::new`、`include_str!`）−5
3. const/static 命名后缀：`_NAME/_LABEL/_TITLE/_MESSAGE/_TOOLTIP` +3；`_PATH/_URL/_KEY/_ID/_EVENT` −3
4. 测试上下文（`mod tests` / `#[cfg(test)]` / `#[test]`）−5
5. 字符串内容正则黑名单（路径、URL、UUID、snake_case、CSS 类、SQL、按键、ANSI 等 15 类）
6. 长度 < 2 或 > 1024 → 非 UI
7. 评分阈值：≥ 6 → `auto_ui`；3-5 → `uncertain`（需人工 review）；< 3 → `not_ui`（不入表）

最终决定权交给翻译表 `decision` 字段（人工可 override 算法）。

### D4：翻译表格式
**JSON 单文件主存储 + 5 态状态机**（详见 `research/translation-table-format.md`）：
- `translations/strings.json`：主表，按 `id` 字典序固定排序，每条 entry 字段顺序固定（diff 友好）
- 主键：`id`（ULID，首次抽取生成，永不变）
- 关键字段：`source` / `source_hash` / `target` / `status` / `occurrences[]` / `flags[]` / `history[]` / `first_seen_commit` / `last_seen_commit`
- 5 态：`new` → `translated` → `approved`；原文变 → `fuzzy`；源中消失 → `obsolete`（3 轮宽限后硬删）
- 增量算法：source 文本完全匹配 → 沿用；相似度 ≥ 0.7 → `fuzzy`（保留旧译 + 入 history）；新原文 → `new`；旧 entry 未被认领 → `obsolete`
- 辅助：`translations/glossary.json`（术语表，LLM 翻译时强制引用）、`translations/.lock.json`（运行时元数据，不入 git）

### D5：项目结构
```
warp_translation/
├── tools/                          # Rust 翻译工具（cargo workspace）
│   ├── Cargo.toml
│   ├── extractor/                  # warp-zh-extractor: 抽取 + 增量合并
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── builder/                    # warp-zh-builder: 生成 build/warp-zh/
│   │   ├── Cargo.toml
│   │   └── src/
│   └── translator/                 # warp-zh-translator: 调 LLM 批量翻译 (MVP 后)
│       └── ...
├── translations/
│   ├── strings.json                # 主表
│   ├── glossary.json               # 术语表
│   └── overrides.json              # 同原文多译 (MVP 不实现)
├── build/                          # gitignore；生成产物
│   └── warp-zh/                    # 翻译后的 warp 副本
├── reports/                        # gitignore；每次抽取/构建的诊断
│   ├── extract-<commit>.json
│   └── build-<commit>.json
├── .trellis/                       # 已存在
└── README.md
```

## Implementation Plan (3 PRs)

### PR1：脚手架 + 抽取器骨架
- 在 `tools/` 下创建 cargo workspace（`extractor` / `builder` 两个 bin）
- 实现 `warp-zh-extractor`：
  - 命令行：`extractor extract --source ../warp --table translations/strings.json`
  - 用 `syn::visit::Visit` 遍历，输出**所有 LitStr** 的 raw extract（暂不应用启发式过滤），写入 `reports/raw-extract.json`
  - 处理 parse 失败的 fallback
  - 处理 SKIP_MACROS 黑名单（`include_str!` 等）
- 写 README 说明项目目标与工具用法
- 测试：跑一次 extract，人工抽样确认抽到了 `"Active AI"` 等已知 UI 字符串
- **DoD**：能从 `../warp` 全量抽出 LitStr 列表，不崩溃

### PR2：UI 启发式 + 翻译表 schema 与增量
- 在 `extractor` 中实装 D3 的评分算法：路径白/黑名单、AST 父节点匹配、反向宏黑名单、内容正则、const 命名
- 实装 D4 的翻译表 schema 与增量合并：
  - 加载旧 `strings.json` → 与 fresh extract diff → 输出新 `strings.json` + report
  - ULID 生成、状态转移、history、obsolete 宽限计数
- 默认配置：阈值 6 自动入表；3-5 入 `uncertain`（带 audit 信息，人工决定）；<3 跳过
- 单元测试：覆盖 fuzzy/obsolete/new/unchanged 四种增量路径
- **DoD**：跑 `extractor extract` 产生稳定的 `strings.json`（重复跑 diff 应为空），所有条目带 audit reasons

### PR3：构建器 + 第一批翻译落地
- 实现 `warp-zh-builder`：
  - 命令行：`builder build --source ../warp --table translations/strings.json --out build/warp-zh`
  - 复制源树（保留 git 文件除 `.git`）
  - 对每个 `.rs` 重做 syn 解析 → 按 entry 的 `(source, file_match)` 在 byte range 应用替换
  - 未命中翻译 / `null target` → 保留原文
  - 输出 `reports/build-<commit>.json`
- 编译验证：`cd build/warp-zh && cargo check`（在子集上跑，至少 `app` crate）必须通过
- 写 `glossary.json` 初版（agent → 智能体？或保留英文？需确认；block / pane / workflow / drive 术语）
- 用 LLM 翻译第一批（菜单 + 设置页 about/ai 两页，约 200 条）→ 填入 `target`
- **DoD**：`build/warp-zh/` 可 `cargo check` 通过；菜单和 about/ai 设置页中文显示正确（可手工 build 应用验证）

## Acceptance Criteria

- [ ] `tools/` 下两个 bin 可 `cargo build` 通过
- [ ] `extractor extract` 能多次重跑产生相同输出（幂等）
- [ ] `strings.json` 入 git 后人工可读、diff 稳定
- [ ] `builder build` 产生的 `build/warp-zh/` 通过 `cargo check`（至少核心 crate）
- [ ] 缺失/未译条目自动回退英文，不破坏编译
- [ ] 术语表存在并被 LLM 翻译流程引用（PR3 中至少手工引用一次）
- [ ] README 描述：如何运行 extract / build、如何添加翻译、如何处理 fuzzy/obsolete

## Definition of Done

- 三个 PR 全部合并
- PR3 提供至少 2 个设置页 + 主菜单的端到端中文化效果（截图或视频）
- 工具可重跑、增量识别正确
- 文档完备（README + glossary）

## Out of Scope

- LICENSE 翻译
- markdown 文档（README/FAQ/specs）翻译
- Rust 注释翻译
- 错误消息翻译（除非加入白名单，MVP 不做）
- AI 系统 prompt 翻译
- 日志 / 测试 / telemetry 字符串
- CLI 工具输出（`crates/warp_cli/`）
- macOS 打包/签名/分发
- 把翻译回推到上游 Warp 仓库
- LLM 自动翻译流水线（PR3 用一次性脚本调用即可，正式自动化留作后续 task）

## Research References

- [`research/syn-string-extraction.md`](research/syn-string-extraction.md) — surgical text replacement + Span::byte_range，避免 quote! 重写
- [`research/ui-string-heuristics.md`](research/ui-string-heuristics.md) — 路径白/黑名单 + AST 父节点评分 + 15 类正则 + const 命名规则
- [`research/translation-table-format.md`](research/translation-table-format.md) — JSON + ULID + 5 态 + 增量算法

## Technical Notes

- Rust toolchain：跟随 `../warp/rust-toolchain.toml`（避免工具与目标 Rust 版本错位）
- syn 错误降级策略：`parse_file` 失败时仍 copy 原文，仅记录到 report；不 panic 不 skip
- Fuzzy 阈值：normalized Levenshtein ≥ 0.7（保守，宁漏勿错）
- Obsolete 宽限：3 次 extract 未回归 → 硬删
- 翻译表与术语表都入 git，便于多人/CI 协作
- `build/warp-zh/` 在 `.gitignore`（构建产物，可重生成）
- `tools/` 自身要 lint / fmt / test 全绿

## Subtasks (post-brainstorm)

PR1/PR2/PR3 是否拆分为独立子 task 由 implement 阶段决定。当前 task 作为伞 task 跟踪整体进度。
