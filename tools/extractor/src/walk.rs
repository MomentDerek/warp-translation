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
pub fn is_ignored_dir(name: &str) -> bool {
    matches!(
        name,
        "target" | ".git" | "node_modules" | ".cargo" | "build" | "dist"
    )
}
