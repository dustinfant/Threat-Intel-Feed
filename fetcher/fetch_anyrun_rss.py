import feedparser
import json
import os
from datetime import datetime

DATA_FILE = "../data/feed_normalized.json"
ANYRUN_RSS = "https://any.run/cybersecurity-blog/rss/"

def fetch_anyrun():
    feed = feedparser.parse(ANYRUN_RSS)
    normalized = []

    for entry in feed.entries:
        normalized.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source": "ANY.RUN",
            "category": entry.get("tags", [{}])[0].get("term", "Uncategorized") if entry.get("tags") else "Uncategorized",
            "iocs": {}  # Can fill later if you parse content
        })
    return normalized

def update_feed():
    existing = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)

    new_entries = fetch_anyrun()
    combined = existing + new_entries

    # Optional: remove duplicates by link
    seen_links = set()
    deduped = []
    for e in combined:
        if e["link"] not in seen_links:
            deduped.append(e)
            seen_links.add(e["link"])

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2)

if __name__ == "__main__":
    update_feed()
