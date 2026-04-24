# AWS Services Integration

## What AWS Provides in Sovereign

| Service | Sovereign Usage |
|---------|-----------|
| S3 | File/image storage with presigned URLs — production-grade object storage |
| SES | Transactional email (confirmations, notifications, alerts) |
| CloudFront | CDN for S3 assets, Next.js ISR cache, API acceleration |
| Cognito | User pools (managed auth) — alternative to custom JWT |
| Lambda | Serverless functions (background jobs, event processors) |
| RDS (PostgreSQL) | Managed relational database — Prisma-compatible |
| Secrets Manager | Secure secrets storage (replaces .env in production) |
| SQS | Message queue for decoupled background processing |
| SNS | Pub/sub notifications, mobile push, fan-out events |
| EventBridge | Event routing, scheduled tasks (cron replacement) |

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "@aws-sdk/client-s3": "^3.750.0"
  "@aws-sdk/s3-request-presigner": "^3.750.0"
  "@aws-sdk/client-ses": "^3.750.0"
  "@aws-sdk/client-sqs": "^3.750.0"
  "@aws-sdk/client-secrets-manager": "^3.750.0"
  "@aws-sdk/client-sns": "^3.750.0"
```

### Environment Variables
```bash
# .env.example
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...           # use IAM role in production — never hardcode
AWS_SECRET_ACCESS_KEY=...           # use IAM role in production — never hardcode
AWS_S3_BUCKET=sovereign-uploads-prod
AWS_SES_FROM_EMAIL=noreply@yourdomain.com
AWS_CLOUDFRONT_DOMAIN=d1234.cloudfront.net
```

> **Production rule:** Never use static IAM credentials in production. Use IAM roles (ECS task role, Lambda execution role, EC2 instance profile). Static keys only in local dev.

---

## S3 — Object Storage

### Client Setup (Singleton)
```typescript
// packages/shared/src/lib/aws/s3.ts
import { S3Client } from '@aws-sdk/client-s3'

export const s3 = new S3Client({
  region: process.env.AWS_REGION!,
  // Credentials auto-resolved: env vars → IAM role → instance profile
  // Never pass credentials explicitly in production
})
```

### Presigned Upload URL (Client-Direct Upload)
```typescript
import { PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'
import { s3 } from './s3'

// Generate a presigned PUT URL — client uploads directly to S3 (no proxy through your API)
export async function getUploadUrl(key: string, contentType: string, expiresIn = 300) {
  const command = new PutObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET!,
    Key: key,
    ContentType: contentType,
  })
  return getSignedUrl(s3, command, { expiresIn })
}

// API route — client requests upload URL, then uploads directly
// POST /api/uploads/presign
export async function POST(req: Request) {
  const { filename, contentType } = await req.json()
  const key = `uploads/${crypto.randomUUID()}-${filename}`
  const uploadUrl = await getUploadUrl(key, contentType)
  const publicUrl = `https://${process.env.AWS_CLOUDFRONT_DOMAIN}/${key}`
  return Response.json({ uploadUrl, publicUrl, key })
}
```

### Presigned Download URL (Private Files)
```typescript
import { GetObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

export async function getDownloadUrl(key: string, expiresIn = 3600) {
  const command = new GetObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET!,
    Key: key,
  })
  return getSignedUrl(s3, command, { expiresIn })
}
```

### Delete Object
```typescript
import { DeleteObjectCommand } from '@aws-sdk/client-s3'

export async function deleteFile(key: string) {
  await s3.send(new DeleteObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET!,
    Key: key,
  }))
}
```

---

## SES — Transactional Email

```typescript
// packages/shared/src/lib/aws/ses.ts
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses'

export const ses = new SESClient({ region: process.env.AWS_REGION! })

export interface EmailOptions {
  to: string | string[]
  subject: string
  html: string
  text: string        // always include plain-text fallback
  replyTo?: string
}

export async function sendEmail(options: EmailOptions) {
  const toAddresses = Array.isArray(options.to) ? options.to : [options.to]

  await ses.send(new SendEmailCommand({
    Source: process.env.AWS_SES_FROM_EMAIL!,
    Destination: { ToAddresses: toAddresses },
    ReplyToAddresses: options.replyTo ? [options.replyTo] : undefined,
    Message: {
      Subject: { Data: options.subject, Charset: 'UTF-8' },
      Body: {
        Html: { Data: options.html, Charset: 'UTF-8' },
        Text: { Data: options.text, Charset: 'UTF-8' },
      },
    },
  }))
}
```

### With React Email (Recommended)
```typescript
import { render } from '@react-email/render'
import { BookingConfirmationEmail } from '@workspace/shared/emails/booking-confirmation'

const html = render(<BookingConfirmationEmail booking={booking} />)
const text = render(<BookingConfirmationEmail booking={booking} />, { plainText: true })

