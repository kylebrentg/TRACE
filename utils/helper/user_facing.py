import random
import textwrap
from typing import Any

from tabulate import tabulate

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.viewer_data import view_list_items, view_records
from utils.types import (
    BarangayMatchingScorer,
    CaseStatusMatchingScorer,
    HeaderMatchingScorer,
    ListOfRecords,
)

# --- Barangay Matching ---


def manual_barangay_matching(
    updated_records: ListOfRecords, rapidfuzz_results: list[BarangayMatchingScorer]
) -> ListOfRecords:

    matched_barangays: ListOfRecords = []

    print("Manual barangay matching is required...")
    print("Remaining barangays:")

    remaining_rapidfuzz_results = sorted(
        [
            {**result} for result in rapidfuzz_results
            if result["rapidfuzz_score"] < 90 or result["rapidfuzz_ambiguous"]
        ],
        key=lambda x: x["rapidfuzz_score"],
        reverse=True,
    )

    # raw barangay -> manually chosen official barangay
    manual_matches: dict[str, str] = {}

    remaining_rapidfuzz_results_copy = sorted(CSVStandard.BARANGAY_NAMES)
    for result in remaining_rapidfuzz_results:
        view_list_items(remaining_rapidfuzz_results_copy, unique=True)
        while True:
            user_input = int(
                input(
                    f"Choose official barangay number to match '{result['raw_barangay']}' (suggestion: {result['official_barangay']}, score: {result['rapidfuzz_score']}; 0 to leave unresolved): "
                )
            )
            if user_input == 0:
                break
            if user_input not in range(1, len(remaining_rapidfuzz_results_copy) + 1):
                print(
                    "Invalid input. Please choose a number between 1 and",
                    len(remaining_rapidfuzz_results_copy),
                )
                continue

            chosen_result = remaining_rapidfuzz_results_copy[user_input - 1]
            manual_matches[result["raw_barangay"]] = chosen_result
            break

    for record in updated_records:
        raw_barangay = record[CSVStandard.BARANGAY]
        matched_barangays.append(
            {
                **record,
                CSVStandard.BARANGAY: manual_matches.get(raw_barangay, raw_barangay),
            }
        )

    return matched_barangays


def display_remaining_barangay(rapidfuzz_results):
    table_headers = ["No.", "Raw Header", "Official Header", "RapidFuzz Score"]
    table_data = []
    counter = 1
    for result in sorted(
        rapidfuzz_results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        table_data.append(
            (
                counter,
                result["raw_barangay"],
                result["official_barangay"],
                result["rapidfuzz_score"],
            )
        )
        counter += 1

    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))


# --- Case Status Matching ---


def manual_case_status_matching(
    updated_records: ListOfRecords, rapidfuzz_results: list[CaseStatusMatchingScorer]
) -> ListOfRecords:

    matched_case_statuses: ListOfRecords = []

    remaining_rapidfuzz_results = sorted(
        [{**result} for result in rapidfuzz_results if result["rapidfuzz_score"] < 90],
        key=lambda x: x["rapidfuzz_score"],
        reverse=True,
    )

    if not remaining_rapidfuzz_results:
        return updated_records

    print("Manual case_status matching is required...")
    print("Remaining case_status:")

    # raw case_status -> manually chosen official case_status
    manual_matches: dict[str, str] = {}

    remaining_rapidfuzz_results_copy = remaining_rapidfuzz_results.copy()
    for result in remaining_rapidfuzz_results:
        display_remaining_case_status(remaining_rapidfuzz_results_copy)
        while True:
            user_input = int(
                input(
                    f"Choose official case_status number to match '{result['raw_case_status']}' (suggestion: {result['official_case_status']}, {result['rapidfuzz_score']}%): "
                )
            )
            if user_input not in range(1, len(remaining_rapidfuzz_results_copy) + 1):
                print(
                    "Invalid input. Please choose a number between 1 and",
                    len(remaining_rapidfuzz_results_copy),
                )
                continue

            chosen_result = remaining_rapidfuzz_results_copy[user_input - 1]
            manual_matches[result["raw_case_status"]] = chosen_result["official_case_status"]
            remaining_rapidfuzz_results_copy.remove(chosen_result)
            break

    for record in updated_records:
        raw_case_status = record[CSVStandard.CASE_STATUS]
        matched_case_statuses.append(
            {
                **record,
                CSVStandard.CASE_STATUS: manual_matches.get(
                    raw_case_status, raw_case_status
                ),
            }
        )

    return matched_case_statuses


def display_remaining_case_status(rapidfuzz_results):
    table_headers = ["No.", "Raw Header", "Official Header", "RapidFuzz Score"]
    table_data = []
    counter = 1
    for result in sorted(
        rapidfuzz_results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        table_data.append(
            (
                counter,
                result["raw_case_status"],
                result["official_case_status"],
                result["rapidfuzz_score"],
            )
        )
        counter += 1

    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))


# --- Header Matching ---


def view_unmatched_raw_headers(
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

        position_to_header = view_unmatched_raw_headers(
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
            confirm = (
                input(
                    f"\nMatch '{chosen_raw_header}' → '{official_header}'? (yes/no): "
                )
                .strip()
                .lower()
            )

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
