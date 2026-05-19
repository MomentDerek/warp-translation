//! End-to-end safety tests for the `build` subcommand. These spawn the
//! built binary against a synthetic source tree to verify:
//!   * the marker-file safety check refuses to overwrite an unmarked dir
//!   * fresh `--out` gets written and the marker dropped
//!   * a second run on the same `--out` succeeds (idempotent)
//!   * non-Rust files are byte-copied (including dotfiles like `.gitignore`)
//!   * ignored dirs (`target`, `.git`, etc.) are NOT mirrored into out
//!   * a `.rs` file that fails to parse is byte-copied verbatim

use std::fs;
use std::path::Path;
use std::process::Command;

fn write(path: &Path, contents: &str) {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).unwrap();
    }
    fs::write(path, contents).unwrap();
}

fn binary_path() -> std::path::PathBuf {
    // The integration test runner sets CARGO_BIN_EXE_<binary> for binaries in
    // the same package.
    let p = env!("CARGO_BIN_EXE_warp-zh-builder");
    std::path::PathBuf::from(p)
}

fn run_build(source: &Path, table: &Path, out: &Path) -> std::process::Output {
    Command::new(binary_path())
        .arg("build")
        .arg("--source")
        .arg(source)
        .arg("--table")
        .arg(table)
        .arg("--out")
        .arg(out)
        .output()
        .expect("spawn builder")
}

const MIN_TABLE: &str = r#"{
  "$schema_version": "1.0.0",
  "metadata": {
    "source_repo": "..",
    "tool_version": "test",
    "entry_count": 1,
    "stats": {}
  },
  "entries": [
    {
      "id": "ID-Hello",
      "source": "Hello",
      "source_hash": "deadbeef",
      "target": "你好",
      "status": "translated",
      "occurrences": [{"file": "lib.rs", "line": 1, "kind": "literal"}],
      "flags": [],
      "history": [],
      "audit": {"score": 8, "verdict": "auto_ui", "reasons": [{"code": "ui", "delta": 5}]},
      "first_seen_commit": "c",
      "last_seen_commit": "c",
      "created_at": "t",
      "updated_at": "t"
    }
  ]
}
"#;

#[test]
fn build_succeeds_and_drops_marker() {
    let tmp = tempfile::tempdir().unwrap();
    let src = tmp.path().join("src");
    let out = tmp.path().join("out");
    let table = tmp.path().join("strings.json");

    write(&src.join("lib.rs"), r#"fn f() { let _ = "Hello"; }"#);
    write(&src.join(".gitignore"), "target\n");
    write(&src.join("README.md"), "doc\n");
    write(&src.join("target/garbage.txt"), "should not be copied\n");
    write(&src.join(".git/config"), "[core]\n");
    // `.cargo/config.toml` is user-authored build config; it must be mirrored
    // into the output so the translated copy builds the same way upstream
    // does. Regression guard for the .cargo-skipped bug.
    write(&src.join(".cargo/config.toml"), "[build]\nrustflags = []\n");
    write(&table, MIN_TABLE);

    let result = run_build(&src, &table, &out);
    assert!(
        result.status.success(),
        "build failed: stdout={} stderr={}",
        String::from_utf8_lossy(&result.stdout),
        String::from_utf8_lossy(&result.stderr)
    );

    // Marker present.
    assert!(out.join(".warp-zh-build-marker").exists());
    // Translated literal applied.
    let lib = fs::read_to_string(out.join("lib.rs")).unwrap();
    assert!(lib.contains("\"你好\""), "got: {lib}");
    // Dotfile copied.
    assert!(out.join(".gitignore").exists());
    // Plain file copied.
    assert!(out.join("README.md").exists());
    // Ignored dirs NOT copied.
    assert!(!out.join("target").exists());
    assert!(!out.join(".git").exists());
    // `.cargo/` IS copied (regression: previously folded into the ignore list).
    let cargo_cfg = out.join(".cargo/config.toml");
    assert!(cargo_cfg.exists(), ".cargo/config.toml must be mirrored");
    assert_eq!(
        fs::read_to_string(&cargo_cfg).unwrap(),
        "[build]\nrustflags = []\n"
    );
}

#[test]
fn build_refuses_to_overwrite_unmarked_dir() {
    let tmp = tempfile::tempdir().unwrap();
    let src = tmp.path().join("src");
    let out = tmp.path().join("existing");
    let table = tmp.path().join("strings.json");

    write(&src.join("lib.rs"), r#"fn f() {}"#);
    write(&table, MIN_TABLE);

    // Pre-create out as a real source-looking dir without the marker.
    fs::create_dir_all(&out).unwrap();
    fs::write(out.join("important.rs"), "fn keep() {}").unwrap();

    let result = run_build(&src, &table, &out);
    assert!(!result.status.success(), "should have refused");
    let stderr = String::from_utf8_lossy(&result.stderr);
    assert!(
        stderr.contains(".warp-zh-build-marker") || stderr.contains("marker"),
        "stderr={stderr}"
    );
    // Original file untouched.
    assert!(out.join("important.rs").exists());
}

#[test]
fn build_idempotent_when_marker_present() {
    let tmp = tempfile::tempdir().unwrap();
    let src = tmp.path().join("src");
    let out = tmp.path().join("out");
    let table = tmp.path().join("strings.json");

    write(&src.join("lib.rs"), r#"fn f() { let _ = "Hello"; }"#);
    write(&table, MIN_TABLE);

    let r1 = run_build(&src, &table, &out);
    assert!(r1.status.success());
    let r2 = run_build(&src, &table, &out);
    assert!(
        r2.status.success(),
        "second run failed: stderr={}",
        String::from_utf8_lossy(&r2.stderr)
    );
    assert!(out.join(".warp-zh-build-marker").exists());
    assert!(out.join("lib.rs").exists());
}

#[test]
fn parse_failure_is_byte_copied() {
    let tmp = tempfile::tempdir().unwrap();
    let src = tmp.path().join("src");
    let out = tmp.path().join("out");
    let table = tmp.path().join("strings.json");
    let report = tmp.path().join("report.json");

    let bad_rs = "fn main() { let x =";
    write(&src.join("good.rs"), r#"fn g() { let _ = "Hello"; }"#);
    write(&src.join("bad.rs"), bad_rs);
    write(&table, MIN_TABLE);

    let result = Command::new(binary_path())
        .arg("build")
        .arg("--source")
        .arg(&src)
        .arg("--table")
        .arg(&table)
        .arg("--out")
        .arg(&out)
        .arg("--report")
        .arg(&report)
        .output()
        .expect("spawn");
    assert!(
        result.status.success(),
        "stderr={}",
        String::from_utf8_lossy(&result.stderr)
    );

    // Bad file copied verbatim.
    let bad_out = fs::read_to_string(out.join("bad.rs")).unwrap();
    assert_eq!(bad_out, bad_rs);
    // Good file translated.
    let good_out = fs::read_to_string(out.join("good.rs")).unwrap();
    assert!(good_out.contains("\"你好\""));
    // Report records the failure.
    let report_text = fs::read_to_string(&report).unwrap();
    assert!(
        report_text.contains("bad.rs"),
        "report should mention bad.rs: {report_text}"
    );
    assert!(
        report_text.contains("\"files_parse_failed\": 1")
            || report_text.contains("\"files_parse_failed\":1"),
        "{report_text}"
    );
}
