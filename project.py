import argparse
import csv

from rich.console import Console

from utils.cleaning.column_cleaner_barangay import clean_column_barangay
from utils.cleaning.column_cleaner_case_status import clean_column_case_status
from utils.cleaning.column_cleaner_date_time import clean_column_date_time
from utils.cleaning.column_cleaner_lat_lng import clean_column_latitude_longitude
from utils.cleaning.column_cleaner_offense_name import clean_column_offense_name
from utils.cleaning.column_cleaner_offense_type import clean_column_offense_type
from utils.cleaning.column_cleaner_type_of_place import clean_column_type_of_place
from utils.cleaning.header_cleaner import (
    clean_headers,
)
from utils.loading.init_argparse import (
    does_csv_file_exists,
    initialize_argparse_engine,
)
from utils.loading.pickle import save_record_to_pickle
from utils.types import ListOfRecords


def main():
    #  1. Ask user csv
    args = initialize_argparse_engine()
    raw_records = load_csv_file(args)

    # 2. Clean records
    cleaned_records = clean_csv_file(raw_records)

    # 3. Store cleaned records to csv and pkl file
    csv_cleaned, pkl_cleaned = save_cleaned_records(
        cleaned_records, args.raw_csv_file_cli_input
    )

    console = Console()
    console.print("[bold green]Files saved successfully:[/bold green]")
    console.print(f"  [green]CSV[/green]: {csv_cleaned}")
    console.print(f"  [yellow]PKL[/yellow]: {pkl_cleaned}")



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
    # Header
    headers_cleaned = clean_headers(raw_records)

    # Column 1 of 9
    offense_type_cleaned = clean_column_offense_type(headers_cleaned)
    # view_column_values(offense_type_cleaned, CSVStandard.OFFENSE_NAME, unique=True)

    # Column 2 of 9
    offense_name_cleaned = clean_column_offense_name(offense_type_cleaned)
    # view_column_values(offense_name_cleaned, CSVStandard.OFFENSE_NAME, unique=True)

    # Column 3 of 9
    type_of_place_cleaned = clean_column_type_of_place(offense_name_cleaned)

    # Column 4 of 9
    barangay_cleaned = clean_column_barangay(type_of_place_cleaned)

    # Column 5 of 9
    case_status_cleaned = clean_column_case_status(barangay_cleaned)

    # Column 6, 7  of 9 (lat and lng columns targeted)
    lat_lng_cleaned = clean_column_latitude_longitude(case_status_cleaned)

    # Column 8, 9  of 9 (date and time columns targeted)
    date_time_cleaned = clean_column_date_time(lat_lng_cleaned)

    cleaned_records = date_time_cleaned.copy()

    return cleaned_records


def save_cleaned_records(
    cleaned_records: ListOfRecords, file_path: str
) -> tuple[str, str]:
    base_name = file_path.rsplit(".", 1)[0].replace("raw", "processed") + "_CLEANED"
    new_csv_file_path = base_name + ".csv"

    # Write to .csv
    with open(new_csv_file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=cleaned_records[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_records)

    # Write to .pkl
    new_pkl_file_path = save_record_to_pickle(
        base_name + ".pkl", cleaned_records
    )

    return new_csv_file_path, new_pkl_file_path


if __name__ == "__main__":
    main()
