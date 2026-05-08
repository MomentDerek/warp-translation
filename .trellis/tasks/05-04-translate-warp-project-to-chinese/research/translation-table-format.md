# Research：翻译表存储格式与增量更新机制

- **Query**: 为"源码字符串 → 中文翻译"的覆盖式翻译工具设计存储格式与增量更新机制
- **Scope**: 外部参考（gettext / Fluent / i18next / Crowdin / Pontoon / Weblate）+ 本项目内部约束（Warp Rust 源码抽取，非侵入，编译保证 fallback）
- **Date**: 2026-05-04

---

## 0. 设计目标回顾（来自 prd.md / D1）

- 工具流程：读 `../warp` → `syn` 抽取字符串字面量 → 查翻译表 → 生成 `build/warp-zh/`
- 翻译表是工具的**单一事实来源**（single source of truth）
- 韧性要求：
  - 已译条目稳定保留
  - 源中删除的条目自动跳过
  - 源中新增的条目标"待翻译"
  - 源中修改的条目（原文变化）警告"可能需重译"
  - 任何缺失/失效条目，生成阶段 fallback 到英文（编译永远成立）
- 翻译表预期规模（粗估）：UI 字符串 1500 ~ 5000 条，单条平均 3~80 字符，少量长描述（200~500 字符）

---

## 1. 存储格式比较

### 1.1 比较表

| 格式 | 人类可读 | 批量编辑（脚本/手工） | git diff 友好度 | 合并冲突 | 工具/生态 | 复杂结构（注释、多元数据） | 适合本项目 |
|---|---|---|---|---|---|---|---|
| **JSON** | 中（转义噪声多，无注释） | 极佳（标准库直接 parse） | 良（每条目一行可保证稳定 diff） | 中（key 顺序可控） | 极广（i18next / VSCode `nls.metadata.json`） | 弱（无原生注释） | ★★★★★ |
| **JSONC / JSON5** | 良（支持注释） | 好（需第三方解析） | 良 | 中 | 中（VSCode 用） | 中 | ★★★★ |
| **TOML** | 极佳 | 中（嵌套表 / 数组维护手工繁琐） | 良 | 低（多行表结构合并易冲突） | 广（Rust 原生） | 中（注释友好） | ★★★ |
| **YAML** | 良 | 差（缩进敏感、易踩坑） | 中 | 高（缩进合并冲突） | 广 | 强 | ★★ |
| **Fluent `.ftl`** | 极佳（专为 i18n 设计） | 中（需 fluent 解析器） | 良 | 中 | 中（Mozilla / Pontoon） | 强（变量 / 复数 / 性别） | ★★★（功能过剩） |
| **gettext `.po` / `.pot`** | 良（`msgid` / `msgstr` 块） | 极佳（`msgmerge` 工具内建增量合并！） | 良（块状 diff 清晰） | 中 | 极广（po4a / Weblate / Crowdin / Transifex 全部原生支持） | 强（注释、`#~` obsolete、上下文） | ★★★★★ |
| **SQLite** | 差（二进制） | 极佳（SQL） | 极差（二进制不可 diff） | 极高 | 广 | 强 | ★（不能放 git 评审） |
| **CSV** | 中 | 极佳（Excel / pandas） | 中（行级 diff 友好但转义脆弱） | 低（行追加合并良好） | 极广 | 弱 | ★★★ |

### 1.2 关键淘汰理由

- **SQLite**：二进制，无法 git diff、无法 PR review，违背"翻译表入 git"的诉求。可作为缓存索引层但不作主存储。
- **YAML**：缩进敏感 + 长字符串多行处理坑多（`>-` / `|` / `\n` 转义），合并冲突最难调，Rust 字符串里常含引号、转义、多行，YAML 表达力反而成负担。
- **CSV**：表头难承载多元数据（注释、状态、commit hash 等），引号转义脆弱（Rust 字符串内含逗号/换行多）。
- **Fluent**：功能过剩。Fluent 的核心价值是"复数 / 性别 / 嵌套消息引用"，本项目是覆盖式硬替换，不需要这些。
- **TOML**：长字符串和嵌套表不友好（每条 entry 是一个 `[[entries]]` 表，diff 很啰嗦）。Rust 项目里 TOML 主要用于配置而非数据。

