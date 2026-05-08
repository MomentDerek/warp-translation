# Quality Guidelines

> Code quality standards for backend (Rust) tools in this project.

---

## Required Patterns

### Canonical-form contract on generated data files

Any data file that is the single source of truth AND lives in git MUST:

1. Be deterministically sortable (entries sorted by a stable key — ULID, lexicographic id, etc.)
2. Have a fixed serialization order for fields within each entry
3. Pretty-print with stable whitespace (typically 2-space indent, one logical block per entry)
4. Update timestamps **only when content actually changes** — re-running the generator on unchanged input MUST produce a byte-identical file

The generator MUST ship a `--check` mode that re-runs the pipeline in memory and compares against the on-disk file:

```rust
fn run_check(source: &Path, table: &Path, lock: &Path) -> Result<()> {
    let merged = run_extract_in_memory(source, table, lock)?;
    let canonical = serde_json::to_string_pretty(&merged)?;
    let on_disk = fs::read_to_string(table)?;
    if canonical.trim_end() != on_disk.trim_end() {
        bail!("translation table is not in canonical form (run extract to fix)");
    }
    println!("--check passed");
    Ok(())
}
```

#### Semantic boundary: `--check` validates structure, NOT content

`--check` guarantees:
- The file is sorted
- Field order is canonical
- No drift from accumulated edits

`--check` does NOT guarantee:
- Translation/content correctness (a target field hand-edited to garbage will pass)
- Schema-version compatibility (assert version separately)
- Source-side invariants (run actual unit tests for those)

Document this boundary wherever the `--check` command appears in CI configs or contributor docs. Future contributors WILL assume `--check` is a content guard if you don't.

#### Exit-code trap in shell pipelines

This is wrong:

```fish
cargo run -p warp-zh-extractor -- extract ... --check 2>&1 | tail -5
echo "exit=$status"   # ← reflects `tail`, not the binary
```

Use one of:

```bash
# bash with pipefail
set -o pipefail
cargo run ... --check 2>&1 | tail -5

# or invoke directly without pipe
cargo run ... --check
echo "exit=$?"
```

CI invocations MUST either set pipefail or check the binary's exit code directly. fish has no pipefail equivalent — invoke without piping.

---

### Output-directory marker file

Tools that delete-and-recreate an output directory MUST drop a marker file on first creation and refuse to delete on subsequent runs if the marker is absent.

```rust
const MARKER: &str = ".warp-zh-build-marker";

fn prepare_out(out: &Path) -> Result<()> {
    if out.exists() {
        if !out.join(MARKER).exists() {
            bail!(
                "refusing to overwrite {}: missing marker file. \
                 Either delete the directory manually or choose a different --out.",
                out.display()
            );
        }
        fs::remove_dir_all(out)?;
    }
    fs::create_dir_all(out)?;
    fs::write(out.join(MARKER), "")?;
    Ok(())
}
```

#### Why

Cost: one empty file per output. Benefit: makes `tool --out ./real-source-dir` a no-op error instead of a data-loss event. The class of bug this prevents is silent and irreversible.

#### When to apply

- Tools that own the entire output tree (build-zh-out, codegen-out, mirror-out)
- NOT for tools that append to a directory or write a single file (no delete-and-recreate to guard)

---

### Idempotency contract

For any tool that processes input and emits output:

1. Re-running with the same input MUST produce byte-identical output.
2. Timestamps in output MAY be updated only on real change. Tools commonly violate this by stamping `updated_at = now()` unconditionally — don't.
3. Tests MUST cover idempotency: write a test that runs the tool twice and asserts the second run produced no diff.

```rust
#[test]
fn extract_is_idempotent() {
    let tmp = tempdir().unwrap();
    let table = tmp.path().join("strings.json");
    run_extract(&fixture_dir(), &table).unwrap();
    let hash1 = sha256_file(&table);
    run_extract(&fixture_dir(), &table).unwrap();
    let hash2 = sha256_file(&table);
    assert_eq!(hash1, hash2);
}
```

---

## Forbidden Patterns

### Don't: stamp `updated_at = now()` unconditionally

```rust
// Wrong
entry.updated_at = now_iso8601();
new_table.insert(entry.id, entry);
```

Breaks idempotency. Re-running the tool flips every `updated_at` and the file diff every run.

```rust
// Correct
if entry_changed(&old_entry, &new_entry) {
    new_entry.updated_at = now_iso8601();
} else {
    new_entry.updated_at = old_entry.updated_at;
}
```

### Don't: skip files on parse failure

If `syn::parse_file` fails on a `.rs` file, copy the file byte-for-byte to the output and record the failure in the build report. Never panic, never silently skip — both produce a corrupted output tree.

```rust
match syn::parse_file(&content) {
    Ok(ast) => apply_translations(&ast, &mut content),
    Err(e) => {
        report.parse_failures.push(ParseFailure { file: rel.to_string(), error: e.to_string() });
        // Fall through: write `content` unchanged
    }
}
fs::write(&out_path, &content)?;
```

### Don't: build a per-run skip list inline

Adding hardcoded skip strings to a function's body grows untracked technical debt. Centralize in a `const` array at module top, with a one-line comment per group.

---

## Testing Requirements

- Every public extractor/builder function has at least one unit test in the same module.
- Idempotency tests are mandatory for any pipeline that writes a canonical file.
- Integration tests that spawn the actual binary (via `assert_cmd` or similar) cover at least: fresh output, repeat run on existing output, parse-failure fallback, marker-safety refusal.
- Use `tempfile::tempdir` for filesystem fixtures — never write into the project's working tree from tests.
