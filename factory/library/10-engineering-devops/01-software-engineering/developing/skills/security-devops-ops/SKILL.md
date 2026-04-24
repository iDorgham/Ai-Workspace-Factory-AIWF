---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Security & DevOps Operations

## Purpose

Implement production-grade security controls, CI/CD pipelines, observability, and deployment practices for Next.js/Node.js applications. Covers RBAC, data privacy, monitoring, system invariants, and GitHub Actions workflows — with exact configurations and MENA compliance context.

**Measurable Impact:**
- Before: Manual deployments → 1-2 outages/month, 30-minute rollback time
- After: CI/CD with automated checks → zero bad deploys, 2-minute rollback
- Before: Console.log debugging → issues discovered by users, hours to diagnose
- After: Structured logging + alerting → issues detected in <5 minutes, diagnosed in <15
- Before: Ad-hoc permissions → privilege escalation risks, compliance gaps
- After: RBAC with least-privilege → zero unauthorized access paths

**Consolidates:** `deploy`, `github-ci-cd`, `rbac`, `data-privacy`, `observability`, `system-invariants`

---

## Technique 1 — RBAC & Permission System

### Role-Based Access Control Architecture

```typescript
// lib/rbac.ts — Permission system
export const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',   // Platform owner (you)
  ORG_ADMIN: 'ORG_ADMIN',       // Organization administrator
  MANAGER: 'MANAGER',            // Department/team manager
  MEMBER: 'MEMBER',              // Regular employee
  VIEWER: 'VIEWER',              // Read-only access
  API_KEY: 'API_KEY',            // Machine/integration access
} as const;

type Role = keyof typeof ROLES;

// Permission definitions: resource.action
export const PERMISSIONS = {
  // Organization management
  'org.read': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER, ROLES.MEMBER, ROLES.VIEWER],
  'org.update': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN],
  'org.delete': [ROLES.SUPER_ADMIN],
  'org.billing': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN],
  
  // User management
  'users.list': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER],
  'users.invite': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER],
  'users.remove': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN],
  'users.changeRole': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN],
  
  // Data access
  'data.read': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER, ROLES.MEMBER, ROLES.VIEWER],
  'data.write': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER, ROLES.MEMBER],
  'data.delete': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN],
  'data.export': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER],
  
  // Reports
  'reports.view': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER, ROLES.VIEWER],
  'reports.create': [ROLES.SUPER_ADMIN, ROLES.ORG_ADMIN, ROLES.MANAGER],
} as const;

// Permission check function
export function hasPermission(userRole: Role, permission: keyof typeof PERMISSIONS): boolean {
  return PERMISSIONS[permission]?.includes(userRole) ?? false;
}

// Middleware-style permission guard for API routes
export function requirePermission(permission: keyof typeof PERMISSIONS) {
  return async (req: NextRequest) => {
    const session = await getSession(req);
    if (!session || !hasPermission(session.role as Role, permission)) {
      return NextResponse.json(
        { error: 'Forbidden', required: permission },
        { status: 403 }
      );
    }
    return null; // Allowed — continue to handler
  };
}

// React component guard
export function PermissionGate({
  permission, children, fallback = null
}: {
  permission: keyof typeof PERMISSIONS;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}) {
  const { role } = useSession();
  if (!hasPermission(role, permission)) return fallback;
  return children;
}
```

---

## Technique 2 — CI/CD Pipeline (GitHub Actions)

### Production Deployment Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '9'

