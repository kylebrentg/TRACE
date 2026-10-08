import argparse
import csv
import pickle

from utils.cleaning.column_cleaner_barangay import clean_column_barangay
from utils.cleaning.column_cleaner_offense_name import clean_column_offense_name
from utils.cleaning.column_cleaner_offense_type import clean_column_offense_type
from utils.cleaning.column_cleaner_type_of_place import clean_column_type_of_place
from utils.cleaning.header_cleaner import (
    clean_headers,
)
from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.viewer_data import view_column_values, view_records
from utils.loading.init_argparse import (
    does_csv_file_exists,
    initialize_argparse_engine,
)
from utils.loading.pickle import load_pickle_file, save_record_to_pickle
from utils.types import ListOfRecords


def main():
    # Temporary comment to focus on a specific feature instead of starting over again
    # args = initialize_argparse_engine()
    # raw_records = load_csv_file(args)
    # cleaned_records = clean_csv_file(raw_records)
    _ = clean_csv_file(
        load_pickle_file("data/interim/2025_crime_records_barangay_cleaned.pkl")
    )


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
    # Temporary comment. Working on other feature
    # raw_records_headers_cleaned = clean_headers(raw_records)

    raw_records_barangay_cleaned = raw_records.copy()

    # Column 1 of 9
    # offense_type_cleaned = clean_column_offense_type(raw_records_headers_cleaned)
    # view_column_values(offense_type_cleaned, CSVStandard.OFFENSE_NAME, unique=True)

    # Column 2 of 9
    # offense_name_cleaned = clean_column_offense_name(offense_type_cleaned)
    # view_column_values(offense_name_cleaned, CSVStandard.OFFENSE_NAME, unique=True)

    # Column 3 of 9
    # type_of_place_cleaned = clean_column_type_of_place(raw_records_offense_name_cleaned)

    # Column 4 of 9
    # barangay_cleaned = clean_column_barangay(raw_records_type_of_place_cleaned)


    view_column_values(raw_records_barangay_cleaned, CSVStandard.BARANGAY, unique=True)
    view_records(raw_records_barangay_cleaned, "Barangay Cleaned")


def func_3(): ...


if __name__ == "__main__":
    main()
