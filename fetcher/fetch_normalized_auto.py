# fetcher/fetch_normalized_auto.py

def run_all():
    total_sources = 0
    total_iocs = 0

    sources = ["source1", "source2", "source3"]  # replace with actual sources
    for source in sources:
        try:
            # Replace this with your actual fetch call
            iocs = fetch_source(source)  
            total_iocs += len(iocs)
            total_sources += 1
            print(f"[+] Fetched {len(iocs)} indicators from {source}")
        except Exception as e:
            print(f"[!] Error fetching {source}: {e}")

    print("\n--- Summary ---")
    print(f"Total sources fetched: {total_sources}")
    print(f"Total indicators fetched: {total_iocs}")

