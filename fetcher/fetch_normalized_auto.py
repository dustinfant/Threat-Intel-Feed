# fetcher/fetch_normalized_auto.py

import traceback
from datetime import datetime

def fetch_sources():
    """
    Put your existing fetch logic here.
    Example: fetch from sources.yaml, normalize feeds, save to feed_normalized.json
    """
    # TODO: replace with your actual fetch logic
    print("Fetching feeds from sources...")
    # Simulate a fetch
    # raise ValueError("Simulated fetch error")  # Uncomment to test error handling
    fetched_count = 42  # example
    return fetched_count

def run_all():
    """
    Main entry for GitHub Actions.
    Ensures errors are logged but do not fail the workflow.
    Prints a simple summary at the end.
    """
    start_time = datetime.utcnow()
    print(f"Starting fetch at {start_time.isoformat()} UTC")
    try:
        count = fetch_sources()
        print(f"✅ Successfully fetched {count} items.")
    except Exception as e:
        print("⚠️ Fetcher encountered an error:")
        print(str(e))
        print(traceback.format_exc())
    finally:
        end_time = datetime.utcnow()
        print(f"Fetcher finished at {end_time.isoformat()} UTC")
        duration = (end_time - start_time).total_seconds()
        print(f"Total duration: {duration:.2f}s")

# If someone runs this file directly, call run_all()
if __name__ == "__main__":
    run_all()