### 1.3 决赛圈：JSON vs gettext `.po`

| 维度 | JSON | `.po` |
|---|---|---|
| 核心数据模型 | 自由 schema（任意字段） | 固定 schema（`msgid` / `msgstr` / `#:` 注释 / `#,` flags） |
| 增量合并 | 自己写算法 | `msgmerge old.po new.pot` 一条命令搞定（业界 30 年验证） |
| obsolete 标记 | 自己设计字段 | `#~ msgid "..."`（标准） |
| fuzzy（原文变更）标记 | 自己设计 | `#, fuzzy`（标准） |
| 上下文消歧 | 自己设计 key | `msgctxt`（原生） |
| 翻译平台 | 部分支持（i18next 系） | 全部原生支持（Crowdin / Weblate / Transifex / Pontoon / Lokalise） |
| Rust 生态 | `serde_json` 一行解析 | `polib` / `gettext-rs`（活跃但需引入） |
| 工具链熟悉度 | 高 | 中（学习曲线在注释/标记语法） |
| LLM 翻译流水线 | 直接 prompt JSON | 需要先解析成结构再喂给 LLM |
| 自定义元数据（如 `stable_id`、源 commit hash） | 任意字段直接加 | 只能塞进 `# extracted-comment` 注释，半结构化 |

### 1.4 推荐

**主存储用 JSON（一行一条目，稳定排序），不引入 gettext。**

理由：

1. **元数据自由**：本项目除原文/译文外，还需 `stable_id` / `original_hash` / `status` / `occurrences[]` / `last_seen_commit` 等若干字段。JSON schema 自由扩展，`.po` 强行塞注释脏。
2. **LLM 流水线友好**：批量翻译就是把待译条目序列化成 JSON 喂给 Claude，再把 JSON 回填，零阻抗。
3. **Rust 工具链零依赖**：`serde_json` 标准能力，`syn` 抽取后直接 `serde` 序列化。
4. **gettext 的核心价值（`msgmerge` / `#, fuzzy`）我们用 50 行 Rust 完全可重新实现**——增量算法本身不复杂（见第 4 节伪代码）。
5. **git diff 友好**：通过排序 + 单行条目数组，diff 输出稳定且易 review（详见第 7 节）。

**保留备选**：若未来要接入 Crowdin / Weblate 做众包翻译，再写一个 `json ↔ po` 转换器即可（一次性脚本）。

---

## 2. 键设计

### 2.1 候选方案

| 方案 | 形式 | 优点 | 缺点 |
|---|---|---|---|
| A | `(file_path, line, original)` | 精确定位 | 行号变化即失效，源文件改 1 行全文件失效 |
| B | `hash(original)` | 全局唯一 | 同一字符串多处出现无法消歧；改动原文失去关联 |
| C | `(module_path, original)` | 行号无关、模块级精度 | `module_path` 不稳定（重命名会断），同模块同字符串仍冲突 |
| D | `(stable_id, original_for_validation)` | 行号 / 路径无关，第一次抽取生成 UUID 后认 ID | 需要持久化 ID，且要回写到抽取索引（不写源码，写在表里） |

### 2.2 推荐：方案 D 变体（`stable_id` 主键 + `original_hash` 校验 + `occurrences[]` 上下文）

核心思想：**主键不依赖源码位置，定位信息作为可变副字段**。源码位置变了无所谓，原文没变 → 翻译保留；原文变了 → 通过 hash 比对触发 fuzzy。

#### 字段 schema（v1）

