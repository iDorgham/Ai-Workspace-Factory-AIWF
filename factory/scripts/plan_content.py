#!/usr/bin/env python3
"""
plan_content.py — /plan content Command Engine v2.0
=====================================================
Runs a smart content planning session that:
  1. Asks: Website content or Blog content?
  2. Detects if content already exists in the workspace
  3. Presents mode options (start fresh / enhance / increase / change)
  4. Runs the structured discovery session (new content only)
  5. Generates a full phase-based content-plan.md

Usage:
    python3 factory/scripts/plan_content.py --workspace sovereign-web
    python3 factory/scripts/plan_content.py --workspace sovereign-web --non-interactive
"""

import json
import os
import shutil
import argparse
from datetime import datetime


# ── Paths ────────────────────────────────────────────────────────────
DISCOVERY_TEMPLATE = ".ai/templates/content-discovery/discovery-interview.json"
SESSION_TEMPLATE   = ".ai/templates/content-discovery/discovery-session.md"
PLAN_TEMPLATE      = ".ai/templates/content-discovery/content-plan-template.md"
PLAN_OUTPUT_DIR    = "plan/{workspace}/"
CONTENT_ROOT       = "workspaces/{workspace}/"
BLOG_ROOT          = "workspaces/{workspace}/blog/"


# ── Helpers ──────────────────────────────────────────────────────────
def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sep(char="─", width=58):
    print(char * width)

def header(title, icon="🌐"):
    print()
    sep("═")
    print(f"  {icon}  {title}")
    sep("═")

def section_header(title, icon="📋"):
    print(f"\n{'─'*55}")
    print(f"  {icon} {title}")
    print(f"{'─'*55}")


# ── Content Existence Detection ───────────────────────────────────────
def detect_existing_content(workspace: str, content_type: str) -> dict:
    """
    Scans the workspace for existing content.
    Returns a summary of what was found.
    """
    if content_type == "blog":
        root = BLOG_ROOT.replace("{workspace}", workspace)
    else:
        root = CONTENT_ROOT.replace("{workspace}", workspace)

    result = {
        "exists": False,
        "root": root,
        "page_count": 0,
        "locale_count": 0,
        "pages": [],
        "has_plan": False,
        "plan_path": PLAN_OUTPUT_DIR.replace("{workspace}", workspace) + "content-plan.md"
    }

    if not os.path.isdir(root):
        return result

    # Scan for page folders with content
    for item in os.listdir(root):
        item_path = os.path.join(root, item)
        if os.path.isdir(item_path) and item not in [".DS_Store", "sitemap.md"]:
            # Check if any locale files exist inside
            locales_found = []
            for locale in ["en", "ar-eg"]:
                locale_path = os.path.join(item_path, locale)
                if os.path.isdir(locale_path) and any(f.endswith(".md") for f in os.listdir(locale_path)):
                    locales_found.append(locale)
            if locales_found:
                result["pages"].append({"name": item, "locales": locales_found})
                result["page_count"] += 1
                result["locale_count"] = max(result["locale_count"], len(locales_found))

    if result["page_count"] > 0:
        result["exists"] = True

    if os.path.isfile(result["plan_path"]):
        result["has_plan"] = True

    return result


def print_content_summary(detected: dict):
    """Prints a formatted summary of what exists."""
    print(f"\n  ┌── Existing Content Found ──────────────────────────────┐")
    print(f"  │  📁 Root:     {detected['root']}")
    print(f"  │  📄 Pages:    {detected['page_count']} page folder(s) with content")
    print(f"  │  🌐 Locales:  {detected['locale_count']} language(s)")
    if detected["pages"]:
        for page in detected["pages"][:6]:
            locales_str = ", ".join(page["locales"])
            print(f"  │     └── {page['name']:<28} [{locales_str}]")
        if len(detected["pages"]) > 6:
            print(f"  │     └── ... and {len(detected['pages']) - 6} more pages")
    print(f"  │  📝 Plan:    {'✅ Found' if detected['has_plan'] else '❌ Not found'}")
    print(f"  └───────────────────────────────────────────────────────┘")


