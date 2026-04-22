#!/usr/bin/env python3
"""Generate missing commands (Req 1) and subagents (Req 2 & 3)."""
import json, os, datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z")

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print(f"  ✓ {path}")

# ── Requirement 1: Extend Thin Command Categories ──────────────────────

COMMANDS = {
    "commands/02-commerce/business-strategy": [
        ("swot.md", {
            "desc": "Run a structured SWOT analysis for a product, market, or venture.",
            "heading": "/swot",
            "body": "Invokes the `@BusinessAnalyst` to produce a comprehensive Strengths, Weaknesses, Opportunities, and Threats matrix.",
            "usage": "/swot <product_or_market> [--depth brief|deep]",
            "tasks": [
                "Gather internal asset data and competitive positioning.",
                "Map external opportunities from market-size-calculator output.",
                "Identify threats using regulatory and competitor intelligence.",
                "Output a `swot-matrix.md` with scored quadrants.",
            ],
            "constraints": [
                "All threat scores must cite a verifiable data source.",
                "Must align with brand positioning defined by `@BrandStrategist`.",
            ],
        }),
        ("forecast.md", {
            "desc": "Generate a 12-month financial forecast with scenario modeling.",
            "heading": "/forecast",
            "body": "Invokes the `@Forecasting` agent to build revenue, expense, and cash-flow projections across best, base, and worst scenarios.",
            "usage": "/forecast <business_unit> [--horizon 6|12|24] [--scenarios base|multi]",
            "tasks": [
                "Pull historical revenue and expense data from workspace context.",
                "Model three scenarios: optimistic, base, and conservative.",
                "Generate a month-by-month P&L projection table.",
                "Output `forecast-report.md` and `scenario-comparison.csv`.",
            ],
            "constraints": [
                "Assumptions must be explicitly documented per scenario.",
                "Growth rates exceeding 30% MoM must include justification.",
            ],
        }),
    ],
    "commands/03-creative/design-media": [
        ("moodboard.md", {
            "desc": "Curate a design moodboard from brand guidelines and reference assets.",
            "heading": "/moodboard",
            "body": "Invokes the `@DesignDirector` to assemble a structured visual moodboard with color palettes, typography, and layout references.",
            "usage": "/moodboard <project_name> [--style minimal|editorial|brutalist]",
            "tasks": [
                "Extract brand tokens from the project's design system.",
                "Curate 5–8 reference images aligned with the target aesthetic.",
                "Map typography pairings and spacing scales.",
                "Output a `moodboard.md` with embedded asset references.",
            ],
            "constraints": [
                "All colors must reference semantic design tokens, not raw hex.",
                "Image references must be from licensed or generated assets.",
            ],
        }),
        ("styleguide.md", {
            "desc": "Generate a living style guide document from existing design tokens.",
            "heading": "/styleguide",
            "body": "Invokes the `@DesignDirector` to produce a comprehensive, developer-ready style guide covering color, type, spacing, and component patterns.",
            "usage": "/styleguide <project_name> [--format md|html] [--scope full|tokens-only]",
            "tasks": [
                "Scan design-token files for color, typography, and spacing definitions.",
                "Document each token with usage examples and do/don't guidelines.",
                "Generate a component pattern inventory with visual hierarchy rules.",
                "Output `style-guide.md` with linked token references.",
            ],
            "constraints": [
                "Must include WCAG 2.2 AA contrast ratios for all color pairs.",
                "Token names must follow the project's existing naming convention.",
            ],
        }),
    ],
    "commands/03-creative/research-analytics": [
        ("benchmark.md", {
            "desc": "Run a competitive benchmark analysis across key market dimensions.",
            "heading": "/benchmark",
            "body": "Invokes the `@ResearchAnalyst` to compare a product or brand against 3–5 competitors across defined KPIs.",
            "usage": "/benchmark <product_name> [--competitors \"A,B,C\"] [--dimensions ux|pricing|features]",
            "tasks": [
                "Identify the top 3–5 competitors for the given product or vertical.",
                "Score each competitor across UX, pricing, feature depth, and market reach.",
                "Generate a comparison matrix with gap analysis.",
                "Output `benchmark-report.md` and `competitor-matrix.csv`.",
            ],
            "constraints": [
                "All competitor data must be sourced from public information.",
                "Scoring rubric must be documented before results are presented.",
            ],
        }),
        ("survey.md", {
            "desc": "Design and analyze a user research survey with statistical rigor.",
            "heading": "/survey",
            "body": "Invokes the `@ResearchAnalyst` to create survey instruments, define sampling methodology, and produce an analysis framework.",
            "usage": "/survey <research_question> [--method quant|qual|mixed] [--sample-size N]",
            "tasks": [
                "Draft survey questions with proper scale types (Likert, NPS, open-ended).",
                "Define target population and minimum sample size for significance.",
                "Create an analysis plan with statistical tests and visualization specs.",
                "Output `survey-instrument.md` and `analysis-plan.md`.",
            ],
            "constraints": [
                "Questions must avoid leading or double-barreled phrasing.",
                "Sample size calculation must target ≥95% confidence level.",
            ],
        }),
    ],
}

