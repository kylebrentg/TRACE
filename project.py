import argparse
import csv
import pickle

from utils.cleaning.column_cleaner_offense_type import clean_column_offense_type
from utils.cleaning.header_cleaner import (
    clean_headers,
)
from utils.constants import CSVStandard
from utils.helper.data_viewer import view_records
from utils.helper.program_tools import exit_now
from utils.loading.loader import (
    does_csv_file_exists,
    initialize_argparse_engine,
    load_pickle_file,
)
from utils.types import ListOfRecords


def main():
    # Commenting this out for the time being for feature addition purposes. No need to go over the very raw csv file again and again
    # args = initialize_argparse_engine()
    # raw_records = load_csv_file(args)
    # cleaned_records = clean_csv_file(raw_records)

    pickle_file_path = "data/interim/raw_records_headers_cleaned.pkl"
    raw_records_headers_cleaned: ListOfRecords = load_pickle_file(pickle_file_path)

    cleaned_records = clean_csv_file(raw_records_headers_cleaned)


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
    # raw_records_headers_cleaned = clean_headers(raw_records) # Headers already cleaned. Commenting this out for the time being

    raw_records_headers_cleaned: ListOfRecords = raw_records.copy()

    # raw_records_offense_type_column_cleaned = clean_column_offense_type(
    #     raw_records_headers_cleaned
    # )


def func_3(): ...


if __name__ == "__main__":
    main()
