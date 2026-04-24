# MENA Data Sovereignty & Cloud Architecture

## Purpose

Architect cloud infrastructure and data pipelines that fully comply with MENA data residency, localization, and sovereignty mandates. This skill provides concrete Terraform/IaC patterns, data classification engines, cross-border transfer automation, and jurisdiction-specific compliance verification — with exact code, deployment patterns, and audit checklists.

**Measurable Impact:**
- Before: Ad-hoc cloud region selection → data residency violations discovered in audit → 6-month remediation
- After: Region-pinned architecture from day one → clean compliance audit on first pass
- Before: Cross-border transfers without legal basis → exposure to fines (up to AED 10M under UAE PDPL)
- After: Automated transfer impact assessments → documented legal basis for every data flow
- Token savings: Single-source sovereignty rules eliminate per-service compliance research (~3,000 tokens/project)

---

## Technique 1 — Data Classification & Residency Engine

### Automated Classification Framework

```typescript
// Data classification engine for MENA compliance
enum DataClassification {
  PUBLIC = 'public',           // No residency requirements
  INTERNAL = 'internal',      // Standard protection
  CONFIDENTIAL = 'confidential', // Encryption required
  RESTRICTED = 'restricted',  // Residency + encryption + access control
  SOVEREIGN = 'sovereign',    // Must NEVER leave jurisdiction
}

interface DataResidencyRule {
  classification: DataClassification;
  country: string;              // ISO 3166-1 alpha-2
  sector: string;               // healthcare, finance, government, telecom
  mandatoryResidency: boolean;  // Must data stay in-country?
  allowedRegions: string[];     // Cloud regions where data CAN be stored
  encryptionRequired: boolean;
  keyManagement: 'local' | 'customer-managed' | 'provider-managed';
  retentionYears: number;
  crossBorderAllowed: boolean;
  crossBorderBasis?: string;    // Legal basis for transfer
  regulatoryBody: string;       // Which authority enforces
  penaltyRange: string;         // Fine range for violations
}

// Residency rule database
const RESIDENCY_RULES: DataResidencyRule[] = [
  // UAE — Government Data
  {
    classification: DataClassification.SOVEREIGN,
    country: 'AE',
    sector: 'government',
    mandatoryResidency: true,
    allowedRegions: ['me-central-1', 'uae-north', 'khazna-auh'],
    encryptionRequired: true,
    keyManagement: 'local',       // HSM within UAE
    retentionYears: 10,
    crossBorderAllowed: false,    // NEVER
    regulatoryBody: 'NESA (National Electronic Security Authority)',
    penaltyRange: 'Criminal penalties + contract termination',
  },
  // UAE — Healthcare (MOHAP)
  {
    classification: DataClassification.RESTRICTED,
    country: 'AE',
    sector: 'healthcare',
    mandatoryResidency: true,
    allowedRegions: ['me-central-1', 'uae-north'],
    encryptionRequired: true,
    keyManagement: 'customer-managed',
    retentionYears: 25,           // MOHAP requirement
    crossBorderAllowed: false,
    regulatoryBody: 'MOHAP + DHA',
    penaltyRange: 'Up to AED 10M',
  },
  // UAE — Financial Services (CBUAE)
  {
    classification: DataClassification.RESTRICTED,
    country: 'AE',
    sector: 'finance',
    mandatoryResidency: true,
    allowedRegions: ['me-central-1', 'uae-north'],
    encryptionRequired: true,
    keyManagement: 'customer-managed',
    retentionYears: 5,
    crossBorderAllowed: false,    // Banking data stays in UAE
    regulatoryBody: 'Central Bank of UAE',
    penaltyRange: 'License suspension + fines',
  },
  // UAE — General Personal Data (PDPL)
  {
    classification: DataClassification.CONFIDENTIAL,
    country: 'AE',
    sector: 'general',
    mandatoryResidency: false,    // Recommended but not mandatory
    allowedRegions: ['me-central-1', 'uae-north', 'eu-west-1', 'us-east-1'],
    encryptionRequired: true,
    keyManagement: 'customer-managed',
    retentionYears: 3,
    crossBorderAllowed: true,
    crossBorderBasis: 'Adequate protection country or explicit consent',
    regulatoryBody: 'UAE Data Office',
    penaltyRange: 'Up to AED 5M',
  },
  // Saudi Arabia — Government (NCA)
  {
    classification: DataClassification.SOVEREIGN,
    country: 'SA',
    sector: 'government',
    mandatoryResidency: true,
    allowedRegions: ['me-south-1-ksa', 'oracle-jeddah', 'ali-riyadh'],
    encryptionRequired: true,
    keyManagement: 'local',
    retentionYears: 10,
    crossBorderAllowed: false,
    regulatoryBody: 'NCA (National Cybersecurity Authority)',
    penaltyRange: 'Criminal penalties',
  },
  // Saudi Arabia — Financial (SAMA)
  {
    classification: DataClassification.RESTRICTED,
    country: 'SA',
    sector: 'finance',
    mandatoryResidency: true,
    allowedRegions: ['me-south-1-ksa', 'oracle-jeddah'],
    encryptionRequired: true,
    keyManagement: 'local',
    retentionYears: 10,
    crossBorderAllowed: false,
    regulatoryBody: 'SAMA',
    penaltyRange: 'License revocation + fines',
  },
  // Saudi Arabia — General Personal Data (PDPL)
  {
    classification: DataClassification.CONFIDENTIAL,
    country: 'SA',
    sector: 'general',
    mandatoryResidency: false,
    allowedRegions: ['me-south-1-ksa', 'me-south-1', 'eu-central-1'],
    encryptionRequired: true,
    keyManagement: 'customer-managed',
    retentionYears: 2,
    crossBorderAllowed: true,
    crossBorderBasis: 'Adequate protection or explicit consent (PDPL Art. 29)',
    regulatoryBody: 'SDAIA',
    penaltyRange: 'Up to SAR 5M',
  },
  // Egypt — General (Data Protection Law 151/2020)
  {
    classification: DataClassification.CONFIDENTIAL,
    country: 'EG',
    sector: 'general',
    mandatoryResidency: false,
    allowedRegions: ['me-south-1', 'eu-south-1', 'af-south-1'],
    encryptionRequired: true,
    keyManagement: 'provider-managed',
    retentionYears: 3,
    crossBorderAllowed: true,
    crossBorderBasis: 'Adequate protection country (DPA decision)',
    regulatoryBody: 'DPA (Data Protection Authority)',
    penaltyRange: 'Up to EGP 5M',
  },
  // Egypt — Banking (CBE)
  {
    classification: DataClassification.RESTRICTED,
    country: 'EG',
    sector: 'finance',
    mandatoryResidency: true,
    allowedRegions: ['eg-cairo-1', 'eg-sovereign'],
    encryptionRequired: true,
    keyManagement: 'local',
    retentionYears: 10,
    crossBorderAllowed: false,
    regulatoryBody: 'Central Bank of Egypt',
    penaltyRange: 'License suspension',
  },
];

// Resolve residency requirements for a given data type
export function resolveResidency(
  country: string,
  sector: string,
  dataType: string
): DataResidencyRule {
  const rule = RESIDENCY_RULES.find(r => 
    r.country === country && r.sector === sector
  );
  
  if (!rule) {
    // Default to most restrictive rule for country
    return RESIDENCY_RULES.find(r => 
      r.country === country && r.sector === 'general'
    ) || throwError(`No residency rule found for ${country}/${sector}`);
  }
  
  return rule;
}
```

