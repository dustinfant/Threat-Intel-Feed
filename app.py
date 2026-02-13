from flask import Flask, render_template, jsonify, send_file
import json
import os
import csv
import io
import uuid
import datetime
from urllib.parse import urlparse

app = Flask(__name__)

DATA_FILE = "data/feed_normalized.json"

IOC_FIELDS = [
    "ip",
    "domain",
    "email",
    "md5",
    "sha1",
    "sha256",
    "file_path",
    "service",
    "cve"
]

# -------------------------
# Helpers
# -------------------------
def load_feed():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def group_by_category(feed):
    grouped = {}
    sources = set()
    for entry in feed:
        grouped.setdefault(entry.get("category", "Unknown"), []).append(entry)
        sources.add(entry.get("source", "Unknown"))
    return grouped, sorted(sources)

def has_real_iocs(entry):
    return any(entry.get("iocs", {}).get(f) for f in IOC_FIELDS)

def get_article_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    feed = load_feed()
    grouped, sources = group_by_category(feed)
    return render_template("index.html", grouped=grouped, sources=sources)

@app.route("/api/feed")
def api_feed():
    return jsonify(load_feed())

# -------------------------
# CSV EXPORT
# -------------------------
@app.route("/export/csv")
def export_csv():
    feed = load_feed()
    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=["title", "source", "link"] + IOC_FIELDS
    )
    writer.writeheader()

    for entry in feed:
        if not has_real_iocs(entry):
            continue

        article_domain = get_article_domain(entry.get("link", ""))

        row = {
            "title": entry.get("title", ""),
            "source": entry.get("source", ""),
            "link": entry.get("link", "")
        }

        for field in IOC_FIELDS:
            values = entry.get("iocs", {}).get(field, [])

            # 🔥 CRITICAL FIX: remove article domain from domain IOCs
            if field == "domain":
                values = [
                    d for d in values
                    if article_domain not in d.lower()
                ]

            row[field] = "; ".join(values)

        writer.writerow(row)

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="ioc_export.csv"
    )

# -------------------------
# STIX EXPORT
# -------------------------
@app.route("/export/stix")
def export_stix():
    feed = load_feed()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    objects = []

    for entry in feed:
        if not has_real_iocs(entry):
            continue

        article_domain = get_article_domain(entry.get("link", ""))

        for ioc_type, values in entry.get("iocs", {}).items():
            if ioc_type not in IOC_FIELDS:
                continue

            for value in values:
                if ioc_type == "domain" and article_domain in value.lower():
                    continue

                objects.append({
                    "type": "indicator",
                    "spec_version": "2.1",
                    "id": f"indicator--{uuid.uuid4()}",
                    "created": now,
                    "modified": now,
                    "name": f"{ioc_type.upper()} Indicator",
                    "indicator_types": ["malicious-activity"],
                    "pattern": f"[{ioc_type}:value = '{value}']",
                    "pattern_type": "stix",
                    "valid_from": now
                })

    bundle = {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid4()}",
        "objects": objects
    }

    return send_file(
        io.BytesIO(json.dumps(bundle, indent=2).encode("utf-8")),
        mimetype="application/json",
        as_attachment=True,
        download_name="ioc_export.stix.json"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5052, debug=False)

