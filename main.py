import argparse
from datetime import datetime
from lib.run import NitterTwitterScraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate actions on Nitter.")
    parser.add_argument("--key", type=str, required=True, help="Search key for Nitter (e.g., 'Python').")
    parser.add_argument("--start", type=str, default="", help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end", type=str, default="", help="End date in YYYY-MM-DD format.")
    parser.add_argument("--lang", type=str.lower, default="", choices=["indonesia"], help="Language to search in. Default is 'all'.")

    args = parser.parse_args()

    # Check if start and end are provided, otherwise set default values
    if not args.start:
        args.start = ""

    if not args.end:
        args.end = ""

    NitterTwitterScraper.run_scraper(args.key, args.start, args.end, args.lang)