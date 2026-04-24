---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# Capability Registry — Agent Index

Machine-readable catalog for **@RuntimeOrchestrator** and **@Router** re-routing. Each entry maps a stable `agent_id` to handles, tier, primary capabilities, and fallback routing order.

## JSON Schema (registry document root)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GALERIACapabilityRegistry",
  "type": "object",
  "required": ["format_version", "agents"],
  "properties": {
    "format_version": { "type": "string", "const": "1.0" },
    "agents": {
      "type": "array",
      "minItems": 35,
      "maxItems": 35,
      "items": {
        "type": "object",
        "required": ["agent_id", "handles", "tier", "capabilities", "task_types", "fallback_agents"],
        "properties": {
          "agent_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "handles": {
            "type": "array",
            "items": { "type": "string", "pattern": "^@[A-Za-z0-9]+$" }
          },
          "tier": {
            "type": "string",
            "enum": ["Leadership", "Execution", "Quality", "Infrastructure", "Orchestration", "Governance", "Performance", "Intelligence", "Learning", "Coordination"]
          },
          "capabilities": { "type": "array", "items": { "type": "string" } },
          "task_types": { "type": "array", "items": { "type": "string" } },
          "fallback_agents": { "type": "array", "items": { "type": "string" } },
          "definition_file": { "type": "string" }
        }
      }
    }
  }
}
```

## YAML — `agents:` (35 entries)

> **Note:** Extended workspace agents beyond this 35 live under `.ai/agents/*.md` and may be added in future `format_version` bumps. Runtime tools MUST accept unknown `agent_id` gracefully and fall back to `@Router`.

```yaml
format_version: "1.0"
agents:
  - agent_id: founder
    handles: ["@Founder"]
    tier: Leadership
    capabilities: [vision_intake, non_technical_planning, prd_discovery]
    task_types: [discovery, prd, stakeholder_alignment]
    fallback_agents: [guide, architect]
    definition_file: .ai/agents/founder.md
  - agent_id: guide
    handles: ["@Guide"]
    tier: Leadership
    capabilities: [orchestration, next_status, sprint_integration]
    task_types: [coordination, status, sprint]
    fallback_agents: [router, runtime-orchestrator]
    definition_file: .ai/agents/guide.md
  - agent_id: architect
    handles: ["@Architect"]
    tier: Leadership
    capabilities: [system_design, contracts_planning, feature_plans]
    task_types: [contract_design, adr, technical_plan]
    fallback_agents: [contract-lock, backend]
    definition_file: .ai/agents/architect.md
  - agent_id: frontend
    handles: ["@Frontend"]
    tier: Execution
    capabilities: [react_ui, rtl, a11y, shadcn]
    task_types: [ui, component, app_router]
    fallback_agents: [design-system, accessibility, i18n]
    definition_file: .ai/agents/frontend.md
  - agent_id: backend
    handles: ["@Backend"]
    tier: Execution
    capabilities: [api, services, zod_pipes, hono_fastify]
    task_types: [api, stub, business_logic]
    fallback_agents: [security, dba, debugger]
    definition_file: .ai/agents/backend.md
  - agent_id: dba
    handles: ["@DBA"]
    tier: Execution
    capabilities: [schema, migrations, zero_downtime]
    task_types: [migration, sql, prisma]
    fallback_agents: [backend, architect]
    definition_file: .ai/agents/dba.md
  - agent_id: qa
    handles: ["@QA"]
    tier: Quality
    capabilities: [unit, integration, e2e, coverage]
    task_types: [test, qa, tdd]
    fallback_agents: [debugger, reviewer, visual-qa]
    definition_file: .ai/agents/qa.md
  - agent_id: reviewer
    handles: ["@Reviewer"]
    tier: Quality
    capabilities: [code_review, drift_gating]
    task_types: [review, merge_gate]
    fallback_agents: [security, architect]
    definition_file: .ai/agents/reviewer.md
  - agent_id: security
    handles: ["@Security"]
    tier: Quality
    capabilities: [owasp, zero_trust, secrets_scan]
    task_types: [security_review, threat_model]
    fallback_agents: [reviewer, backend]
    definition_file: .ai/agents/security.md
  - agent_id: design-system
    handles: ["@DesignSystem"]
    tier: Quality
    capabilities: [tokens, components, visual_governance]
    task_types: [tokens, ui_audit, ds]
    fallback_agents: [frontend, brand-guardian]
    definition_file: .ai/agents/design-system.md
  - agent_id: content
    handles: ["@Content"]
    tier: Quality
    capabilities: [i18n_keys, copy, gov_ux_tone]
    task_types: [copy, i18n_content, docs_ux]
    fallback_agents: [i18n, frontend]
    definition_file: .ai/agents/content.md
  - agent_id: automation
    handles: ["@Automation"]
    tier: Infrastructure
    capabilities: [cicd, git, deploy, branch_strategy]
    task_types: [ci, deploy, branch, commit]
    fallback_agents: [devops-engineer, dependency-manager]
    definition_file: .ai/agents/automation.md
  - agent_id: router
    handles: ["@Router"]
    tier: Orchestration
    capabilities: [routing, dependency_graph, parallelism]
    task_types: [route, swarm_plan]
    fallback_agents: [runtime-orchestrator, guide]
    definition_file: .ai/agents/router.md
  - agent_id: contract-lock
    handles: ["@ContractLock"]
    tier: Governance
    capabilities: [zod_validate, lock_fingerprint, drift_detect]
    task_types: [contract_validate, lock]
    fallback_agents: [architect, error-detective]
    definition_file: .ai/agents/contract-lock.md
  - agent_id: context-slicer
    handles: ["@ContextSlicer"]
    tier: Performance
    capabilities: [dmp_enforcement, context_compression]
    task_types: [context_slice, token_cut]
    fallback_agents: [guide, runtime-orchestrator]
    definition_file: .ai/agents/context-slicer.md
  - agent_id: metrics-agent
    handles: ["@MetricsAgent"]
    tier: Intelligence
    capabilities: [velocity, compliance_scores, cache_hit]
    task_types: [metrics, dashboard]
    fallback_agents: [analytics-agent, forecasting-agent]
    definition_file: .ai/agents/metrics.md
  - agent_id: risk-agent
    handles: ["@RiskAgent"]
    tier: Intelligence
    capabilities: [risk_register_5x5, mitigation_triggers]
    task_types: [risk, mitigation]
    fallback_agents: [architect, escalation-handler]
    definition_file: .ai/agents/risk.md
  - agent_id: analytics-agent
    handles: ["@AnalyticsAgent"]
    tier: Intelligence
    capabilities: [trends, recommendations]
    task_types: [analytics, reporting]
    fallback_agents: [forecasting-agent, metrics-agent]
    definition_file: .ai/agents/analytics.md
  - agent_id: forecasting-agent
    handles: ["@ForecastingAgent"]
    tier: Intelligence
    capabilities: [forecasting, scenarios]
    task_types: [forecast, modeling]
    fallback_agents: [analytics-agent, metrics-agent]
    definition_file: .ai/agents/forecasting.md
  - agent_id: retro-facilitator
    handles: ["@RetroFacilitator"]
    tier: Learning
    capabilities: [retrospectives, memory_updates]
    task_types: [retro, lessons]
    fallback_agents: [knowledge-synthesizer, tutor]
    definition_file: .ai/agents/retro.md
  - agent_id: escalation-handler
    handles: ["@EscalationHandler"]
    tier: Coordination
    capabilities: [sbar, blocked_tasks, sla]
    task_types: [escalation, unblock]
    fallback_agents: [guide, founder]
    definition_file: .ai/agents/escalation.md
  - agent_id: optimizer
    handles: ["@Optimizer"]
    tier: Performance
    capabilities: [lighthouse, bundle, caching]
    task_types: [perf, web_vitals]
    fallback_agents: [frontend, performance-engineer]
    definition_file: .ai/agents/optimizer.md
  - agent_id: visual-qa
    handles: ["@VisualQA"]
    tier: Quality
    capabilities: [playwright, visual_regression, percy]
    task_types: [e2e_visual, visual_test]
    fallback_agents: [qa, accessibility]
    definition_file: .ai/agents/visual-qa.md
  - agent_id: brand-guardian
    handles: ["@BrandGuardian"]
    tier: Quality
    capabilities: [brand_grammar, tone, luxury]
    task_types: [brand, voice]
    fallback_agents: [content, design-system]
    definition_file: .ai/agents/brand-guardian.md
  - agent_id: tutor
    handles: ["@Tutor"]
    tier: Learning
    capabilities: [teaching, learning_progress]
    task_types: [teach, explain]
    fallback_agents: [guide, knowledge-synthesizer]
    definition_file: .ai/agents/tutor.md
  - agent_id: error-detective
    handles: ["@ErrorDetective"]
    tier: Quality
    capabilities: [error_capture, anti_pattern_promotion]
    task_types: [triage, ap_promote, drift_triage]
    fallback_agents: [debugger, knowledge-synthesizer]
    definition_file: .ai/agents/error-detective.md
  - agent_id: knowledge-synthesizer
    handles: ["@KnowledgeSynthesizer"]
    tier: Intelligence
    capabilities: [distill_lessons, skills_agents_updates]
    task_types: [synthesis, playbook]
    fallback_agents: [retro-facilitator, guide]
    definition_file: .ai/agents/knowledge-synthesizer.md
  - agent_id: debugger
    handles: ["@Debugger"]
    tier: Quality
    capabilities: [root_cause, minimal_fix]
    task_types: [debug, incident]
    fallback_agents: [qa, backend]
    definition_file: .ai/agents/debugger.md
  - agent_id: dependency-manager
    handles: ["@DependencyManager"]
    tier: Quality
    capabilities: [pnpm_catalog, upgrades, audits]
    task_types: [deps, supply_chain]
    fallback_agents: [security, automation]
    definition_file: .ai/agents/dependency-manager.md
  - agent_id: runtime-orchestrator
    handles: ["@RuntimeOrchestrator"]
    tier: Orchestration
    capabilities: [runtime_loop, drift_reroute, checkpoint, filesystem_truth]
    task_types: [runtime_swarm, monitor, reroute]
    fallback_agents: [router, guide]
    definition_file: .ai/agents/runtime-orchestrator.md
  - agent_id: accessibility
    handles: ["@Accessibility"]
    tier: Quality
    capabilities: [wcag, a11y_audit, axe]
    task_types: [a11y, audit_accessibility]
    fallback_agents: [frontend, visual-qa]
    definition_file: .ai/agents/accessibility.md
  - agent_id: i18n
    handles: ["@I18n"]
    tier: Quality
    capabilities: [rtl, locales, message_keys]
    task_types: [i18n, rtl_qa]
    fallback_agents: [content, frontend]
    definition_file: .ai/agents/i18n.md
  - agent_id: devops-engineer
    handles: ["@DevopsEngineer"]
    tier: Infrastructure
    capabilities: [infra, pipelines, observability]
    task_types: [devops, infra]
    fallback_agents: [automation, security]
    definition_file: .ai/agents/devops-engineer.md
  - agent_id: integration-specialist
    handles: ["@IntegrationSpecialist"]
    tier: Execution
    capabilities: [third_party_apis, webhooks, integrations]
    task_types: [integration, oauth, webhook]
    fallback_agents: [backend, security]
    definition_file: .ai/agents/integration-specialist.md
  - agent_id: mobile-developer
    handles: ["@MobileDeveloper"]
    tier: Execution
    capabilities: [react_native, expo, mobile_ux]
    task_types: [mobile, app_store]
    fallback_agents: [frontend, qa]
    definition_file: .ai/agents/mobile-developer.md
```

## Matching Algorithm (for tools / humans)

1. Normalize task → `task_types[]` + optional `domain` string from feature plan.
2. Score each agent: intersection of `task_types` + keyword overlap in `capabilities`.
3. Pick max score; tie-break by lower `fallback_agents` depth to `@Router`.
4. If no match score > 0 → `@Router` → `@EscalationHandler`.

---

*Registry version 1.0 — aligned to CLAUDE.md §2 core roster + runtime + specialist extensions*