print("─── Requirement 1: Thin Command Extension ───")
for cat_path, cmds in COMMANDS.items():
    for fname, c in cmds:
        tasks = "\n".join(f"{i+1}. {t}" for i, t in enumerate(c["tasks"]))
        constraints = "\n".join(f"- {x}" for x in c["constraints"])
        content = f"""---
description: {c['desc']}
---

# {c['heading']}

{c['body']}

## Usage
`{c['usage']}`

## Tasks
{tasks}

## Constraints
{constraints}
"""
        write(f"{cat_path}/{fname}", content)

# ── Requirement 2: Extend Thin Subagent Categories ─────────────────────

SUBAGENTS_THIN = {
    "subagents/01-cyber/ai-automation-ops": [
        ("workflow-orchestrator.json", {
            "id": "workflow-orchestrator",
            "name": "Workflow Orchestration Engine",
            "description": "Coordinates multi-step AI automation pipelines with branching logic, retry policies, and observability hooks.",
            "capabilities": ["dag-execution-planning", "retry-backoff-management", "pipeline-observability-metrics", "conditional-branching-logic"],
        }),
        ("prompt-optimizer.json", {
            "id": "prompt-optimizer",
            "name": "Prompt Optimization Specialist",
            "description": "Analyzes and refines LLM prompts for cost efficiency, latency reduction, and output quality improvement.",
            "capabilities": ["prompt-compression-analysis", "token-budget-optimization", "few-shot-example-curation", "output-quality-scoring"],
        }),
        ("agent-health-monitor.json", {
            "id": "agent-health-monitor",
            "name": "Agent Health Monitor",
            "description": "Continuously monitors AI agent performance, detects regressions, and triggers automated remediation workflows.",
            "capabilities": ["latency-anomaly-detection", "output-drift-monitoring", "cost-per-run-tracking", "auto-remediation-triggering"],
        }),
    ],
    "subagents/01-cyber/mobile-ios-apple": [
        ("appstore-compliance-checker.json", {
            "id": "appstore-compliance-checker",
            "name": "App Store Compliance Checker",
            "description": "Validates iOS app submissions against Apple's latest App Store Review Guidelines and metadata requirements.",
            "capabilities": ["guideline-violation-scanning", "metadata-validation", "privacy-label-verification", "entitlement-audit"],
        }),
        ("swift-performance-profiler.json", {
            "id": "swift-performance-profiler",
            "name": "Swift Performance Profiler",
            "description": "Profiles Swift and SwiftUI code for memory leaks, CPU hotspots, and rendering performance bottlenecks.",
            "capabilities": ["instruments-trace-analysis", "memory-leak-detection", "swiftui-render-profiling", "energy-impact-assessment"],
        }),
    ],
    "subagents/01-cyber/saas-platforms": [
        ("subscription-lifecycle-manager.json", {
            "id": "subscription-lifecycle-manager",
            "name": "Subscription Lifecycle Manager",
            "description": "Manages the full subscription lifecycle including trial conversion, upgrades, downgrades, and churn prevention workflows.",
            "capabilities": ["trial-conversion-optimization", "plan-migration-orchestration", "churn-prediction-scoring", "dunning-retry-management"],
        }),
        ("tenant-isolation-auditor.json", {
            "id": "tenant-isolation-auditor",
            "name": "Tenant Isolation Auditor",
            "description": "Audits multi-tenant SaaS architectures for data isolation violations, cross-tenant leaks, and permission boundary breaches.",
            "capabilities": ["row-level-security-validation", "cross-tenant-query-detection", "permission-boundary-testing", "data-residency-verification"],
        }),
    ],
    "subagents/03-creative/ai-generative-media": [
        ("image-prompt-engineer.json", {
            "id": "image-prompt-engineer",
            "name": "Image Prompt Engineer",
            "description": "Crafts and iterates on text-to-image prompts for consistent brand-aligned visual output across generative models.",
            "capabilities": ["prompt-structure-optimization", "style-consistency-enforcement", "negative-prompt-engineering", "model-specific-syntax-adaptation"],
        }),
        ("asset-variation-generator.json", {
            "id": "asset-variation-generator",
            "name": "Asset Variation Generator",
            "description": "Produces systematic visual asset variations for A/B testing, localization, and multi-platform delivery.",
            "capabilities": ["aspect-ratio-adaptation", "color-palette-swapping", "text-overlay-localization", "batch-variation-rendering"],
        }),
    ],
    "subagents/05-verticals/crypto-web3": [
        ("defi-protocol-analyzer.json", {
            "id": "defi-protocol-analyzer",
            "name": "DeFi Protocol Analyzer",
            "description": "Analyzes decentralized finance protocols for yield sustainability, liquidity risks, and smart contract dependencies.",
            "capabilities": ["yield-sustainability-modeling", "impermanent-loss-calculation", "liquidity-pool-risk-scoring", "protocol-dependency-mapping"],
        }),
        ("tokenomics-modeler.json", {
            "id": "tokenomics-modeler",
            "name": "Tokenomics Modeler",
            "description": "Models token supply dynamics, vesting schedules, and emission curves to evaluate long-term economic viability.",
            "capabilities": ["supply-emission-simulation", "vesting-schedule-analysis", "inflation-deflation-modeling", "governance-weight-calculation"],
        }),
    ],
}

