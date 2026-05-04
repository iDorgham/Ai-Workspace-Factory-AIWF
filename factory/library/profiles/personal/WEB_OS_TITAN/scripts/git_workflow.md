# Git workflow — branches, commits, tags, releases, deploy tags, push/pull

This profile assumes the **AIWF command docs** in **`factory/library/commands/git.md`** are mirrored into the workspace. Prefer **`/git`** semantics over ad-hoc scripts when the orchestrator supports it.

## 1. Branching model (recommended)

| Branch | Purpose |
|--------|---------|
| **`main`** | Production-ready; protected. |
| **`develop`** | Integration for CMS + frontend + content pipelines (optional). |
| **`feature/<slug>`** | SDD feature work tied to a phase or spec id. |
| **`content/<topic>`** | Large editorial campaigns that should not block code release. |

Create feature branches before **`/dev implement`** on shared repos:

```bash
git checkout main && git pull && git checkout -b feature/cms-dashboard-spec-01
```

## 2. Commits

- Use **`/git auto`** (documented in `git.md`) when your workspace implements that router.  
- Otherwise: **conventional commits** (`feat:`, `fix:`, `chore:`) + reference spec / phase id in the body.

## 3. Tags

| Tag kind | Example | Notes |
|----------|---------|-------|
| **Release** | `v1.4.0` | Semantic version for user-facing site + CMS. |
| **Deploy** | `deploy/prod-2026-05-04` or env-specific | Marks what reached which environment; pair with CI/CD job names. |
| **Phase / SDD** | `phase/03-design-complete` | Optional traceability for Omega-style gates. |

```bash
git tag -a v1.4.0 -m "Release: portfolio + CMS dashboard"
git push origin v1.4.0
```

## 4. Silent phase / release automation (AIWF repo tool)

On the **AIWF factory** repo (not necessarily inside a client shard), phase tagging may use:

- **`factory/library/scripts/core/silent_phase_release.py`**

Read that script’s header before wiring CI. Shards should copy **only** the automation they intend to support.

## 5. Density gate (before “release” claims)

From AIWF repo root:

```bash
python3 factory/scripts/core/spec_density_gate_v2.py --phase .ai/plan/content/phase-01-example
```

Adjust `--phase` to your real phase path.

## 6. Push / pull hygiene

```bash
git pull --rebase origin main
git push -u origin HEAD
```

For **tags**:

```bash
git push origin --tags
```

## 7. Deploy tags vs release tags

- **Release tag** = semver for humans and changelog.  
- **Deploy tag** = immutable marker tied to a **deployment** record (preview vs production). Keep both only if your CD system reads deploy tags.

**Deploy policy:** follow workspace **`AGENTS.md`** — production only via explicit **`/deploy`** (or equivalent), not from a post-commit hook.

**Traceability:** `2026-05-04` — WEB_OS_TITAN git workflow companion.