```
TranslationEntry {
  // ===== 主键 =====
  id: string                // ULID 或 UUIDv7，第一次抽取时生成，永不变更
                            // 用 ULID 因为可读且时序排序

  // ===== 内容 =====
  source: string            // 原文（英文），权威字段
  source_hash: string       // sha256(source) 前 16 字节 hex；冗余但用于快速比对
  target: string | null     // 中文译文；null 或 "" 表示待翻译

  // ===== 状态 =====
  status: enum              // "new" | "translated" | "fuzzy" | "approved" | "obsolete"
                            // - new: 自动抽取出来还没翻
                            // - translated: 有译文，未审核
                            // - fuzzy: 原文变过，旧译文已迁移过来但需复核
                            // - approved: 人工/QA 通过
                            // - obsolete: 源中已不存在（软删，保留 N 个版本后再硬删）

  // ===== 上下文（可变，仅参考） =====
  occurrences: [             // 出现位置列表（同一原文可能多处出现）
    {
      file: string           // 相对 ../warp 的路径，e.g. "app/src/settings_view/ai_page.rs"
      line: number           // 抽取时的行号
      kind: string           // "literal" | "macro_arg" | "const_def" | ...
      context_hint: string?  // 上下文摘要，e.g. "fn render_ai_page > Button::new"
    }
  ]

  // ===== 元数据 =====
  notes: string?            // 译者注释 / 术语决策 / 不译原因
  flags: string[]           // ["needs_review", "term:agent", "do_not_translate", ...]
  history: [                 // 原文变更轨迹，最多保留 5 条
    { source: string, source_hash: string, changed_at: string }
  ]
  first_seen_commit: string  // 源仓库 git commit（首次发现该原文时）
  last_seen_commit: string   // 最近一次抽取时仍存在于源中的 commit
  created_at: string         // ISO 8601
  updated_at: string
}
```

#### 为什么用 `stable_id` 而不是 `hash(source)` 直接做主键

- 重译时（`source` 改了）我们要保留 ID 不变，方便人审 diff（"原来 'Active AI' 现在是 'AI Active'，旧译沿用？"）
- 同一原文多处出现仍是 1 个 entry（occurrences 是数组），简化翻译工作量；如果某处需要不同译文（极少见），用 `flags` + `notes` 标注，或拆出子表（参见 §2.3）

#### 同原文多处需不同译文的极端情况

例：英文 `"Open"` 在"打开文件"和"开放（vs 关闭状态）"两处含义不同。
处理：人工把 entry 拆为两条，主键 `id` 不同，并在 `occurrences[].context_hint` 区分；抽取器维持原状（仍按 hash 找主键），但允许通过 `(file, line)` override 表（次表）覆盖：

```
overrides.json: { "<file>:<line>": "<entry_id>" }
```

MVP 阶段不实现 overrides，先观察实际冲突量。

---

## 3. 推荐 schema 完整定义

主表文件：`translations/strings.json`

```json
{
  "$schema_version": "1.0.0",
  "metadata": {
    "source_repo": "../warp",
    "source_commit": "abcdef1234567890",
    "tool_version": "warp-zh-extractor 0.1.0",
    "entry_count": 5,
    "stats": {
      "new": 1,
      "translated": 1,
      "fuzzy": 1,
      "approved": 1,
      "obsolete": 1
    },
    "last_changed_at": "2026-05-04T10:00:00Z"
  },
  "entries": [
    /* 数组按 id 字典序固定排序 */
  ]
}
```

> **字段命名说明**：从 `extracted_at` 改名为 `last_changed_at` —— 当某次重跑没有产生 entry 级别变化时，时间戳不再被刷新，从而保证幂等运行的字节级一致输出（idempotency）。

辅助文件：

| 文件 | 作用 |
|---|---|
| `translations/strings.json` | 主表，入 git |
| `translations/glossary.json` | 术语表（agent / pane / block / workflow → 中文标准译法），翻译时 LLM 必读 |
| `translations/overrides.json` | （可选）`(file:line) → entry_id` 显式映射，处理同原文多译 |
| `translations/.lock.json` | 不入 git，记录上次抽取 commit、扫描耗时等运行时数据 |

**排序约定**（关键，决定 diff 友好度）：
- `entries` 按 `id` 升序（ULID 时序，新增条目落到尾部，但若 ID 用 UUIDv7/v4 也接受字典序，**总之要稳定**）
- 每个 entry 的 keys 按固定顺序：
  `id` / `source` / `source_hash` / `target` / `status` / `occurrences` / `notes` / `flags` / `history` / `audit` / `first_seen_commit` / `last_seen_commit` / `created_at` / `updated_at`

