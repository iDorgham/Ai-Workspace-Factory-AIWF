# Health Data Privacy & MENA Healthcare Compliance

## Purpose

Implement healthcare-grade data protection for digital health platforms operating in MENA markets. This skill provides concrete patterns for PHI handling, FHIR API integration, consent management, and compliance with MOHAP (UAE), SFDA (Saudi), and Egypt MOH regulations — with exact code, audit checklists, and anti-pattern catalogs.

**Measurable Impact:**
- Before: PHI exposure in logs/URLs → data breach, regulatory fine up to AED 10M (MOHAP)
- After: Zero PHI in application layer — tokenized references only → clean audit
- Before: Ad-hoc consent management → patient complaints, license revocation risk
- After: Granular consent ledger with audit trail → full DHA/MOHAP compliance
- Token savings: Structured health data patterns eliminate 50% of compliance rework

---

## Technique 1 — PHI Data Classification & Handling

### MENA PHI Classification Framework

```markdown
## PHI Classification Levels

### Level 1 — Direct Identifiers (NEVER in application layer)
- Patient full name (Arabic + English)
- Emirates ID / Saudi Iqama / Egyptian National ID
- Medical Record Number (MRN)
- Phone number, email address
- Physical address
- Photographs (facial)
- Biometric data (fingerprints, retinal scans)

### Level 2 — Sensitive Clinical Data (Encrypted, access-controlled)
- Diagnosis codes (ICD-10/ICD-11)
- Lab results and imaging reports
- Medication history
- Surgical records
- Mental health records (additional protections in UAE)
- Genetic/genomic data
- Substance abuse treatment records

### Level 3 — Operational Health Data (Standard protection)
- Appointment schedules (de-identified)
- Aggregate statistics
- Anonymized research data
- Facility operational metrics
```

### Data Handling Patterns

```typescript
// ✅ CORRECT: Tokenized PHI references
interface PatientContext {
  // Application layer uses opaque tokens, NEVER real identifiers
  patientToken: string;          // UUID mapped to MRN in secure vault
  sessionId: string;             // Ephemeral session reference
  consentScope: ConsentScope[];  // What data this session can access
  accessLevel: 'read' | 'write' | 'emergency';
  practitionerToken: string;     // Provider identity token
}

// ❌ ANTI-PATTERN: Direct PHI in application objects
interface NEVER_DO_THIS {
  patientName: string;     // PHI in memory
  emiratesId: string;      // Direct identifier
  diagnosis: string;       // Clinical data unprotected
  mrn: string;             // Medical Record Number exposed
}

// PHI Vault Service — separates identifiers from clinical data
export class PHIVaultService {
  /**
   * Store PHI in encrypted vault, return opaque token
   * Vault uses AES-256-GCM with HSM-managed keys
   * Key rotation: every 90 days (MOHAP requirement)
   */
  async tokenize(phi: DirectIdentifier): Promise<string> {
    const token = crypto.randomUUID();
    await this.vault.store({
      token,
      data: await this.encrypt(phi),
      classification: 'level-1',
      createdAt: new Date().toISOString(),
      expiresAt: this.calculateRetention(phi.type), // Country-specific
      facility: phi.facilityId,
    });
    
    await this.auditLog.record({
      action: 'phi.tokenized',
      token, // Log token, NEVER the PHI itself
      actor: this.currentPractitioner,
      timestamp: new Date().toISOString(),
    });
    
    return token;
  }
  
  /**
   * Resolve token to PHI — requires valid consent + access level
   */
  async resolve(
    token: string, 
    consent: ConsentRecord, 
    purpose: AccessPurpose
  ): Promise<DirectIdentifier> {
    // Verify consent covers this access
    if (!this.validateConsent(consent, purpose)) {
      await this.auditLog.record({
        action: 'phi.access_denied',
        reason: 'insufficient_consent',
        token,
        requestedPurpose: purpose,
      });
      throw new PHIAccessDenied('Consent does not cover this access purpose');
    }
    
    const encrypted = await this.vault.retrieve(token);
    const phi = await this.decrypt(encrypted.data);
    
    await this.auditLog.record({
      action: 'phi.accessed',
      token,
      purpose,
      actor: this.currentPractitioner,
      timestamp: new Date().toISOString(),
    });
    
    return phi;
  }
  
  /**
   * Data retention periods by jurisdiction
   */
  private calculateRetention(type: string): Date {
    const retentionYears: Record<string, number> = {
      // UAE (MOHAP): Medical records retained for 25 years
      'uae-medical-record': 25,
      // Saudi (MOH): 10 years after last visit
      'ksa-medical-record': 10,
      // Egypt (MOH): 15 years
      'egy-medical-record': 15,
      // Pediatric records: until patient reaches 25 years old + retention
      'pediatric': 30,
    };
    const years = retentionYears[type] ?? 10;
    return new Date(Date.now() + years * 365.25 * 24 * 60 * 60 * 1000);
  }
}
```

