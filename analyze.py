import json
import sys
import os
from collections import Counter
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
DEFAULT_LOG_FILE = "feedback_log.json"


# ── Helpers ───────────────────────────────────────────────────────────────────
def load_logs(filepath: str) -> list:
    """Load and return all log entries from JSON file."""
    if not os.path.exists(filepath):
        print(f"  ❌ Log file not found: '{filepath}'")
        print("  Run agent.py first to generate interactions.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ❌ Malformed JSON in '{filepath}': {e}")
            sys.exit(1)

    if not isinstance(data, list):
        print("  ❌ Log file must contain a JSON array.")
        sys.exit(1)

    return data


def divider(char="─", width=52):
    print(char * width)


# ── Core analysis ─────────────────────────────────────────────────────────────
def analyze(logs: list) -> dict:
    """Run all analysis and return results dict."""
    total = len(logs)
    good_entries = [e for e in logs if e.get("feedback") == "good"]
    bad_entries  = [e for e in logs if e.get("feedback") == "bad"]

    good_count = len(good_entries)
    bad_count  = len(bad_entries)
    pending    = total - good_count - bad_count  # no feedback yet

    # Top 3 failed queries (most repeated bad queries first)
    bad_queries = [e.get("user_input", "").strip() for e in bad_entries]
    top_3_failed = Counter(bad_queries).most_common(3)

    # Additional: satisfaction rate
    rated = good_count + bad_count
    satisfaction = round((good_count / rated) * 100, 1) if rated > 0 else 0.0

    return {
        "total": total,
        "good": good_count,
        "bad": bad_count,
        "pending": pending,
        "satisfaction": satisfaction,
        "top_3_failed": top_3_failed,
        "bad_entries": bad_entries,
    }


# ── Report printer ────────────────────────────────────────────────────────────
def print_report(results: dict, log_file: str) -> None:
    """Print a formatted analysis report to stdout."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print()
    divider("═")
    print("  📊  MEDIBOT — PERFORMANCE ANALYSIS REPORT")
    divider("═")
    print(f"  Log file : {log_file}")
    print(f"  Generated: {now}")
    divider()

    # ── Section 1: Counts ────────────────────────────────────────────────
    print("  RESPONSE COUNTS")
    divider()
    print(f"  Total responses    : {results['total']}")
    print(f"  👍 Good feedback   : {results['good']}")
    print(f"  👎 Bad feedback    : {results['bad']}")
    print(f"  ⏳ Pending/no FB   : {results['pending']}")
    print(f"  Satisfaction rate  : {results['satisfaction']}%")
    divider()

    # ── Section 2: Top 3 failed queries ─────────────────────────────────
    print("  TOP 3 FAILED QUERIES  (received 👎 feedback)")
    divider()

    if not results["top_3_failed"]:
        print("  🎉 No negative feedback recorded. Great job!")
    else:
        for rank, (query, count) in enumerate(results["top_3_failed"], start=1):
            times = "time" if count == 1 else "times"
            # Truncate long queries for display
            display_query = query[:65] + "..." if len(query) > 65 else query
            print(f"  {rank}. \"{display_query}\"")
            print(f"     Failed {count} {times}")
            if rank < len(results["top_3_failed"]):
                print()

    divider()

    # ── Section 3: All failed interactions ──────────────────────────────
    if results["bad_entries"]:
        print("  ALL FAILED INTERACTIONS (for review)")
        divider()
        for i, entry in enumerate(results["bad_entries"], start=1):
            ts = entry.get("timestamp", "unknown")[:19].replace("T", " ")
            q  = entry.get("user_input", "")[:70]
            print(f"  [{i}] {ts}")
            print(f"      Query   : {q}")
            print()

    divider("═")
    print("  END OF REPORT")
    divider("═")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    # Allow optional --file argument
    log_file = DEFAULT_LOG_FILE
    args = sys.argv[1:]
    if "--file" in args:
        idx = args.index("--file")
        if idx + 1 < len(args):
            log_file = args[idx + 1]

    logs = load_logs(log_file)
    results = analyze(logs)
    print_report(results, log_file)

    # Return exit code 1 if bad feedback > 50% (useful in CI pipelines)
    if results["total"] > 0 and results["bad"] / results["total"] > 0.5:
        print("  ⚠️  Warning: more than 50% negative feedback rate.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
