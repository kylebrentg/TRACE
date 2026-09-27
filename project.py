import argparse
import csv
from typing import Any

from utils.debugging.checking_records import check_records
from utils.loading.loader import does_csv_file_exists, initialize_argparse_engine


def main():
    args: argparse.Namespace = initialize_argparse_engine()
    raw_records: list[dict] = load_csv_file(args)

    check_records(raw_records)


def load_csv_file(args: argparse.Namespace) -> list[dict[str | Any, str | Any]]:

    if not does_csv_file_exists(args.raw_csv_file_cli_input):
        raise ValueError(f"CSV file not found: {args.raw_csv_file_cli_input}")

    with open(args.raw_csv_file_cli_input, newline="") as file:
        reader = csv.DictReader(file)
        raw_records = list(reader)
    return raw_records


def func_2(): ...


def func_3(): ...


if __name__ == "__main__":
    main()
