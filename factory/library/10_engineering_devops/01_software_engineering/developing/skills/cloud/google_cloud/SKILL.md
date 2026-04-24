---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Google Cloud Integration

## What GCP Provides in Sovereign

| Service | Sovereign Usage |
|---------|-----------|
| Cloud Storage (GCS) | Object storage — alternative to S3/R2 |
| Cloud Run | Serverless containers — scale to zero, auto-scale |
| BigQuery | Analytics warehouse — event data, reporting, ML |
| Secret Manager | Secure secrets (DB passwords, API keys) |
| Pub/Sub | Event streaming, background jobs, fan-out |
| Vertex AI | LLM APIs (Gemini), embeddings, ML model hosting |
| Google Maps | Location APIs (Places, Geocoding, Directions) |
| Cloud Tasks | Managed task queue (HTTP-based, like QStash) |
| Firebase (GCP-native) | Auth + Firestore (see firebase_integration.md) |
| Cloud SQL | Managed PostgreSQL/MySQL — Prisma-compatible |

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "@google-cloud/storage": "^7.15.0"
  "@google-cloud/pubsub": "^4.9.0"
  "@google-cloud/secret-manager": "^5.6.0"
  "@google-cloud/bigquery": "^8.0.0"
  "@google-cloud/tasks": "^5.5.0"
  "@googlemaps/google-maps-services-js": "^3.4.0"
  "@google/generative-ai": "^0.21.0"    # Gemini SDK
```

### Environment Variables
```bash
# .env.example
GOOGLE_CLOUD_PROJECT_ID=sovereign-production
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json  # local dev only
# Production: use Workload Identity (GKE/Cloud Run) — no key file needed

GCS_BUCKET_NAME=sovereign-uploads-prod
GOOGLE_MAPS_API_KEY=AIzaSy...
GEMINI_API_KEY=AIzaSy...
```

> **Production rule:** Use Workload Identity Federation on Cloud Run / GKE — no service account key files. Key files only in local dev.

---

## Cloud Storage (GCS)

### Client Setup
```typescript
// packages/shared/src/lib/gcp/storage.ts
import { Storage } from '@google-cloud/storage'

// Credentials auto-resolved: GOOGLE_APPLICATION_CREDENTIALS → Workload Identity
export const storage = new Storage({ projectId: process.env.GOOGLE_CLOUD_PROJECT_ID })
export const bucket  = storage.bucket(process.env.GCS_BUCKET_NAME!)
```

### Signed Upload URL (Direct Client Upload)
```typescript
export async function getUploadSignedUrl(filename: string, contentType: string) {
  const key = `uploads/${crypto.randomUUID()}-${filename}`
  const file = bucket.file(key)

  const [url] = await file.getSignedUrl({
    version: 'v4',
    action: 'write',
    expires: Date.now() + 5 * 60 * 1000,   // 5 minutes
    contentType,
  })

  return { url, key, publicUrl: `https://storage.googleapis.com/${process.env.GCS_BUCKET_NAME}/${key}` }
}
```

### Signed Download URL (Private Files)
```typescript
export async function getDownloadSignedUrl(key: string, expiresInSeconds = 3600) {
  const [url] = await bucket.file(key).getSignedUrl({
    version: 'v4',
    action: 'read',
    expires: Date.now() + expiresInSeconds * 1000,
  })
  return url
}
```

---

## Secret Manager — Production Secrets

```typescript
// packages/shared/src/lib/gcp/secrets.ts
import { SecretManagerServiceClient } from '@google-cloud/secret-manager'

const client = new SecretManagerServiceClient()
const secretCache = new Map<string, string>()

export async function getSecret(secretName: string, version = 'latest'): Promise<string> {
  const cacheKey = `${secretName}@${version}`
  if (secretCache.has(cacheKey)) return secretCache.get(cacheKey)!

  const name = `projects/${process.env.GOOGLE_CLOUD_PROJECT_ID}/secrets/${secretName}/versions/${version}`
  const [accessResponse] = await client.accessSecretVersion({ name })
  const value = accessResponse.payload!.data!.toString()

  secretCache.set(cacheKey, value)
  return value
}

// Usage
const databaseUrl = await getSecret('DATABASE_URL')
const apiKey      = await getSecret('STRIPE_SECRET_KEY')
```

---

## Pub/Sub — Event Streaming

### Publisher
```typescript
// packages/shared/src/lib/gcp/pubsub.ts
import { PubSub } from '@google-cloud/pubsub'

export const pubsub = new PubSub({ projectId: process.env.GOOGLE_CLOUD_PROJECT_ID })

export async function publishEvent<T>(topicName: string, payload: T, attributes?: Record<string, string>) {
  const topic = pubsub.topic(topicName)
  const data = Buffer.from(JSON.stringify(payload))
  const messageId = await topic.publishMessage({ data, attributes })
  return messageId
}