# ── Mode Selection ─────────────────────────────────────────────────────
def ask_content_type() -> tuple:
    """Ask if the user wants website or blog content, return (type, seo_requested)."""
    header("/plan content — Content Planning Engine v2.0", "🌐")
    print("  Content Planner Agent | Sovereign Factory\n")
    sep()
    print("\n  What type of content do you want to plan?\n")
    print("    1. 🌐 Website Content  (pages, sections, legal, forms, popups)")
    print("    2. 📝 Blog Content     (articles, series, topic clusters, SEO posts)")
    print()
    choice = input("  Your choice [1 or 2]: ").strip()
    content_type = "blog" if choice == "2" else "website"

    seo_requested = False
    if content_type == "website":
        seo_requested = ask_seo_recommendation()

    return content_type, seo_requested


def ask_seo_recommendation() -> bool:
    """
    Presented immediately after 'Website Content' is selected.
    Strongly recommends SEO research before content creation.
    Returns True if the user wants an SEO phase included.
    """
    print()
    sep("─")
    print("  💡 RECOMMENDATION: Start with SEO Research & Planning")
    sep("─")
    print("""
  Before writing a single word of website content, an SEO
  research phase will ensure every page targets the right
  keywords, outranks competitors, and drives real organic traffic.

  ┌── What the SEO Phase Includes ──────────────────────────┐
  │  🔍 Keyword Discovery   — Find high-value search terms  │
  │  🏆 Competitor Audit    — Analyze top 3 rivals          │
  │  📊 Gap Analysis        — Identify content opportunities│
  │  📝 Meta Strategy       — Title + description templates │
  │  🗺️  Keyword Map        — Assign keywords per page       │
  └─────────────────────────────────────────────────────────┘

  ⏱️  Estimated effort: 1 phase (before content creation)
  🤖 Agents: SEO Research Agent, Keyword Mapper, Gap Analyst
    """)
    choice = input("  Include SEO Research phase? [Y / n]: ").strip().lower()
    seo_requested = choice not in ["n", "no"]
    if seo_requested:
        print("  ✅ SEO Research phase will be added to your content plan.\n")
    else:
        print("  ⏭️  Skipping SEO phase. You can add it later with /plan content.\n")
    return seo_requested


def ask_existing_mode(detected: dict) -> str:
    """
    When content already exists, ask the user what they want to do.
    Returns one of: 'fresh' | 'enhance' | 'increase' | 'change'
    """
    section_header("Existing Content Detected", "⚠️")
    print_content_summary(detected)
    print("\n  What would you like to do with the existing content?\n")
    print("    1. 🗑️  Delete and Start Fresh       — Remove all content and start over")
    print("    2. ✨  Enhance & Edit               — Improve quality, tone, and clarity")
    print("    3. 📈  Increase Content             — Expand sections, add more depth")
    print("    4. 🔄  Change Specific Pages        — Target and modify selected pages only")
    print("    5. ❌  Cancel                       — Exit without changes")
    print()
    choice = input("  Your choice [1-5]: ").strip()
    modes = {"1": "fresh", "2": "enhance", "3": "increase", "4": "change", "5": "cancel"}
    return modes.get(choice, "cancel")


def ask_which_pages_to_change(detected: dict) -> list:
    """Ask which pages to target when mode is 'change'."""
    section_header("Select Pages to Change", "🔄")
    pages = detected["pages"]
    print("\n  Available pages:\n")
    for i, page in enumerate(pages, 1):
        locales_str = ", ".join(page["locales"])
        print(f"    {i:>2}. {page['name']:<35} [{locales_str}]")
    print()
    raw = input("  Enter page numbers (comma-separated, e.g. 1,3,5) or 'all': ").strip()
    if raw.lower() == "all":
        return [p["name"] for p in pages]
    selected = []
    for idx in raw.split(","):
        idx = idx.strip()
        if idx.isdigit() and 1 <= int(idx) <= len(pages):
            selected.append(pages[int(idx) - 1]["name"])
    return selected


