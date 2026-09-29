import argparse
import csv

from utils.cleaning.header_cleaner import (
    instant_header_matching,
    manual_header_matching_step,
    normalize_headers,
    rapidfuzz_header_matching,
)
from utils.helper.data_viewer import view_rapid_fuzz_results
from utils.loading.loader import does_csv_file_exists, initialize_argparse_engine
from utils.types import HeaderMatchingScorer, ListOfRecords


def main():
    args = initialize_argparse_engine()
    raw_records = load_csv_file(args)
    cleaned_records = clean_csv_file(raw_records)


def load_csv_file(args: argparse.Namespace) -> ListOfRecords:

    if not does_csv_file_exists(args.raw_csv_file_cli_input):
        raise ValueError(f"CSV file not found: {args.raw_csv_file_cli_input}")

    with open(args.raw_csv_file_cli_input, newline="") as file:
        reader = csv.DictReader(file)
        raw_records = list(reader)

        if not raw_records:
            raise ValueError(f"{args.raw_csv_file_cli_input} is empty: {raw_records}")

    return raw_records


def clean_csv_file(raw_records: ListOfRecords) -> ListOfRecords:
    headers_matched: list[HeaderMatchingScorer] = []

    # 1. Normalize headers
    records_headers_normalized = normalize_headers(raw_records)

    # 2. Determine matched headers
    headers_matched.extend(instant_header_matching(records_headers_normalized))

    # 3. Match headers via rapidfuzz
    headers_matched.extend(
        rapidfuzz_header_matching(records_headers_normalized, headers_matched)
    )

    # 4. Manually match remaining headers
    headers_matched.extend(
        manual_header_matching_step(records_headers_normalized, headers_matched)
    )

    view_rapid_fuzz_results(headers_matched, "PINALLY")


def func_3(): ...


if __name__ == "__main__":
    main()