> **`audit` 字段说明**：携带 D3 启发式打分链路（`score: number`、`verdict: "auto_ui" | "uncertain" | "not_ui"`、`reasons: [{code, delta}]`），存于每条留下来的 entry（注：`not_ui` 已被过滤不会进表，实际只会出现 `auto_ui` / `uncertain`），方便人工 review 时复盘"这条字符串为什么通过了启发式" —— D3 必备审计字段。

---

## 4. 增量更新算法（伪代码）

```text
INPUT:
  old_table : Map<id, Entry>            // 上次的 strings.json
  fresh_extract : List<RawString>        // 本次 syn 抽取出的所有字符串
                                         // 每条含 (source, file, line, kind, context_hint)
  source_commit : string                 // 当前 ../warp 的 git HEAD

OUTPUT:
  new_table : Map<id, Entry>
  report : { added, changed, removed, unchanged }

ALGORITHM extract_and_merge:

  // ---------- 1. 把 fresh_extract 按 source 文本聚合 ----------
  fresh_by_source : Map<source, List<Occurrence>> = {}
  for raw in fresh_extract:
    fresh_by_source[raw.source].append(Occurrence{raw.file, raw.line, raw.kind, raw.context_hint})

  // ---------- 2. 索引 old_table，便于按 source / hash 查找 ----------
  old_by_source : Map<source, Entry>      = index_by_source(old_table)
  old_by_hash   : Map<source_hash, Entry> = index_by_hash(old_table)

  new_table = {}
  seen_old_ids : Set<id> = {}
  report = { added: [], changed: [], removed: [], unchanged: [] }

  // ---------- 3. 遍历每个新抽取的原文 ----------
  for source, occurrences in fresh_by_source:
    h = sha256_short(source)

    // 3a. 完全匹配：原文一字不差
    if source in old_by_source:
      entry = clone(old_by_source[source])
      entry.occurrences = occurrences            // 位置无脑覆盖
      entry.last_seen_commit = source_commit
      entry.updated_at = now()
      // status: 不动（保留原来的 translated / approved 等）
      new_table[entry.id] = entry
      seen_old_ids.add(entry.id)
      report.unchanged.append(entry.id)
      continue

    // 3b. hash 匹配：理论上不会发生（hash 同源文本不同）—— 跳过
    //     真正"原文变了"的判定靠下面的启发式

    // 3c. 启发式：是否是某个旧 entry 的"修改版"
    //     在 old_by_source 中找一个"非常相似"的（编辑距离 / 共同前缀）
    //     用于把翻译沿用过来并标 fuzzy
    candidate = find_similar(source, old_by_source.keys(), threshold=0.7)

    if candidate is not None:
      old_entry = old_by_source[candidate]
      if old_entry.id in seen_old_ids:
        // 已被本轮另一条新原文认领，避免双重认领；走新增分支
        candidate = None

    if candidate is not None:
      entry = clone(old_by_source[candidate])
      // 把旧原文压入 history
      entry.history.prepend({
        source: entry.source,
        source_hash: entry.source_hash,
        changed_at: now()
      })
      entry.history = entry.history[:5]          // 只留最近 5 次
      entry.source = source
      entry.source_hash = h
      entry.status = "fuzzy"                     // 关键：标记需复核
      entry.occurrences = occurrences
      entry.last_seen_commit = source_commit
      entry.updated_at = now()
      new_table[entry.id] = entry
      seen_old_ids.add(entry.id)
      report.changed.append({id: entry.id, old: candidate, new: source})
      continue

    // 3d. 全新原文
    entry = Entry{
      id: ulid(),
      source: source,
      source_hash: h,
      target: null,
      status: "new",
      occurrences: occurrences,
      notes: null,
      flags: [],
      history: [],
      first_seen_commit: source_commit,
      last_seen_commit: source_commit,
      created_at: now(),
      updated_at: now()
    }
    new_table[entry.id] = entry
    report.added.append(entry.id)

  // ---------- 4. 处理 old 中未被新抽取认领的条目 ----------
  for id, old_entry in old_table:
    if id in seen_old_ids: continue

    // 软删：标 obsolete，保留 N 个版本（如 3 次抽取）后再硬删
    if old_entry.status == "obsolete":
      ages = count_runs_since(old_entry.last_seen_commit)
      if ages >= 3:
        report.removed.append(id)
        continue                                  // 不写入 new_table = 硬删
      // 否则保留 obsolete 状态
      new_table[id] = old_entry
    else:
      old_entry.status = "obsolete"
      old_entry.updated_at = now()
      new_table[id] = old_entry
      report.removed.append(id)

  // ---------- 5. 排序 + 写盘 ----------
  sort_entries_by_id(new_table)
  write_json("translations/strings.json", new_table, source_commit)

  return new_table, report
```