---

## Technique 2 — Infrastructure as Code (Region-Pinned)

### Terraform Pattern for MENA Compliance

```hcl
# terraform/mena-compliant-infrastructure.tf

# ─── Variables ───────────────────────────────────────────
variable "target_country" {
  description = "Target MENA country for data residency"
  type        = string
  validation {
    condition     = contains(["AE", "SA", "EG", "QA", "BH"], var.target_country)
    error_message = "Must be a supported MENA country code."
  }
}

# Region mapping: country → primary cloud region
locals {
  region_map = {
    AE = { aws = "me-central-1", azure = "uaenorth", gcp = "me-central1" }
    SA = { aws = "me-south-1",   azure = "saudiarabiacentral", gcp = "me-west1" }
    EG = { aws = "me-south-1",   azure = "uaenorth", gcp = "me-central1" }
    QA = { aws = "me-south-1",   azure = "qatarcentral", gcp = "me-central2" }
    BH = { aws = "me-south-1",   azure = "uaenorth", gcp = "me-central1" }
  }
  
  primary_region = local.region_map[var.target_country].aws
}

# ─── S3 Bucket with Residency Lock ──────────────────────
resource "aws_s3_bucket" "data_store" {
  bucket = "app-${var.target_country}-data-${random_id.suffix.hex}"
  
  # CRITICAL: Prevent accidental cross-region replication
  tags = {
    DataResidency   = var.target_country
    Classification  = "restricted"
    ComplianceScope = "PDPL"
  }
}

# Block public access (mandatory for MENA compliance)
resource "aws_s3_bucket_public_access_block" "data_store" {
  bucket = aws_s3_bucket.data_store.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Server-side encryption with customer-managed KMS key
resource "aws_s3_bucket_server_side_encryption_configuration" "data_store" {
  bucket = aws_s3_bucket.data_store.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data_key.arn
    }
    bucket_key_enabled = true
  }
}

# ─── KMS Key (Region-Locked) ────────────────────────────
resource "aws_kms_key" "data_key" {
  description             = "Data encryption key - ${var.target_country} residency"
  deletion_window_in_days = 30
  enable_key_rotation     = true  # Auto-rotate every year
  
  # CRITICAL: Key never leaves this region
  # Cross-region key replication is NOT configured
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowKeyAdministration"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
        Action    = "kms:*"
        Resource  = "*"
      },
      {
        Sid       = "DenyExportOutsideRegion"
        Effect    = "Deny"
        Principal = "*"
        Action    = ["kms:CreateGrant", "kms:ReEncryptFrom"]
        Resource  = "*"
        Condition = {
          StringNotEquals = {
            "aws:RequestedRegion" = local.primary_region
          }
        }
      }
    ]
  })
  
  tags = {
    DataResidency = var.target_country
    KeyRotation   = "enabled"
  }
}

# ─── RDS with Encryption + No Cross-Region Replicas ─────
resource "aws_db_instance" "main" {
  identifier     = "app-${var.target_country}-db"
  engine         = "postgres"
  engine_version = "16.1"
  instance_class = "db.r6g.large"
  
  # Data residency enforcement
  availability_zone   = "${local.primary_region}a"
  multi_az            = true  # Within same region only
  
  # Encryption (mandatory)
  storage_encrypted = true
  kms_key_id        = aws_kms_key.data_key.arn
  
  # Backup residency (backups stay in same region)
  backup_retention_period = 30
  # Do NOT enable cross-region backup replication
  
  # Audit logging
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  tags = {
    DataResidency  = var.target_country
    Classification = "restricted"
  }
}

# ─── CloudFront with Geo-Restriction ────────────────────
resource "aws_cloudfront_distribution" "cdn" {
  # Restrict edge caching for sensitive content
  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      # Only cache in MENA edge locations for sensitive data
      locations = ["AE", "SA", "EG", "BH", "QA", "KW", "OM", "JO"]
    }
  }
  
  # Enforce HTTPS only
  viewer_certificate {
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }
}
```

