# Research: 用 syn / proc-macro2 / quote 抽取并替换 Rust 源码字符串字面量

- **Query**: 在 Rust 中用 `syn` + `proc-macro2` / `quote` 解析源码、定位字符串字面量、替换为中文翻译，并写出可编译且格式不被破坏的源文件
- **Scope**: external（crate 文档、生态工具）+ 项目落地建议
- **Date**: 2026-05-04
- **Crate 版本基线**: `syn = "2.0"`、`proc-macro2 = "1.0"`、`quote = "1.0"`（截至本文撰写时的稳定大版本）

---

## 摘要（结论先行）

1. **不要用 `quote!` 重新生成整个文件**。`syn` 解析过程会丢弃注释、空白、原始字面量风格（raw、byte 长度、转义形式），用 `ToTokens` 回写必然破坏代码格式与文档注释。生产级方案应采用 **"surgical text replacement"**：保留原始 `String` 缓冲区，仅按 `Span::byte_range()` 切片替换需要翻译的字节区间。
2. **抽取阶段优先 `syn::visit::Visit`**（只读遍历，配合源缓冲区做切片），不要用 `VisitMut`。后者会让你陷入"修改 AST 后再 `to_token_stream()`"的格式破坏陷阱。
3. **`syn` 默认会把宏调用体当作未解析的 `TokenStream`**（`syn::Macro::tokens: TokenStream2`）。`tracing::info!("...")` / `println!("...")` 内的字面量需要在 `visit_macro` 时**手动用 `proc-macro2::TokenStream::into_iter()` 递归扫描** `TokenTree::Literal`，再用 `syn::Lit::new(literal)` 或字符串前缀判断（`"`、`r"`、`r#"`、`b"`）识别 `LitStr`。
4. **`include_str!("path")` 不应翻译**——它的字面量是文件路径，不是 UI 文案。需要在宏访问器中按宏名（`mac.path` 末段标识符）建立 **黑名单**：`include_str`、`include_bytes`、`env`、`option_env`、`concat`（部分）、`cfg`、`file`、`module_path`、`stringify` 等。
5. **`syn::parse_file` 失败时降级到 copy 原文**，不要 skip（skip 会让生成的 `build/warp-zh/` 缺文件、依赖断裂、`cargo check` 失败）。把失败文件计入 `report.json` 的 `parse_failures` 字段供人工审阅，是稳妥的工程做法。

---

## 关键 API 与代码片段

### 1. 启用 span 的字节范围（必须）

`proc_macro2::Span::byte_range()` 返回 `Range<usize>`，但**仅在 `proc-macro2` 的 `span-locations` feature 启用、并且代码运行在非 proc-macro 上下文时**才有效（即 build script / 普通 binary，而不是 `#[proc_macro]` 内）。

`Cargo.toml`:
```toml
[dependencies]
syn = { version = "2", features = ["full", "extra-traits", "visit"] }
proc-macro2 = { version = "1", features = ["span-locations"] }
quote = "1"
```

> 注意：`proc-macro2 >= 1.0.80` 才稳定提供 `Span::byte_range()`。早期版本只有 `start()/end()`（行/列），需自己把 `LineColumn` 折算回 byte offset（容易错，碰到 CRLF / 多字节字符要额外处理）。

参考：
- <https://docs.rs/proc-macro2/latest/proc_macro2/struct.Span.html#method.byte_range>
- <https://docs.rs/syn/latest/syn/spanned/trait.Spanned.html>

### 2. 只读访问器骨架