### 4.1 算法关键点

1. **原文是事实标准**：抽取出的 source 文本就是查找键，不依赖行号/路径。
2. **fuzzy 阈值**：`find_similar` 推荐用 normalized Levenshtein ≥ 0.7 或 token-set 相似度。**保守**：阈值越高越不会误把"无关新文案"当成"旧文案的修改"——宁可漏 fuzzy 也不要错认。
3. **认领冲突**：一条旧 entry 只能被认领一次（`seen_old_ids` 守护）；多条新文本和同一旧文本相似时，第一条认领（按抽取顺序），其他判 new。MVP 这个简单策略足够；进阶可用 Hungarian matching 做最优配对。
4. **obsolete 软删 → 硬删**：默认保留 3 次抽取仍未回归就清理。配置项 `obsolete_grace_runs = 3`。
5. **history**：仅在 fuzzy 路径写入；保留旧 source + hash + 时间戳；用于 review 时还原"曾经怎么写"。
6. **hash 用途**：序列化时写入 `source_hash`，但**判定原文是否变化的真正依据是 source 字符串本身比对**（hash 只是给人/工具快速对比的冗余）。

### 4.2 检测原文变化

```
def is_source_changed(old_entry, fresh_source):
    return old_entry.source != fresh_source

def quick_check(old_entry, fresh_source):
    # 大表场景下先比 hash，hash 不同必然不同
    return old_entry.source_hash != sha256_short(fresh_source)
```

实际算法用 source 直接相等比较（O(n)，n=条目数，5000 条无压力）；hash 仅作为序列化字段供外部工具/人快速 grep。

### 4.3 软删 vs 硬删的取舍

| 策略 | 优点 | 缺点 | 推荐 |
|---|---|---|---|
| 硬删（删了就消失） | 表干净 | 字符串短暂下线再回来要重译 | ✗ |
| 永久软删 | 可追溯 | 表越来越大 | ✗ |
| **N 次抽取宽限期** | 兼顾两者 | 实现稍复杂 | **✓** |

3 次宽限的语义：源仓库连续 3 次提交都未出现该字符串 → 真正废弃 → 硬删。配合 `last_seen_commit` 字段判断。

---

## 5. 多版本 / 源仓库 commit 跟踪

**结论：要写。**

每次抽取记录两层：

1. **顶层 `metadata.source_commit`**：本次抽取对应的 `../warp` HEAD commit
2. **每条 entry 的 `first_seen_commit` / `last_seen_commit`**：用于判断该字符串"首次出现于哪次源更新"以及"最近还活着没"

实际收益：
- 软删宽限期判断（"上次见到是几次提交前"）
- review 时定位字符串引入的 PR（沿 commit hash 回溯）
- LLM 翻译时可附带 commit hash 提示（不强制）

**`.lock.json`**（不入 git）：

```json
{
  "last_extract_commit": "abcdef1234567890",
  "last_extract_at": "2026-05-04T10:00:00Z",
  "extract_run_count": 17
}
```

`extract_run_count` 用于配合 `last_seen_commit` 实现宽限期（粗粒度）。

---

## 6. 审核流 / 状态字段设计

