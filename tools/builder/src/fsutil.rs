//! Filesystem helpers: ensure parent dirs, copy a single file preserving
//! contents (no metadata copy needed for source trees), check permissions.

use std::fs;
use std::path::Path;

use anyhow::{Context, Result};

pub fn ensure_parent_dir(path: &Path) -> Result<()> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent)
                .with_context(|| format!("create dir: {}", parent.display()))?;
        }
    }
    Ok(())
}

pub fn copy_file_bytes(src: &Path, dst: &Path) -> Result<()> {
    ensure_parent_dir(dst)?;
    fs::copy(src, dst).with_context(|| {
        format!("copy {} -> {}", src.display(), dst.display())
    })?;
    Ok(())
}

pub fn write_file(path: &Path, contents: &[u8]) -> Result<()> {
    ensure_parent_dir(path)?;
    fs::write(path, contents).with_context(|| format!("write: {}", path.display()))?;
    Ok(())
}