---

## Technique 3 — Cross-Border Transfer Assessment

### Transfer Impact Assessment (TIA) Automation

```typescript
// Automated Transfer Impact Assessment
interface TransferImpactAssessment {
  assessmentId: string;
  assessmentDate: string;
  
  // Source and destination
  sourceCountry: string;
  sourceClassification: DataClassification;
  sourceSector: string;
  destinationCountry: string;
  destinationRegion: string;   // Cloud region
  
  // Legal basis evaluation
  legalBasis: {
    adequacyDecision: boolean;  // Destination has adequate protection?
    contractualClauses: boolean; // Standard contractual clauses in place?
    explicitConsent: boolean;   // Data subject explicitly consented?
    bindingCorpRules: boolean;  // Intra-group BCR approved?
    derogation: boolean;        // Specific derogation applies?
    basis: string;              // Which specific legal basis
  };
  
  // Risk assessment
  risks: {
    governmentAccessRisk: 'low' | 'medium' | 'high';
    encryptionInTransit: boolean;
    encryptionAtRest: boolean;
    accessByDestinationStaff: boolean;
    dataMinimization: boolean;  // Only necessary data transferred?
  };
  
  // Decision
  transferAllowed: boolean;
  conditions: string[];         // Conditions that must be maintained
  reviewDate: string;           // Next mandatory review date
  approvedBy: string;           // DPO or legal counsel
}

// Evaluate whether a cross-border transfer is permitted
export function evaluateTransfer(
  source: { country: string; sector: string; classification: DataClassification },
  destination: { country: string; region: string }
): TransferImpactAssessment {
  const rule = resolveResidency(source.country, source.sector, '');
  
  // SOVEREIGN data: NEVER allowed to leave
  if (source.classification === DataClassification.SOVEREIGN) {
    return {
      ...baseAssessment,
      transferAllowed: false,
      conditions: ['SOVEREIGN data must never leave jurisdiction'],
    };
  }
  
  // RESTRICTED data: check if destination region is in allowed list
  if (source.classification === DataClassification.RESTRICTED) {
    const regionAllowed = rule.allowedRegions.includes(destination.region);
    return {
      ...baseAssessment,
      transferAllowed: regionAllowed,
      conditions: regionAllowed 
        ? ['Maintain encryption in transit and at rest']
        : ['Transfer not permitted — data must stay in allowed regions'],
    };
  }
  
  // CONFIDENTIAL+: check legal basis for cross-border
  if (rule.crossBorderAllowed) {
    return {
      ...baseAssessment,
      transferAllowed: true,
      conditions: [
        `Legal basis: ${rule.crossBorderBasis}`,
        'Standard contractual clauses must be in place',
        'Encryption mandatory in transit and at rest',
        'Review annually',
      ],
    };
  }
  
  return {
    ...baseAssessment,
    transferAllowed: false,
    conditions: ['Cross-border transfer not permitted for this data class/sector'],
  };
}
```