**采用四状态机（外加一个 obsolete 终态）**：

```
   [new] --LLM翻译--> [translated] --人工 review--> [approved]
                            |
                            v
                  原文变化   [fuzzy] --人工复核--> [translated] / [approved]
                            
   任意状态 --源中消失--> [obsolete] --N轮宽限--> 硬删
```

**为什么不用"`target` 为空 = 待译"的极简方案**：
- 状态信息和数据信息分离更清晰，方便统计 dashboard
- `fuzzy` 是关键状态——`target` 非空但需复核，单字段无法表达
- `approved` 状态让翻译流水线可以"已审核条目不再回炉 LLM"，省 token

**最小集**（如果还想再省）：保留 `new` / `translated` / `fuzzy` / `obsolete` 四态，砍掉 `approved`，用 `flags: ["approved"]` 替代。

**MVP 推荐：保留五态完整方案**——多一个枚举值不增加任何工程复杂度，但语义清晰。

---

## 7. 示例文件（≥5 条目，覆盖 5 种状态）

```json
{
  "$schema_version": "1.0.0",
  "metadata": {
    "source_repo": "../warp",
    "source_commit": "a1b2c3d4e5f6a7b8",
    "tool_version": "warp-zh-extractor 0.1.0",
    "entry_count": 6,
    "stats": { "new": 1, "translated": 1, "fuzzy": 1, "approved": 2, "obsolete": 1 },
    "last_changed_at": "2026-05-04T10:00:00Z"
  },
  "entries": [
    {
      "id": "01HW8K3M2P0001",
      "source": "Active AI",
      "source_hash": "9c1185a5c5e9fc54",
      "target": "活动 AI",
      "status": "approved",
      "occurrences": [
        { "file": "app/src/settings_view/ai_page.rs", "line": 42, "kind": "literal", "context_hint": "render_ai_page > section_header" }
      ],
      "notes": null,
      "flags": [],
      "history": [],
      "audit": {
        "score": 6,
        "verdict": "auto_ui",
        "reasons": [
          { "code": "path_whitelist", "delta": 3 },
          { "code": "sentence_shape", "delta": 2 },
          { "code": "title_case_phrase", "delta": 1 }
        ]
      },
      "first_seen_commit": "0000000000000000",
      "last_seen_commit": "a1b2c3d4e5f6a7b8",
      "created_at": "2026-04-20T09:00:00Z",
      "updated_at": "2026-05-04T10:00:00Z"
    },
    {
      "id": "01HW8K3M2P0002",
      "source": "Next Command",
      "source_hash": "1d4f8a9b2c0e3f55",
      "target": "下一条命令",
      "status": "translated",
      "occurrences": [
        { "file": "app/src/settings_view/ai_page.rs", "line": 88, "kind": "literal", "context_hint": "ShortcutBinding::label" }
      ],
      "notes": "Block 上下文里的 next command",
      "flags": ["term:command"],
      "history": [],
      "first_seen_commit": "0000000000000000",
      "last_seen_commit": "a1b2c3d4e5f6a7b8",
      "created_at": "2026-04-20T09:00:00Z",
      "updated_at": "2026-05-01T08:30:00Z"
    },
    {
      "id": "01HW8K3M2P0003",
      "source": "Show agent tips when typing",
      "source_hash": "ab12cd34ef567890",
      "target": "输入时显示代理提示",
      "status": "fuzzy",
      "occurrences": [
        { "file": "app/src/settings_view/ai_page.rs", "line": 121, "kind": "literal", "context_hint": "Toggle::label" }
      ],
      "notes": null,
      "flags": ["term:agent"],
      "history": [
        {
          "source": "Show agent tips",
          "source_hash": "11223344aabbccdd",
          "changed_at": "2026-05-04T10:00:00Z"
        }
      ],
      "first_seen_commit": "0000000000000000",
      "last_seen_commit": "a1b2c3d4e5f6a7b8",
      "created_at": "2026-04-20T09:00:00Z",
      "updated_at": "2026-05-04T10:00:00Z"
    },
    {
      "id": "01HW8K3M2P0004",
      "source": "Let AI generate the next command based on your recent terminal history.",
      "source_hash": "5e8a7b6c4d3e2f1a",
      "target": null,
      "status": "new",
      "occurrences": [
        { "file": "app/src/settings_view/ai_page.rs", "line": 156, "kind": "const_def", "context_hint": "const NEXT_COMMAND_DESCRIPTION" }
      ],
      "notes": null,
      "flags": [],
      "history": [],
      "audit": {
        "score": 4,
        "verdict": "uncertain",
        "reasons": [
          { "code": "sentence_shape", "delta": 2 },
          { "code": "const_name_describes_ui", "delta": 2 }
        ]
      },
      "first_seen_commit": "a1b2c3d4e5f6a7b8",
      "last_seen_commit": "a1b2c3d4e5f6a7b8",
      "created_at": "2026-05-04T10:00:00Z",
      "updated_at": "2026-05-04T10:00:00Z"
    },
    {
      "id": "01HW8K3M2P0005",
      "source": "Quit Warp?",
      "source_hash": "f00ba12bad5eed00",
      "target": "退出 Warp？",
      "status": "approved",
      "occurrences": [
        { "file": "app/src/quit_warning/dialog.rs", "line": 30, "kind": "literal", "context_hint": "ConfirmDialog::title" },
        { "file": "crates/warpui/src/platform/mac/menus.rs", "line": 412, "kind": "macro_arg", "context_hint": "menu_item!(quit, ...)" }
      ],
      "notes": "中文问号要用全角",
      "flags": [],
      "history": [],
      "first_seen_commit": "0000000000000000",
      "last_seen_commit": "a1b2c3d4e5f6a7b8",
      "created_at": "2026-04-20T09:00:00Z",
      "updated_at": "2026-04-25T14:00:00Z"
    },
    {
      "id": "01HW8K3M2P0006",
      "source": "Beta Feature: Workflow Autopilot",
      "source_hash": "deadbeefcafebabe",
      "target": "Beta 功能：工作流自动驾驶",
      "status": "obsolete",
      "occurrences": [],
      "notes": "feature flag 下线，源中已删除",
      "flags": [],
      "history": [],
      "first_seen_commit": "0000000000000000",
      "last_seen_commit": "999888777666555",
      "created_at": "2026-04-15T09:00:00Z",
      "updated_at": "2026-05-04T10:00:00Z"
    }
  ]
}
```

