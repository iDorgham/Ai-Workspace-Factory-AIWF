---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Legal Review & Compliance

## Purpose
Validate AI-generated assets, marketing copy, and brand elements for trademark, copyright, and regulatory compliance. Prevents legal risks before public release.

## When to Activate
- AI-generated logos, images, or brand assets
- Marketing copy or public-facing content
- Trademark usage verification
- GDPR/regional compliance checks
- User-generated content moderation

## Step-by-Step Execution

### 1. Trademark Verification

**Check Brand Names & Logos:**
```typescript
// apps/api/src/services/legal/trademark-check.ts
import { type BrandConfig } from '@sovereign/contracts/brand'

export async function checkTrademark(brandName: string): Promise<TrademarkResult> {
  // Check against trademark databases (via API)
  const response = await fetch('https://api.trademark-db.com/search', {
    method: 'POST',
    body: JSON.stringify({ query: brandName, jurisdiction: 'US' })
  })
  
  const results = await response.json()
  
  return {
    brandName,
    conflicts: results.conflicts,
    riskLevel: assessRisk(results.conflicts),
    recommendation: generateRecommendation(results.conflicts),
  }
}

function assessRisk(conflicts: TrademarkConflict[]): RiskLevel {
  if (conflicts.some(c => c.status === 'registered' && c.similarity > 0.85)) {
    return 'critical'
  }
  if (conflicts.some(c => c.similarity > 0.70)) {
    return 'high'
  }
  return 'low'
}
```

**Automated Scans:**
- Brand name against USPTO, EUIPO, WIPO databases
- Logo similarity search against registered trademarks
- Domain name availability check
- Social media handle availability

### 2. Copyright Verification for AI Assets

**AI-Generated Image Review:**
```markdown
## AI Asset Copyright Checklist

### Image Generation Prompts
- [ ] Prompt does not reference copyrighted characters (Disney, Marvel, etc.)
- [ ] Prompt does not request reproduction of specific artwork
- [ ] Prompt does not include trademarked brand names as subjects
- [ ] Style references are generic ("impressionist", "art deco") not artist-specific

### Output Validation
- [ ] Image does not contain recognizable trademarked logos
- [ ] Image does not depict trademarked products (Coca-Cola bottles, etc.)
- [ ] Image does not include copyrighted text or signage
- [ ] Image does not reproduce recognizable copyrighted artwork

### Licensing Compliance
- [ ] AI model license allows commercial use
- [ ] Generated assets comply with model provider's terms of service
- [ ] No restrictions on generated content usage
```

**AI Text Content Review:**
```markdown
## AI-Generated Copy Compliance

### Copyright Checks
- [ ] Does not reproduce copyrighted quotes or passages
- [ ] Does not reproduce song lyrics, poems, or published works
- [ ] Does not reproduce content from specific websites/sources

### Trademark Checks
- [ ] Does not use trademarked terms without proper attribution (™ or ®)
- [ ] Does not imply endorsement by brands or celebrities
- [ ] Does not use competitor brand names in comparisons

### Regulatory Compliance
- [ ] Health claims are substantiated (no false medical claims)
- [ ] Financial claims include required disclaimers
- [ ] Age-restricted content has appropriate warnings
- [ ] Accessibility statements present (if required)
```

### 3. GDPR Compliance Checks

**Data Privacy Review:**
```typescript
// apps/api/src/middleware/gdpr-compliance.ts
import { type UserConsent } from '@sovereign/contracts/user'

export const gdprMiddleware = async (c: Context, next: Next) => {
  // Check consent before processing
  const consent = await getUserConsent(c.req.cookie('session_id'))
  
  if (!consent.dataProcessing) {
    return c.json({ 
      error: 'CONSENT_REQUIRED',
      message: 'Data processing requires explicit consent',
      consentUrl: '/privacy/consent'
    }, 403)
  }
  
  // Ensure data residency
  if (consent.region === 'EU' && !isEUDataCenter()) {
    return c.json({ 
      error: 'DATA_RESIDENCY_VIOLATION',
      message: 'EU data must remain in EU data centers'
    }, 400)
  }
  
  await next()
}
```

**GDPR Compliance Checklist:**
- [ ] Explicit consent collected before data processing
- [ ] Right to access: Users can request their data
- [ ] Right to deletion: Users can request data removal
- [ ] Right to portability: Data exportable in standard format
- [ ] Data minimization: Only necessary data collected
- [ ] Purpose limitation: Data used only for stated purposes
- [ ] Storage limitation: Data retained only as long as necessary
- [ ] Data residency: EU data stays in EU data centers

### 4. Content Moderation

**User-Generated Content Review:**
```typescript
// apps/api/src/services/content-moderation.ts
import { type ModerationResult } from '@sovereign/contracts/moderation'

export async function moderateContent(content: string): Promise<ModerationResult> {
  const checks = await Promise.all([
    checkHateSpeech(content),
    checkHarassment(content),
    checkSpam(content),
    checkPIILeak(content),
    checkCopyrightContent(content),
  ])
  
  const violations = checks.filter(c => c.violated)
  
  return {
    passed: violations.length === 0,
    violations: violations.map(v => ({
      type: v.type,
      severity: v.severity,
      message: v.message,
      suggestion: v.suggestion,
    })),
  }
}
```

**Moderation Categories:**
| Category | Detection Method | Action |
|----------|------------------|--------|
| Hate speech | AI classifier + keyword matching | Block + flag |
| Harassment | Context analysis + pattern matching | Block + warn |
| Spam | Rate limiting + pattern detection | Throttle + flag |
| PII leak | Regex patterns (email, phone, SSN) | Redact + warn |
| Copyright | Similarity matching | Flag for review |

### 5. License Compliance

**Dependency License Scan:**
```bash
# Scan all dependencies for license compatibility
pnpm licenses list --json > .tmp/licenses.json

# Check against allowed licenses
const ALLOWED_LICENSES = [
  'MIT',
  'Apache-2.0',
  'BSD-2-Clause',
  'BSD-3-Clause',
  'ISC',
  '0BSD',
]

const violations = dependencies.filter(
  dep => !ALLOWED_LICENSES.includes(dep.license)
)
```

**License Risk Matrix:**
| License | Commercial Use | Modification | Distribution | Risk Level |
|---------|----------------|--------------|--------------|---------
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| MIT | ✅ | ✅ | ✅ | Low |
| Apache-2.0 | ✅ | ✅ | ✅ | Low |
| GPL-3.0 | ✅ | ✅ | ⚠️ Must open-source | High |
| AGPL-3.0 | ✅ | ✅ | ⚠️ Network use triggers | Critical |
| Proprietary | ⚠️ Check terms | ❌ | ❌ | Critical |

## Common Mistakes
- Not checking AI outputs for trademarked content
- Assuming "AI-generated" means "copyright-free"
- Collecting user data without explicit consent
- Not providing data deletion mechanism
- Using GPL/AGPL dependencies in proprietary software
- Not verifying image model commercial usage rights

## Success Criteria
- [ ] Trademark search completed for brand name
- [ ] AI-generated assets reviewed for copyrighted content
- [ ] GDPR consent mechanism implemented
- [ ] Data deletion pathway available
- [ ] All dependency licenses compatible with project license
- [ ] Content moderation active for user-generated content
- [ ] No critical/high legal findings
- [ ] Legal review documented and archived