# API Contract — {{PHASE_NAME}}

**Contract Type:** API / Service Interface  
**Version:** 1.0.0  
**Reasoning Hash:** {{REASONING_HASH}}  

---

## Endpoint / Interface Definition

```yaml
contract_id: "{{CONTRACT_ID}}"
type: "{{rest|graphql|internal|event}}"
version: "1.0.0"

endpoints:
  - path: "{{PATH}}"
    method: "{{GET|POST|PUT|DELETE}}"
    description: "{{DESCRIPTION}}"
    auth: "{{bearer|api_key|none}}"
    request_schema: "contracts/schemas/{{schema}}.json"
    response_schema: "contracts/schemas/{{schema}}_response.json"
    law_151_applies: true
    rate_limit: "{{N}} req/min"
```

---

## Request Schema

```json
{
  "{{field_1}}": "{{type}} — {{description}}",
  "{{field_2}}": "{{type}} — {{description}}"
}
```

---

## Response Schema

```json
{
  "status": "success | error",
  "data": {},
  "reasoning_hash": "string",
  "timestamp": "ISO8601"
}
```

---

## Error Codes

| Code | Type | Description | Recovery |
|------|------|-------------|----------|
| 400 | SOFT_WARN | Invalid input | Validate and retry |
| 403 | HARD_BLOCK | Sovereignty violation | Check OMEGA Gate |
| 500 | AUTO_FIX | Internal error | healing_bot_v2 triggered |
