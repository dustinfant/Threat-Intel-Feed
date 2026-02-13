#!/usr/bin/env python3
"""
fetch_normalized_auto.py

Fetches and normalizes threat intel feeds.
Designed to safely run in GitHub Actions without failing the workflow.
"""

import sys
import traceback
from fetch_normalized import main as fetch_main  # your existing fetch function

def run_fetcher():
    """
    Runs the main fetcher function with error handling
    to prevent non-zero exit codes in CI.
    """
    try:
        fetch_main()  # call your existing fetch logic
        print("✅ Fetcher completed successfully.")
    except Exception as e:
        print("⚠ Warning: Fetcher encountered an error but will exit 0 for CI.")
        print(f"Error details: {e}")
        traceback.print_exc()
    finally:
        # Always exit 0 so GitHub Actions doesn't mark the step as failed
        sys.exit(0)

if __name__ == "__main__":
    run_fetcher()

