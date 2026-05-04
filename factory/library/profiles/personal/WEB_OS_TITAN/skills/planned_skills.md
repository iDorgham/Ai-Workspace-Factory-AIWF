# Planned skills — WEB_OS_TITAN

Skill ids = directories under **`factory/library/skills/<id>/`** (mirror to `.ai/skills/` per sync).

**Manifest order (final refinement):** **SDD spine** → **(1) content** → **(2) design system** → **(3) MVP** → **(4) extended**. Agents should prefer earlier tiers for speed; full tables below remain the human index (not every row may appear in `workspace_bundle.manifest.yaml` if trimmed later).

## SDD + teaching + planning

| Skill id | Use |
|----------|-----|
| `guide_sdd_mastery` | Phases, manifests, density gate vocabulary. |
| `guide_teaching` | Layered explanations for mixed-skill teams. |
| `guide_instructor_domains` | Web / SEO / content teaching anchors. |
| `official_vercel_adr_skill` | Architecture decision records and change logs. |
| `official_github_project_workflow_analysis_blueprint_generator` | Workflow and delivery analysis blueprints. |

## Architecture + programming

| Skill id | Use |
|----------|-----|
| `official_github_acquire_codebase_knowledge` | Map and explain large codebases quickly. |
| `official_github_architecture_blueprint_generator` | System and module architecture sketches. |
| `official_github_web_coder` | Web-focused implementation patterns. |

## Content + SEO + analysis

| Skill id | Use |
|----------|-----|
| `marketing_seo_audit` | Technical + on-page SEO. |
| `marketing_content_creation` | Long-form + microcopy. |
| `marketing_campaign_planning` | Editorial calendar + channels. |
| `marketing_competitive_analysis` | Intel from scraped competitors. |
| `marketing_competitive_brief` | Structured competitive summaries. |
| `content_architecture` | IA, hubs, and reusable content models. |
| `content_synthesis` | Merge sources into coherent drafts. |
| `data_statistical_analysis` | Quant readouts for content and campaigns. |

**SEO · AEO · GEO-style tuning:** use `marketing_seo_audit` plus CMS skills; **`official_sanity_io_seo_aeo_best_practices`** covers answer-engine (AEO) patterns often grouped under “GEO” for generative search surfaces.

## Product + design + platform

| Skill id | Use |
|----------|-----|
| `engineering_documentation` | Runbooks for CMS, frontend, and deploy. |
| `design_design_system` | Tokens, components, dashboard density. |
| `design_accessibility` | Public site + CMS a11y. |
| `design_critique` | Portfolio and marketing visual QA. |
| `design_ux_copy` | Microcopy and UX writing for web surfaces. |
| `official_anthropics_frontend_design` | Frontend design patterns and polish. |
| `official_figma_figma_create_design_system_rules` | Design-system rules and tokens from Figma workflows. |
| `official_figma_figma_generate_design` | Figma-integrated UI workflows. |
| `official_figma_figma_implement_design` | From design to implementation handoff. |
| `official_google_labs_code_shadcn_ui` | shadcn/ui composition and theming. |
| `official_vercel_labs_web_design_guidelines` | Web design quality bar for shipped UI. |
| `official_github_web_design_reviewer` | Structured UI review from GitHub skill pack. |
| `official_google_labs_code_stitch_design` | AI-assisted UI blocks and layout iteration (typography + composition). |

## UI components & library hygiene

| Skill id | Use |
|----------|-----|
| `official_google_labs_code_react_components` | Reusable React UI patterns. |
| `official_vercel_labs_composition_patterns` | Composable UI and data boundaries on Vercel stacks. |
| `official_github_oo_component_documentation` | Object-oriented component docs and contracts. |
| `component_deduplication` | Reduce duplicate components across apps. |
| `dependency_resolution_for_components` | Package and import graph hygiene for UI libs. |
| `library_quality_audit` | Library-wide quality and consistency passes. |

## React + animation

| Skill id | Use |
|----------|-----|
| `official_vercel_labs_react_best_practices` | React patterns for App Router style stacks. |
| `official_vercel_labs_react_view_transitions` | View Transitions / motion-friendly navigation. |
| `official_github_react18_lifecycle_patterns` | React 18+ lifecycle and effects discipline. |
| `official_github_gsap_framer_scroll_animation` | Scroll-led motion and interaction. |
| `official_remotion_dev_remotion` | Programmatic video / motion in React. |

## Branding + Arabic