**示例如何对应 5 种状态**：

| id 后四位 | 状态 | 说明 |
|---|---|---|
| 0001 | `approved` | 已审核，跨多次抽取保持稳定 |
| 0002 | `translated` | LLM 已译，待人工 review |
| 0003 | `fuzzy` | 原文从 "Show agent tips" 改为 "Show agent tips when typing"，旧译文沿用并标 fuzzy；history 保留旧值 |
| 0004 | `new` | 本次抽取新增；`first_seen_commit == 当前 commit` |
| 0005 | `approved` 多处出现 | `occurrences` 数组示意一条 entry 跨文件复用 |
| 0006 | `obsolete` | 源中已删，`occurrences` 为空，等待宽限期到了硬删 |

---

## 8. git diff 友好度评估

### 8.1 推荐格式（JSON + 严格排序）的 diff 表现

**关键规则**：
1. `entries` 数组按 `id` 升序
2. 每 entry 内 keys 顺序固定（schema-defined）
3. JSON pretty-print 用 2 空格缩进，每个数组元素一块连续行
4. 字符串内的 `\n` 不转成多行（保留 `\\n` 字面量），保证一条目占有限且固定的行块

**典型 diff 场景与可读性**：

| 场景 | git diff 表现 | 友好度 |
|---|---|---|
| 新增 1 个原文 | 在数组尾部（或按 id 排序的某处）插入 ~14 行连续块，diff 是 `+` 块 | ★★★★★ |
| 翻译某个 entry | 单行 `target: null` → `target: "中文"`，加 `status` 行变化 | ★★★★★ |
| 原文变更 | 4-5 行变化（source / source_hash / status / updated_at / history 数组+1） | ★★★★ |
| 删除（标 obsolete） | 1-2 行变化（`status` + `occurrences` 清空） | ★★★★★ |
| 硬删 | 整块 `-` 14 行 | ★★★★★ |
| 重命名某个 source | 仅触动相关 entry，不影响其他 | ★★★★★ |
| 抽取顺序变化 | **零影响**（按 id 排序） | ★★★★★ |