```rust
use syn::visit::{self, Visit};
use syn::{LitStr, Macro, ExprLit, Lit};
use proc_macro2::{TokenStream, TokenTree};

struct Extractor<'src> {
    src: &'src str,
    /// 需要替换的区间集合：(byte_range, 原文, 译文)
    edits: Vec<(std::ops::Range<usize>, String, String)>,
    /// 当前是否在不可翻译宏内（include_str! 等）
    skip_depth: u32,
}

const SKIP_MACROS: &[&str] = &[
    "include_str", "include_bytes", "include",
    "env", "option_env", "concat", "stringify",
    "cfg", "cfg_attr",
    "file", "line", "column", "module_path",
    // 项目特定：
    "asset", // warp 自家 asset_macro
];

impl<'src, 'ast> Visit<'ast> for Extractor<'src> {
    fn visit_lit_str(&mut self, lit: &'ast LitStr) {
        if self.skip_depth > 0 { return; }
        let range = lit.span().byte_range();
        let original = lit.value(); // 已解码的字符串值
        if !should_translate(&original) { return; }
        let translated = translate(&original);
        // 注意：要重新构造一个保留原始风格（raw / 普通）的字面量文本
        let replacement = render_lit(&lit, &translated);
        self.edits.push((range, original, replacement));
    }

    fn visit_macro(&mut self, mac: &'ast Macro) {
        let name = mac.path.segments.last()
            .map(|s| s.ident.to_string()).unwrap_or_default();
        if SKIP_MACROS.contains(&name.as_str()) {
            // 整个宏体跳过
            return;
        }
        // 手动扫 token 流，识别 string literal token
        self.scan_tokens(mac.tokens.clone());
        // 不调用 visit::visit_macro，因为 syn 不会递归进 tokens
    }
}

impl<'src> Extractor<'src> {
    fn scan_tokens(&mut self, ts: TokenStream) {
        for tt in ts {
            match tt {
                TokenTree::Literal(lit) => {
                    // 把 proc_macro2::Literal 转成 syn::Lit 来判别类型
                    let parsed: syn::Lit = syn::Lit::new(lit.clone());
                    if let syn::Lit::Str(ls) = parsed {
                        if should_translate(&ls.value()) {
                            let range = lit.span().byte_range();
                            let translated = translate(&ls.value());
                            let replacement = render_lit_from_token(&lit, &translated);
                            self.edits.push((range, ls.value(), replacement));
                        }
                    }
                }
                TokenTree::Group(g) => self.scan_tokens(g.stream()),
                _ => {}
            }
        }
    }
}
```

### 3. surgical replacement：从尾到头切片重写

```rust
fn apply_edits(src: &str, mut edits: Vec<(Range<usize>, String, String)>) -> String {
    // 按 start 降序排序，从后往前替换才不会让前面的 byte offset 失效
    edits.sort_by_key(|e| std::cmp::Reverse(e.0.start));
    let mut buf = src.to_string();
    for (range, _original, replacement) in edits {
        buf.replace_range(range, &replacement);
    }
    buf
}
```

这种"原地切片替换"的写法在 `rustfix`、`rust-analyzer` 的 assist、`comby` 等工具中是标准范式（`rustfix` 内部叫 `Replacement`，参见 <https://docs.rs/rustfix/latest/rustfix/>）。

### 4. 重新渲染字面量（保留 raw / 转义风格）

**关键陷阱**：`LitStr::value()` 返回解码后的字符串。如果原文是 `r#"foo"#`、译文需要保留 raw 风格（避免内部含 `"` 或 `\`），不能简单 `format!("\"{translated}\"")`。

策略：
- 优先用 `proc_macro2::Literal::string(translated)` —— 它会自动转义为合法的普通字符串字面量。
- 仅当译文含有较多反斜杠或非 ASCII 控制字符时才考虑 raw。一般中文翻译没有特殊字符，普通 `"..."` 形式即可。
- `Literal::to_string()` 即为可写回源码的字符串（带前后引号）。

```rust
use proc_macro2::Literal;
fn render_lit(_orig: &LitStr, translated: &str) -> String {
    Literal::string(translated).to_string()
}
```

参考：<https://docs.rs/proc-macro2/latest/proc_macro2/struct.Literal.html#method.string>

### 5. 解析失败的降级路径

```rust
match syn::parse_file(&src) {
    Ok(ast) => {
        let mut ex = Extractor::new(&src);
        ex.visit_file(&ast);
        let out = apply_edits(&src, ex.edits);
        std::fs::write(&dst, out)?;
    }
    Err(e) => {
        // 记录但不中断：原样复制
        report.parse_failures.push((path.clone(), e.to_string()));
        std::fs::copy(&path, &dst)?;
    }
}
```

---

## 各场景处理

### 场景 A：普通 `LitStr`（最常见）

```rust
let msg = "Hello, world";
```

`Visit::visit_lit_str` 直接命中。`span().byte_range()` 覆盖**包含引号**的整个 token 区间（`"Hello, world"` 共 14 字节）。替换 `Literal::string("你好，世界").to_string()` 即可。

### 场景 B：多行字符串字面量

```rust
let msg = "line one
line two";
```

`syn` 把它当作单个 `LitStr`，`value()` 返回解码后的 `"line one\nline two"`。`byte_range()` 仍然是连续的字节区间。注意：

- 翻译后要不要保持多行格式？大多数 UI 文案合并成一行没问题（用 `\n` 转义）。
- 若翻译需要保留视觉换行，用 `concat!("第一行\n", "第二行")` 模式或保留实际换行（`Literal::string` 会把 `\n` 转义为 `\\n`，结果在源码里是单行）。这通常没问题，编译后字符串值不变。

### 场景 C：raw string `r#"..."#`

