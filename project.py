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
from utils.loading.init_argparse import (
    does_csv_file_exists,
    initialize_argparse_engine,
)
from utils.loading.pickle import load_pickle_file, save_record_to_pickle
from utils.types import ListOfRecords


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
    raw_records_headers_cleaned = clean_headers(raw_records)

    pkl_file_path = save_record_to_pickle(
        "data/interim/2025_crime_records.pkl", raw_records_headers_cleaned
    )

    view_records(load_pickle_file(pkl_file_path), "This is a PKL File Records:")

    


def func_3(): ...


if __name__ == "__main__":
    main()
