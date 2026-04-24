---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Service Selection Guide

## How to Use This Guide

Run this guide at `/init` time or whenever adding a new service category.
@Architect and @Guide consult this before proposing any infrastructure.

Decision order:
1. Read the **project profile** (founder/pro mode, team size, scale target, deadline)
2. Apply the **decision tree** for each service category
3. Record decisions in `.ai/memory/decisions.md` with rationale
4. Check the **integration matrix** for conflicts

---

## Database Selection

```
START: What is your primary data model?

├── Relational data (users, bookings, orders, invoices)?
│   ├── Need database branching per PR? → NEON (serverless PostgreSQL + branching)
│   ├── Need Auth + RLS + Realtime built-in? → SUPABASE (PostgreSQL + full platform)
│   ├── Enterprise / self-hosted / complex migrations? → RDS (AWS) or Cloud SQL (GCP)
│   └── Cloudflare-only edge stack? → D1 (SQLite at edge)
│
├── Document / flexible schema (varied product types, content)?
│   ├── Google/Firebase ecosystem? → FIRESTORE
│   ├── Offline-first mobile? → FIRESTORE (offline sync built-in)
│   └── Complex queries needed? → Switch to Supabase/Neon (Firestore has limited querying)
│
├── Key-value / cache / session?
│   └── → UPSTASH REDIS (serverless, works in Edge + Node.js)
│
└── Analytics / reporting / data warehouse?
    └── → BIGQUERY (GCP) or store events in Postgres + query with Prisma
```

### Quick Reference: PostgreSQL Providers

| Need | Best Choice |
|------|------------|
| Simplest setup, Founder mode | Supabase (built-in auth + studio) |
| PR preview branches, CI isolation | Neon (database branching) |
| Railway PaaS project | Railway Postgres (managed, same platform) |
| AWS-native stack | RDS PostgreSQL |
| GCP-native stack | Cloud SQL or AlloyDB |
| Cloudflare Workers only | D1 (SQLite, no full PostgreSQL) |

---

## Auth Selection

```
START: Who are your users and how do they sign in?

├── Social login (Google/Apple/GitHub) is primary?
│   ├── Already using Supabase DB? → SUPABASE AUTH (built-in)
│   ├── Mobile app with push notifications? → FIREBASE AUTH + FCM
│   └── Need enterprise SSO (SAML/OIDC)? → AUTH0 or COGNITO
│
├── Email + password only?
│   ├── Using Supabase? → SUPABASE AUTH
│   ├── Using Firebase? → FIREBASE AUTH
│   └── Custom control needed? → BUILD CUSTOM (JWT + bcrypt + Prisma User model)
│
├── Multi-tenant SaaS (per-org auth)?
│   ├── Need org management UI? → CLERK
│   └── Custom tenant isolation? → SUPABASE AUTH + RLS policies per tenant
│
└── B2B / enterprise clients?
    └── → WORKOS (SSO, Directory Sync, SAML) or AUTH0 (enterprise)
```

---

## File Storage Selection

```
START: Who uploads files? From where? How are they served?

├── User-uploaded files (avatars, documents)?
│   ├── Already on Supabase? → SUPABASE STORAGE (simplest)
│   ├── Already on Firebase? → FIREBASE STORAGE
│   ├── Need zero egress fees? → CLOUDFLARE R2
│   ├── AWS-native stack? → AWS S3 + CLOUDFRONT
│   └── GCP-native stack? → GOOGLE CLOUD STORAGE + CDN
│
├── CMS media (blog images, marketing assets)?
│   ├── Using Sanity? → SANITY CDN (built-in)
│   ├── Using Contentful? → CONTENTFUL ASSETS (built-in)
│   └── Custom? → R2 or S3 + CDN
│
└── Large files (video, design files >1GB)?
    └── → R2 (no egress fees) or S3 with CloudFront
```

### Cost Comparison (Egress Fees)

| Provider | Egress Cost | Notes |
|---------|------------|-------|
| Cloudflare R2 | **$0** | Best for high-traffic assets |
| Supabase Storage | $0.09/GB | Included in plan up to limit |
| Firebase Storage | $0.12/GB | GCS-backed |
| AWS S3 | $0.09/GB | + CloudFront $0.0075–$0.02/GB |
| GCS | $0.08–$0.12/GB | Varies by region |

---

## Backend / Compute Selection

```
START: What kind of backend are you building?

├── API server (REST/GraphQL)?
│   ├── Need serverless / no DevOps? → VERCEL (Next.js API routes or Hono)
│   ├── Container-based / PaaS? → RAILWAY (simplest) or CLOUD RUN (scalable)
│   ├── Edge API (latency-critical)? → CLOUDFLARE WORKERS + HONO
│   └── AWS-native? → LAMBDA + API GATEWAY or ECS
│
├── Background jobs?
│   ├── HTTP-based queue (serverless)? → UPSTASH QSTASH
│   ├── At-edge queue? → CLOUDFLARE QUEUES
│   ├── AWS-native? → SQS + LAMBDA
│   ├── GCP-native? → CLOUD TASKS or PUB/SUB + CLOUD RUN
│   └── Firebase project? → CLOUD FUNCTIONS (Gen 2)
│
├── Scheduled tasks (cron)?
│   ├── Vercel project? → VERCEL CRONS (next.config)
│   ├── Railway project? → RAILWAY CRON SERVICE
│   ├── Cloudflare? → WORKERS CRON TRIGGERS
│   └── GCP? → CLOUD SCHEDULER → PUB/SUB → CLOUD RUN
│
└── Real-time (WebSockets, presence)?
    ├── Using Supabase? → SUPABASE REALTIME
    ├── Using Firebase? → FIREBASE REALTIME DB or FIRESTORE onSnapshot
    ├── Cloudflare? → DURABLE OBJECTS
    └── Custom? → UPSTASH (Pub/Sub) or Pusher
```