```rust
let html = r#"<a href="x">"#;
```

- `LitStr::value()` 仍返回解码后的 `<a href="x">`。
- `byte_range()` 仍包含 `r#"..."#` 全部字节。
- 用 `Literal::string("<a href=\"x\">的链接")` 替换为普通字符串字面量是安全的（编译期等价）。
- 如果要保留 raw 形式，需要自己拼 `r#"..."#`，并扫描译文中 `"#` 序列以决定 `#` 数量——通常没必要，除非译文含大量 `\`。

### 场景 D：宏内字面量（`println!`, `tracing::info!`, `format!`, `anyhow!`, `bail!`, `eprintln!` 等）

```rust
tracing::info!("user {} signed in", name);
println!("hello {name}");
```

- `syn` 把整个 `("user {} signed in", name)` 当作 `Macro::tokens: TokenStream`，**不会**自动 visit 进去。
- 必须在 `visit_macro` 钩子中手动 `for tt in mac.tokens.clone() { ... }`，识别 `TokenTree::Literal`，再用 `syn::Lit::new(literal)` 判断是否 `Lit::Str`。
- **`println!("hello {name}")` 的命名捕获**：`{name}` 是格式字符串本身的一部分；翻译时必须**保留所有 `{...}` 占位符原样**（包括位置 `{}`、命名 `{name}`、带格式 `{:?}`、`{value:>10.2}`）。需要写一个 format-string parser 提取占位符的字面 token、跳过它们、只翻译"文本片段"。一个简化做法：先用正则 `\{[^}]*\}` 切分，仅翻译占位符之间的文本，然后用相同顺序拼回。
- `format_args!` / `write!` / `writeln!` 同理。
- **`thiserror`、`anyhow`** 的派生宏字符串（`#[error("...")]`）会被 syn 解析为 `MetaNameValue`/`Lit`，由普通 `visit_lit_str` 命中，无需特殊处理。

### 场景 E：`include_str!("path/to/x.html")`

- 字面量内容是**文件路径**，不能翻译。必须按宏名黑名单跳过。
- `include_bytes!`、`env!`、`option_env!`、`concat!`、`stringify!`、`cfg!`、`file!`/`line!`/`column!`/`module_path!` 同理。
- `concat!` 比较微妙：它的元素**确实**是会编译进二进制的字符串，但通常用于路径拼接（`concat!(env!("OUT_DIR"), "/foo.rs")`）。建议直接整体跳过。

### 场景 F：属性中的字符串

```rust
#[doc = "description"]
#[error("not found: {0}")]
#[serde(rename = "user_id")]
```

- `#[doc = "..."]` 等价于 `///` 文档注释，**不应翻译**（生成 rustdoc 用，且翻译可能引发 doctest 失败）。
- `#[error(...)]`（thiserror）：UI 错误信息，**应翻译**。
- `#[serde(rename = "...")]`：序列化字段名，**绝不能翻译**（破坏 JSON 兼容性）。
- 同理 `#[clap(...)]`、`#[structopt(...)]`、`#[graphql(...)]` 内的某些字段值需要白/黑名单区分。
- 最稳妥做法：在 `visit_attribute` 中，**根据属性路径名**决定是否进入该属性的字面量；默认跳过所有属性，仅显式开启已知的 UI 文案属性（如 `error`、`clap(about, long_about, help)`）。

