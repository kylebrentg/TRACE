from tabulate import tabulate

from utils.types import (
    BarangayMatchingScorer,
    CaseStatusMatchingScorer,
    HeaderMatchingScorer,
    ListOfRecords,
)

# =============================================================================
# --- RECORDS & HEADERS VIEWER ---
# =============================================================================


def view_records(
    raw_records: ListOfRecords, title: str | None = None, unique: bool = False
) -> None:
    """Prints an optional title and the records."""
    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)

    if unique:
        displayed_records = []
        seen = set()
        for r in raw_records:
            t = tuple(sorted(r.items()))
            if t not in seen:
                seen.add(t)
                displayed_records.append(r)
    else:
        displayed_records = raw_records

    limit = None if unique else 5
    records_to_show = displayed_records[:limit] if limit else displayed_records

    for index, record in enumerate(records_to_show, start=1):
        print(f"{index}. {record}", "\n")

    if limit and len(displayed_records) > limit:
        print(f"...omitting {len(displayed_records) - limit}")
    print("-" * 25)


def view_record_headers(raw_records: ListOfRecords, title: str | None = None) -> None:
    """Prints an optional title and the headers of the first record."""
    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    for record in raw_records:
        print(record.keys())
        break
    print("-" * 25)


# =============================================================================
# --- COLUMN VALUES & LIST VIEWER ---
# =============================================================================


def view_column_values(
    records: ListOfRecords,
    column_name: str,
    title: str | None = None,
    unique: bool = False,
) -> None:
    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print(f"Column: {column_name}")
    print("-" * 25)

    if unique:
        # Get unique values preserving order
        column_values = list(
            dict.fromkeys(
                record[column_name] for record in records if column_name in record
            )
        )
    else:
        column_values = [
            record[column_name] for record in records if column_name in record
        ]

    limit = None if unique else 20
    values_to_show = column_values[:limit] if limit else column_values

    for index, value in enumerate(values_to_show, start=1):
        if value in ("", " ", None):
            print(f"{index}. ''")
            continue
        print(f"{index}. {value}")

    if limit and len(column_values) > limit:
        print(f"...omitting {len(column_values) - limit}")
    print("-" * 25)


def view_list_items(
    items: list[str],
    title: str | None = None,
    representation: bool | None = None,
    unique: bool = False,
) -> None:
    """Prints an optional title and the items in the list.

    Pass ``representation=True`` to display each item's exact Python
    representation. Pass ``unique=True`` to display each value only once.
    """
    if representation not in (None, True):
        raise ValueError("representation must be None or 'True'")

    displayed_items = list(dict.fromkeys(items)) if unique else items

    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)

    limit = None if unique else 20
    items_to_show = displayed_items[:limit] if limit else displayed_items

    for index, item in enumerate(items_to_show, start=1):
        displayed_item = repr(item) if representation == True else item
        print(f"{index}. {displayed_item}")

    if limit and len(displayed_items) > limit:
        print(f"...omitting {len(displayed_items) - limit}")
    print("-" * 25)


# =============================================================================
# --- FUZZY MATCHING RESULTS VIEWER ---
# =============================================================================


def view_fuzzy_header_matching_results(
    results: list[HeaderMatchingScorer],
    title: str | None = None,
    unique: bool = False,
) -> None:
    """Prints an optional title and the RapidFuzz header matching results table."""
    table_headers = ["raw_header", "official_header", "rapidfuzz_score"]
    table_data = []

    if unique:
        seen = set()
        displayed_results = []
        for r in results:
            key = (r["raw_header"], r["official_header"], r["rapidfuzz_score"])
            if key not in seen:
                seen.add(key)
                displayed_results.append(r)
    else:
        displayed_results = results

    for result in sorted(
        displayed_results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        table_data.append([str(result[header]) for header in table_headers])

    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    print("-" * 25)


def view_fuzzy_barangay_matching_results(
    results: list[BarangayMatchingScorer],
    title: str | None = None,
    unique: bool = False,
) -> None:
    """Prints an optional title and the RapidFuzz barangay matching results table."""
    table_headers = ["raw_barangay", "official_barangay", "rapidfuzz_score"]
    table_data = []

    if unique:
        seen = set()
        displayed_results = []
        for r in results:
            key = (r["raw_barangay"], r["official_barangay"], r["rapidfuzz_score"])
            if key not in seen:
                seen.add(key)
                displayed_results.append(r)
    else:
        displayed_results = results

    for result in sorted(
        displayed_results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        table_data.append([str(result[header]) for header in table_headers])

    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    print("-" * 25)


def view_fuzzy_case_status_matching_results(
    results: list[CaseStatusMatchingScorer],
    title: str | None = None,
    unique: bool = False,
) -> None:
    """Prints an optional title and the RapidFuzz case status matching results table."""
    table_headers = ["raw_case_status", "official_case_status", "rapidfuzz_score"]
    table_data = []

    if unique:
        seen = set()
        displayed_results = []
        for r in results:
            key = (
                r["raw_case_status"],
                r["official_case_status"],
                r["rapidfuzz_score"],
            )
            if key not in seen:
                seen.add(key)
                displayed_results.append(r)
    else:
        displayed_results = results

    for result in sorted(
        displayed_results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        table_data.append([str(result[header]) for header in table_headers])

    print("=" * 50)
    if title is not None:
        print(f"Table Title: {title}")
    print("-" * 25)
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    print("-" * 25)


# Backward compatibility and alternative naming aliases
view_fuzzy_matching_results = view_fuzzy_header_matching_results
view_header_fuzzy_matching_results = view_fuzzy_header_matching_results
view_barangay_fuzzy_matching_results = view_fuzzy_barangay_matching_results
view_case_status_fuzzy_matching_results = view_fuzzy_case_status_matching_results
