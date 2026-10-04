from tabulate import tabulate

from utils.types import HeaderMatchingScorer, ListOfRecords

# --- Record Viewer ---


def view_records(raw_records: ListOfRecords, title: str | None = None) -> None:
    """Prints an optional title and the first 5 records in the raw records."""
    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    for index, record in enumerate(raw_records[:5], start=1):
        print(f"{index}. {record}", "\n")
    if len(raw_records) > 5:
        print(f"...omitting {len(raw_records) - 5}")
    print("-" * 25)


def view_headers_only(raw_records: ListOfRecords, title: str | None = None) -> None:
    """Prints an optional title and the headers of the first record."""
    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    for record in raw_records:
        print(record.keys())
        break
    print("-" * 25)


def view_list(
    items: list[str], title: str | None = None, representation: bool | None = None
) -> None:
    """Prints an optional title and the items in the list.

    Pass ``representation="repr"`` to display each item's exact Python
    representation.
    """
    if representation not in (None, True):
        raise ValueError("representation must be None or 'True'")

    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    for index, item in enumerate(items[:20], start=1):
        displayed_item = repr(item) if representation == True else item
        print(f"{index}. {displayed_item}")
    if len(items) > 20:
        print(f"...omitting {len(items) - 20}")
    print("-" * 25)


# --- RapidFuzz Results Viewer ---


def view_rapid_fuzz_results(
    results: list[HeaderMatchingScorer], title: str | None = None
) -> None:
    """Prints an optional title and the RapidFuzz results table."""
    table_headers = ["raw_header", "official_header", "rapidfuzz_score"]
    table_data = []

    for result in sorted(
        results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        table_data.append([str(result[header]) for header in table_headers])

    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    print("-" * 25)
