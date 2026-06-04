# CI: Build Chinese Warp

`build-translation.yml` builds the localization overlay end-to-end. It has four jobs:

| Job | Runner | What it does | Cost |
|---|---|---|---|
| `tools` | ubuntu | Build + unit-test the Rust extractor/builder. No upstream Warp needed. | seconds–minutes |
| `build-localized` | ubuntu | Clone upstream Warp, run the builder, publish `build/warp-zh` + a coverage summary as artifacts. | minutes (clone-bound) |
| `package` | macOS **and** Linux | Build installable packages from the localized tree via upstream Warp's `script/bundle --channel oss` (the `warp-oss` bin — self-contained, no private warp-channel-config): Linux **deb/rpm/AppImage**, macOS **unsigned `.dmg`** (`--nosign`). Uploaded as `warp-zh-installer-*` artifacts. A successful bundle also proves the translated source compiles in release mode. | **heavy** (tens of minutes) |
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
