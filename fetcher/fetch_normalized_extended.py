#!/usr/bin/env python3
"""
Threat Intel Feed Normalized Fetcher - Extended Sources
Python 3 compatible, UTF-8 safe, deduplicated, normalized feed items.
Includes many popular threat intel sources automatically.
"""

import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import io  # For UTF-8 safe writes

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

OUTPUT_FILE = "data/feed_normalized.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5"
}

# -------------------------
# Extended sources list
# -------------------------
SOURCES = [
    # General
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "category": "general", "type": "rss"},
    {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "category": "general", "type": "rss"},
    {"name": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/", "category": "general", "type": "rss"},

    # Investigative
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "category": "investigative", "type": "rss"},

    # Government
    {"name": "CISA Alerts", "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml", "category": "government", "type": "rss"},

    # Research
    {"name": "SANS ISC", "url": "https://isc.sans.edu/rssfeed.xml", "category": "research", "type": "rss"},
    {"name": "Palo Alto Unit 42", "url": "https://unit42.paloaltonetworks.com/feed/", "category": "research", "type": "rss"},
    {"name": "Secureworks CTU", "url": "https://www.secureworks.com/blog/feed/", "category": "research", "type": "rss"},

    # Vendors
    {"name": "Mandiant Blog", "url": "https://www.mandiant.com/resources/blog/feed", "category": "vendor", "type": "rss"},
    {"name": "CrowdStrike Blog", "url": "https://www.crowdstrike.com/blog/feed/", "category": "vendor", "type": "rss"},
    {"name": "Proofpoint Blog", "url": "https://www.proofpoint.com/us/rss.xml", "category": "vendor", "type": "rss"},
]

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
    feed = [fetch_source(src) for src in SOURCES]
    normalized_feed = normalize_feed(feed)

    with io.open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized_feed, f, indent=2, ensure_ascii=False)

    print("[+] Wrote normalized feed: {}".format(OUTPUT_FILE))
    print("[+] Total items:", len(normalized_feed))

if __name__ == "__main__":
    main()