### 8.2 反例（如果不严格排序）

- 如果按抽取顺序写盘，源文件移动 1 行 → 整文件大量条目重排 → diff 全乱（i18next 项目里的常见痛点）。
- 如果用 object 而非 array (`{ "id1": {...}, "id2": {...} }`），JSON 标准未规定 key 顺序，部分序列化库会按 hash 序，diff 不稳。

**对策固化在工具里**：
- 写盘函数内置 `sort(entries, key=id)`
- CI 检查：`extract --check`，若 `strings.json` 不符合 canonical 排序，pipeline 失败，避免人工编辑破坏 diff 友好性

### 8.3 与其他格式的对比（同一变更的 diff 行数）

变更：原文 `"Show agent tips"` → `"Show agent tips when typing"`

| 格式 | diff 行数（增/改/删） | 可读性 |
|---|---|---|
| JSON（推荐） | ~7 行 | 高（字段名清晰） |
| `.po` | ~5 行（`msgid` 一行 + `#, fuzzy` 一行） | 高（结构紧凑） |
| TOML（每条 `[[entries]]`） | ~10 行 | 中（多行嵌套表干扰） |
| YAML | ~6 行 | 中（缩进若变会全文重排） |
| CSV | 1 行（整行替换） | 低（无字段语义） |
| SQLite | 不可 diff | 无 |

JSON 的 diff 行数稍多于 `.po`，但由于字段语义自描述，review 起来负担反而更小。

### 8.4 合并冲突场景

并发场景：A 翻译了 entry X（改 target），B 翻译了 entry Y（改 target）。

- 推荐 JSON：两个 entry 按 id 排序位置不同 → 各自局部修改 → git 自动 merge 成功
- TOML / YAML：嵌套结构有时会触发 line-based merge 失败（需手工解）
- `.po`：通常 OK（块状）

JSON + 严格排序在合并友好度上和 `.po` 持平，且没有 `.po` 解析器依赖。

---

## 9. 结论摘要

| 议题 | 结论 |
|---|---|
| 存储格式 | **JSON**（人类可读 + Rust 原生 + 自由 schema + LLM 友好） |
| 主键 | **`stable_id` (ULID)** + `original_hash` 校验 + `occurrences[]` 副字段 |
| 增量算法 | source 直接比对优先；相似度匹配触发 fuzzy；obsolete 软删 + 3 轮宽限硬删 |
| 多版本 | 顶层记 `source_commit`，每条 entry 记 `first_seen_commit` / `last_seen_commit` |
| 审核流 | 五态机：`new` / `translated` / `fuzzy` / `approved` / `obsolete` |
| git diff | 强制 `id` 排序 + 固定字段顺序 + 行块化 → diff 行数最小且稳定 |
| 失效兜底 | 生成阶段：未命中 / `target` 为空 / `status == obsolete` → 全部 fallback 英文（编译保证） |

---

## 10. Caveats / 后续待定

- **同原文多译**支持留作 v2（先观察 MVP 期实际冲突量；预计 < 5%）
- **fuzzy 相似度阈值**需要在真实数据上调参（建议先 0.7，跑 2-3 次源更新后看误判率）
- **术语表 `glossary.json`** 未在本研究展开（另研究主题）；schema 推荐 `{ term: { en, zh, notes, do_not_translate? } }`
- **过大的长文本**（如 NUX 介绍 200+ 字符）是否拆段翻译？本研究按整段一条 entry 处理；若用户希望段级细分，需要在抽取阶段做语义切分（额外复杂度）
- **ID 生成器选 ULID 还是 UUIDv7**：均可；ULID 字典序 = 时序，diff 时新条目落尾部，更直觉。MVP 推荐 ULID。