| Skill id | Use |
|----------|-----|
| `marketing_brand_review` | Brand consistency across site and CMS. |
| `marketing_brand_voice` | Voice and tone for marketing surfaces. |
| `brand_voice_enforcement` | Guardrails on copy and claims. |
| `official_anthropics_brand_guidelines` | Brand guideline authoring and checks. |
| `egyptian_arabic_content_master` | Humanized Egyptian Arabic web and marketing copy. |
| `bilingual_content` | Arabic–English and mixed-locale content patterns. |
| `legal_content_mena` | MENA legal-plain copy; pairs with RTL layout and `design_accessibility`. |

**RTL UI:** no single `rtl` skill id in-library — combine **`design_design_system`**, **`design_accessibility`**, **`bilingual_content`**, and framework logical properties / `dir=rtl` in implementation guides.

## Security + compliance

| Skill id | Use |
|----------|-----|
| `official_github_agent_owasp_compliance` | OWASP-oriented agent and app checks. |
| `official_github_agent_supply_chain` | Dependency and supply-chain hygiene. |
| `official_github_ai_prompt_engineering_safety_review` | Safer prompts and tool use. |
| `official_github_mcp_security_audit` | MCP server and connector risk review. |
| `official_github_security_review` | Structured security review flows. |
| `official_semgrep_semgrep` | Core Semgrep policy and usage. |
| `official_semgrep_code_security` | Static rules for application code. |
| `official_semgrep_llm_security` | LLM and agent-specific Semgrep guidance. |

## Performance + CMS runtime

| Skill id | Use |
|----------|-----|
| `official_neondatabase_neon_postgres_egress_optimizer` | Neon egress and query cost discipline. |
| `official_automattic_wp_performance` | WordPress performance tuning (Automattic pack). |
| `official_wordpress_wp_performance` | Core Web Vitals and WP stack performance. |

## Debug, test, automation & observability

| Skill id | Use |
|----------|-----|
| `official_github_webapp_testing` | Web app testing strategy and checks. |
| `official_browserbase_ui_test` | Browser automation for UI flows. |
| `official_github_agentic_eval` | Agent and model output evaluation. |
| `official_github_quality_playbook` | Cross-cutting code quality gates and reviews. |
| `official_github_chrome_devtools` | Performance, network, and Lighthouse-style profiling in Chrome. |
| `official_cloudflare_web_perf` | Edge and CDN-side web performance patterns. |
| `official_browserbase_functions` | Serverless browser automation deployment. |
| `official_github_playwright_automation_fill_in_form` | Playwright form and flow automation. |
| `official_langfuse_langfuse` | Traces, scores, and analytics for AI features. |

## Prompt engineering & model APIs

| Skill id | Use |
|----------|-----|
| `official_google_labs_code_enhance_prompt` | Prompt refinement for coding agents. |
| `official_github_arize_prompt_optimization` | Experiment-driven prompt tuning. |
| `official_github_prompt_builder` | Structured prompt assembly. |
| `official_github_boost_prompt` | Short prompt boosts and constraints. |
| `official_anthropics_claude_api` | Claude API usage patterns. |
| `official_google_gemini_vertex_ai_api_dev` | Gemini / Vertex AI API development. |
| `official_google_gemini_gemini_api_dev` | Google AI Gemini API (consumer / AI Studio style). |
| `official_google_gemini_gemini_interactions_api` | Multi-turn and tool-style Gemini interactions. |
| `official_google_gemini_gemini_live_api_dev` | Live / low-latency Gemini audio and streaming patterns. |

**IDE / CLI packs not in `factory/library/skills/`:** **Cursor** (`.cursor/` + Cursor docs), **Antigravity** (`/guide` → `.ai/commands/guide.md`), **Gemini CLI**, **Qwen CLI**, **OpenCode**, **Kilo** — wire via repo rules and vendor CLIs; no matching `skill.md` ids were found to list here.

## GitHub Actions, CI·CD, branching & PRs

| Skill id | Use |
|----------|-----|
| `official_github_create_github_action_workflow_specification` | Authoring and reviewing Action workflow YAML. |
| `official_github_git_flow_branch_creator` | Git-flow style branches and release hygiene. |
| `official_github_create_github_pull_request_from_specification` | Spec-to-PR automation patterns. |
| `official_github_my_pull_requests` | Triaging and curating your open PRs. |

## GitHub Copilot

| Skill id | Use |
|----------|-----|
| `official_github_github_copilot_starter` | Onboarding Copilot in repos and teams. |
| `official_github_copilot_cli_quickstart` | **Copilot CLI** usage and guardrails. |
| `official_github_copilot_instructions_blueprint_generator` | Repository Copilot instruction files. |
| `official_github_copilot_sdk` | Programmatic Copilot / coding-agent integration. |
| `official_github_suggest_awesome_github_copilot_skills` | Curated Copilot skill patterns. |

