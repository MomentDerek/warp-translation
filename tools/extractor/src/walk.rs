use std::path::{Path, PathBuf};
use walkdir::WalkDir;

/// Walk a source tree and return every `.rs` file, skipping `target/`,
/// `.git/`, and other generated directories. The result is sorted to
/// guarantee deterministic extraction output.
pub fn collect_rust_files(root: &Path) -> Vec<PathBuf> {
    let mut files: Vec<PathBuf> = WalkDir::new(root)
        .follow_links(false)
        .into_iter()
        .filter_entry(|e| !is_ignored_dir(e.file_name().to_string_lossy().as_ref()))
        .filter_map(|e| e.ok())
        .filter(|e| e.file_type().is_file())
        .map(|e| e.into_path())
        .filter(|p| p.extension().is_some_and(|ext| ext == "rs"))
        .collect();
    files.sort();
    files
}

/// Directories whose contents we never copy or scan. Shared with the builder
/// so the copied source tree mirrors what the extractor saw.
///
/// Only truly generated / reproducible dirs go here. User-authored hidden
/// config dirs (notably `.cargo/`, which carries `config.toml` for target /
/// registry settings) must NOT be skipped — the translated copy needs them
/// to build the same way upstream does.
pub fn is_ignored_dir(name: &str) -> bool {
    matches!(name, "target" | ".git" | "node_modules" | "build" | "dist")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ignores_generated_dirs() {
        for name in ["target", ".git", "node_modules", "build", "dist"] {
            assert!(is_ignored_dir(name), "{name} should be ignored");
        }
    }

    #[test]
    fn does_not_ignore_cargo_config_dir() {
        // `.cargo/config.toml` carries registry / target build config the
        // translated copy must inherit. Regression guard: see PR fix for
        // "builder skipping .cargo hidden dir".
        assert!(!is_ignored_dir(".cargo"));
    }

    #[test]
    fn does_not_ignore_normal_dirs() {
        for name in ["src", "crates", "app", "tests", ".github"] {
            assert!(!is_ignored_dir(name), "{name} should not be ignored");
        }
    }
}