jobs:
  quality:
    name: Quality Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with: { version: '${{ env.PNPM_VERSION }}' }
      - uses: actions/setup-node@v4
        with: { node-version: '${{ env.NODE_VERSION }}', cache: 'pnpm' }
      - run: pnpm install --frozen-lockfile
      
      # Type checking
      - run: pnpm tsc --noEmit
      
      # Linting
      - run: pnpm lint
      
      # Unit & integration tests
      - run: pnpm test --coverage
      
      # Build verification
      - run: pnpm build
      
      # Bundle size check (fail if > threshold)
      - name: Check bundle size
        run: |
          SIZE=$(du -sk .next/ | cut -f1)
          echo "Bundle size: ${SIZE}KB"
          if [ "$SIZE" -gt 10000 ]; then
            echo "::error::Bundle too large: ${SIZE}KB > 10MB"
            exit 1
          fi

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm audit --audit-level=high
      - name: Check for secrets
        run: |
          # Fail if any .env files are committed
          if git ls-files | grep -E '\.env$|\.env\.local$|\.env\.production$'; then
            echo "::error::Environment files found in repository!"
            exit 1
          fi

  deploy:
    name: Deploy
    needs: [quality, security]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Pre-commit Hooks

```json
// package.json — lint-staged + husky
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

---

## Technique 3 — Observability & Monitoring

### Structured Logging

```typescript
// lib/logger.ts — Structured JSON logging
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  level: LogLevel;
  message: string;
  correlationId?: string;
  userId?: string;
  orgId?: string;
  duration?: number;
  metadata?: Record<string, unknown>;
  timestamp: string;
}

export const logger = {
  info: (message: string, meta?: Partial<LogEntry>) => log('info', message, meta),
  warn: (message: string, meta?: Partial<LogEntry>) => log('warn', message, meta),
  error: (message: string, meta?: Partial<LogEntry>) => log('error', message, meta),
  debug: (message: string, meta?: Partial<LogEntry>) => log('debug', message, meta),
};

function log(level: LogLevel, message: string, meta?: Partial<LogEntry>) {
  const entry: LogEntry = {
    level,
    message,
    timestamp: new Date().toISOString(),
    ...meta,
  };
  
  // In production: send to log aggregator (Axiom, Datadog, etc.)
  // In dev: pretty-print to console
  if (process.env.NODE_ENV === 'production') {
    console.log(JSON.stringify(entry));
  } else {
    console.log(`[${level.toUpperCase()}] ${message}`, meta?.metadata || '');
  }
}

// Performance tracking wrapper
export async function withTiming<T>(
  label: string,
  fn: () => Promise<T>,
  ctx?: { correlationId: string }
): Promise<T> {
  const start = performance.now();
  try {
    const result = await fn();
    const duration = Math.round(performance.now() - start);
    logger.info(`${label} completed`, { duration, correlationId: ctx?.correlationId });
    return result;
  } catch (error) {
    const duration = Math.round(performance.now() - start);
    logger.error(`${label} failed`, { duration, correlationId: ctx?.correlationId, metadata: { error } });
    throw error;
  }
}
```

### Health Check Endpoint

```typescript
// app/api/health/route.ts — System health for monitoring
export async function GET() {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: process.env.VERCEL_GIT_COMMIT_SHA?.slice(0, 7) || 'local',
    timestamp: new Date().toISOString(),
  };
  
  const healthy = checks.database.ok && checks.redis.ok;
  
  return NextResponse.json(checks, { status: healthy ? 200 : 503 });
}

async function checkDatabase(): Promise<{ ok: boolean; latencyMs: number }> {
  const start = performance.now();
  try {
    await prisma.$queryRaw`SELECT 1`;
    return { ok: true, latencyMs: Math.round(performance.now() - start) };
  } catch {
    return { ok: false, latencyMs: Math.round(performance.now() - start) };
  }
}
```

---

## Technique 4 — Data Privacy & System Invariants

### Data Classification & Protection

```markdown
## Data Classification Rules

CRITICAL (encryption at rest + in transit, audit log every access):
  - Passwords (never stored — bcrypt hash only)
  - Payment card data (delegate to payment processor — never store)
  - National ID numbers (encrypted column, access logged)
  - API secrets and tokens

