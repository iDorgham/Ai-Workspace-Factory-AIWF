# `factory/` — AIWF engine layer

Executable Python packages, automation scripts, tests, the **global library**, and **industrial OS shard sources** under **`factory/shards/`**. Canonical human specs live under **`docs/`** (`docs/product/PRD.md`, `docs/overview/CONTEXT.md`, …); runtime logs and factory-generated artifacts go under **`docs/reports/`** (including **`docs/reports/factory/`**).

---

## Layout

| Path | Role |
|------|------|
| **`core/`** | Python modules (`factory_manager`, `healing_bot`, `neural_sync`, `regional_controller`, omega helpers). Import as `factory.core.*` — not shell scripts. |
| **`scripts/`** | CLI and maintenance tools (`scripts/core/`, `scripts/automation/`, `scripts/maintenance/`). Run with `python3 factory/scripts/...` from repo root. |
| **`tests/`** | Pytest harness (`pytest factory/tests/`). |
| **`library/`** | Global agents, skills, design packs, planning mirror, registries — see `factory/library/README.md`. |
| **`shards/`** | Six industrial OS trees (`CORE_OS_SAAS`, `WEB_OS_TITAN`, …) for **`/mat`**. Large bodies are typically **gitignored**; see `factory/shards/README.md`. |
| **`stubs/`** | Small scaffold manifests (`industrial_templates.yaml`, `distribution/`, `fintech/` seeds) — not the full OS shards. |
| **`cfg/`** | One-word bundle: **`config/`**, **`manifests/`**, **`schema/`**, **`intake/`**, **`registry/`**, **`logs/`** (factory-local config + intake + logs). |
| **`dashboard/`** | TUI (`omega_tui_lite.py`, …) and **`dashboard/pages/`** (markdown “dashboard” content moved from repo-root `dashboard/`). |

**Removed / relocated (v20.3 housekeeping):**

- **`factory/profiles/`** — retired JSON composition packs; use industrial OS templates + `metadata.json` in spawned workspaces instead.
- **`factory/reports/`** → **`docs/reports/factory/`** — swarm state, headless execution log, registry repairs, composition notes (single `docs/` tree at repo root).
- **`factory/docs/`** — retired; deep library snapshot lives at **`docs/reference/DEEP_LIBRARY_DOC.md`**.

---

## Why `core/`, `scripts/`, and `tests/` stay separate

- **`core/`** is importable library code consumed by scripts and tests.
- **`scripts/`** is entrypoints and orchestration (different packaging and `PYTHONPATH` expectations).
- **`tests/`** follows pytest discovery; co-locating tests under `scripts/` would break layout conventions and CI.

Do not flatten these into one folder without a dedicated migration (imports and CI paths would all change).

---

## Related

- Materialize: `bash .ai/scripts/factory_materialize.sh` (repo root).
- Orientation: `docs/overview/CONTEXT.md` · Full spec: `docs/product/PRD.md`.
