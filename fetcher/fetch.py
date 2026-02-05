#!/usr/bin/env python3
"""
Threat Intel Feed Fetcher
Python 3 compatible, UTF-8 safe, parses RSS + HTML headlines.
"""

import yaml
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

SOURCES_FILE = "sources.yaml"
OUTPUT_FILE = "data/feed.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5"
}

# -------------------------
# Load sources from YAML
# -------------------------
def load_sources():
    with open(SOURCES_FILE, "r") as f:
        data = yaml.safe_load(f)
        return data.get("sources", [])

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

    for item in channel.findall("item")[:5]:  # only top 5
        title = item.findtext("title")
        link = item.findtext("link")
        description = item.findtext("description")

        items.append({
            "title": title,
            "link": link,
            "summary": description
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
            headlines.append({
                "title": text,
                "link": None,
                "summary": None
            })
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

    return entry

# -------------------------
# Main
# -------------------------
def main():
    feed = []
    sources = load_sources()

    for src in sources:
        feed.append(fetch_source(src))

    # Python 3 UTF-8 safe write
    with io.open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)

    print("[+] Wrote {}".format(OUTPUT_FILE))

if __name__ == "__main__":
    main()