---

## Email Selection

```
START: What type of emails?

├── Transactional (confirmations, receipts, alerts)?
│   ├── High deliverability + analytics? → RESEND (developer-first, React Email)
│   ├── AWS-native stack? → AWS SES (cheapest at scale)
│   ├── GCP-native? → SENDGRID (GCP Marketplace) or MAILGUN
│   └── Firebase project? → FIREBASE EXTENSIONS (Trigger Email)
│
└── Marketing / newsletters?
    └── → LOOPS (developer-first) or MAILCHIMP / KLAVIYO
```

---

## CMS Selection

```
START: Who edits content? What type?

├── Non-technical editors need a UI?
│   ├── Structured content (blog, docs, landing pages)? → SANITY (flexible schema, embedded studio)
│   ├── Marketing team prefers Notion-like UX? → CONTENTFUL
│   └── Enterprise / compliance needs? → CONTENTFUL (SOC2, enterprise SLA)
│
├── Developer-controlled content (in-code)?
│   └── → Use i18n (t() keys) + .md files — no CMS needed
│
└── E-commerce product catalog?
    └── → SANITY (flexible) or SHOPIFY (if full e-commerce)
```

---

## Monitoring & Observability Selection

```
START: What do you need to observe?

├── Error tracking (exceptions, crashes)?
│   └── → SENTRY (best-in-class, Next.js native, session replay)
│
├── Performance monitoring (APM)?
│   └── → SENTRY PERFORMANCE (included) or DATADOG (enterprise)
│
├── Logs?
│   ├── Vercel project? → VERCEL LOG DRAINS → LOGFLARE or AXIOM
│   ├── Railway? → RAILWAY built-in logs + drain to AXIOM
│   └── AWS/GCP? → CLOUDWATCH / CLOUD LOGGING (native)
│
└── Analytics (user behavior)?
    ├── Simple? → VERCEL ANALYTICS or PLAUSIBLE (privacy-first)
    └── Advanced? → POSTHOG (open-source) or MIXPANEL
```

---

## Deployment Platform Selection

```
START: Team size? Technical level? Scale?

├── Founder / solo dev / MVP?
│   └── → VERCEL (Next.js) or RAILWAY (any stack) — zero DevOps
│
├── Small team / growing product?
│   ├── Next.js? → VERCEL (best Next.js support)
│   ├── Docker containers? → RAILWAY → CLOUD RUN (as team scales)
│   └── Need edge globally? → CLOUDFLARE PAGES + WORKERS
│
├── Enterprise / large team?
│   ├── AWS-native? → ECS FARGATE + RDS + CloudFront
│   └── GCP-native? → CLOUD RUN + Cloud SQL + Cloud CDN
│
└── Open-source / self-hosted?
    └── → COOLIFY (self-hosted Heroku) or KAMAL (Docker deploy)
```

---

## Integration Compatibility Matrix

| | Supabase | Neon | Firebase | Railway | Vercel | Cloudflare |
|--|--|--|--|--|--|--|
| Prisma | ✅ | ✅ | ❌ (NoSQL) | ✅ | ✅ | ✅ (D1 adapter) |
| Next.js | ✅ | ✅ | ✅ | ✅ | ✅ (native) | ✅ (Pages) |
| Hono | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (native) |
| Upstash | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sentry | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (Workers) |
| Edge runtime | ⚠️ (HTTP driver) | ✅ (HTTP driver) | ✅ | ❌ | ✅ | ✅ (native) |

---

## Decision Recording Template

When a service is chosen, log to `.ai/memory/decisions.md`:

```markdown
## [DATE] — [Service Category] Decision

**Chosen:** [Service Name]
**Alternatives considered:** [List]
**Rationale:** [Why this one — constraints, team, scale, cost]
**Trade-offs accepted:** [What we're giving up]
**Revisit trigger:** [When to reconsider — e.g., "when MAU > 50K" or "when team > 5 devs"]
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Stack Composition Examples

### Founder Mode — Fast MVP
```
DB:         Supabase (auth + db + storage in one)
Backend:    Next.js API routes on Vercel
Cache:      Upstash Redis
Email:      Resend + React Email
Errors:     Sentry
Deploy:     Vercel
```

### Pro Mode — Scalable Product
```
DB:         Neon (branching per PR) + Prisma
Auth:       Custom JWT or Clerk
Storage:    Cloudflare R2
Backend:    Hono on Cloudflare Workers
Queue:      Upstash QStash
Email:      AWS SES
Errors:     Sentry
Deploy:     Cloudflare Pages + Workers
```

### Enterprise Mode — Full Cloud
```
DB:         RDS PostgreSQL (AWS) or Cloud SQL (GCP)
Auth:       Cognito (AWS) or WorkOS (SAML/SSO)
Storage:    S3 + CloudFront (AWS) or GCS + CDN (GCP)
Backend:    ECS Fargate (AWS) or Cloud Run (GCP)
Queue:      SQS (AWS) or Pub/Sub (GCP)
Email:      AWS SES
Errors:     Sentry + Datadog
CMS:        Contentful (enterprise SLA)
Deploy:     GitHub Actions → ECR/GCR → ECS/Cloud Run
```