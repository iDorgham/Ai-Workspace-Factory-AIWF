---
name: cloudflare-email-service
description: Send and receive transactional emails with Cloudflare Email Service (Email Sending + Email Routing). Use when building email sending (Workers binding or REST API), email routing, Agents SDK email handling, or integrating email into any app — Workers, Node.js, Python, Go, etc. Also use for email deliverability, SPF/DKIM/DMARC, wrangler email setup, MCP email tools, or when a coding agent needs to send emails.
---

# Cloudflare Email Service

Your knowledge of the Cloudflare Email Service may be outdated. **Prefer retrieval over pre-training** for any Email Service task.

## FIRST: Check Prerequisites

1. **Domain onboarded?** Run `npx wrangler email sending list`
2. **Binding configured?** Look for `send_email` in `wrangler.jsonc`

## Quick Start — Workers Binding

```jsonc
// wrangler.jsonc
{ "send_email": [{ "name": "EMAIL" }] }
```

```typescript
const response = await env.EMAIL.send({
  to: "user@example.com",
  from: { email: "welcome@yourdomain.com", name: "My App" },
  subject: "Welcome!",
  html: "<h1>Welcome!</h1>",
  text: "Welcome!",
});
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `send_email` binding | Add `"send_email": [{ "name": "EMAIL" }]` to wrangler.jsonc |
| Sending from unverified domain | Run `wrangler email sending enable yourdomain.com` |
| Missing `text` field | Always include both `html` and `text` versions |
| Using `email` key in REST API `from` | REST API uses `address` not `email` |