## Orchestration & AI swarm

| Skill id | Use |
|----------|-----|
| `multi_tool_orchestration` | Routing work across tools and steps. |
| `workspace_audit_orchestrator` | Cross-surface audit and orchestration passes. |

**AI swarm:** align with **AGENTS.md** (Swarm Router v3, T0/T1); these skills support orchestration discipline, not a separate “swarm” package id.

## Claude Code–style Anthropic tooling

| Skill id | Use |
|----------|-----|
| `official_anthropics_skill_creator` | Authoring skills for Claude-style agents. |
| `official_anthropics_mcp_builder` | MCP servers and tools for Anthropic clients. |

## Dashboard UI & design

| Skill id | Use |
|----------|-----|
| `data_interactive_dashboard_builder` | Interactive dashboards from data products. |
| `official_axiomhq_building_dashboards` | Axiom-style observability dashboards. |

Pair with **`design_design_system`**, **`official_figma_figma_generate_design`**, and **design pack** `factory/library/templates/design/dashboard/design.md` for visual dashboard chrome.

## Headless CMS (Sanity + WordPress)

| Skill id | Use |
|----------|-----|
| `official_sanity_io_sanity_best_practices` | Sanity Studio and content lake hygiene. |
| `official_sanity_io_content_modeling_best_practices` | Schemas, references, and portable text. |
| `official_sanity_io_seo_aeo_best_practices` | SEO and answer-engine optimization in Sanity. |
| `official_wordpress_wp_rest_api` | Headless and decoupled WP via REST. |
| `official_wordpress_wp_plugin_development` | Plugin boundaries and extensibility. |
| `official_automattic_wp_block_development` | Gutenberg block development. |
| `official_automattic_wp_plugin_development` | Automattic plugin patterns and releases. |

## Backend, API + database

| Skill id | Use |
|----------|-----|
| `official_apollographql_apollo_client` | Client-side GraphQL consumption. |
| `official_apollographql_apollo_server` | GraphQL API design and server patterns. |
| `official_apollographql_graphql_schema` | Schema design and evolution. |
| `official_github_openapi_to_application_code` | OpenAPI-driven API and codegen flows. |
| `official_github_typespec_api_operations` | TypeSpec-first API descriptions. |
| `official_prisma_prisma_postgres` | Prisma with Postgres. |
| `official_neondatabase_neon_postgres` | Neon serverless Postgres. |
| `official_supabase_supabase` | Supabase (Auth, DB, Edge, Storage). |
| `official_supabase_supabase_postgres_best_practices` | Postgres tuning and RLS-minded patterns on Supabase. |

## TypeScript, JavaScript & CLIs

| Skill id | Use |
|----------|-----|
| `official_github_javascript_typescript_jest` | JS/TS testing with Jest-style workflows. |
| `official_github_typescript_mcp_server_generator` | TypeScript MCP server scaffolding. |
| `official_prisma_prisma_cli` | Prisma CLI migrations and introspection. |
| `official_tinybirdco_tinybird_typescript_sdk_guidelines` | TypeScript analytics SDK discipline. |
| `official_supabase_supabase` | **Includes Supabase CLI** (`supabase` commands) in skill body. |

**CSS:** no top-level `css` skill folder — use **`official_google_labs_code_shadcn_ui`** + **`official_vercel_labs_web_design_guidelines`**.

## GitHub, GitHub CLI, CI, deploy & Vercel

| Skill id | Use |
|----------|-----|
| `official_github_github_issues` | Issue-driven delivery. |
| `official_callstackincubator_github` | GitHub platform patterns beyond Actions. |
| `official_callstackincubator_github_actions` | GitHub Actions workflows and CI hygiene. |
| `official_github_gh_cli` | **`gh`** GitHub CLI automation. |
| `official_github_cli_mastery` | Broader GitHub CLI mastery. |
| `official_github_technology_stack_blueprint_generator` | Stack selection and architecture blueprints. |
| `official_github_mcp_deploy_manage_agents` | Deploy and operate MCP-style agents. |
| `sovereign_deploy_router` | AIWF deploy routing conventions (explicit gates). |
| `official_vercel_use_ai_sdk` | Vercel + AI SDK when stack matches. |
| `official_vercel_develop_ai_functions_example` | Vercel AI Functions patterns. |
| `official_vercel_labs_deploy_to_vercel` | Deploy flows and platform checks. |
| `official_vercel_labs_vercel_cli_with_tokens` | **Vercel CLI** and token-safe automation. |
