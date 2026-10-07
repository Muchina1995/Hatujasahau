"""
Fetch recent High Court (KEHC) judgments from Kenya Law and store a
filtered, deduplicated JSON file for the Hatujasahau corruption tracker.

Run on a schedule via GitHub Actions (see .github/workflows/fetch-judgments.yml).
Designed to be safe to run repeatedly: it stops paging once it reaches
judgments already saved from a previous run, and never overwrites history --
only appends new entries.

IMPORTANT — this is a first-pass script, not a finished one:
Kenya Law's HTML structure was inspected via extracted page text, not raw
source. The CSS selectors below are best-effort guesses at a reasonable
structure. Before relying on this in production:
  1. Open https://new.kenyalaw.org/judgments/KEHC/ in a browser, view source
     or use dev tools, and confirm the actual tag/class names around each
     judgment link.
  2. Adjust `parse_listing_page()` accordingly.
  3. Check https://new.kenyalaw.org/robots.txt and Kenya Law's terms of use
     before scraping at any real frequency, and keep the delay between
     requests -- don't remove REQUEST_DELAY_SECONDS.
"""

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://new.kenyalaw.org"
COURT_CODE = "KEHC"  # High Court. Other codes: KESC (Supreme Court),
                      # KECA (Court of Appeal), KEELRC, KEELC.
LISTING_URL = f"{BASE_URL}/judgments/{COURT_CODE}/"

OUTPUT_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "kehc-judgments.json"

MAX_PAGES_PER_RUN = 5          # safety cap so a single run can't crawl forever
REQUEST_DELAY_SECONDS = 2.0    # be polite -- don't hammer a government site

# Case titles are matched (case-insensitive) against these keywords to decide
# whether a judgment is relevant to the corruption tracker. Adjust freely.
CORRUPTION_KEYWORDS = [
    "corruption",
    "anti-corruption",
    "eacc",
    "ethics and anti-corruption",
    "bribery",
    "abuse of office",
    "unexplained assets",
    "economic crimes",
    "procurement",
    "public funds",
    "fraud",
]

USER_AGENT = (
    "HatujasahauBot/0.1 (+https://hatujasahau.org; "
    "civic accountability tracker; contact via site contact form)"
)

# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------

def fetch_page(url: str, params: dict | None = None) -> BeautifulSoup | None:
    """Fetch a page and return parsed HTML, or None on failure."""
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  [warn] request failed for {url}: {exc}", file=sys.stderr)
        return None
    return BeautifulSoup(resp.text, "html.parser")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

# A judgment detail link looks like:
#   /akn/ke/judgment/kehc/2026/1612/eng@2026-02-13
# Capture the trailing date for sorting/display.
JUDGMENT_LINK_RE = re.compile(r"^/akn/ke/judgment/[a-z]+/\d{4}/\d+/eng@(\d{4}-\d{2}-\d{2})$")


def parse_listing_page(soup: BeautifulSoup) -> list[dict]:
    """
    Extract judgment entries from a listing page.

    Best-effort approach: find every <a> whose href matches the Akoma Ntoso
    judgment URL pattern, and use its link text as the citation/title. This
    is resilient to unknown wrapper markup, at the cost of not capturing
    extra metadata (e.g. outcome, judge) that may sit in sibling elements.
    Once you've inspected the real HTML, prefer targeting the actual
    listing-item container for cleaner extraction.
    """
    entries = []
    seen_urls = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        match = JUDGMENT_LINK_RE.match(href)
        if not match:
            continue

        full_url = BASE_URL + href
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        title_text = link.get_text(strip=True)
        if not title_text:
            continue

        entries.append(
            {
                "citation": title_text,
                "url": full_url,
                "date": match.group(1),
                "court": COURT_CODE,
            }
        )

    return entries


def matches_keywords(entry: dict) -> bool:
    text = entry["citation"].lower()
    return any(keyword in text for keyword in CORRUPTION_KEYWORDS)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

def load_existing() -> dict:
    if not OUTPUT_FILE.exists():
        return {"last_updated": None, "judgments": []}
    with OUTPUT_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save(data: dict) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    existing = load_existing()
    known_urls = {j["url"] for j in existing["judgments"]}

    new_entries = []
    page = 1

    while page <= MAX_PAGES_PER_RUN:
        print(f"Fetching page {page}: {LISTING_URL}")
        soup = fetch_page(LISTING_URL, params={"page": page})
        if soup is None:
            break

        page_entries = parse_listing_page(soup)
        if not page_entries:
            print("  No judgment links found on this page -- stopping.")
            break

        relevant = [e for e in page_entries if matches_keywords(e)]
        genuinely_new = [e for e in relevant if e["url"] not in known_urls]

        print(f"  {len(page_entries)} judgments seen, {len(relevant)} keyword matches, "
              f"{len(genuinely_new)} new")

        new_entries.extend(genuinely_new)

        # Listings are sorted newest-first. If every entry on this page was
        # already known, older pages will be too -- stop paging.
        all_already_known = all(e["url"] in known_urls for e in page_entries)
        if all_already_known:
            print("  Reached previously-seen judgments -- stopping pagination.")
            break

        page += 1
        time.sleep(REQUEST_DELAY_SECONDS)

    if not new_entries:
        print("No new corruption-related judgments found.")
        return

    existing["judgments"] = new_entries + existing["judgments"]
    existing["last_updated"] = datetime.now(timezone.utc).isoformat()
    save(existing)
    print(f"Saved {len(new_entries)} new entries to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