def ask_enhance_options() -> dict:
    """Ask what aspects to enhance."""
    section_header("Enhancement Options", "✨")
    print("\n  What would you like to enhance?\n")
    print("    1. 📝 Rewrite / Improve all section copy")
    print("    2. 🔍 SEO — Inject keywords and improve meta descriptions")
    print("    3. 🎙️ Brand Voice — Strengthen tone and consistency")
    print("    4. 🌐 Add missing Arabic (AR-EG) translations")
    print("    5. ➕ Add missing sections (popups, forms, CTAs)")
    print("    6. 🔄 All of the above")
    print()
    raw = input("  Your choices (comma-separated numbers): ").strip()
    options = {
        "1": "rewrite", "2": "seo", "3": "brand_voice",
        "4": "add_arabic", "5": "add_sections", "6": "all"
    }
    if "6" in raw:
        return {"mode": "all"}
    selected = {}
    for idx in raw.split(","):
        key = options.get(idx.strip())
        if key:
            selected[key] = True
    return selected


def handle_fresh_start(workspace: str, content_type: str, content_root: str):
    """Confirm and execute full content wipe."""
    section_header("Delete & Start Fresh", "🗑️")
    print(f"\n  ⚠️  WARNING: This will permanently delete:")
    print(f"     {content_root}")
    print()
    confirm = input("  Type DELETE to confirm, or anything else to cancel: ").strip()
    if confirm == "DELETE":
        shutil.rmtree(content_root, ignore_errors=True)
        print(f"  ✅ Content deleted. Starting fresh discovery session...\n")
        return True
    else:
        print("  ❌ Cancelled. Nothing was deleted.")
        return False


