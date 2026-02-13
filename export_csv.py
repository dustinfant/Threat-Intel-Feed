#!/usr/bin/env python3

import json
import csv
from pathlib import Path

# Input stays where normalized data already lives
INPUT_FILE = Path("data/feed_normalized.json")

# Output goes to project root
OUTPUT_FILE = Path("feed_iocs_only.csv")

IOC_FIELDS = ["ip", "domain", "url", "md5", "sha1", "sha256", "email"]

def has_real_iocs(entry):
    iocs = entry.get("iocs", {})
    return any(iocs.get(field) for field in IOC_FIELDS)

def normalize_iocs(iocs):
    return {
        field: ";".join(sorted(set(iocs.get(field, []))))
        for field in IOC_FIELDS
    }

def main():
    with INPUT_FILE.open(encoding="utf-8") as f:
        feed = json.load(f)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "source", "link"] + IOC_FIELDS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        exported = 0

        for entry in feed:
            # 🔥 Skip entries with zero IOCs
            if not has_real_iocs(entry):
                continue

            row = {
                "title": entry.get("title", ""),
                "source": entry.get("source", ""),
                "link": entry.get("link", "")
            }

            row.update(normalize_iocs(entry.get("iocs", {})))
            writer.writerow(row)
            exported += 1

    print(f"[+] Exported {exported} IOC-bearing entries to ./{OUTPUT_FILE.name}")

if __name__ == "__main__":
    main()