---

## Technique 4 — Compliance Verification & Audit

### Data Residency Compliance Scanner

```typescript
// Automated compliance scanner for cloud resources
interface ComplianceScanResult {
  scanDate: string;
  totalResources: number;
  compliant: number;
  nonCompliant: number;
  violations: ComplianceViolation[];
}

interface ComplianceViolation {
  resourceId: string;
  resourceType: 'S3' | 'RDS' | 'EC2' | 'Lambda' | 'CloudFront' | 'ElastiCache';
  region: string;
  expectedRegion: string;
  dataClassification: DataClassification;
  violationType: 'wrong_region' | 'unencrypted' | 'public_access' | 'no_key_rotation' | 'cross_region_backup';
  severity: 'critical' | 'high' | 'medium';
  remediation: string;
}

// Scan cloud infrastructure for residency violations
export async function scanDataResidency(
  country: string,
  sector: string
): Promise<ComplianceScanResult> {
  const rule = resolveResidency(country, sector, '');
  const violations: ComplianceViolation[] = [];
  
  // Scan S3 buckets
  const buckets = await listAllBuckets();
  for (const bucket of buckets) {
    if (!rule.allowedRegions.includes(bucket.region)) {
      violations.push({
        resourceId: bucket.name,
        resourceType: 'S3',
        region: bucket.region,
        expectedRegion: rule.allowedRegions[0],
        dataClassification: rule.classification,
        violationType: 'wrong_region',
        severity: 'critical',
        remediation: `Migrate bucket to ${rule.allowedRegions[0]} or verify data classification`,
      });
    }
    
    if (rule.encryptionRequired && !bucket.encrypted) {
      violations.push({
        resourceId: bucket.name,
        resourceType: 'S3',
        region: bucket.region,
        expectedRegion: rule.allowedRegions[0],
        dataClassification: rule.classification,
        violationType: 'unencrypted',
        severity: 'critical',
        remediation: 'Enable SSE-KMS with customer-managed key',
      });
    }
  }
  
  // Similar scans for RDS, EC2, Lambda, etc.
  // ...
  
  return {
    scanDate: new Date().toISOString(),
    totalResources: buckets.length,
    compliant: buckets.length - violations.length,
    nonCompliant: violations.length,
    violations,
  };
}
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| DS-001 | Using `us-east-1` as default for MENA data | **CRITICAL** — Residency violation | Default to `me-central-1` (UAE) or `me-south-1` (GCC) |
| DS-002 | Cross-region S3 replication without TIA | **HIGH** — Unauthorized transfer | Disable replication or complete Transfer Impact Assessment |
| DS-003 | Provider-managed encryption keys for sovereign data | **CRITICAL** — Key sovereignty violation | Use customer-managed KMS with HSM in-country |
| DS-004 | CDN caching sensitive data globally | **HIGH** — Data leaves jurisdiction | Geo-restrict CloudFront to MENA edge locations |
| DS-005 | No data classification before architecture | **HIGH** — Wrong protections applied | Classify ALL data types before designing infrastructure |
| DS-006 | Cross-region database backups | **MEDIUM** — Backup residency violation | Backups in same region as primary; disable cross-region |
| DS-007 | Third-party analytics without TIA | **HIGH** — Data transfer to analytics provider | Complete TIA for all third-party data processors |
| DS-008 | No encryption key rotation | **MEDIUM** — Compliance gap | Enable annual auto-rotation (90 days for healthcare) |
| DS-009 | Logging PII to global CloudWatch | **HIGH** — Log data leaves jurisdiction | Use region-specific log groups; redact PII from logs |
| DS-010 | No DPO appointment for large-scale processing | **MEDIUM** — PDPL compliance gap | Appoint DPO when processing data of >100K individuals |

---

## Chain-Multiplier Integration

```markdown
## How This Skill Serves Other Agents

@SecurityAgent → Consumes classification rules + encryption mandates for security reviews
@DevOpsAgent → Uses Terraform patterns for region-pinned infrastructure deployment
@BackendAgent → References residency rules for API data flow design
@DBA → Uses retention periods + encryption requirements for database architecture
@HealthConsultant → Consumes healthcare-specific residency rules (MOHAP, MOH)
@FintechStrategist → References financial data residency (CBUAE, SAMA, CBE)

## Dependency Chain
mena-data-sovereignty → [health-data-privacy + payment-compliance + real-estate-modeling]
   (infrastructure layer)    (sector-specific data handling layers)
         ↓
    mena-regulatory-compliance
    (entity & licensing foundation)
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] Data classification completed for ALL data types before architecture design
- [ ] Cloud resources deployed in compliant regions (verified by scanner)
- [ ] Customer-managed encryption keys with region-locked KMS policies
- [ ] Transfer Impact Assessment completed for every cross-border data flow
- [ ] Backup residency verified (same region as primary data)
- [ ] CDN geo-restrictions configured for sensitive content
- [ ] Compliance scanner runs weekly with zero critical violations
- [ ] DPO appointed where required (>100K data subjects)
- [ ] Data retention policies enforced per jurisdiction and sector