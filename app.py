import json
from flask import Flask, render_template
import os

app = Flask(__name__)
DATA_FILE = os.path.join("data", "feed_normalized.json")

def load_feeds():
    if not os.path.exists(DATA_FILE):
        return {}, []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        feeds = json.load(f)

    grouped = {}
    sources_set = set()

    for feed in feeds:
        if not isinstance(feed, dict):
            continue
        category = feed.get("category", "Uncategorized").title()
        grouped.setdefault(category, []).append(feed)

        source = feed.get("source")
        if source:
            sources_set.add(source)

    # Sort sources alphabetically
    sources_list = sorted(sources_set)
    return grouped, sources_list

@app.route("/")
def index():
    grouped, sources = load_feeds()
    return render_template("index.html", grouped=grouped, sources=sources)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5052)

