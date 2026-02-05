# Threat Intel Feed

**Threat Intel Feed** is a Python Flask application that aggregates the latest cybersecurity news and threat intelligence from multiple sources. It fetches RSS feeds, normalizes them, and displays the latest article titles, summaries, and publication dates in a clean dashboard.

## Features

- Aggregates multiple threat intelligence sources (Dark Reading, The Hacker News, Krebs on Security, CISA Alerts, SANS ISC, Unit 42, CrowdStrike, Proofpoint, etc.)
- Shows the latest article title, summary, and published date
- Categorized by type (General, Investigative, Government, Research, Vendor)
- Dark-themed dashboard for easy reading
- Automated fetching and normalization of RSS feeds

## Installation

bash
git clone git@github.com:dustinfant/Threat-Intel-Feed.git
cd Threat-Intel-Feed
pip install -r requirements.txt

## Usage

Fetch the latest feeds:

python fetcher/fetch_normalized.py

Start the Flask dashboard:

python app.py

Open your browser at http://localhost:5052
