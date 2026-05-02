"""
Enrich competitor info files with structured company/contact/domain data.

Outputs:
- content/<active_project>/scraped/<slug>/info.md
"""

from __future__ import annotations

import html as html_lib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, project_scraped_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
INDEX_PATH = project_scraped_dir() / "index.json"
HEADERS = {
    "User-Agent": "SovereignBot/1.0 (competitive research; contact@sovereign.studio)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(r"(\+?\d[\d\-\s().]{7,}\d)")
SOCIAL_RE = re.compile(
    r"https?://(?:www\.)?(?:facebook|instagram|linkedin|x|twitter|youtube|tiktok)\.com/[^\s\"'<>]+",
    re.IGNORECASE,
)
LOCATION_LINK_RE = re.compile(
    r"https?://(?:www\.)?(?:maps\.google\.com|google\.com/maps|goo\.gl/maps|maps\.app\.goo\.gl|waze\.com|openstreetmap\.org)[^\s\"'<>]*",
    re.IGNORECASE,
)
ADDRESS_HINT_RE = re.compile(
    r"(address|location|head office|office|city|country|state|zip|postal)",
    re.IGNORECASE,
)


@dataclass
class DomainWhois:
    creation_date: str = "unknown"
    updated_date: str = "unknown"
    expiry_date: str = "unknown"
    registrar: str = "unknown"
    raw_exists: bool = False


def fetch_html(url: str, timeout: int = 15) -> str:
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError, Exception):
        return ""


def html_to_text(html: str) -> str:
    clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = html_lib.unescape(clean)
    clean = clean.replace("&nbsp;", " ")
    clean = clean.replace("·", " ")
    clean = re.sub(r"\s{2,}", " ", clean)
    return clean.strip()


def extract_links(html: str, base_url: str) -> list[str]:
    raw = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    links = []
    seen = set()
    for href in raw:
        absolute = urljoin(base_url, href.strip())
        if absolute.startswith(("http://", "https://")) and absolute not in seen:
            seen.add(absolute)
            links.append(absolute)
    return links


def pick_contact_like_pages(links: list[str]) -> list[str]:
    keywords = (
        "contact",
        "about",
        "team",
        "broker",
        "agent",
        "our-team",
        "staff",
        "consultant",
    )
    chosen = []
    for link in links:
        lower = link.lower()
        if any(k in lower for k in keywords):
            chosen.append(link)
    return chosen[:8]


def unique_preserve(items: list[str]) -> list[str]:
    out = []
    seen = set()
    for item in items:
        norm = item.strip()
        if not norm or norm in seen:
            continue
        seen.add(norm)
        out.append(norm)
    return out


def clean_snippet(text: str, max_len: int = 220) -> str:
    s = html_lib.unescape(text or "")
    s = s.replace("·", " ")
    s = re.sub(r"\s{2,}", " ", s).strip(" -")
    if len(s) > max_len:
        s = s[:max_len].rstrip() + "..."
    return s


def is_simple_ascending_sequence(digits: str) -> bool:
    # Reject values like "12345678910" that come from UI lists, not phones.
    if not digits.startswith("123456789"):
        return False
    return digits in ("12345678910", "123456789", "1234567890")


def clean_phone_candidates(candidates: list[str]) -> list[str]:
    cleaned = []
    for raw in candidates:
        p = raw.strip()
        digits = re.sub(r"\D", "", p)
        if len(digits) < 8 or len(digits) > 15:
            continue
        # skip date-like strings accidentally captured as phone numbers
        if re.search(r"\b(19|20)\d{2}\b", p) and ("+" not in p):
            continue
        if is_simple_ascending_sequence(digits):
            continue
        cleaned.append(p)
    return unique_preserve(cleaned)


def extract_broker_contacts_from_agent_pages(agent_pages: list[str]) -> list[dict]:
    brokers = []
    for page in agent_pages:
        html = fetch_html(page)
        if not html:
            continue
        text = html_to_text(html)
        emails = unique_preserve(EMAIL_RE.findall(text))
        phones = clean_phone_candidates(PHONE_RE.findall(text))

        # Name guess priority: URL slug -> title
        slug = Path(urlparse(page).path).name.replace("-", " ").strip()
        title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else ""
        name_guess = slug.title() if slug else title[:120]
        if not name_guess:
            name_guess = page
        name_guess = clean_snippet(name_guess, 120)
        if len(name_guess.split()) < 2:
            continue
        if re.search(r"\b(real estate|properties|brokerage)\b", name_guess, re.IGNORECASE):
            continue

        # Keep only useful broker entries.
        if not emails and not phones:
            continue
        brokers.append(
            {
                "name_or_role": name_guess,
                "emails": emails[:3],
                "phones": phones[:3],
            }
        )
    return brokers[:20]


