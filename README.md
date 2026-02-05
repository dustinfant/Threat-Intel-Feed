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

<img width="1907" height="1009" alt="Screenshot from 2026-02-05 12-32-43" src="https://github.com/user-attachments/assets/80a3472b-8cfd-47d5-874f-bd253068358d" />
![Screenshot from 2026-02-05 12-32-49](https://github.com/user-attachments/assets/b011c98a-6f1a-402c-81f8-4bc4bf64fddd)
<img width="1920" height="1008" alt="Screenshot from 2026-02-05 12-32-49" src="https://github.com/user-attachments/assets/8718d23c-ca08-4e22-a11b-6b391609ed74" />
<img width="1920" height="1008" alt="Screenshot from 2026-02-05 12-32-52" src="https://github.com/user-attachments/assets/8d1d2599-0b56-4ad6-bdf1-2d84a2f83337" />
<img width="1920" height="1010" alt="Screenshot from 2026-02-05 12-32-56" src="https://github.com/user-attachments/assets/32d8a4ef-99a2-4d76-8860-856aaecb3813" />
<img width="1920" height="1007" alt="Screenshot from 2026-02-05 12-33-00" src="https://github.com/user-attachments/assets/fb1d6611-4aec-44e6-9c67-fd43c3d06457" />
