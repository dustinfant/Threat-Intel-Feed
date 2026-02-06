import feedparser
import requests
import yaml
import json
import os
import bleach
from datetime import datetime
from bs4 import BeautifulSoup

DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "feed_normalized.json")
SOURCES_FILE = "sources.yaml"

ALLOWED_TAGS = [
    "p", "ul", "ol", "li", "strong", "em", "b", "i", "a", "code", "pre", "br"
]

ALLOWED_ATTRS = {
    "a": ["href", "title", "target"]
}

def sanitize_html(html):
    if not html:
        return ""
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True
    )
    return cleaned

def load_sources():
    with open(SOURCES_FILE, "r") as f:
        return yaml.safe_load(f)

def fetch_feed(source):
    print(f"[*] Fetching {source['name']}…")
    entries = []

    feed = feedparser.parse(source["url"])
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "")

        raw_summary = (
            entry.get("summary") or
            entry.get("description") or
            ""
        )

        # Normalize summary text
        soup = BeautifulSoup(raw_summary, "html.parser")
        normalized_html = str(soup)

        summary = sanitize_html(normalized_html)

        published = entry.get("published", "")
        tags = [t.term for t in entry.get("tags", [])] if "tags" in entry else []

        entries.append({
            "source": source["name"],
            "category": source["category"],
            "title": title,
            "link": link,
            "summary": summary,
            "published": published,
            "tags": tags or ["News"]
        })

    return entries

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    sources = load_sources()

    all_entries = []

    print("[*] Starting normalized fetch")

    for source in sources:
        try:
            entries = fetch_feed(source)
            all_entries.extend(entries)
        except Exception as e:
            print(f"[!] Failed to fetch {source['name']}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    print(f"[+] Wrote {len(all_entries)} entries to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