---

## Technique 2 — FHIR API Integration (HL7 R4)

### FHIR Resource Patterns for MENA

```typescript
// FHIR R4 Patient resource with MENA extensions
interface FHIRPatientMENA {
  resourceType: 'Patient';
  id: string; // Server-assigned, NOT the MRN
  
  identifier: [
    {
      system: 'urn:oid:2.16.840.1.113883.4.56'; // UAE Emirates ID
      value: string; // Encrypted reference, not raw ID
      period: { start: string; end: string };
    },
    {
      system: 'http://mohap.gov.ae/mrn';
      value: string; // Facility MRN
    }
  ];
  
  name: [
    {
      use: 'official';
      family: string;
      given: string[];
      text: string; // Full name in Arabic
      extension: [{
        url: 'http://hl7.org/fhir/StructureDefinition/language',
        valueCode: 'ar'; // Arabic name
      }];
    },
    {
      use: 'official';
      family: string;
      given: string[];
      text: string; // Full name in English
      extension: [{
        url: 'http://hl7.org/fhir/StructureDefinition/language',
        valueCode: 'en';
      }];
    }
  ];
  
  // MENA-specific: Nabidh (UAE national health platform) integration
  extension: [{
    url: 'http://nabidh.ae/fhir/StructureDefinition/nabidh-id',
    valueString: string; // Nabidh unified patient identifier
  }];
}

// FHIR API security headers
const fhirHeaders = {
  'Content-Type': 'application/fhir+json',
  'Authorization': `Bearer ${accessToken}`,
  'X-Request-ID': crypto.randomUUID(),       // Correlation ID
  'X-Consent-Reference': consentId,          // Required: consent proof
  'X-Purpose-Of-Use': 'TREATMENT',           // From HL7 PurposeOfUse
  'X-Facility-ID': facilityId,               // DHA/MOHAP facility code
  'Accept-Language': 'ar-AE, en-US',         // Bilingual response
};
```

### Nabidh Integration (UAE National Health Platform)

```markdown
## Nabidh Connectivity Requirements (UAE)
- All DHA-licensed facilities MUST integrate with Nabidh
- Data exchange: HL7 FHIR R4 (preferred) or HL7 v2.x messages
- Required transactions: ADT (Admit/Discharge/Transfer), Lab, Radiology, Pharmacy
- Patient matching: Emirates ID-based unified patient index
- Consent: Opt-out model (patients can restrict access)
- Security: TLS 1.3, mTLS for facility-to-Nabidh connections
- Uptime SLA: 99.9% availability for critical transactions
- Test environment: sandbox.nabidh.ae for integration testing
```

---

## Technique 3 — Consent Management System

### Granular Consent Ledger

```typescript
// Consent record structure (immutable audit trail)
interface ConsentRecord {
  consentId: string;
  patientToken: string;       // Tokenized patient reference
  
  // Granular consent categories (MOHAP/DHA requirements)
  scope: {
    treatment: boolean;       // Access for treatment purposes
    payment: boolean;         // Insurance/billing access
    research: boolean;        // De-identified research use
    publicHealth: boolean;    // Mandatory reporting (communicable diseases)
    marketing: boolean;       // Health promotion (explicit opt-in only)
    crossBorder: boolean;     // Data sharing outside UAE/KSA
    geneticData: boolean;     // Special consent for genomic data
    mentalHealth: boolean;    // Additional protections
  };
  
  // Consent metadata
  grantedAt: string;          // ISO 8601
  expiresAt: string;          // Default: 2 years (UAE), renewable
  grantedBy: 'patient' | 'guardian' | 'legal_representative';
  guardianId?: string;        // For minors (< 18 UAE, < 18 KSA)
  
  // Consent method
  method: 'digital_signature' | 'biometric' | 'witnessed_paper';
  language: 'ar' | 'en' | 'ar-en'; // Bilingual consent forms
  
  // Withdrawal tracking
  withdrawnAt?: string;
  withdrawalReason?: string;
  
  // Immutability: consent records are append-only
  // Previous versions retained for audit trail
  previousVersions: string[]; // Array of previous consentIds
}

// Emergency access override (Break-the-Glass)
interface EmergencyAccess {
  accessId: string;
  patientToken: string;
  practitionerToken: string;
  reason: 'life_threatening' | 'unconscious_patient' | 'public_health_emergency';
  overrideJustification: string; // Free text, reviewed post-hoc
  facilitySupervisor: string;    // Must be notified within 24 hours
  accessDuration: number;        // Maximum: 72 hours
  // Automatic audit review triggered after emergency access
  auditReviewStatus: 'pending' | 'justified' | 'unjustified';
}
```