def parse_whois(domain: str) -> DomainWhois:
    """
    Uses system whois if available.
    """
    try:
        proc = subprocess.run(
            ["whois", domain],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
        if not raw.strip():
            return DomainWhois()

        def pick(patterns: list[str]) -> str:
            for p in patterns:
                m = re.search(p, raw, re.IGNORECASE)
                if m:
                    return m.group(1).strip()
            return "unknown"

        return DomainWhois(
            creation_date=pick([
                r"Creation Date:\s*(.+)",
                r"Registered On:\s*(.+)",
                r"Domain Create Date:\s*(.+)",
            ]),
            updated_date=pick([
                r"Updated Date:\s*(.+)",
                r"Last Updated On:\s*(.+)",
            ]),
            expiry_date=pick([
                r"Registry Expiry Date:\s*(.+)",
                r"Expiry Date:\s*(.+)",
                r"Registrar Registration Expiration Date:\s*(.+)",
            ]),
            registrar=pick([
                r"Registrar:\s*(.+)",
                r"Sponsoring Registrar:\s*(.+)",
            ]),
            raw_exists=True,
        )
    except Exception:
        return DomainWhois()


def estimate_website_age(creation_date: str) -> str:
    if creation_date == "unknown":
        return "unknown"
    # extract YYYY-MM-DD-ish prefix
    m = re.search(r"(\d{4})[-/](\d{2})[-/](\d{2})", creation_date)
    if not m:
        return "unknown"
    try:
        dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        years = (now - dt).days // 365
        return f"{years}+ years"
    except Exception:
        return "unknown"


def collect_company_info(name: str, website: str) -> dict:
    homepage_html = fetch_html(website)
    homepage_text = html_to_text(homepage_html)
    links = extract_links(homepage_html, website)
    extra_pages = pick_contact_like_pages(links)

    all_text_parts = [homepage_text]
    for page in extra_pages:
        html = fetch_html(page)
        if html:
            all_text_parts.append(html_to_text(html))
    corpus = "\n".join(all_text_parts)

    emails = unique_preserve(EMAIL_RE.findall(corpus))
    phones = clean_phone_candidates(PHONE_RE.findall(corpus))
    socials = unique_preserve([s.rstrip(".,;") for s in SOCIAL_RE.findall(homepage_html + "\n" + corpus)])
    location_links = unique_preserve(
        [s.rstrip(".,;") for s in LOCATION_LINK_RE.findall(homepage_html + "\n" + corpus)]
    )
    contact_page = next((p for p in extra_pages if "contact" in p.lower()), "not found")

    # Address/location extraction
    address_candidates = []
    location_signals = []
    location_terms = [m.lower() for m in ["Hurghada", "El Gouna", "Sahl Hasheesh", "Soma Bay", "Makadi Bay", "Red Sea", "Egypt"]]
    address_re = re.compile(r"(street|st\.|road|rd\.|avenue|ave\.|building|tower|floor|district|compound|city|country|zip|postal)", re.IGNORECASE)
    chunks = re.split(r"(?<=[.!?])\s+", corpus)
    for ch in chunks:
        snippet = clean_snippet(ch)
        lower = snippet.lower()
        has_location = any(t in lower for t in location_terms)
        if address_re.search(snippet) and (re.search(r"\d", snippet) or "," in snippet):
            address_candidates.append(snippet)
        elif has_location:
            location_signals.append(snippet)
    address_candidates = unique_preserve(address_candidates)[:5]
    location_signals = unique_preserve(location_signals)[:8]

    about_summary = "not found"
    about_page = next((p for p in extra_pages if "about" in p.lower()), None)
    if about_page:
        about_text = html_to_text(fetch_html(about_page))
        if about_text:
            sentences = re.split(r"(?<=[.!?])\s+", about_text)
            useful = [clean_snippet(s, 280) for s in sentences if 50 <= len(s.strip()) <= 320]
            if useful:
                about_summary = useful[0]
    if about_summary == "not found" and homepage_text:
        sentences = re.split(r"(?<=[.!?])\s+", homepage_text)
        useful = [clean_snippet(s, 280) for s in sentences if 50 <= len(s.strip()) <= 320]
        if useful:
            about_summary = useful[0]

    agent_pages = [p for p in extra_pages if "/agent/" in p.lower()]
    brokers = extract_broker_contacts_from_agent_pages(agent_pages)

    domain = urlparse(website).netloc.lower().replace("www.", "")
    whois = parse_whois(domain)
    website_age = estimate_website_age(whois.creation_date)

    return {
        "company_name": name,
        "website": website,
        "domain": domain,
        "emails": emails[:15],
        "phones": phones[:15],
        "social_media": socials[:20],
        "location_links": location_links[:12],
        "contact_page": contact_page,
        "address_candidates": address_candidates,
        "location_signals": location_signals,
        "about_us": about_summary,
        "whois": whois,
        "website_age_estimate": website_age,
        "contact_like_pages": extra_pages,
        "brokers": brokers,
    }


def render_info_md(comp: dict, details: dict) -> str:
    whois: DomainWhois = details["whois"]
    lines = [
        f"# {details['company_name']}",
        "",
        "## Company Profile",
        "",
        f"- **Name:** {details['company_name']}",
        f"- **Website:** {details['website']}",
        f"- **Primary Markets:** {', '.join(comp.get('primary_markets', [])) or 'unknown'}",
        f"- **Segment:** {comp.get('segment', 'unknown')}",
        "",
        "## About Us",
        "",
        f"- {details.get('about_us', 'not found')}",
        "",
        "## Contact Information",
        "",
        f"- **Phone(s):** {', '.join(details['phones']) if details['phones'] else 'not found'}",
        f"- **Email(s):** {', '.join(details['emails']) if details['emails'] else 'not found'}",
        f"- **Contact Page:** {details.get('contact_page', 'not found')}",
        "",
        "## Address",
        "",
    ]

    if details["address_candidates"]:
        lines.extend([f"- {x}" for x in details["address_candidates"]])
    else:
        lines.append("- No clear street address parsed from public pages.")

    lines.extend([
        "",
        "## Location Signals",
        "",
    ])
    if details.get("location_signals"):
        lines.extend([f"- {x}" for x in details["location_signals"]])
    else:
        lines.append("- No extra location signals parsed.")

    lines.extend([
        "",
        "## Location Links",
        "",
    ])
    if details.get("location_links"):
        lines.extend([f"- {x}" for x in details["location_links"]])
    else:
        lines.append("- not found")

    lines.extend([
        "",
        "## Social Media",
        "",
    ])
    if details["social_media"]:
        lines.extend([f"- {x}" for x in details["social_media"]])
    else:
        lines.append("- not found")

    lines.extend([
        "",
        "## Website / Domain Intelligence",
        "",
        f"- **Domain:** {details['domain']}",
        f"- **Website age estimate:** {details['website_age_estimate']}",
        f"- **WHOIS creation date:** {whois.creation_date}",
        f"- **WHOIS updated date:** {whois.updated_date}",
        f"- **WHOIS expiry date:** {whois.expiry_date}",
        f"- **WHOIS registrar:** {whois.registrar}",
        "",
        "## Broker / Agent Contacts",
        "",
    ])

    if details["brokers"]:
        for idx, b in enumerate(details["brokers"], start=1):
            lines.append(f"### Broker/Agent {idx}")
            lines.append(f"- **Name or role:** {b['name_or_role']}")
            lines.append(f"- **Phones:** {', '.join(b['phones']) if b['phones'] else 'not found'}")
            lines.append(f"- **Emails:** {', '.join(b['emails']) if b['emails'] else 'not found'}")
            lines.append("")
    else:
        lines.append("- No broker list confidently extracted from scanned pages.")
        lines.append("")

    lines.extend([
        "## Source Pages Scanned",
        "",
    ])
    if details["contact_like_pages"]:
        lines.extend([f"- {p}" for p in details["contact_like_pages"]])
    else:
        lines.append("- Homepage only")

    lines.extend([
        "",
        f"_Generated at: {datetime.now(timezone.utc).isoformat()}_",
    ])
    return "\n".join(lines).strip() + "\n"


def run() -> None:
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"Missing competitors index: {INDEX_PATH}")

    index_data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    competitors = index_data.get("competitors", [])

    for comp in competitors:
        slug = comp.get("id") or comp.get("slug")
        name = comp.get("name") or slug or "unknown"
        website = comp.get("website") or comp.get("url")
        if not slug or not website:
            continue

        details = collect_company_info(name, website)
        output = render_info_md(comp, details)
        out_path = project_scraped_dir() / slug / "info.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"updated: {out_path}")


if __name__ == "__main__":
    run()
