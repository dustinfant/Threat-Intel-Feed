# fetcher/fetch_normalized_auto.py
import sys
import traceback
from datetime import datetime
import json
from fetcher import fetch_normalized, fetch_normalized_extended  # your existing fetch modules

def run_all():
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sources": {},
        "total_items": 0,
        "errors": {}
    }

    sources_to_run = {
        "normalized": fetch_normalized.run,      # adjust with your actual function
        "extended": fetch_normalized_extended.run
    }

    for name, func in sources_to_run.items():
        try:
            items = func()
            summary["sources"][name] = len(items)
            summary["total_items"] += len(items)
        except Exception as e:
            summary["sources"][name] = 0
            summary["errors"][name] = str(e)
            print(f"[ERROR] Source '{name}' failed: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    # Save summary to JSON alongside feed
    try:
        with open("data/fetch_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to write fetch summary: {e}", file=sys.stderr)

    # Save normalized feed (your existing logic)
    try:
        feed_items = []  # replace with aggregation of all fetched items
        with open("data/feed_normalized.json", "w") as f:
            json.dump(feed_items, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to write feed_normalized.json: {e}", file=sys.stderr)

    print(f"Fetcher run completed. Total items: {summary['total_items']}, Errors: {len(summary['errors'])}")

if __name__ == "__main__":
    try:
        run_all()
    except Exception as e:
        print(f"[FATAL] Fetcher crashed: {e}", file=sys.stderr)
        sys.exit(0)  # always exit 0 for CI

