use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct BuildStats {
    pub files_copied: usize,
    pub files_modified: usize,
    pub files_parse_failed: usize,
    pub literals_replaced: usize,
    pub literals_kept_english: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FailureItem {
    pub file: String,
    pub error: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UntranslatedFile {
    pub file: String,
    pub kept_english: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BuildReport {
    pub source_root: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub source_commit: Option<String>,
    pub out_root: String,
    pub built_at: String,
    pub tool_version: String,
    pub stats: BuildStats,
    pub parse_failures: Vec<FailureItem>,
    pub untranslated_files: Vec<UntranslatedFile>,
}