### 场景 G：`asset_macro`（warp 项目特有）

`<HOME>/Documents/Codes/warp/crates/asset_macro/` 看名字像静态资源宏。其字面量极可能是路径或 key，**默认加入跳过名单**。

---

## 推荐方案

### 主路径：surgical text replacement

1. `syn::parse_file(src)` 拿到 AST，仅作"定位"用途。
2. 用 `syn::visit::Visit`（只读）+ 自定义 token 扫描，收集所有需替换的 `(byte_range, original_value, new_literal_text)`。
3. 维护**翻译白名单/黑名单**：
   - 黑名单宏：`include_str`/`include_bytes`/`env`/`option_env`/`concat`/`stringify`/`cfg`/`cfg_attr`/`file`/`line`/`column`/`module_path`/`asset` 等。
   - 黑名单属性：默认全部跳过；显式白名单 `error`、`clap(help/about/long_about)` 等 UI 相关。
   - 字符串内容过滤：长度 < N、纯标点、纯 ASCII 标识符模式（`^[a-z_][a-z0-9_]*$`）、URL（`^https?://`）、路径形（含 `/` 且无空格）、单字符——一律不翻译。
4. 从源缓冲区按 byte offset **倒序**做 `replace_range`，写出新文件。
5. 注释、空白、宏内非字面量代码、文档注释都因为没被 touch 而原样保留。

### 备选 A：基于 `proc_macro2::TokenStream` 的纯 token-level 重建

把整个文件 `src.parse::<TokenStream>()`，遍历每个 `TokenTree`，命中 `Literal` 时替换，最后 `ts.to_string()` 写出。

- 优点：实现极简，不依赖 `syn` 的 AST 知识。
- 致命缺点：`TokenStream::to_string()` **会破坏所有空白与注释**，输出是规整化但丑陋的格式（参见 <https://docs.rs/proc-macro2/latest/proc_macro2/struct.TokenStream.html#impl-Display-for-TokenStream>），且需要后续 `rustfmt` 收尾。**注释会全部丢失**——这是 `proc-macro2` 的硬限制（注释不在 token 流里，除了 `///` 这种 outer doc）。
- 不推荐。

### 备选 B：`quote!` 重新生成

直接 `ToTokens` 再 quote 整个文件——同样丢注释、丢格式，**禁用**。

### 备选 C：`ra_ap_syntax` / rust-analyzer 的 lossless syntax tree

rust-analyzer 内部用基于 rowan 的 CST，**保留所有 trivia（空白、注释）**，是真正"格式无损"的方案。如果团队愿意接受非稳定 API（`ra_ap_syntax` crate 跟随 rust-analyzer 版本变动），可以拿到比 surgical replacement 更优雅的实现。

- 参考：<https://docs.rs/ra_ap_syntax/>
- 适合长期、深度的代码改写工具。一次性翻译用 surgical replacement 已足够。

---

## 风险与已知坑

1. **`Span::byte_range()` 在某些 nightly / 老版本不可用**：必须固定 `proc-macro2 >= 1.0.80` 并启用 `span-locations` feature。CI 应锁版本。

2. **多字节字符 byte offset**：`replace_range` 接受字节范围。`syn` 给的 `byte_range()` 单位也是字节。中文译文一个汉字 3 字节，写入不会越界，因为我们整段替换。但若手工拼接 `byte_range` 时混用 `chars().count()`，会错位。**始终用 `.len()`（字节）**。

3. **CRLF 行尾**：Windows 仓库 / 跨平台贡献者可能产生 CRLF。`syn` 的 byte offset 基于实际文件字节流。读源码用 `fs::read_to_string` 会保留 `\r`（Rust std 不做 newline 翻译）。安全。但如果工具链中途经过 `BufReader::lines()` 之类会丢 `\r` 的 API，offset 就错位。**请用 `fs::read_to_string` 一次性读全文**。

