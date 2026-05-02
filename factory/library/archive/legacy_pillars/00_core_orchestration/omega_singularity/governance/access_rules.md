# Sovereign Workspace — Access & Role Rules v3.2
# ============================================================
# Defines which personas can trigger which commands.
# Enforced by workflow-agent before execution.
# ============================================================

## ROLES

| Role | Description | Personas |
|------|-------------|---------|
| `strategist` | Content planning, topic selection, reviews | Alex (Content Strategist) |
| `seo` | SEO optimization, keyword strategy, audits | Sam (SEO Specialist) |
| `brand` | Voice, design, approvals | Maya (Brand/Design Lead) |
| `admin` | Full access including destructive commands | Workspace Owner |

---

## COMMAND PERMISSIONS

| Command | `strategist` | `seo` | `brand` | `admin` |
|---------|:---:|:---:|:---:|:---:|
| `/research competitors` | ✅ | ✅ | ✅ | ✅ |
| `/scrape *` | ✅ | ✅ | — | ✅ |
| `/sync` | ✅ | ✅ | — | ✅ |
| `/extract brand voice from *` | — | — | ✅ | ✅ |
| `/refine brand voice` | — | — | ✅ | ✅ |
| `/create *` | ✅ | — | — | ✅ |
| `/compare sovereign vs competitor *` | ✅ | ✅ | ✅ | ✅ |
| `/polish content in content/` | ✅ | ✅ | — | ✅ |
| `/optimize images in content/` | — | ✅ | — | ✅ |
| `/review` | ✅ | ✅ | ✅ | ✅ |
| `/approve` | — | — | ✅ | ✅ |
| `/revise [feedback]` | ✅ | ✅ | ✅ | ✅ |
| `/export` | — | ✅ | — | ✅ |
| `/archive old content` | — | — | — | ✅ |
| `/memory save \| load \| clear` | ✅ | ✅ | ✅ | ✅ |
| `/budget check` | ✅ | ✅ | ✅ | ✅ |

---

## ENFORCEMENT RULES

1. If role is unset: default to `strategist` permissions
2. If unauthorized command attempted: return clear message — "This command requires [role] access."
3. `/approve` is gated to `brand` or `admin` only — brand alignment is the final quality gate owner
4. `/archive` is destructive (compresses data) — `admin` only
5. `/export` requires both approval (by brand role) and export permission (seo/admin)