def generate_enhancement_plan(workspace: str, mode: str, options: dict, pages: list = None):
    """Generate a targeted enhancement plan."""
    timestamp = datetime.now().isoformat()
    output_dir = PLAN_OUTPUT_DIR.replace("{workspace}", workspace)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"content-enhance-plan-{timestamp[:10]}.md")

    mode_title = {
        "enhance": "✨ Enhancement Plan",
        "increase": "📈 Content Expansion Plan",
        "change":  "🔄 Targeted Change Plan"
    }.get(mode, "Content Update Plan")

    target_scope = "All Pages" if not pages else ", ".join(pages)

    lines = [
        f"# {mode_title} — {workspace}",
        f"",
        f"> **Generated:** {timestamp}",
        f"> **Mode:** {mode.title()}",
        f"> **Target Scope:** {target_scope}",
        f"",
        f"---",
        f"",
        f"## 📋 Enhancement Tasks",
        f"",
    ]

    # Expand tasks per mode
    if mode == "enhance":
        tasks = []
        if options.get("all") or options.get("rewrite"):
            tasks += ["- [ ] `ENH-001` — Rewrite all section copy for clarity and impact",
                      "- [ ] `ENH-002` — Improve subheadlines and body text per page"]
        if options.get("all") or options.get("seo"):
            tasks += ["- [ ] `ENH-003` — Inject target keywords into all headings and meta",
                      "- [ ] `ENH-004` — Optimize meta descriptions for all pages"]
        if options.get("all") or options.get("brand_voice"):
            tasks += ["- [ ] `ENH-005` — Run brand voice validation across all content",
                      "- [ ] `ENH-006` — Replace passive voice with industrial imperatives"]
        if options.get("all") or options.get("add_arabic"):
            tasks += ["- [ ] `ENH-007` — Generate missing AR-EG translations for all pages",
                      "- [ ] `ENH-008` — Add RTL formatting markers to all Arabic sections"]
        if options.get("all") or options.get("add_sections"):
            tasks += ["- [ ] `ENH-009` — Add exit-intent popup to all major pages",
                      "- [ ] `ENH-010` — Add primary CTA block to all inner pages",
                      "- [ ] `ENH-011` — Add cookie consent banner (EN + AR-EG)"]
        lines += tasks or ["- [ ] `ENH-001` — General enhancement pass"]

    elif mode == "increase":
        lines += [
            "- [ ] `EXP-001` — Add 2+ new sections to each page",
            "- [ ] `EXP-002` — Expand hero sublines and feature descriptions",
            "- [ ] `EXP-003` — Add case study / testimonial sections",
            "- [ ] `EXP-004` — Add FAQ section to all product pages",
            "- [ ] `EXP-005` — Add 'How It Works' step-by-step section",
        ]

    elif mode == "change":
        for i, page in enumerate(pages or [], 1):
            lines += [
                f"- [ ] `CHG-{i:03}` — Targeted rewrite of `{page}` (EN + AR-EG)",
            ]

    lines += [
        "",
        "---",
        "",
        "## 🤖 Agents Required",
        "",
        "| Agent | Role |",
        "|:---|:---|",
        "| **Creator Agent (EN)** | Rewrite and expand English content |",
        "| **Creator Agent (AR-EG)** | Arabic translations and RTL formatting |",
        "| **SEO Agent** | Keyword injection and meta optimization |",
        "| **Brand Agent** | Voice validation and tone enforcement |",
        "",
        "## ⚙️ Script",
        "",
        "```bash",
        f"python3 factory/core/content_engine.py  # Re-run after changes",
        "```",
        "",
        f"*Generated: {timestamp}*"
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


# ── Discovery Session ─────────────────────────────────────────────────
def run_discovery_session(workspace: str, content_type: str) -> dict:
    """Full structured discovery for new content."""
    section_header(f"Discovery Session — {content_type.title()} Content", "🔍")
    print(f"  Workspace: {workspace}")
    print(f"  Answer each question to generate your content plan.\n")

    template = load_json(DISCOVERY_TEMPLATE)
    answers = {"content_type": content_type}

    # Skip home-page style questions for blog content
    skip_sections = {"S1", "S2"} if content_type == "blog" else set()

    for section in template["sections"]:
        if section["id"] in skip_sections:
            continue

        section_header(section["title"])
        for q in section["questions"]:
            print(f"\n  {q['id']} — {q['prompt']}")
            if q["type"] == "single-choice":
                for i, opt in enumerate(q["options"], 1):
                    print(f"    {i}. {opt}")
                answers[q["id"]] = input("  Your choice (number or text): ").strip()
            elif q["type"] == "multi-choice":
                for i, opt in enumerate(q["options"], 1):
                    print(f"    {i}. {opt}")
                answers[q["id"]] = input("  Choices (comma-separated numbers): ").strip()
            elif q["type"] == "boolean":
                raw = input("  Yes / No: ").strip().lower()
                answers[q["id"]] = raw in ["yes", "y", "1"]
            elif q["type"] == "text":
                answers[q["id"]] = input(f"  Your answer [{q.get('placeholder', '')}]: ").strip()

    # Blog-specific extra questions
    if content_type == "blog":
        section_header("Blog Content Settings", "📝")
        print("\n  B1 — How many blog posts do you want to plan?")
        answers["B1"] = input("  Number of posts (e.g. 10): ").strip()
        print("\n  B2 — What are the main topics or content pillars?")
        answers["B2"] = input("  Topics (comma-separated): ").strip()
        print("\n  B3 — Do you need topic clusters (pillar + subtopics)?")
        answers["B3"] = input("  Yes / No: ").strip().lower() in ["yes", "y", "1"]
        print("\n  B4 — Publishing frequency target?")
        print("    1. 1 post/week   2. 2 posts/week   3. Daily   4. Monthly")
        answers["B4"] = input("  Your choice: ").strip()

    return answers


# ── Plan Generation ───────────────────────────────────────────────────
def generate_plan(workspace: str, answers: dict) -> str:
    """Generate the content-plan.md from the template."""
    plan_template = load_template(PLAN_TEMPLATE)
    timestamp     = datetime.now().isoformat()
    content_type  = answers.get("content_type", "website")

    plan_content = plan_template
    plan_content = plan_content.replace("{WORKSPACE_NAME}", workspace)
    plan_content = plan_content.replace("{TIMESTAMP}", timestamp)
    plan_content = plan_content.replace("{HOME_STYLE}", answers.get("Q1.1", "Not specified"))
    plan_content = plan_content.replace("{PRIMARY_GOAL}", answers.get("Q1.2", "Not specified"))
    plan_content = plan_content.replace("{LANGUAGES}", answers.get("Q4.1", "Not specified"))
    plan_content = plan_content.replace("{SEO_PHASE}", "✅ Enabled" if answers.get("Q5.1") else "❌ Skipped")
    plan_content = plan_content.replace("{RTL_SUPPORT}", "✅ Yes" if answers.get("Q4.3") else "❌ No")
    plan_content = plan_content.replace("{ELEMENTS_COUNT}", str(answers.get("Q6.1", "TBD")))
    plan_content = plan_content.replace("{workspace}", workspace)
    plan_content = plan_content.replace("{SITEMAP_TREE}", "│   ├── en/\n│   └── ar-eg/")
    plan_content = plan_content.replace("{LEGAL_TREE}", "│   ├── privacy_policy/\n│   ├── terms_of_service/\n│   └── data_residency_protocol/")
    plan_content = plan_content.replace("{INNER_PAGES_TASKS}", "> *(Run `/dev` to scaffold all inner page task blocks.)*")

    pages_answer = answers.get("Q3.1", "")
    page_count = len([p.strip() for p in pages_answer.split(",") if p.strip()]) if pages_answer else "TBD"
    plan_content = plan_content.replace("{PAGE_COUNT}", str(page_count))

    # Prepend content type header
    content_type_badge = "🌐 Website" if content_type == "website" else "📝 Blog"
    plan_content = f"**Content Type:** {content_type_badge}\n\n" + plan_content

    output_dir  = PLAN_OUTPUT_DIR.replace("{workspace}", workspace)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "content-plan.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(plan_content)

    answers_path = os.path.join(output_dir, "discovery-answers.json")
    with open(answers_path, "w", encoding="utf-8") as f:
        json.dump({"workspace": workspace, "timestamp": timestamp, "answers": answers}, f, indent=4, ensure_ascii=False)

    return output_path


# ── Main ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="/plan content v2.0")
    parser.add_argument("--workspace", required=True, help="Workspace slug (e.g. sovereign-web)")
    parser.add_argument("--non-interactive", action="store_true", help="Output discovery template only")
    args   = parser.parse_args()
    workspace = args.workspace

    if args.non_interactive:
        session = load_template(SESSION_TEMPLATE)
        out = f"plan/{workspace}/discovery-session.md"
        os.makedirs(f"plan/{workspace}/", exist_ok=True)
        with open(out, "w") as f:
            f.write(session)
        print(f"✅ Discovery session saved to: {out}")
        return

    # ── Step 1: Content Type ──────────────────────────────────────────
    content_type, seo_requested = ask_content_type()
    content_root = (BLOG_ROOT if content_type == "blog" else CONTENT_ROOT).replace("{workspace}", workspace)

    # ── Step 2: Detect Existing Content ──────────────────────────────
    detected = detect_existing_content(workspace, content_type)

    if detected["exists"]:
        mode = ask_existing_mode(detected)

        if mode == "cancel":
            print("\n  ❌ Cancelled. No changes made.\n")
            return

        elif mode == "fresh":
            deleted = handle_fresh_start(workspace, content_type, content_root)
            if not deleted:
                return
            # Fall through to full discovery session

        elif mode in ("enhance", "increase"):
            options = ask_enhance_options() if mode == "enhance" else {}
            output_path = generate_enhancement_plan(workspace, mode, options)
            print(f"\n{'='*58}")
            print(f"  ✅ Enhancement Plan Generated!")
            print(f"  📄 {output_path}")
            print(f"\n  💡 Next Step: /dev — Execute tasks against this plan")
            print(f"{'='*58}\n")
            return

        elif mode == "change":
            pages = ask_which_pages_to_change(detected)
            output_path = generate_enhancement_plan(workspace, "change", {}, pages=pages)
            print(f"\n{'='*58}")
            print(f"  ✅ Targeted Change Plan Generated!")
            print(f"  📄 {output_path}")
            print(f"  🎯 Targeting {len(pages)} page(s): {', '.join(pages)}")
            print(f"\n  💡 Next Step: /dev — Execute the targeted changes")
            print(f"{'='*58}\n")
            return

    # ── Step 3: Full Discovery Session (New or Fresh-Start) ──────────
    answers                 = run_discovery_session(workspace, content_type)
    answers["seo_requested"] = seo_requested   # Inject SEO decision into answers
    output_path             = generate_plan(workspace, answers)

    print(f"\n{'='*58}")
    print(f"  ✅ Content Plan Generated!")
    print(f"  📄 {output_path}")
    print(f"  📊 discovery-answers.json saved")
    if seo_requested:
        print(f"  🔍 SEO Research phase — Phase 0 included in plan")
    print(f"\n  💡 Suggested Next Steps:")
    if seo_requested:
        print(f"     /plan audit  — Run SEO Research phase first")
    print(f"     /dev         — Execute Phase 1 (Architecture)")
    print(f"     /test        — Validate specs before creation")
    print(f"{'='*58}\n")


if __name__ == "__main__":
    main()