print("\n─── Requirement 2: Thin Subagent Extension ───")
for cat_path, items in SUBAGENTS_THIN.items():
    for fname, data in items:
        write(f"{cat_path}/{fname}", json.dumps(data, indent=2) + "\n")

# ── Requirement 3: Populate Empty Subagent Categories ──────────────────

SUBAGENTS_EMPTY = {
    "subagents/02-commerce/business-strategy": [
        ("competitive-intel-scanner", {
            "id": "competitive-intel-scanner",
            "name": "Competitive Intelligence Scanner",
            "description": "Scans public data sources to build structured competitive profiles and market positioning maps.",
            "capabilities": ["competitor-feature-matrix-generation", "pricing-model-extraction", "market-share-estimation", "positioning-gap-identification"],
        }),
        ("unit-economics-modeler", {
            "id": "unit-economics-modeler",
            "name": "Unit Economics Modeler",
            "description": "Calculates and validates unit economics including CAC, LTV, payback period, and contribution margins.",
            "capabilities": ["cac-ltv-ratio-calculation", "cohort-retention-analysis", "contribution-margin-breakdown", "payback-period-projection"],
        }),
        ("go-to-market-planner", {
            "id": "go-to-market-planner",
            "name": "Go-to-Market Planner",
            "description": "Structures channel strategies, launch timelines, and distribution plans for new product market entry.",
            "capabilities": ["channel-prioritization-scoring", "launch-timeline-generation", "partner-ecosystem-mapping", "market-entry-sequencing"],
        }),
    ],
    "subagents/03-creative/creative-marketing": [],  # already ≥3
    "subagents/03-creative/design-media": [
        ("typography-pairing-engine", {
            "id": "typography-pairing-engine",
            "name": "Typography Pairing Engine",
            "description": "Recommends and validates typeface pairings based on brand personality, readability, and visual hierarchy rules.",
            "capabilities": ["font-harmony-scoring", "readability-analysis", "variable-font-optimization", "cross-platform-fallback-mapping"],
        }),
        ("layout-grid-generator", {
            "id": "layout-grid-generator",
            "name": "Layout Grid Generator",
            "description": "Generates responsive grid systems and spacing scales tailored to specific design systems and viewport requirements.",
            "capabilities": ["responsive-breakpoint-calculation", "modular-scale-generation", "grid-overlay-export", "spacing-token-derivation"],
        }),
        ("color-system-architect", {
            "id": "color-system-architect",
            "name": "Color System Architect",
            "description": "Designs comprehensive color systems with semantic tokens, accessibility-verified palettes, and dark mode derivatives.",
            "capabilities": ["palette-generation-from-brand", "wcag-contrast-verification", "dark-mode-derivation", "semantic-token-mapping"],
        }),
    ],
    "subagents/03-creative/research-analytics": [
        ("trend-forecaster", {
            "id": "trend-forecaster",
            "name": "Trend Forecaster",
            "description": "Identifies emerging market and consumer trends from search data, social signals, and industry reports.",
            "capabilities": ["search-volume-trend-analysis", "social-signal-aggregation", "trend-lifecycle-classification", "early-adopter-pattern-detection"],
        }),
        ("cohort-analyzer", {
            "id": "cohort-analyzer",
            "name": "Cohort Analyzer",
            "description": "Segments user populations into behavioral cohorts and tracks retention, engagement, and conversion metrics over time.",
            "capabilities": ["behavioral-segmentation", "retention-curve-generation", "conversion-funnel-analysis", "cohort-comparison-visualization"],
        }),
        ("ab-test-evaluator", {
            "id": "ab-test-evaluator",
            "name": "A/B Test Evaluator",
            "description": "Evaluates experiment results with statistical rigor, calculating significance, effect sizes, and practical impact.",
            "capabilities": ["bayesian-significance-testing", "effect-size-calculation", "sample-ratio-mismatch-detection", "sequential-testing-support"],
        }),
    ],
    "subagents/04-ops/product-delivery": [
        ("sprint-velocity-tracker", {
            "id": "sprint-velocity-tracker",
            "name": "Sprint Velocity Tracker",
            "description": "Tracks and forecasts team velocity across sprints using historical data and capacity adjustments.",
            "capabilities": ["velocity-trend-analysis", "capacity-adjustment-modeling", "sprint-burndown-generation", "completion-date-forecasting"],
        }),
        ("release-gate-checker", {
            "id": "release-gate-checker",
            "name": "Release Gate Checker",
            "description": "Validates release readiness by checking quality gates, test coverage, documentation, and compliance requirements.",
            "capabilities": ["quality-gate-validation", "test-coverage-threshold-check", "changelog-completeness-audit", "dependency-vulnerability-scan"],
        }),
        ("incident-classifier", {
            "id": "incident-classifier",
            "name": "Incident Classifier",
            "description": "Classifies production incidents by severity, impact radius, and root cause category for faster triage.",
            "capabilities": ["severity-auto-classification", "impact-radius-estimation", "root-cause-categorization", "escalation-path-recommendation"],
        }),
    ],
}

print("\n─── Requirement 3: Empty Subagent Categories ───")
for cat_path, items in SUBAGENTS_EMPTY.items():
    for slug, data in items:
        write(f"{cat_path}/{slug}/{slug}.json", json.dumps(data, indent=2) + "\n")

print("\n✅ Commands and Subagents complete.")