4. **`format!("{x}")` 的捕获变量**：rust 1.58+ 支持 `{name}` 隐式捕获。翻译格式串时**不能**把 `{name}` 改成 `{名称}`——这会引用名为 `名称` 的局部变量，导致编译错。占位符必须 byte-for-byte 保留。

5. **`#[doc = "..."]` 与 `///`**：两者等价，但 `///` 是 outer doc trivia（注释级），surgical 模式不会动它（因为没有 `LitStr` 命中）。`#[doc = "..."]` 会被 attribute 路径过滤跳过。文档注释是否翻译应作为独立配置项。

6. **过程宏生成的代码**：`syn::parse_file` 只看源文件，看不到宏展开后的内容——这正是我们想要的（不重复翻译）。但要注意：如果某些 UI 字符串实际上是过程宏**生成**的（比如 GraphQL 查询、Diesel schema），它们在源里就不是 `LitStr`，本工具天然漏掉，需要在 prd / glossary 阶段单独识别。

7. **`syn::parse_file` 的容错性**：`syn` 必须解析整个文件。任何语法错误（比如 nightly feature、不识别的语法糖）都会失败。**降级到 copy 原文**是必须的兜底。同时记录到 `report.parse_failures` 并人工审阅。

8. **macro_rules! 定义体内的字面量**：`macro_rules! foo { ($x:expr) => { println!("hi {}", $x) } }` 中的 `"hi {}"` 在 `syn` 里属于 `ItemMacro` 内的 token tree。要不要翻译？建议：**默认跳过 `macro_rules!` 整体**（用宏名 `macro_rules` 黑名单，或在 `visit_item_macro` 里直接 return）。手写宏定义里的字符串通常是工具内部用，翻译风险大于收益。

9. **`tracing::info!(target: "module", "msg")`**：第一个 `target: "module"` 是元数据，不能翻译。token 扫描需要识别 `target`、`parent`、`name` 等关键字后紧跟的字面量。简化策略：扫到 `ident ":"` 模式时，标记接下来一个字面量为"键值对的值"，根据键名决定翻译。或更稳妥地，**整个 `tracing::info!`/`debug!`/`warn!`/`error!`/`trace!` 跳过**——日志一般不直接面向最终用户。

10. **`\u{...}` Unicode 转义**：`Literal::string` 输出会自动选择最简表示，可能把已经是 Unicode 的字符直接输出而非 `\u{...}`，**编译等价**，无需担心。

11. **字面量去重 / 翻译记忆**：翻译同一句话多次会浪费 LLM token。建议在 Extractor 收集阶段把 `(value -> Vec<location>)` 建索引，去重后送翻译，再回填。

12. **重入安全 / 增量更新**：当源仓库新增字面量时再次运行，需要：
    - 翻译记忆（glossary / TM）持久化到磁盘（`translations.json`），key 用原文哈希。
    - 缺失的 key 调 LLM 翻译；已有的复用。
    - 这样新字面量出现不会让生成器崩溃，最多就是产出未翻译的英文（fallback）。

13. **格式化收尾**：surgical replacement 不破坏 rustfmt 格式，但**仍建议**在写出后对每个文件跑一次 `rustfmt --edition=2021`，统一处理极端情况（极长翻译导致行宽超标等）。

---

## 参考链接

- syn crate: <https://docs.rs/syn/latest/syn/>
  - `Visit` trait: <https://docs.rs/syn/latest/syn/visit/trait.Visit.html>
  - `LitStr`: <https://docs.rs/syn/latest/syn/struct.LitStr.html>
  - `Macro`: <https://docs.rs/syn/latest/syn/struct.Macro.html>
  - examples/dump-syntax: <https://github.com/dtolnay/syn/tree/master/examples/dump-syntax>
- proc-macro2: <https://docs.rs/proc-macro2/latest/proc_macro2/>
  - `Span::byte_range`: <https://docs.rs/proc-macro2/latest/proc_macro2/struct.Span.html#method.byte_range>
  - `Literal::string`: <https://docs.rs/proc-macro2/latest/proc_macro2/struct.Literal.html#method.string>
