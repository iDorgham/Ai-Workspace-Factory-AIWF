# Design Document — {{PHASE_NAME}}

**Phase:** {{PHASE_NUMBER}} — {{PHASE_NAME}}  
**Planning Type:** {{PLANNING_TYPE}}  
**Reasoning Hash:** {{REASONING_HASH}}  
**Timestamp:** {{ISO_TIMESTAMP}}  

> C4 Diagrams: Context + Container are mandatory. Component level is required for phases 03+.  
> Keep all diagrams focused: ≤25 elements, unidirectional arrows, technology tags on every element.

---

## 1. System Context (C4 Level 1)

See `c4-context.mmd` for the rendered diagram.

**Narrative:**  
{{CONTEXT_NARRATIVE — describe the system boundary, external actors, and primary relationships}}

---

## 2. Container Architecture (C4 Level 2)

See `c4-containers.mmd` for the rendered diagram.

**Narrative:**  
{{CONTAINER_NARRATIVE — describe each container, its technology, and its responsibility}}

### Container Inventory

| Container | Technology | Responsibility | Owner Agent |
|-----------|------------|----------------|-------------|
| {{CONTAINER_1}} | {{TECH}} | {{RESPONSIBILITY}} | {{AGENT}} |
| {{CONTAINER_2}} | {{TECH}} | {{RESPONSIBILITY}} | {{AGENT}} |

---

## 3. Component Design (C4 Level 3)

_Expand in phase-03-detailed-design. Leave as placeholder in earlier phases._

---

## 4. Data Flow

```
{{SOURCE}} → [{{ACTION}}] → {{DESTINATION}}
{{DESTINATION}} → [{{TRANSFORM}}] → {{OUTPUT}}
```

---

## 5. Key Design Decisions

| Decision | Options Considered | Chosen | Rationale |
|----------|--------------------|--------|-----------|
| {{DECISION_1}} | {{OPTIONS}} | {{CHOSEN}} | {{RATIONALE}} |
| {{DECISION_2}} | {{OPTIONS}} | {{CHOSEN}} | {{RATIONALE}} |

---

## 6. Design Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {{RISK_1}} | Medium | High | {{MITIGATION}} |
| {{RISK_2}} | Low | Medium | {{MITIGATION}} |
