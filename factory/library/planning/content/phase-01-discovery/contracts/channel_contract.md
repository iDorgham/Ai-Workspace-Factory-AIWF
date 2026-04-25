# Channel Contract — Phase 01: Discovery

**Contract Type:** Channel / Distribution Rules  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## Channel Definitions

```yaml
channel_contract:
  id: "aiwf-v21-channel-contract"
  version: "1.0.0"

  channels:
    - id: "github"
      priority: P1
      audience: [P2_pragmatic_dev, P1_sovereign_builder]
      content_types: [README, technical_docs, quick_start, architecture_diagrams]
      brand_voice: "precise, dense, developer-native"
      publish_gate: "spec_architect_v2 review + SEO ≥85 + readability ≥65"
      cadence: "On release; updated with each phase completion"

    - id: "linkedin"
      priority: P2
      audience: [P1_sovereign_builder, P4_ai_director]
      content_types: [thought_leadership, case_studies, architecture_posts, launch_announcement]
      brand_voice: "authoritative, strategic, founder-voice (Dorgham)"
      publish_gate: "brand_voice ≥92 + no clichés + CTA required"
      cadence: "3× per week during launch window"

    - id: "x_twitter"
      priority: P2
      audience: [P2_pragmatic_dev, AI_community]
      content_types: [architecture_threads, feature_announcements, quote_cards]
      brand_voice: "sharp, systems-focused, no fluff"
      publish_gate: "brand_voice ≥92 + 280 chars/post"
      cadence: "Daily during launch week; 3× per week ongoing"

    - id: "dev_communities"
      priority: P3
      audience: [P2_pragmatic_dev]
      content_types: [deep_dive_posts, tutorial_cross_posts, HackerNews_Show_HN]
      brand_voice: "technical, honest, builder-to-builder"
      publish_gate: "readability ≥65 + code examples present"
      cadence: "1–2× per phase completion milestone"

    - id: "arabic_mena"
      priority: P3
      audience: [P3_mena_pioneer]
      content_types: [arabic_linkedin_post, arabic_readme_section, community_post]
      brand_voice: "Arabic — precise, regionally aware, Law 151/2020 explicit"
      publish_gate: "native Arabic review + RTL rendering verified"
      cadence: "3 pieces total for launch (as per Law 151 scope decision)"
      law_151_note: "Content must not reference real Egyptian user data"
```
