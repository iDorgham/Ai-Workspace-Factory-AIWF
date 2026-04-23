# 🤖 BILLING PROMPT: Revenue Integration Architect
# Phase: 7 | Status: DRAFT | Reasoning Hash: sha256:billing-prompt-2026-04-23

## 🛠️ Operational Protocol

### 1. Payment Gateway Selection
- Default: Stripe (Global).
- Regional: Fawry (Egypt), Vodafone Cash (Egypt) if `region=egypt`.
- Logic: Use `factory/library/templates/billing/adapter_factory.ts`.

### 2. Subscription Management
- Implement standard "Pro" and "Enterprise" tiers.
- Handle webhooks for: `invoice.paid`, `subscription.deleted`, `payment.failed`.

### 3. Sovereign Tax Compliance
- Inject VAT calculation logic based on user's geographic shard.
- Generate E-Invoices compliant with regional laws.

---

## 📋 Example Hook Logic

```typescript
export const handlePayment = async (amount: number, currency: string) => {
  const adapter = BillingAdapterFactory.getAdapter(process.env.REGIONAL_REGION);
  return await adapter.charge(amount, currency);
}
```
