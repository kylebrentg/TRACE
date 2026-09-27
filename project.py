import argparse
import csv

from utils.cleaning.cleaner import normalize_headers
from utils.debugging.checking_records import check_records, view_headers_only
from utils.loading.loader import does_csv_file_exists, initialize_argparse_engine
from utils.types import RawRecords


def main():
    args = initialize_argparse_engine()
    raw_records = load_csv_file(args)
    cleaned_records = clean_csv_file(raw_records)


def load_csv_file(args: argparse.Namespace) -> RawRecords:

    if not does_csv_file_exists(args.raw_csv_file_cli_input):
        raise ValueError(f"CSV file not found: {args.raw_csv_file_cli_input}")

    with open(args.raw_csv_file_cli_input, newline="") as file:
        reader = csv.DictReader(file)
        raw_records = list(reader)

        if not raw_records:
            raise ValueError(f"{args.raw_csv_file_cli_input} is empty: {raw_records}")

    return raw_records


def clean_csv_file(raw_records: RawRecords):
    raw_records_headers_normalized = normalize_headers(raw_records)

    # return raw_records_headers_normalized


def func_3(): ...


if __name__ == "__main__":
    main()
