#!/usr/bin/env python3
"""
Threat Intel Feed Normalized Fetcher - Auto Merge
Python 3 compatible, UTF-8 safe, deduplicated, normalized feed items.
Automatically merges extended default sources with user sources.yaml.
"""

import os
import yaml
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import io

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

OUTPUT_FILE = "data/feed_normalized.json"
SOURCES_FILE = "sources.yaml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5"
}

# -------------------------
# Default extended sources
# -------------------------
DEFAULT_SOURCES = [
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "category": "general", "type": "rss"},
    {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "category": "general", "type": "rss"},
    {"name": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/", "category": "general", "type": "rss"},
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "category": "investigative", "type": "rss"},
    {"name": "CISA Alerts", "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml", "category": "government", "type": "rss"},
    {"name": "SANS ISC", "url": "https://isc.sans.edu/rssfeed.xml", "category": "research", "type": "rss"},
    {"name": "Palo Alto Unit 42", "url": "https://unit42.paloaltonetworks.com/feed/", "category": "research", "type": "rss"},
    {"name": "Secureworks CTU", "url": "https://www.secureworks.com/blog/feed/", "category": "research", "type": "rss"},
    {"name": "Mandiant Blog", "url": "https://www.mandiant.com/resources/blog/feed", "category": "vendor", "type": "rss"},
    {"name": "CrowdStrike Blog", "url": "https://www.crowdstrike.com/blog/feed/", "category": "vendor", "type": "rss"},
    {"name": "Proofpoint Blog", "url": "https://www.proofpoint.com/us/rss.xml", "category": "vendor", "type": "rss"},
]

# -------------------------
# Load user sources from YAML
# -------------------------
def load_user_sources():
    """
    Load user sources from the YAML/JSON config file.
    Handles both:
      - a dictionary with a "sources" key
      - a list at the top level
    """
    import yaml  # or json if using JSON
    with open("config.yml", "r") as f:  # replace with your actual config file path
        data = yaml.safe_load(f)

    if isinstance(data, list):
        return data  # top-level list

    if isinstance(data, dict):
        return data.get("sources", [])  # dict with "sources" key

    return []  # fallback


# -------------------------
# Merge sources
# -------------------------
def merge_sources(defaults, users):
    merged = { (s['name'], s['url']): s for s in defaults }
    for s in users:
        key = (s['name'], s['url'])
        merged[key] = s  # user source overrides if duplicate
    return list(merged.values())

# -------------------------
# RSS Parsing
# -------------------------
def parse_rss(xml_text):
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    channel = root.find("channel")
    if channel is None:
        return items

    for item in channel.findall("item")[:5]:
        items.append({
            "title": item.findtext("title"),
            "link": item.findtext("link"),
            "summary": item.findtext("description")
        })
    return items

# -------------------------
# HTML Headline Parsing
# -------------------------
def parse_html(html):
    if not HAS_BS4:
        return []

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
        tag.decompose()

    headlines = []
    seen = set()
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(" ", strip=True)
        if text and 40 <= len(text) <= 160 and text not in seen:
            headlines.append({"title": text, "link": None, "summary": None})
            seen.add(text)
        if len(headlines) >= 5:
            break
    return headlines

# -------------------------
# Fetch single source
# -------------------------
def fetch_source(src):
    entry = {
        "name": src.get("name"),
        "url": src.get("url"),
        "category": src.get("category", "uncategorized"),
        "type": src.get("type", "html"),
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }

    try:
        r = requests.get(src.get("url"), headers=HEADERS, timeout=20)
        entry["status"] = r.status_code
        entry["content_length"] = len(r.text)
        if entry["type"] == "rss":
            entry["items"] = parse_rss(r.text)
        else:
            entry["items"] = parse_html(r.text)
    except Exception as e:
        entry["error"] = str(e)
        entry["items"] = []

    return entry

# -------------------------
# Normalize feed items
# -------------------------
def normalize_feed(feed):
    normalized = []
    seen = set()
    for src in feed:
        for item in src.get("items", []):
            key = (item.get("title"), item.get("link"))
            if key in seen or not item.get("title"):
                continue
            seen.add(key)
            normalized.append({
                "source": src.get("name"),
                "category": src.get("category"),
                "title": item.get("title"),
                "link": item.get("link"),
                "summary": item.get("summary")
            })
    return normalized

# -------------------------
# Main
# -------------------------
def main():
    user_sources = load_user_sources()
    sources = merge_sources(DEFAULT_SOURCES, user_sources)

    feed = [fetch_source(src) for src in sources]
    normalized_feed = normalize_feed(feed)

    os.makedirs("data", exist_ok=True)
    with io.open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized_feed, f, indent=2, ensure_ascii=False)

    print("[+] Wrote normalized feed: {}".format(OUTPUT_FILE))
    print("[+] Total items:", len(normalized_feed))
    print("[+] Total sources fetched:", len(sources))

if __name__ == "__main__":
    main()

