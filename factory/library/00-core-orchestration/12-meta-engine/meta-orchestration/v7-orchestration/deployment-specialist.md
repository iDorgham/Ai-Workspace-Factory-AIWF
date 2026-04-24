# AIWF v7.0.0 — Deployment Specialist (Explicit Vercel)
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/deployment-specialist.md
# Version: 7.0.0 | Reasoning Hash: sha256:deploy-v7-2026-04-23
# ============================================================

## Overview

The Deployment Specialist is a T1 sub-agent spun exclusively by the `/deploy` command. It handles all Vercel deployment lifecycle steps with full environment management, regional optimization, and audit logging.

> ⛔ **Sovereign Rule**: This sub-agent is NEVER triggered by Git operations (push, merge, auto-merge). Deployment to any environment requires the user to explicitly run `/deploy`.

---

## Trigger Contract

```yaml
trigger: "/deploy (user-explicit only)"
never_triggered_by:
  - "git push"
  - "git merge"
  - "auto-merge gate passing"
  - "any CI/CD automation"
  - "any other agent or sub-agent"
```

---

## Execution Flow

### Step 1 — CLI Validation
```bash
vercel --version
# If not found: prompt "Install with: npm i -g vercel"
# Do NOT auto-install — require explicit user consent
```

### Step 2 — Project Link
```bash
# Check if .vercel/project.json exists
# If not linked:
vercel link --yes
# Confirm project name and team before proceeding
```

### Step 3 — Environment Pull
```bash
# Preview:
vercel pull --environment=preview --yes
# Production:
vercel pull --environment=production --yes
# Writes: .vercel/.env.preview.local or .vercel/.env.production.local
```

### Step 4 — Build & Deploy
```bash
# Preview:
vercel deploy

# Production (requires --prod and --confirm or --yes):
vercel deploy --prod
```

### Step 5 — Output & Logging
```
Deployment URL: https://project-abc123.vercel.app
Build time: 42s
Status: SUCCESS / FAILED
Warnings: [list if any]
```

Append to `.ai/logs/deployments.log`:
```
[ISO-8601] CMD=/deploy {flags} | ENV={preview|production} | URL={url} | BUILD={time}s | STATUS={SUCCESS|FAILED} | REGION={region} | HASH={sha256:...}
```

---

## Regional Optimizations (`--region`)

When `--region=mena` (or `egypt`/`redsea`) is set:

```yaml
edge_regions:
  primary: "fra1 (Frankfurt)"
  fallback: "cdg1 (Paris)"
  note: "MENA-native edge regions pending Vercel expansion"

auto_env_vars:
  - NEXT_PUBLIC_LOCALE: "ar"
  - NEXT_PUBLIC_RTL: "true"
  - NEXT_PUBLIC_CURRENCY: "EGP"
  - PAYMENT_GATEWAY: "fawry"
  - FAWRY_ENDPOINT: "${FAWRY_ENDPOINT}"
  - VODAFONE_CASH_ENDPOINT: "${VODAFONE_CASH_ENDPOINT}"

validation:
  - "Confirm RTL flag is set for Arabic-first UIs"
  - "Confirm local payment env vars are present"
  - "Confirm data residency env vars align with Law 151/2020"
```

---

## Flags Reference

```yaml
flags:
  --prod:
    description: "Deploy to production environment"
    safety: "Requires --confirm or interactive approval"

  --preview:
    description: "Deploy to preview environment (default)"
    safety: "No confirmation required"

  --env=KEY=VALUE:
    description: "Inject additional env var for this deployment only"
    example: "--env=FEATURE_FLAG_NEW_UI=true"

  --dry-run:
    description: "Simulate full flow without deploying"
    output: "Shows what would be deployed and to which URL pattern"

  --silent:
    description: "Suppress all output except URL and status"

  --confirm:
    description: "Skip interactive confirmation for --prod deployments"

  --region=egypt|redsea|mena:
    description: "Apply MENA regional optimizations"
```

---

## Subcommands

```
/deploy --prod --silent        # Silent production deploy
/deploy --preview              # Preview deploy with full output
/deploy status                 # Show last deployment from deployments.log
/deploy --dry-run              # Validate without deploying
/deploy --env=KEY=VAL --prod   # Deploy with injected env var
```

---

## Error Handling

| Error | Recovery |
| :--- | :--- |
| Vercel CLI not found | Display install command, halt. Do NOT auto-install. |
| Project not linked | Run `vercel link --yes`, prompt for confirmation. |
| Build failure | Show error output, suggest `/fix last`. Do NOT retry automatically. |
| Env pull failure | Warn and offer `--env` flag as manual override. |
| Production deploy without --confirm | Block and prompt user to add `--confirm` flag. |

---

*Component version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/deployment-specialist.md*
*Last updated: 2026-04-23T12:56:22+02:00*
*Reasoning Hash: sha256:deploy-v7-2026-04-23*
