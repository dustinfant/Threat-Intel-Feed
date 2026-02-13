# 🚨🚨🚨 **THREAT INTEL FEED** 🚨🚨🚨


⚡ A Python Flask web dashboard that aggregates and displays
   the latest cybersecurity news from multiple RSS feeds.
   Quickly see titles, summaries, and publication dates of
   top threat intelligence sources.

────────────────────────────────────────────────────────────

📌 Features

• Aggregates multiple threat intelligence sources:
  Dark Reading, The Hacker News, Krebs on Security,
  CISA Alerts, SANS ISC, Unit 42, Huntress, Proofpoint, etc.

• Displays article title, summary, and published date

• Categorized by type: General, Investigative,
  Government, Research, Vendor

• Dark-themed dashboard for easy reading

• Automated fetching and normalization of RSS feeds

• Export feeds to CSV or STIX using `export_csv.py`

────────────────────────────────────────────────────────────

💻 Installation

bash

git clone git@github.com:dustinfant/Threat-Intel-Feed.git

cd Threat-Intel-Feed

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

────────────────────────────────────────────────────────────

🚀 Usage

Fetch and normalize feeds:
python fetcher/fetch_normalized.py

Start the Flask dashboard:
python app.py

Open in your browser at:
http://localhost:5052

────────────────────────────────────────────────────────────

📷 Screenshots

<img width="1920" height="1080" alt="Screenshot from 2026-02-13 15-31-56" src="https://github.com/user-attachments/assets/ea14422c-1454-4008-a6f2-b6c9607d210e" />


<img width="1920" height="1080" alt="Screenshot from 2026-02-13 15-32-00" src="https://github.com/user-attachments/assets/375a6897-ffd2-4801-8347-b3eccb56606b" />


<img width="1920" height="1080" alt="Screenshot from 2026-02-13 15-32-03" src="https://github.com/user-attachments/assets/30fe1e0a-5d3b-4fc8-ab31-4db84898b4b8" />


<img width="1920" height="1080" alt="Screenshot from 2026-02-13 15-32-45" src="https://github.com/user-attachments/assets/befb3160-72b4-406f-b694-0a79001faa6c" />

────────────────────────────────────────────────────────────

🧹 Cleaning & Maintenance

• Ignore cache/log files in .gitignore:

__pycache__/

*.pyc

*.log

data/cache/

*.bak

feed_iocs_only.csv

venv/

• Regularly clear old cached .txt files in data/cache

• Commit only source code, templates, and config files

────────────────────────────────────────────────────────────

📖 About

Threat Intel Feed is a lightweight, organized dashboard to
quickly see top cybersecurity news and threat intelligence
updates from multiple sources — perfect for analysts or
security enthusiasts.
