# `/deploy` — Vercel Deployment Command
**Version**: 7.0.0
**Agent**: Deployment Specialist (spun by Swarm Router v3)

> ⚠️ **EXPLICIT ONLY**: This command NEVER runs automatically. Deployment to Vercel is triggered ONLY when the user explicitly runs `/deploy`. Git pushes and auto-merges do NOT trigger this command.

---

## Synopsis

```
/deploy [--prod | --preview] [--env=KEY=VALUE] [--dry-run] [--silent] [--confirm] [--region=egypt|redsea|mena]
/deploy status
```

## Description

Deploys the current workspace (or specified phase output) to Vercel. Supports both preview and production deployments with full environment variable management and regional optimization.

## Execution Steps

1. **CLI Check**: Verify Vercel CLI is available (`vercel --version`). If not found, prompt to install: `npm i -g vercel`.
2. **Project Link**: If not already linked, run `vercel link --yes` to associate with the Vercel project.
3. **Environment Pull**: Run `vercel pull --environment=preview` (or `production`) to sync `.vercel/.env.*` files.
4. **Build & Deploy**:
   - Preview: `vercel deploy`
   - Production: `vercel deploy --prod`
5. **Output**: Display deployment URL, build duration, and any warnings.
6. **Audit Log**: Append to `.ai/logs/deployments.log`:
   ```
   [ISO-8601] /deploy --prod | URL: https://... | Hash: sha256:... | Region: mena | Status: SUCCESS
   ```

## Flags

| Flag | Description |
| :--- | :--- |
| `--prod` | Deploy to production environment. |
| `--preview` | Deploy to preview environment (default if no flag). |
| `--env=KEY=VALUE` | Inject additional environment variables for this deployment. |
| `--dry-run` | Simulate the deployment flow without actually deploying. |
| `--silent` | Suppress non-essential output. Only show URL and status. |
| `--confirm` | Skip confirmation prompt for production deployments. |
| `--region=egypt\|redsea\|mena` | Auto-configure MENA-friendly edge regions and local payment env vars. |

## Subcommands

- `/deploy --prod --silent` — Production deploy with minimal output.
- `/deploy --preview` — Preview deploy for review before promotion.
- `/deploy status` — Show last deployment status from `.ai/logs/deployments.log`.
- `/deploy --dry-run` — Validate the deployment config without deploying.

## Regional Optimizations (`--region`)

When `--region=mena` (or `egypt`/`redsea`) is active, the Deployment Specialist auto-configures:
- Vercel edge function regions closest to MENA (e.g., `fra1`, `cdg1` as fallbacks until ME-specific regions are available).
- Injects environment variables for local payment gateways (Fawry API keys, Vodafone Cash endpoints).
- Validates that `NEXT_PUBLIC_LOCALE=ar` or RTL flags are set for Arabic-first UIs.

## Audit Log Format

File: `.ai/logs/deployments.log`

```
[2026-04-23T12:44:57+02:00] CMD=/deploy --prod | ENV=production | REGION=mena | URL=https://aiwf-v7.vercel.app | BUILD=45s | STATUS=SUCCESS | HASH=sha256:abc123...
```

---

*Command version: 7.0.0 | Last updated: 2026-04-23*
