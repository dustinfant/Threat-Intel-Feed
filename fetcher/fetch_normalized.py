import json
import feedparser
import os
import yaml
from html import unescape
import re

SOURCES_FILE = os.path.join(os.path.dirname(__file__), "..", "sources.yaml")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "feed_normalized.json")

def load_sources():
    if not os.path.exists(SOURCES_FILE):
        print(f"Sources file not found: {SOURCES_FILE}")
        return []
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = yaml.safe_load(f)
    return sources

def clean_html(raw_html):
    """Remove HTML tags and unescape entities."""
    if not raw_html:
        return "No description available"
    text = re.sub('<[^<]+?>', '', raw_html)  # strip tags
    return unescape(text).strip()

def fetch_feed(url):
    d = feedparser.parse(url)
    items = []
    for entry in d.entries[:5]:  # latest 5 articles
        summary = entry.get("summary", "") or entry.get("description", "")
        clean_summary = clean_html(summary)
        # Optionally truncate long summaries
        if len(clean_summary) > 400:
            clean_summary = clean_summary[:400] + "..."
        items.append({
            "title": entry.get("title", "No title"),
            "summary": clean_summary,
            "published": entry.get("published", ""),
            "link": entry.get("link", "#")
        })
    return items

def main():
    sources = load_sources()
    all_feeds = []

    for source in sources:
        url = source.get("url")
        category = source.get("category", "Uncategorized")
        if not url:
            continue
        articles = fetch_feed(url)
        for a in articles:
            feed_item = a.copy()
            feed_item["category"] = category
            feed_item["site"] = source.get("name", "Unnamed")
            all_feeds.append(feed_item)
        print(f"Fetched {len(articles)} items from {source.get('name')}")

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_feeds, f, indent=2)
    print(f"All feeds saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