SENSITIVE (encrypted in transit, access controlled):
  - Email addresses, phone numbers
  - Physical addresses
  - Date of birth
  - Financial data (invoices, salaries)

INTERNAL (standard protection):
  - Usernames, display names
  - Organization names
  - Product usage data
  - Feature flags

PUBLIC (no protection needed):
  - Marketing content
  - Published prices
  - Public API documentation

## MENA Data Residency
  - UAE: PDPL requires personal data stored in UAE or adequate jurisdiction
  - Saudi: PDPL requires data residency notification to SDAIA
  - Egypt: Data Protection Law requires express consent for cross-border
  → Use region-pinned database (Supabase ME region, AWS me-south-1)
```

### System Invariants (Automated Guards)

```typescript
// scripts/check-invariants.ts — Run in CI + pre-deploy
const INVARIANTS = [
  {
    name: 'No secrets in source code',
    check: async () => {
      const result = await exec('grep -r "sk_live\\|sk_test\\|PRIVATE_KEY" src/ --include="*.ts" -l');
      return result.stdout.trim() === '';
    },
  },
  {
    name: 'All API routes have auth middleware',
    check: async () => {
      const routes = await glob('app/api/**/route.ts');
      for (const route of routes) {
        if (route.includes('/health') || route.includes('/webhooks')) continue;
        const content = await readFile(route, 'utf-8');
        if (!content.includes('getSession') && !content.includes('requirePermission')) {
          throw new Error(`${route} missing auth check`);
        }
      }
      return true;
    },
  },
  {
    name: 'No console.log in production code',
    check: async () => {
      const result = await exec('grep -r "console.log" src/ --include="*.ts" -l');
      return result.stdout.trim() === '';
    },
  },
  {
    name: 'Environment variables validated',
    check: async () => {
      // Ensure lib/env.ts exists and imports zod
      const content = await readFile('lib/env.ts', 'utf-8');
      return content.includes('z.object') && content.includes('.parse');
    },
  },
];
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| SEC-001 | Admin role with wildcard permissions | **HIGH** — No least-privilege | Define explicit permissions per role |
| SEC-002 | Auth check missing on new API route | **CRITICAL** — Open endpoint | Middleware catches all /api/* by default |
| SEC-003 | Console.log for production logging | **HIGH** — Unstructured, no aggregation | Structured JSON logger with correlation IDs |
| SEC-004 | No CI/CD — manual deployments | **HIGH** — Human error, no quality gates | GitHub Actions with lint + test + build + deploy |
| SEC-005 | Storing PII without classification | **HIGH** — MENA PDPL violation | Classify all data; encrypt CRITICAL/SENSITIVE |
| SEC-006 | No health check endpoint | **MEDIUM** — Can't monitor uptime | /api/health with DB + Redis checks |
| SEC-007 | Deploying without running tests | **CRITICAL** — Shipping broken code | CI blocks deploy unless tests pass |
| SEC-008 | RBAC checked client-side only | **CRITICAL** — Client bypass trivial | Server-side permission check mandatory |
| SEC-009 | Secrets in .env committed to git | **CRITICAL** — Credential leak | .env in .gitignore + pre-commit check |
| SEC-010 | No CORS configuration | **MEDIUM** — CSRF attacks possible | Explicit CORS headers in middleware |

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] RBAC permission system with ≥4 roles and per-action permissions
- [ ] PermissionGate component for UI-level access control
- [ ] CI/CD pipeline: lint → typecheck → test → build → security scan → deploy
- [ ] Pre-commit hooks with lint-staged running ESLint + Prettier
- [ ] Structured JSON logging with correlation IDs on all API routes
- [ ] Health check endpoint monitoring database + Redis latency
- [ ] Data classification applied to all PII fields (CRITICAL/SENSITIVE/INTERNAL)
- [ ] System invariants automated in CI (no secrets, auth on all routes)
- [ ] No console.log in production code (enforced by lint rule)
- [ ] MENA data residency requirements documented and enforced