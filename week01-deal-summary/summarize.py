import csv


def load_deals(path):
    """Read a CSV of deals and return a list of dicts with numeric amounts."""
    deals = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row["amount"] = int(row["amount"])  # convert text to a number as we load
            deals.append(row)
    return deals  # hand the finished list back to whoever called this function


def group_totals(deals, field):
    """Total the deal amounts by any field: stage, rep, vendor, account..."""
    totals = {}
    for deal in deals:
        key = deal[field]  # field is a parameter, so this one loop works for every grouping
        totals[key] = totals.get(key, 0) + deal["amount"]
    return totals


def print_ranked(title, totals):
    """Print a {name: amount} dictionary, largest first."""
    print(f"\n{title}")
    for name, value in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"  {name:<14} ${value:>9,}")


def print_summary(deals):
    open_deals = [d for d in deals if not d["stage"].startswith("Closed")]
    closed_deals = [d for d in deals if d["stage"].startswith("Closed")]
    won_deals = [d for d in deals if d["stage"] == "Closed Won"]

    total_value = sum(d["amount"] for d in deals)
    # Guard against dividing by zero if nothing has closed yet
    win_rate = len(won_deals) / len(closed_deals) if closed_deals else 0

    print(f"Loaded {len(deals)} deals\n")
    print(f"Total deal value:  ${total_value:,}")
    print(f"Average deal size: ${total_value / len(deals):,.0f}")
    print(f"Open pipeline:     ${sum(d['amount'] for d in open_deals):,} across {len(open_deals)} deals")
    print(f"Closed won:        ${sum(d['amount'] for d in won_deals):,} across {len(won_deals)} deals")
    print(f"Win rate:          {win_rate:.0%} ({len(won_deals)} of {len(closed_deals)} closed deals)")

    print_ranked("Pipeline by stage", group_totals(deals, "stage"))
    print_ranked("Open pipeline by rep", group_totals(open_deals, "rep"))
    print_ranked("Open pipeline by vendor", group_totals(open_deals, "vendor"))


def main():
    deals = load_deals("deals.csv")
    print_summary(deals)


# Run main() only when this file is executed directly, not when another script imports it
if __name__ == "__main__":
    main()