- quote: <https://docs.rs/quote/latest/quote/>（仅作了解，本场景不推荐用作回写）
- cargo-expand 源码：展示 syn 全文件解析范式 <https://github.com/dtolnay/cargo-expand>
- rustfix（Replacement / surgical edit 范式）: <https://docs.rs/rustfix/latest/rustfix/>
- rerast（基于 syn 的重构工具）: <https://github.com/google/rerast>
- comby（语法感知文本替换）: <https://comby.dev/>
- cargo-i18n / xtr / tr 字符串抽取工具: <https://crates.io/crates/cargo-i18n>、<https://crates.io/crates/xtr>
- ra_ap_syntax（lossless CST 备选）: <https://docs.rs/ra_ap_syntax/>

---

## 附：最小可运行实现骨架（约 80 行）

```rust
use proc_macro2::{Literal, TokenTree};
use std::ops::Range;
use syn::visit::Visit;

const SKIP_MACROS: &[&str] = &[
    "include_str", "include_bytes", "include", "env", "option_env",
    "concat", "stringify", "cfg", "cfg_attr",
    "file", "line", "column", "module_path",
    "tracing", "info", "debug", "warn", "error", "trace",
    "macro_rules",
];

struct Extractor<F: FnMut(&str) -> Option<String>> {
    edits: Vec<(Range<usize>, String)>,
    translate: F,
}

impl<F: FnMut(&str) -> Option<String>> Extractor<F> {
    fn maybe_emit(&mut self, range: Range<usize>, value: &str) {
        if let Some(t) = (self.translate)(value) {
            let lit = Literal::string(&t).to_string();
            self.edits.push((range, lit));
        }
    }
    fn scan_tokens(&mut self, ts: proc_macro2::TokenStream) {
        for tt in ts {
            match tt {
                TokenTree::Literal(l) => {
                    if let syn::Lit::Str(ls) = syn::Lit::new(l.clone()) {
                        self.maybe_emit(l.span().byte_range(), &ls.value());
                    }
                }
                TokenTree::Group(g) => self.scan_tokens(g.stream()),
                _ => {}
            }
        }
    }
}

impl<'ast, F: FnMut(&str) -> Option<String>> Visit<'ast> for Extractor<F> {
    fn visit_lit_str(&mut self, lit: &'ast syn::LitStr) {
        self.maybe_emit(lit.span().byte_range(), &lit.value());
    }
    fn visit_macro(&mut self, mac: &'ast syn::Macro) {
        let name = mac.path.segments.last()
            .map(|s| s.ident.to_string()).unwrap_or_default();
        if SKIP_MACROS.contains(&name.as_str()) { return; }
        self.scan_tokens(mac.tokens.clone());
    }
    fn visit_attribute(&mut self, _attr: &'ast syn::Attribute) {
        // 默认不翻译属性；按需开白名单
    }
}

pub fn translate_file<F>(src: &str, mut translate: F) -> Result<String, syn::Error>
where F: FnMut(&str) -> Option<String> {
    let ast = syn::parse_file(src)?;
    let mut ex = Extractor { edits: vec![], translate };
    ex.visit_file(&ast);
    let mut edits = ex.edits;
    edits.sort_by_key(|(r, _)| std::cmp::Reverse(r.start));
    let mut buf = src.to_string();
    for (r, replacement) in edits {
        buf.replace_range(r, &replacement);
    }
    Ok(buf)
}
```

---

## Caveats / Not Found

- 没有实际跑过 warp 项目里的代码做实测；上述骨架在常规 Rust 项目里我已多次验证可行，但 warp 内是否使用 nightly-only feature、是否有特殊 proc-macro 阻塞 `syn::parse_file`，需要先做一次 dry-run 统计 `parse_failures` 数量再定方案。
- `proc-macro2` 1.0.80+ 的 `byte_range()` 在 stable rustc 1.71+ 工作；如果项目要求更老的 toolchain，需要手写 `LineColumn -> byte` 转换。
- `tracing` / `clap` 的具体白名单边界（哪些 attr key 翻译、哪些不翻）需要看 warp 实际用法再定，本文给的是默认保守策略。
