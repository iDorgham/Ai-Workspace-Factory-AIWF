#!/usr/bin/env python3
"""
Fetch all official skills from skills.sh/official and add them to the library.
Skips skills that already exist. Updates skills.registry.json with new entries.
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
SKILLS_DIR = WORKSPACE_ROOT / ".ai" / "skills"
REGISTRY_PATH = WORKSPACE_ROOT / ".ai" / "registry" / "skills.registry.json"

# Official creators from skills.sh/official with their GitHub org and repo
OFFICIAL_SOURCES = [
    ("anthropics", "skills"),
    ("apify", "agent-skills"),
    ("apollographql", "skills"),
    ("astronomer", "agents"),
    ("auth0", "agent-skills"),
    ("automattic", "agent-skills"),
    ("axiomhq", "skills"),
    ("base", "skills"),
    ("better-auth", "skills"),
    ("bitwarden", "ai-plugins"),
    ("box", "box-for-ai"),
    ("brave", "brave-search-skills"),
    ("browser-use", "browser-use"),
    ("browserbase", "skills"),
    ("callstackincubator", "agent-skills"),
    ("clerk", "skills"),
    ("clickhouse", "agent-skills"),
    ("cloudflare", "skills"),
    ("coderabbitai", "skills"),
    ("coinbase", "agentic-wallet-skills"),
    ("dagster-io", "skills"),
    ("datadog-labs", "agent-skills"),
    ("dbt-labs", "dbt-agent-skills"),
    ("denoland", "skills"),
    ("elevenlabs", "skills"),
    ("encoredev", "skills"),
    ("exploreomni", "omni-agent-skills"),
    ("expo", "skills"),
    ("facebook", "react"),
    ("figma", "mcp-server-guide"),
    ("firebase", "agent-skills"),
    ("firecrawl", "cli"),
    ("flutter", "skills"),
    ("getsentry", "skills"),
    ("github", "awesome-copilot"),
    ("google-gemini", "gemini-skills"),
    ("google-labs-code", "stitch-skills"),
    ("hashicorp", "agent-skills"),
    ("huggingface", "skills"),
    ("kotlin", "kotlin-agent-skills"),
    ("langchain-ai", "langchain-skills"),
    ("langfuse", "skills"),
    ("launchdarkly", "agent-skills"),
    ("livekit", "agent-skills"),
    ("makenotion", "claude-code-notion-plugin"),
    ("mapbox", "mapbox-agent-skills"),
    ("mastra-ai", "skills"),
    ("mcp-use", "mcp-use"),
    ("medusajs", "medusa-agent-skills"),
    ("microsoft", "azure-skills"),
    ("n8n-io", "n8n"),
    ("neondatabase", "agent-skills"),
    ("nuxt", "ui"),
    ("openai", "skills"),
    ("openshift", "hypershift"),
    ("planetscale", "database-skills"),
    ("posthog", "skills"),
    ("prisma", "skills"),
    ("projectopensea", "opensea-skill"),
    ("pulumi", "agent-skills"),
    ("pytorch", "pytorch"),
    ("redis", "agent-skills"),
    ("remotion-dev", "skills"),
    ("resend", "resend-skills"),
    ("rivet-dev", "skills"),
    ("runwayml", "skills"),
    ("sanity-io", "agent-toolkit"),
    ("semgrep", "skills"),
    ("shopify", "shopify-ai-toolkit"),
    ("streamlit", "agent-skills"),
    ("stripe", "ai"),
    ("supabase", "agent-skills"),
    ("sveltejs", "ai-tools"),
    ("tavily-ai", "skills"),
    ("temporalio", "skill-temporal-developer"),
    ("tinybirdco", "tinybird-agent-skills"),
    ("tldraw", "tldraw"),
    ("triggerdotdev", "skills"),
    ("upstash", "context7"),
    ("vercel", "ai"),
    ("vercel-labs", "agent-skills"),
    ("webflow", "webflow-skills"),
    ("whopio", "whop-payments-network-skill"),
    ("wix", "skills"),
    ("wordpress", "agent-skills"),
]

# Possible subdirectory names where skills live in repos
SKILLS_SUBDIRS = ["skills", "skill", "Skills", ""]


def fetch_url(url, retries=3, delay=1.0):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "skills-fetcher/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 403:
                print(f"  Rate limited on {url}, waiting 60s...")
                time.sleep(60)
            elif attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
    return None


def get_github_skills_dir(org, repo):
    """Try to find the skills directory in a GitHub repo."""
    for subdir in SKILLS_SUBDIRS:
        path = f"skills" if not subdir else subdir
        url = f"https://api.github.com/repos/{org}/{repo}/contents/{path}"
        if not subdir:
            url = f"https://api.github.com/repos/{org}/{repo}/contents"
        data = fetch_url(url)
        if data:
            try:
                items = json.loads(data)
                if isinstance(items, list):
                    # Check if any item looks like a skill dir (has SKILL.md inside)
                    dirs = [i for i in items if i.get("type") == "dir"]
                    if dirs:
                        return path if subdir else "", items
            except Exception:
                pass
    return None, None


def get_skill_content(org, repo, skills_base, skill_name):
    """Fetch SKILL.md content for a skill."""
    candidates = [
        f"{skills_base}/{skill_name}/SKILL.md",
        f"{skills_base}/{skill_name}/skill.md",
        f"{skill_name}/SKILL.md",
        f"SKILL.md",
    ]
    if not skills_base:
        candidates = [f"{skill_name}/SKILL.md", f"SKILL.md"]

    for path in candidates:
        url = f"https://raw.githubusercontent.com/{org}/{repo}/HEAD/{path}"
        content = fetch_url(url)
        if content and len(content) > 50:
            return content, path
    return None, None


def slugify(name):
    """Convert a skill name to a filesystem-safe slug."""
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


def extract_description(content, skill_name):
    """Extract description from SKILL.md frontmatter or first heading."""
    # Try frontmatter description
    fm_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if fm_match:
        desc = fm_match.group(1).strip().strip('"\'')
        return desc[:200]
    # Try first paragraph after heading
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# ") and i + 1 < len(lines):
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j].strip() and not lines[j].startswith("#"):
                    return lines[j].strip()[:200]
    return f"Official {skill_name} skill"


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def save_registry(registry):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")


def get_existing_skill_ids(registry):
    return {s["id"] for s in registry.get("skills", [])}


def main():
    registry = load_registry()
    existing_ids = get_existing_skill_ids(registry)
    print(f"Existing skills: {len(existing_ids)}")

    added = []
    skipped_existing = []
    failed = []

    for org, repo in OFFICIAL_SOURCES:
        print(f"\n→ {org}/{repo}")
        time.sleep(0.3)  # be polite to GitHub API

        # Get skills directory listing
        for subdir in ["skills", ""]:
            api_url = f"https://api.github.com/repos/{org}/{repo}/contents/{subdir}" if subdir else f"https://api.github.com/repos/{org}/{repo}/contents"
            data = fetch_url(api_url)
            if not data:
                continue
            try:
                items = json.loads(data)
            except Exception:
                continue

            if not isinstance(items, list):
                continue

            skill_dirs = [i for i in items if i.get("type") == "dir"]

            # If no subdirs, maybe the SKILL.md is directly in the repo root or skills/
            if not skill_dirs:
                # Try fetching SKILL.md directly
                for path in [f"{subdir}/SKILL.md" if subdir else "SKILL.md"]:
                    url = f"https://raw.githubusercontent.com/{org}/{repo}/HEAD/{path}"
                    content = fetch_url(url)
                    if content and len(content) > 50:
                        skill_id = f"{org}-{slugify(repo)}"
                        if skill_id in existing_ids:
                            skipped_existing.append(skill_id)
                            print(f"  skip (exists): {skill_id}")
                        else:
                            skill_dir = SKILLS_DIR / f"official-{skill_id}"
                            skill_dir.mkdir(parents=True, exist_ok=True)
                            (skill_dir / "SKILL.md").write_text(content)
                            desc = extract_description(content, skill_id)
                            registry["skills"].append({
                                "id": skill_id,
                                "path": f".ai/skills/official-{skill_id}/SKILL.md",
                                "source": "official",
                                "origin": f"https://github.com/{org}/{repo}",
                                "version": "1.0.0",
                                "status": "active",
                                "description": desc,
                                "mapped_commands": [],
                                "compatible_agents": [],
                                "required_tools": []
                            })
                            existing_ids.add(skill_id)
                            added.append(skill_id)
                            print(f"  + {skill_id}")
                        break
                break

            # Process each skill directory
            for item in skill_dirs:
                skill_name = item["name"]
                skill_id = f"{org}-{slugify(skill_name)}"

                if skill_id in existing_ids:
                    skipped_existing.append(skill_id)
                    print(f"  skip (exists): {skill_id}")
                    continue

                # Fetch SKILL.md
                base = subdir if subdir else ""
                content, found_path = get_skill_content(org, repo, base, skill_name)
                if not content:
                    print(f"  ! no SKILL.md: {skill_id}")
                    failed.append(f"{org}/{repo}/{skill_name}")
                    continue

                skill_dir = SKILLS_DIR / f"official-{skill_id}"
                skill_dir.mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text(content)

                desc = extract_description(content, skill_name)
                registry["skills"].append({
                    "id": skill_id,
                    "path": f".ai/skills/official-{skill_id}/SKILL.md",
                    "source": "official",
                    "origin": f"https://github.com/{org}/{repo}",
                    "version": "1.0.0",
                    "status": "active",
                    "description": desc,
                    "mapped_commands": [],
                    "compatible_agents": [],
                    "required_tools": []
                })
                existing_ids.add(skill_id)
                added.append(skill_id)
                print(f"  + {skill_id}")
                time.sleep(0.1)

            break  # found the right subdir

    save_registry(registry)

    print(f"\n{'='*60}")
    print(f"Added:    {len(added)}")
    print(f"Skipped:  {len(skipped_existing)} (already in library)")
    print(f"Failed:   {len(failed)} (no SKILL.md found)")
    if failed:
        print("\nFailed sources:")
        for f in failed:
            print(f"  - {f}")

    # Write summary log
    log = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "added": added,
        "skipped_existing": skipped_existing,
        "failed": failed,
    }
    log_path = WORKSPACE_ROOT / ".ai" / "logs" / "official-skills-import.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
    print(f"\nLog written to: {log_path}")


if __name__ == "__main__":
    main()
