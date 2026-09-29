from tabulate import tabulate

from utils.types import HeaderMatchingScorer, ListOfRecords

# --- Record Viewer ---


def view_records(raw_records: ListOfRecords, title: str | None = None) -> None:
    """Prints an optional title and the first 5 records in the raw records."""
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 50)
    for i, record in enumerate(raw_records[:5]):
        print(f"Record {i + 1}: {record}", "\n")
    print("-" * 50)


def view_headers_only(raw_records: ListOfRecords, title: str | None = None) -> None:
    """Prints an optional title and the headers of the first record."""
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 50)
    for record in raw_records:
        print(record.keys())
        break
    print("-" * 50)

def view_list(items: list[str], title: str | None = None) -> None:
    """Prints an optional title and the items in the list."""
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 50)
    for item in items:
        print(item)
    print("-" * 50)


# --- RapidFuzz Results Viewer ---


def view_rapid_fuzz_results(
    results: list[HeaderMatchingScorer], title: str | None = None
) -> None:
    """Prints an optional title and the RapidFuzz results table."""
    table_headers = ["raw_header", "official_header", "rapidfuzz_score"]
    table_data = []

    for result in sorted(results, key=lambda x: x["rapidfuzz_score"], reverse=True):
        table_data.append([str(result[header]) for header in table_headers])

    if title is not None:
        print(f"Table Title: {title}")
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
