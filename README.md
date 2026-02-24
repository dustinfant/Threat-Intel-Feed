📡 Threat-Intel-Feed

Threat-Intel-Feed is a Python + Flask application that aggregates, normalizes, and displays up-to-date threat intelligence content from multiple cybersecurity RSS feeds — including research blogs, vendor advisories, and government alerts. The dashboard provides filtering by source and category and also extracts IOCs (IPs, domains, hashes, CVEs) for enrichment and export.

This tool is ideal for SOC analysts, threat hunters, blue teamers, and cybersecurity researchers who want a central intel dashboard without relying on paid platforms.

🧠 Features

✅ Aggregates multiple cybersecurity dashboards in one view

✅ Normalizes RSS feeds into structured JSON data

✅ Extracts Indicators of Compromise (IPs, domains, hashes, CVEs, emails)

✅ Auto-refreshes feeds hourly while the server runs

✅ Filterable UI by source, category, and IOC presence

✅ CSV & STIX export of IOCs

✅ Lightweight Flask-based dashboard


🚀 Screenshots

<img width="1920" height="967" alt="Screenshot from 2026-02-24 14-29-55" src="https://github.com/user-attachments/assets/19272788-6a90-4eee-be43-95823ee87b1a" />


<img width="1920" height="970" alt="Screenshot from 2026-02-24 14-30-09" src="https://github.com/user-attachments/assets/c9d1b7c0-bf45-4837-ad08-2e45b10f3fce" />




📦 Project Structure

<img width="446" height="632" alt="Screenshot from 2026-02-24 14-34-49" src="https://github.com/user-attachments/assets/3d264739-5b1c-4601-b155-f4e40e72296c" />


🛠️ Installation

Clone the repository:

git clone https://github.com/dustinfant/Threat-Intel-Feed.git
cd Threat-Intel-Feed


Install dependencies:

pip install -r requirements.txt
📡 Run the Feed Fetcher

Before starting the dashboard, populate the normalized feed:

python fetcher/fetch_normalized.py

This will pull all configured sources from sources.yaml, extract content, and save to data/feed_normalized.json.


🌐 Start the Dashboard
python app.py

Then open your browser and navigate to:

http://localhost:5052

The dashboard will show articles grouped by category.


🔄 Auto-Refresh & Indicators

While app.py is running:

Feeds are automatically refreshed every hour via APScheduler.

IOCs are extracted from article content and available for export.


📊 Exporting IOCs

CSV Export:

/export/csv

STIX 2.1 Export:

/export/stix
🗂 sources.yaml

Add new sources by editing sources.yaml. Each entry contains:

- name: Some Source
  url: https://example.com/feed.xml
  category: vendor|research|government|general


🧪 Example Feeds Included

Some of the sources currently configured:

ZDNet Security (General)

BleepingComputer (General)

Check Point Research (Vendor)

CISA Alerts (Government)

Reddit r/netsec (Community)
… and more.


🧠 Why This Matters

This project gives you:

A centralized view of disparate cybersecurity feeds

Real-time trending threat intel

Ability to export IOCs for SIEM/EDR ingestion

A portfolio-ready tool that demonstrates automation + threat intel knowledge
