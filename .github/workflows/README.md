# CI: Build Chinese Warp

`build-translation.yml` builds the localization overlay end-to-end. It has three jobs:

| Job | Runner | What it does | Cost |
|---|---|---|---|
| `tools` | ubuntu | Build + unit-test the Rust extractor/builder. No upstream Warp needed. | seconds–minutes |
| `build-localized` | ubuntu | Clone upstream Warp, run the builder, publish `build/warp-zh` + a coverage summary as artifacts. | minutes (clone-bound) |
| `compile` | macOS **and** Linux | `cargo check -p warp` on the localized tree — the real "does it compile" proof. Mirrors upstream Warp's build setup. | **heavy** (tens of minutes) |

### Triggers

- **push / PR** touching `tools/**`, `translations/**`, or the workflow files.
- **`workflow_dispatch`** with inputs:
  - `warp_ref` — upstream `warpdotdev/warp` ref to build against (default: the pinned commit in the workflow's `DEFAULT_WARP_REF`, which is what `strings.json` was last extracted at; `translations/.lock.json` is gitignored so the pin lives in the workflow).
  - `run_compile` — set `false` to skip the heavy `compile` job and only produce the localized tree.

## Local testing with `act`

[`act`](https://nektosact.com) runs workflows in **Linux Docker containers only** — it **cannot emulate macOS**, so the `compile` job's `macos-latest` leg never runs locally. The `compile` job is therefore guarded with `if: ${{ !github.event.act }}` and skips entirely under `act`. Validate it on real GitHub Actions.

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

### Why the real compile isn't tested under `act`

`cargo check -p warp` requires upstream Warp's full toolchain (protoc, Node/Corepack
for `build.rs`, Git LFS assets, and on macOS the `MACOSX_DEPLOYMENT_TARGET` /
Xcode setup from Warp's `build.rs`). That is what the `compile` job provides on
GitHub-hosted macOS + Linux runners. Locally, run the equivalent by hand:

```bash
cd tools && cargo run -p warp-zh-builder -- build \
    --source ../../warp --table ../translations/strings.json \
    --out ../build/warp-zh --report ../reports/build.json
cd ../build/warp-zh && MACOSX_DEPLOYMENT_TARGET=14.0 cargo check -p warp
```
