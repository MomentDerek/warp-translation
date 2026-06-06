# CI: Build Chinese Warp

Two workflows:

- **`build-translation.yml`** — builds + packages + releases the localization overlay (below).
- **`daily-sync-translate.yml`** — the unattended daily pipeline that watches
  upstream releases, translates new strings, and cuts a tag that drives
  `build-translation.yml`. See [Daily automation](#daily-automation-daily-sync-translateyml).

## `build-translation.yml`

`build-translation.yml` builds the localization overlay end-to-end. It has four jobs:

| Job | Runner | What it does | Cost |
|---|---|---|---|
| `tools` | ubuntu | Build + unit-test the Rust extractor/builder. No upstream Warp needed. | seconds–minutes |
| `build-localized` | ubuntu | Clone upstream Warp, run the builder, publish `build/warp-zh` + a coverage summary as artifacts. | minutes (clone-bound) |
| `package` | macOS **and** Linux | Build installable packages from the localized tree via upstream Warp's `script/bundle --channel oss` (the `warp-oss` bin — self-contained, no private warp-channel-config): Linux **deb/rpm/AppImage**, macOS **unsigned `.dmg`** (`--nosign`). Uploaded as `warp-zh-installer-*` artifacts. A successful bundle also proves the translated source compiles in release mode. **Runs on tag pushes + `workflow_dispatch` only** (branch pushes/PRs get the cheap `tools` + `build-localized` signal). | **heavy** (tens of minutes) |
| `release` | ubuntu | **Tag pushes only.** Downloads the `warp-zh-installer-*` artifacts and publishes them as a GitHub Release on the tag. | seconds |

### Triggers

- **push / PR** touching `tools/**`, `translations/**`, or the workflow files.
- **tag push** (`tags: ['*']`) — builds everything and cuts a GitHub Release (see [Cutting a release](#cutting-a-release)).
- **`workflow_dispatch`** with inputs:
  - `warp_ref` — upstream `warpdotdev/warp` ref to build against (default: the pinned commit in the workflow's `DEFAULT_WARP_REF`, which is what `strings.json` was last extracted at; `translations/.lock.json` is gitignored so the pin lives in the workflow).
  - `build_packages` — set `false` to skip the heavy `package` job and only produce the localized tree.

### Cutting a release

Pushing **any tag** builds the installers on both runners and publishes a GitHub Release with those assets attached:

```bash
git tag v1.0.0
git push origin v1.0.0
```

- The release is **published** (not a draft/prerelease), titled after the tag, with auto-generated notes.
- Assets: macOS `WarpOss-arm64.dmg` (unsigned) + Linux `*.deb` / `*.rpm` / `*.AppImage`.
- `GIT_RELEASE_TAG` becomes the tag name, so deb/rpm versions derive from it — prefer version-like tags such as `v1.2.3`.
- Re-pushing the same tag re-runs the build and **clobbers** the existing release assets (idempotent).
- The `release` job needs `contents: write` (granted at job level; the workflow default is read-only) and uses the built-in `GITHUB_TOKEN` — no extra secrets.

> Tag pushes build against `DEFAULT_WARP_REF` (the pinned upstream commit `strings.json` was extracted at), not whatever is newest upstream. Bump that pin and re-extract before tagging if you want a release against a newer Warp.

> **macOS `.dmg` is unsigned.** It is built with `script/bundle --nosign`, so it is **not** code-signed or notarized. On first launch macOS Gatekeeper blocks it — right-click → Open (or `xattr -dr com.apple.quarantine Warp.app`) to run it. For a distributable signed/notarized build you'd add Apple Developer ID secrets and switch `--nosign` to `--read-passwords-from-env`.

## Local testing with `act`

[`act`](https://nektosact.com) runs workflows in **Linux Docker containers only** — it **cannot emulate macOS**, so the `package` job's `macos-latest` leg never runs locally. The `package` job is therefore guarded with `if: ${{ !github.event.act }}` and skips entirely under `act`. Validate it on real GitHub Actions.

### Prerequisites

```bash
brew install act              # the simulator
# plus a container runtime — Docker Desktop, Colima, or OrbStack — running.
```

Defaults live in [`.actrc`](../../.actrc): amd64 emulation (required on Apple Silicon) and the `catthehacker/ubuntu:act-latest` runner image.

### List the plan

```bash
act -W .github/workflows/build-translation.yml -l          # list jobs
act -W .github/workflows/build-translation.yml -n          # dry-run (validate structure)
```

### Run the self-contained job (recommended local smoke test)

The `tools` job needs no upstream Warp and is the right thing to actually execute locally:

```bash
act -W .github/workflows/build-translation.yml -j tools
```

### Run the localized-tree build locally

`build-localized` clones upstream Warp (large) inside the container and needs the
artifact server for `upload-artifact`:

```bash
act -W .github/workflows/build-translation.yml -j build-localized \
    --artifact-server-path "$PWD/.artifacts"
```

> First run pulls the runner image (~1 GB) and clones Warp — expect several
> minutes. `--pull=false` skips re-pulling the image on later runs.

### Why packaging isn't tested under `act`

`script/bundle` requires upstream Warp's full toolchain (protoc, Node/Corepack
for `build.rs`, Go, Git LFS assets, `cargo-bundle`, `create-dmg`/`linuxdeploy`,
and on macOS the `MACOSX_DEPLOYMENT_TARGET` setup). That is what the `package`
job provides on GitHub-hosted macOS + Linux runners. Locally, run the
equivalent by hand:

```bash
# 1. produce the localized tree
cd tools && cargo run -p warp-zh-builder -- build \
    --source ../../warp --table ../translations/strings.json \
    --out ../build/warp-zh --report ../reports/build.json
# 2. compile-check, or build a package
cd ../build/warp-zh
MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp           # quick verify, or:
script/bundle --nosign --channel oss --arch aarch64         # macOS unsigned WarpOss.dmg
script/bundle --channel oss --packages appimage,deb,rpm     # Linux WarpOss packages
```

---

## Daily automation (`daily-sync-translate.yml`)

A scheduled, unattended pipeline that keeps the overlay in step with upstream
releases and cuts a localized release automatically. It does **not** duplicate
`build-translation.yml` — it ends by pushing a tag, which is what triggers the
build/package/release machinery above.

### Flow

```
cron 06:30 UTC (or workflow_dispatch)
        │
   ┌────▼─────┐  detect: resolve latest upstream warpdotdev/warp tag for the
   │  detect  │          channel (default: dev) and compare to our pin
   └────┬─────┘          (translations/strings.json → metadata.source_commit).
        │ should_run?     Skips the rest when already current.
   ┌────▼───────────┐  sync-translate:
   │ sync-translate │   1. clone upstream at that tag → run warp-zh-extractor
   └────┬───────────┘      (incremental: new / fuzzy / obsolete; 2nd pass
        │                   hard-deletes obsolete; --check drift annotation).
        │                2. diff_table.py classifies the changes.
        │                3. new>0 → build_batch.py → headless `claude -p` runs the
        │                   EXISTING .claude/workflows/translate_batch.mjs
        │                   (opus implementers → apply_batch.py → check). Must PASS.
        │                4. bump DEFAULT_WARP_REF pin, commit to main, push a tag
        │                   named after the upstream release.
        ▼
  tag push → build-translation.yml → package (macOS+Linux) → GitHub Release
             (dev/preview tags auto-marked prerelease)
```

`fuzzy` / `obsolete` entries are **surfaced** (run summary + `daily-diff`
artifact) but **not** auto-translated — fuzzy needs the manual RUNBOOK resync
(no invariant gate for direct edits), and stale/untranslated strings fall back
to English in the build, so the release is never broken. obsolete entries are
hard-removed by the extractor's fixed-point pass.

### Inputs (`workflow_dispatch`)

| Input | Default | Meaning |
|---|---|---|
| `channel` | `dev` | Upstream release channel to track (`dev` / `preview` / `stable`). |
| `force` | `false` | Run even if already at the latest upstream tag. |
| `dry_run` | `false` | Detect + extract + diff only — no translate, commit, or release. |

### Required secrets

| Secret | Used for |
|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Auth for the headless Claude Code translation run, **billed against your Claude subscription** (Pro/Max) rather than the pay-per-token API. Generate it locally with `claude setup-token` (opens a browser, authorizes with your subscription, prints a long-lived `sk-ant-oat…` token). The translate step prefers this when present. |
| `ANTHROPIC_API_KEY` | *Alternative* to the OAuth token — pay-per-token API billing. Set **one** of the two. If both are set, the OAuth token wins (the step unsets the API key). |
| `WARP_ZH_PAT` | A PAT used to push the commit + tag. **Required** because pushes made with the default `GITHUB_TOKEN` do **not** trigger other workflows — the release tag would land but `build-translation.yml` would never fire. Fine-grained PAT scoped to this repo with **Contents: Read and write** *and* **Workflows: Read and write** (the daily commit edits `build-translation.yml`'s pin, and GitHub rejects PAT pushes that touch `.github/workflows/**` without the Workflows permission). Classic-PAT equivalent: `repo` + `workflow` scopes. |

Add the auth secret + `WARP_ZH_PAT` under **Settings → Secrets and variables → Actions**.

> **Subscription auth + usage limits.** `CLAUDE_CODE_OAUTH_TOKEN` is the
> Anthropic-sanctioned way to run Claude Code headlessly on a subscription. Note
> the translate step can fan out up to 8 parallel **opus** implementers, which is
> token-heavy — a **Max** plan has the headroom; a **Pro** plan's smaller cap may
> throttle/fail on a large day (many new strings). The token is long-lived but can
> expire or be revoked, in which case the run fails auth and you regenerate it.

### Helper scripts (also locally runnable)

- `tools/translations/kit/resolve_upstream.py` — list upstream tags (via `gh
  api`, falling back to `git ls-remote`), pick the latest for a channel, compare
  to the pin, emit `should_run` / `upstream_tag` / `upstream_sha` GH outputs.
- `tools/translations/kit/diff_table.py` — diff a `strings.json` before/after an
  extractor run into `new` / `fuzzy` / `obsolete` / `deleted` counts (the same
  logic `sync-upstream-translations.ts` uses inline).

### Local simulation

```bash
# 1. detect logic against live upstream (needs `gh auth login`):
python3 tools/translations/kit/resolve_upstream.py --channel dev
#    → should_run=true/false, upstream_tag, upstream_sha, current_pin

# 2. real incremental diff against a newer ref (clone upstream at that sha first):
cp translations/strings.json /tmp/before.json
( cd tools && ./target/release/warp-zh-extractor extract \
    --source /path/to/warp-clone --table ../translations/strings.json --lock ../translations/.lock.json )
python3 tools/translations/kit/diff_table.py /tmp/before.json translations/strings.json --report /tmp/diff.json

# 3. structural validation of the workflow YAML:
act -W .github/workflows/daily-sync-translate.yml -l        # list jobs
act schedule -W .github/workflows/daily-sync-translate.yml -n   # dry-run
```

> `act` runs Linux containers with host networking, so on a machine that proxies
> `github.com` the in-container `detect` step can't reach the API — validate
> `resolve_upstream.py` directly (step 1) and use `-n` for structure. On real
> GitHub runners there is no such proxy.