// Usage
await publishEvent('booking-events', {
  type: 'booking.confirmed',
  bookingId: booking.id,
  userId: booking.userId,
}, { eventVersion: '1.0' })
```

### Subscriber (Cloud Run endpoint)
```typescript
// apps/api/src/routes/pubsub/booking-events.ts
import { BookingEventSchema } from '@workspace/shared/contracts/events'

export async function POST(req: Request) {
  const body = await req.json()

  // Pub/Sub wraps message in base64
  const data = JSON.parse(Buffer.from(body.message.data, 'base64').toString())
  const event = BookingEventSchema.parse(data)  // always validate

  switch (event.type) {
    case 'booking.confirmed':
      await handleBookingConfirmed(event)
      break
  }

  return new Response(null, { status: 204 })  // 204 = ack, 4xx/5xx = retry
}
```

---

## BigQuery — Analytics

```typescript
// packages/shared/src/lib/gcp/bigquery.ts
import { BigQuery } from '@google-cloud/bigquery'

export const bigquery = new BigQuery({ projectId: process.env.GOOGLE_CLOUD_PROJECT_ID })

// Track an event (append-only, insert-then-forget pattern)
export async function trackEvent(dataset: string, table: string, event: Record<string, unknown>) {
  await bigquery
    .dataset(dataset)
    .table(table)
    .insert([{ ...event, _timestamp: new Date().toISOString() }])
}

// Run analytics query
export async function runQuery<T>(sql: string, params?: unknown[]): Promise<T[]> {
  const [rows] = await bigquery.query({
    query: sql,
    params,
    location: 'US',
  })
  return rows as T[]
}

// Example: daily booking revenue
const revenue = await runQuery<{ date: string; total: number }>(`
  SELECT
    DATE(created_at) AS date,
    SUM(total_price) / 100 AS total
  FROM \`sovereign.bookings\`
  WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY date
  ORDER BY date DESC
`)
```

---

## Cloud Run — Container Deployment

### Dockerfile (Next.js + Cloud Run)
```dockerfile
FROM node:24-alpine AS base
RUN corepack enable pnpm

FROM base AS deps
WORKDIR /app
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=8080

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 8080
CMD ["node", "server.js"]
```

### Deploy to Cloud Run
```bash
# Build and push to Google Artifact Registry
gcloud builds submit --tag us-central1-docker.pkg.dev/PROJECT_ID/sovereign/api:latest

# Deploy
gcloud run deploy sovereign-api \
  --image us-central1-docker.pkg.dev/PROJECT_ID/sovereign/api:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --min-instances 0 \
  --max-instances 10 \
  --set-secrets DATABASE_URL=DATABASE_URL:latest \  # pull from Secret Manager
  --service-account sovereign-api@PROJECT_ID.iam.gserviceaccount.com
```

---

## Google Maps

```typescript
// packages/shared/src/lib/gcp/maps.ts
import { Client } from '@googlemaps/google-maps-services-js'

const maps = new Client()

export async function geocodeAddress(address: string) {
  const response = await maps.geocode({
    params: { address, key: process.env.GOOGLE_MAPS_API_KEY! },
  })
  const result = response.data.results[0]
  if (!result) throw new Error(`No results for address: ${address}`)

  return {
    lat: result.geometry.location.lat,
    lng: result.geometry.location.lng,
    formattedAddress: result.formatted_address,
  }
}
```

---

## Vertex AI / Gemini

```typescript
// packages/shared/src/lib/gcp/gemini.ts
import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!)
const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' })

export async function generateText(prompt: string) {
  const result = await model.generateContent(prompt)
  return result.response.text()
}
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[GCP-001]** Committing service account key JSON files — use Workload Identity in Cloud Run/GKE, GOOGLE_APPLICATION_CREDENTIALS only in local dev
- **[GCP-002]** BigQuery streaming inserts without error handling — insertErrors are returned in response, not thrown
- **[GCP-003]** Pub/Sub subscriber returning 200 on processing error — return 4xx/5xx to trigger retry; return 204 only on success
- **[GCP-004]** Cloud Run without `--service-account` flag — defaults to Compute Engine SA which has broad permissions
- **[GCP-005]** Hardcoding `GOOGLE_MAPS_API_KEY` without API restrictions — restrict key to specific APIs and IP/referrer
- **[GCP-006]** Secret Manager without version caching — each call is billed; cache in memory per process lifetime
- **[GCP-007]** GCS without lifecycle rules — old uploads accumulate indefinitely; add storage class transitions and expiry

## Success Criteria
- [ ] No service account JSON keys in repo — Workload Identity used on Cloud Run/GKE
- [ ] All secrets fetched from Secret Manager (not env vars in Cloud Run deployment)
- [ ] Pub/Sub subscribers return 204 on success, 4xx/5xx on failure (for retry)
- [ ] BigQuery inserts handle `insertErrors` array in response
- [ ] Cloud Run deployed with minimal-permission service account
- [ ] Google Maps API key restricted to specific APIs and referrers
- [ ] Secret Manager values cached in-process (not fetched per request)