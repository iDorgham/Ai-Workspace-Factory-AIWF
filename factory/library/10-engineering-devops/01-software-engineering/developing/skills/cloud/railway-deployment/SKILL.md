# Railway Deployment

## What Railway Provides in Sovereign

| Feature | Sovereign Value |
|---------|-----------|
| Auto-deploy from Git | Push to branch → Railway builds and deploys |
| Managed PostgreSQL | One-click Postgres with backups — no DevOps |
| Managed Redis | One-click Redis — pairs with Prisma + caching |
| Environment groups | staging / production environments, mirrored config |
| Private networking | Services talk over private network (no public exposure needed) |
| Volume storage | Persistent disk (for uploaded files on small projects) |
| Custom domains | `yourdomain.com` → Railway service, HTTPS auto-provisioned |
| CLI + GitHub App | `railway run` locally, auto PR preview environments |

**When to choose Railway:** Founder-mode projects, solo teams, early-stage apps needing zero DevOps overhead. Upgrade path: containerize and move to Cloud Run / ECS when team scales.

---

## Setup

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "@railway/cli": "^3.12.0"   # devDependencies — optional, most users use global install
```

### Install Railway CLI
```bash
# Install globally (recommended)
npm install -g @railway/cli

# Or via brew (macOS)
brew install railway

# Login
railway login
```

---

## Project Initialization

```bash
# Link an existing Railway project
railway link [project-id]

# Or create new from directory
railway init

# Add a PostgreSQL service (one command)
railway add --service postgres

# Add a Redis service
railway add --service redis

# View all services + env vars
railway status
```

---

## railway.json — Service Configuration

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "node apps/api/dist/index.js",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

### Monorepo Configuration (Sovereign)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pnpm install --frozen-lockfile && pnpm build --filter=api"
  },
  "deploy": {
    "startCommand": "pnpm start --filter=api",
    "healthcheckPath": "/health"
  }
}
```

---

## Environment Variables

```bash
# Set variables via CLI (recommended over Railway dashboard for scripts)
railway variables set DATABASE_URL="postgresql://..."
railway variables set NODE_ENV="production"
railway variables set JWT_SECRET="$(openssl rand -base64 32)"

# Reference another service's variable (private networking)
# Railway auto-injects: DATABASE_URL, REDIS_URL for linked services

# View all set variables
railway variables

# Copy vars from one environment to another
railway variables --environment staging | railway variables set --environment production
```

### Reference Variables (Private Networking)
```bash
# In Railway dashboard or CLI — reference the Postgres service variable
# Railway injects these automatically when services are in the same project:
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
```

---

## Multi-Environment Setup (Staging + Production)

```bash
# Railway environments = isolated copies of all services

# Create staging environment
railway environment create staging

# Deploy to staging
railway up --environment staging

# Deploy to production
railway up --environment production

# Run migrations in staging
railway run --environment staging pnpm prisma migrate deploy

# Promote staging to production (via dashboard or CLI)
```

### Environment-Specific railway.json
```json
{
  "environments": {
    "production": {
      "deploy": {
        "numReplicas": 2,
        "healthcheckPath": "/health"
      }
    },
    "staging": {
      "deploy": {
        "numReplicas": 1
      }
    }
  }
}
```

---

## Database on Railway

### PostgreSQL Setup
```bash
# Add Postgres to project
railway add --service postgres

# Get connection string for local dev
railway variables --service postgres

# Run Prisma migrations against Railway DB
railway run pnpm prisma migrate deploy

# Open Prisma Studio against Railway DB
railway run pnpm prisma studio
```

### Prisma Configuration
```prisma
// prisma/schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")        // Railway injects this
  directUrl = env("DATABASE_DIRECT_URL") // set manually for migrations
}
```

```bash
# Railway injects DATABASE_URL (pooled via PgBouncer on Pro plan)
# Set DATABASE_DIRECT_URL separately for Prisma migrations
railway variables set DATABASE_DIRECT_URL="postgresql://..."
```

---

## GitHub Actions Integration

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Run migrations
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          DATABASE_DIRECT_URL: ${{ secrets.DATABASE_DIRECT_URL }}
        run: railway run pnpm prisma migrate deploy

      - name: Deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up --environment production --detach
```

---

## PR Preview Environments

Railway GitHub App auto-creates ephemeral environments per PR:

```bash
# 1. Install Railway GitHub App on your repo
# 2. In Railway project settings → enable PR Environments

# Each PR gets:
# - Isolated copy of all services
# - Unique URL: https://[service]-pr-[number].up.railway.app
# - Auto-destroyed when PR is merged/closed

# Run migrations on PR environment automatically:
# Add to railway.json under deploy.releaseCommand:
{
  "deploy": {
    "releaseCommand": "pnpm prisma migrate deploy"
  }
}
```

---

## Useful Railway CLI Commands

```bash
railway status           # show all services, URLs, health
railway logs             # stream logs from deployed service
railway logs --tail 100  # last 100 lines
railway shell            # SSH into running container
railway run <cmd>        # run command with Railway env vars injected
railway up               # deploy current directory
railway up --detach      # deploy without following logs
railway domain           # manage custom domains
railway volume           # manage persistent volumes
railway redeploy         # trigger redeploy without code push
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[RW-001]** Not setting `DATABASE_DIRECT_URL` — Railway's pooled URL breaks Prisma migrations (same as NP-001)
- **[RW-002]** Hardcoding `railway.json` start command for local dev — use `railway run` prefix locally to inject vars
- **[RW-003]** Not using `releaseCommand` for migrations — migrations run manually, can drift from code
- **[RW-004]** Using Railway volumes for user uploads at scale — volumes are single-region; use R2/S3 for production file storage
- **[RW-005]** Running `railway up` from CI without `--detach` — CI hangs waiting for logs instead of finishing
- **[RW-006]** Not enabling PR environments — manual preview deploys are slow and inconsistent
- **[RW-007]** Using Railway for >$500/month workloads without evaluating Cloud Run — Railway is PaaS with premium pricing at scale

## Success Criteria
- [ ] `releaseCommand` in railway.json runs `prisma migrate deploy` automatically on deploy
- [ ] `DATABASE_DIRECT_URL` set separately from `DATABASE_URL` for migrations
- [ ] PR environments enabled via Railway GitHub App
- [ ] `RAILWAY_TOKEN` stored in GitHub Actions secrets (not in code)
- [ ] Staging and production are separate Railway environments (not separate projects)
- [ ] User-uploaded files stored in R2/S3/GCS (not Railway volumes)
- [ ] Health check endpoint (`/health`) configured and responding correctly