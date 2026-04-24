import os
import json

profile_dir = "/Users/Dorgham/Documents/Work/Devleopment/AIWF/factory/profiles"

mappings = {
    "factory/library/01-software-engineering": "factory/library/10-engineering-devops/01-software-engineering",
    "factory/library/03-security-compliance": "factory/library/10-engineering-devops/03-security-compliance",
    "factory/library/10-operations-qa": "factory/library/10-engineering-devops/10-operations-qa",
    "factory/library/05-data-analytics": "factory/library/10-engineering-devops/05-data-analytics",
    "factory/library/06-branding": "factory/library/20-content-strategy/06-branding",
    "factory/library/16-content-dominance": "factory/library/20-content-strategy/16-content-dominance",
    "factory/library/07-visibility-optimization": "factory/library/20-content-strategy/07-visibility-optimization",
    "factory/library/09-social-engagement": "factory/library/20-content-strategy/09-social-engagement",
    "factory/library/04-business-strategy": "factory/library/20-content-strategy/04-business-strategy",
    "factory/library/08-media-production": "factory/library/20-content-strategy/08-media-production",
    "factory/library/02-web-platforms": "factory/library/30-web-platforms/02-web-platforms",
    "factory/library/18-saas-boilerplate": "factory/library/30-web-platforms/18-saas-boilerplate",
    "factory/library/11-industry-verticals": "factory/library/40-verticals/11-industry-verticals",
    "factory/library/13-gaming-entertainment": "factory/library/40-verticals/13-gaming-entertainment",
    "factory/library/15-music-sound-engineering": "factory/library/40-verticals/15-music-sound-engineering",
    "factory/library/14-ai-intelligence": "factory/library/50-intelligence-marketing/14-ai-intelligence",
    "factory/library/06-intel-data": "factory/library/50-intelligence-marketing/06-intel-data",
    "factory/library/17-performance-marketing-growth": "factory/library/50-intelligence-marketing/17-performance-marketing-growth",
    "factory/library/06-frontier": "factory/library/50-intelligence-marketing/06-frontier",
    "factory/library/12-meta-engine": "factory/library/00-core-orchestration/12-meta-engine",
    "factory/library/07-meta": "factory/library/00-core-orchestration/07-meta",
    "factory/library/commands": "factory/library/00-core-orchestration/commands",
    "factory/library/skills": "factory/library/00-core-orchestration/skills"
}

for filename in os.listdir(profile_dir):
    if filename.endswith(".json"):
        path = os.path.join(profile_dir, filename)
        with open(path, 'r') as f:
            content = f.read()
        
        updated = content
        for old, new in mappings.items():
            updated = updated.replace(old, new)
        
        if updated != content:
            with open(path, 'w') as f:
                f.write(updated)
            print(f"[UPDATED] {filename}")

print("Profile migration complete.")
