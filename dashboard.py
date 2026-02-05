#!/usr/bin/env python3
from flask import Flask, render_template
import json
import os

app = Flask(__name__)

FEED_FILE = "data/feed_normalized.json"

# -------------------------
# Load feed
# -------------------------
def load_feed():
    if os.path.exists(FEED_FILE):
        with open(FEED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# -------------------------
# Group feed by category
# -------------------------
def group_by_category(feed):
    categories = {}
    for item in feed:
        cat = item.get("category", "uncategorized")
        categories.setdefault(cat, []).append(item)
    return categories

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    feed = load_feed()
    grouped = group_by_category(feed)
    return render_template("index.html", grouped=grouped)

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5052, debug=True)