await sendEmail({
  to: booking.guest.email,
  subject: t('email.booking.confirmation.subject'),
  html,
  text,
})
```

---

## SQS — Message Queue

```typescript
// packages/shared/src/lib/aws/sqs.ts
import { SQSClient, SendMessageCommand, ReceiveMessageCommand, DeleteMessageCommand } from '@aws-sdk/client-sqs'

export const sqs = new SQSClient({ region: process.env.AWS_REGION! })

export async function enqueueJob<T>(queueUrl: string, payload: T, delaySeconds = 0) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: queueUrl,
    MessageBody: JSON.stringify(payload),
    DelaySeconds: delaySeconds,
    MessageGroupId: 'default',           // required for FIFO queues
    MessageDeduplicationId: crypto.randomUUID(),  // idempotency key
  }))
}
```

---

## Secrets Manager — Production Secrets

```typescript
// packages/shared/src/lib/aws/secrets.ts
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager'

const client = new SecretsManagerClient({ region: process.env.AWS_REGION! })

// Cache secrets in memory for the Lambda/container lifetime
const secretCache = new Map<string, unknown>()

export async function getSecret<T>(secretName: string): Promise<T> {
  if (secretCache.has(secretName)) return secretCache.get(secretName) as T

  const response = await client.send(new GetSecretValueCommand({ SecretId: secretName }))
  const value = JSON.parse(response.SecretString!) as T
  secretCache.set(secretName, value)
  return value
}

// Usage
const dbConfig = await getSecret<{ url: string; password: string }>('sovereign/production/database')
```

---

## CloudFront — CDN Setup

### S3 + CloudFront (Infrastructure as Code — CDK)
```typescript
// infrastructure/lib/storage-stack.ts (AWS CDK)
import * as s3 from 'aws-cdk-lib/aws-s3'
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront'
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins'

const bucket = new s3.Bucket(this, 'UploadsBucket', {
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,   // always block direct public access
  encryption: s3.BucketEncryption.S3_MANAGED,
  versioned: true,
})

const distribution = new cloudfront.Distribution(this, 'CDN', {
  defaultBehavior: {
    origin: origins.S3BucketOrigin.withOriginAccessControl(bucket),
    cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
  },
})
```

---

## Cognito — Managed Auth (Optional)

```typescript
// packages/shared/src/lib/aws/cognito.ts
import {
  CognitoIdentityProviderClient,
  InitiateAuthCommand,
  SignUpCommand,
  ConfirmSignUpCommand,
} from '@aws-sdk/client-cognito-identity-provider'

const cognito = new CognitoIdentityProviderClient({ region: process.env.AWS_REGION! })

export async function signUp(email: string, password: string) {
  await cognito.send(new SignUpCommand({
    ClientId: process.env.COGNITO_CLIENT_ID!,
    Username: email,
    Password: password,
    UserAttributes: [{ Name: 'email', Value: email }],
  }))
}

export async function signIn(email: string, password: string) {
  const result = await cognito.send(new InitiateAuthCommand({
    AuthFlow: 'USER_PASSWORD_AUTH',
    ClientId: process.env.COGNITO_CLIENT_ID!,
    AuthParameters: { USERNAME: email, PASSWORD: password },
  }))
  return result.AuthenticationResult   // contains AccessToken, IdToken, RefreshToken
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

- **[AWS-001]** Hardcoding AWS credentials in code or committing to git — use IAM roles in production, env vars only in local dev
- **[AWS-002]** Making S3 bucket fully public — always use presigned URLs or CloudFront signed URLs for private assets
- **[AWS-003]** Using S3 as a static file server directly — always put CloudFront in front for CDN caching and HTTPS
- **[AWS-004]** SES in sandbox mode in production — verify domain + request production access before launch
- **[AWS-005]** Not setting S3 bucket versioning — no recovery path if files are accidentally overwritten or deleted
- **[AWS-006]** Creating new `S3Client` / `SESClient` per request in Lambda — instantiate outside the handler for connection reuse
- **[AWS-007]** SQS standard queue for order-sensitive jobs — use FIFO queues when message order matters
- **[AWS-008]** Secrets in environment variables in Lambda — use Secrets Manager with in-memory caching

## Success Criteria
- [ ] No AWS credentials in code or committed .env files
- [ ] S3 bucket blocks all public access — assets served via CloudFront
- [ ] Presigned URLs used for all direct client uploads/downloads
- [ ] SES domain verified + production access enabled before launch
- [ ] AWS SDK clients instantiated once (outside Lambda handler / at module level)
- [ ] Secrets fetched from Secrets Manager with in-memory cache
- [ ] SQS FIFO queue used where message ordering matters
- [ ] IAM roles follow least-privilege principle