---

## Technique 4 — MENA Healthcare Regulatory Compliance

### Country-Specific Requirements

```markdown
## UAE — MOHAP & DHA

### MOHAP (Federal)
- Health Data Law: Federal Law No. 2 of 2019
- PHI retention: 25 years from last encounter
- Breach notification: 72 hours to MOHAP + affected patients
- Telemedicine: DOH/MOHAP license required, UAE-based servers
- AI in healthcare: MOHAP approval required for diagnostic AI tools
- Penalties: Up to AED 10M for health data breaches

### DHA (Dubai)
- Nabidh integration: Mandatory for all DHA-licensed facilities
- Clinical coding: ICD-10-AM (Australian Modification)
- Prescriptions: e-Prescription via DHA Salama system
- Insurance: ePrior authorization via DHA platforms

## Saudi Arabia — MOH & SFDA

### MOH (Ministry of Health)
- NPHIES: National Platform for Health Information Exchange
- Seha platform: Mandatory connectivity for all licensed facilities
- Data residency: All patient data stored within Saudi Arabia
- Telemedicine: SCFHS (Saudi Commission) license required
- PHI retention: 10 years from last encounter

### SFDA (Saudi Food and Drug Authority)
- Medical device software: SFDA Class B/C classification
- Clinical decision support: SFDA pre-market notification
- AI/ML medical devices: Special regulatory pathway

## Egypt — MOH
- Health Information Act (draft, expected 2025)
- NTRA compliance for health data transmission
- CBE regulations for health insurance payments
- Telemedicine: MOH circular regulation
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| HEALTH-001 | Patient name/ID in URL params | **CRITICAL** — PHI exposure in server logs | Use POST body + tokenized references |
| HEALTH-002 | PHI in error messages/stack traces | **CRITICAL** — Log exfiltration | Sanitize all error outputs; use tokens only |
| HEALTH-003 | Shared database credentials for PHI access | **HIGH** — No audit trail | Per-user credentials + RBAC |
| HEALTH-004 | No consent check before PHI access | **CRITICAL** — Regulatory violation | Consent gate on every PHI resolution |
| HEALTH-005 | Storing PHI in client-side storage | **HIGH** — Device theft exposure | Server-side only; session-scoped access |
| HEALTH-006 | Screenshot/recording not disabled on health screens | **MEDIUM** — Unauthorized capture | FLAG_SECURE (Android) / preventScreenCapture (iOS) |
| HEALTH-007 | No Break-the-Glass for emergencies | **HIGH** — Treatment delay | Emergency override with post-hoc audit |
| HEALTH-008 | PHI backup without encryption | **CRITICAL** — Data at rest violation | AES-256 encryption for all backups |
| HEALTH-009 | Sending PHI via unencrypted channels | **CRITICAL** — Data in transit violation | TLS 1.3 mandatory; mTLS for facility-to-facility |
| HEALTH-010 | No data retention policy enforcement | **MEDIUM** — Storage bloat + compliance gap | Automated retention enforcement per jurisdiction |

---

## Chain-Multiplier Integration

```markdown
## How This Skill Serves Other Agents

@SecurityAgent → Consumes PHI classification + audit checklist for health app reviews
@BackendAgent → Uses FHIR API patterns and PHI vault service architecture
@DBA → References data retention rules and encryption requirements per jurisdiction
@HealthConsultant → Primary consumer for all health compliance decisions
@Frontend → Uses consent form patterns and PHI-safe display rules

## Dependency Chain
mena-data-sovereignty → health-data-privacy → rbac-permission-system → api-security-patterns
  (jurisdiction rules)    (PHI handling)       (access control)         (endpoint hardening)
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] Zero PHI (names, IDs, MRN) in application logs, URLs, or error messages
- [ ] PHI Vault Service implemented with tokenization + HSM-managed encryption
- [ ] Consent management system with granular scope and immutable audit trail
- [ ] FHIR R4 API integration patterns applied for health data exchange
- [ ] Break-the-Glass emergency access with post-hoc audit review
- [ ] Country-specific retention periods enforced (25y UAE, 10y KSA, 15y EGY)
- [ ] Nabidh integration validated (if UAE deployment)
- [ ] All health data stored within jurisdiction (MOHAP/MOH data residency)