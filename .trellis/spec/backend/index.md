# Backend (Rust Tooling) Guidelines

> Conventions for the Rust translation tooling in `tools/` (`warp-zh-extractor`, `warp-zh-builder`).

---

## Overview

This project has no application backend, database, or service layer. The "backend" here is the
Rust tooling that extracts UI strings from the Warp source tree, maintains the canonical
`translations/strings.json` table, and builds the translated source. Guidelines below cover that
tooling only.

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Quality Guidelines](./quality-guidelines.md) | Canonical-form contract, marker-file safety, idempotency | Active |
| [Rust syn Extraction](./rust-syn-extraction.md) | `Visit::visit_attribute` + `skip_depth` for doc-attr / macro filtering | Active |

---

**Language**: All documentation should be written in **English**.
