# 🌌 THE DELIVERY GALAXY (AIWF WORKSPACES)
### *Autonomous Production Shards & Experimental Incubation Tiers*

---

## 🏗️ OVERVIEW

The `workspaces/` directory is the physical manifestation of the **AI Workspace Factory**: templates you copy from, plus **client** and **personal** tiers where real project trees live. Each shard can be geofenced and governed per **Law 151/2020** when MENA applies.

---

## 🏛️ SHARD TIERING (v20.0 EQUILIBRIUM)

### 1. 📂 `clients/` [MENA-LOCKED]

- **Status**: Production-grade / compliance-critical.
- **Residency**: Locked to MENA regional posture when the product requires it (e.g. `me-central-1`).
- **Governance**: Each shard should carry its own `.ai/` registry and `metadata.json`.
- **Routing**: Deployed via your **Sovereign CD** pipeline and Omega release practice.
- **Docs**: [`clients/README.md`](clients/README.md) — what belongs in this tier.

### 2. 🧪 `personal/` [GLOBAL-PUBLIC]

- **Status**: R&D / high-velocity incubation.
- **Residency**: Non-sensitive experiments; still isolate from `clients/` (F4-style separation).
- **Governance**: Optional tier-level [`personal/metadata.json`](personal/metadata.json) + [`personal/README.md`](personal/README.md).
- **Audit**: Periodic structural health checks on important shards.

### 3. 🌌 `templates/` [INDUSTRIAL OS REGISTRY]

- **Six** OMEGA-style starter trees (e.g. **CORE_OS_SAAS**, **WEB_OS_TITAN**, …) under `workspaces/templates/<NAME>/`.
- **Source of truth** for `/init`-style materialization; not edited as live production code.

---

## 🚀 Materializing a new workspace

From the **AIWF repository root** (directory that contains `workspaces/templates/`):

```bash
bash .ai/scripts/factory_materialize.sh
```

**Cursor:** use slash **`/mat`** — it tells the assistant to run the same command in a **real Terminal** (interactive `read` prompts do not work reliably from chat stdin).

**Prompts (in order):**

| Step | Question | You can enter |
|------|-----------|----------------|
| 1 | Template | Index `0`…`n-1`, or **folder name** (e.g. `CORE_OS_SAAS`), or a **unique** substring (e.g. `saas`). Case-insensitive. |
| 2 | Layer | `0` / `clients` / `client` / `mena-locked`, or `1` / `personal` / `private` / `rnd` / `rd`. |
| 3 | Workspace name | Final **slug** for `workspaces/<layer>/<slug>/`. |

The script finds the repo root automatically (walks upward until `workspaces/templates/` exists). After copy + path localization it runs template **sanitize** (if present), **`git init`**, and an initial commit.

---

## 📌 Git tracking (this repository)

Root **`.gitignore`** uses `workspaces/*` with a small **allowlist**. In practice:

- **`workspaces/templates/`** — the whole tree is **not committed** (ignored like slug folders); keep templates in your working copy or supply them via your own distribution policy.
- **`workspaces/clients/<slug>/`** and **`workspaces/personal/<slug>/`** — **not committed**.
- **Committed** paths: `workspaces/README.md` (this file), `workspaces/.gitkeep`, `workspaces/clients/README.md`, `workspaces/personal/README.md`, `workspaces/personal/metadata.json`.

---

## 🛡️ SHARD ANATOMY

Every materialized workspace is intended to be a **self-contained** software environment with:

- **`.ai/`** — local agent memory, commands, plans, skills as copied from the template.
- **`metadata.json`** (per shard) — `workspace_type`, `region`, residency, timestamps (create in shard when missing).
- **`.cursor/rules/`** (optional) — IDE alignment; sync from canonical rules when policy requires.
- **`CLAUDE.md` / `AGENTS.md`** — onboarding manifests when the template provides them.

---

*Governor: Dorgham | Registry: workspaces/README.md | Status: OMEGA-CERTIFIED*
