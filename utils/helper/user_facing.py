import random
import textwrap
from typing import Any

from tabulate import tabulate

from utils.helper.program_tools import exit_now
from utils.types import HeaderMatchingScorer, ListOfRecords


def display_raw_headers_remaining(
    raw_headers_matched: list[str], raw_records: ListOfRecords
) -> dict[int, str]:
    """Displays a numbered table of remaining (unmatched) raw headers with sample values.

    Returns:
        A dict mapping position number -> raw header name, so callers
        can look up which header the user picked by number.
    """
    table_headers = ["No.", "Raw Header", "Samples Values"]
    table_data: list[tuple[int, str, str]] = []
    position_to_header: dict[int, str] = {}

    all_raw_headers = next(iter(raw_records)).keys()

    pos = 0
    for header in all_raw_headers:
        if header in raw_headers_matched:
            continue

        header_all_values = list(
            dict.fromkeys(record[header] for record in raw_records)
        )

        header_random_values: list[str | Any] = random.sample(
            header_all_values, k=min(5, len(header_all_values))
        )

        values_string: str = ", ".join(str(header) for header in header_random_values)

        wrapped_values = textwrap.fill(values_string, width=50)

        pos += 1

        table_data.append((pos, header, wrapped_values))
        position_to_header[pos] = header

    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    return position_to_header


def manual_header_matching(
    official_headers_remaining: list[str],
    raw_headers_matched: list[str],
    raw_records: ListOfRecords,
) -> list[HeaderMatchingScorer]:
    """Walks the user through manually matching each remaining official header.

    For each official header, displays:
        1. The official header that needs a match.
        2. A numbered table of remaining raw headers with sample values.

    The user enters the number of a raw header, confirms with yes/no,
    and the match is recorded with a score of 100.

    Args:
        official_headers_remaining: Official headers that still need a match.
        raw_headers_matched: Raw headers already matched (mutated in-place
            as new matches are confirmed).
        raw_records: The full raw records (used to pull sample values).

    Returns:
        A list of confirmed HeaderMatchingScorer dicts (score 100 each).
    """
    if not official_headers_remaining:
        return []

    manual_matches: list[HeaderMatchingScorer] = []

    print("\n" + "=" * 60)
    print("  MANUAL HEADER MATCHING")
    print("  The following official headers still need a match:")
    print("=" * 60)
    for i, header in enumerate(official_headers_remaining, start=1):
        print(f"    {i}. {header}")

    for official_header in official_headers_remaining:
        print("\n" + "-" * 60)
        print(f"  Official header to match:  {official_header}")
        print("-" * 60)
        print("\nRemaining raw headers:\n")

        position_to_header = display_raw_headers_remaining(
            raw_headers_matched, raw_records
        )

        if not position_to_header:
            print("No remaining raw headers to choose from.")
            continue

        # --- ask the user to pick a number ---
        while True:
            choice = input(
                f"\nEnter the number of the raw header to match with "
                f"'{official_header}': "
            ).strip()

            if not choice.isdigit() or int(choice) not in position_to_header:
                print(
                    f"Invalid choice. Please enter a number between "
                    f"1 and {len(position_to_header)}."
                )
                continue

            chosen_raw_header = position_to_header[int(choice)]

            # --- confirm ---
            confirm = input(
                f"\nMatch '{chosen_raw_header}' → '{official_header}'? (yes/no): "
            ).strip().lower()

            if confirm in ("yes", "y"):
                manual_matches.append(
                    {
                        "raw_header": chosen_raw_header,
                        "official_header": official_header,
                        "rapidfuzz_score": 100.00,
                    }
                )
                raw_headers_matched.append(chosen_raw_header)
                break
            else:
                print("Match cancelled. Try again.\n")
                continue

    return manual_matches
