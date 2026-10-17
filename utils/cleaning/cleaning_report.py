import csv
import pickle

from utils.helper.viewer_data import view_records

"""
Decomposition:
  1. load saved csv and pkl file in memory
  2. create an id number for each record for both files
  3. use random library to choose number to get records from csv and pkl file
  4. A max of 10 values for each of the columns to write
"""

raw_csv_path = "data/raw/2025_crime_records.csv"
cleaned_csv_path = "data/processed/2025_crime_records_CLEANED.csv"
cleaned_pkl_path = "data/processed/2025_crime_records_CLEANED.pkl"


def write_cleaning_report(raw_csv_path, cleaned_csv_path, cleaned_pkl_path) -> str:
    raw_csv_records, cleaned_csv_records, cleaned_pkl_records = __load_records(
        raw_csv_path, cleaned_csv_path, cleaned_pkl_path
    )
    headers = __headers_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    offense_type = __offense_type_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    offense_name = __offense_name_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    date_committed = __date_committed_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    time_committed = __time_committed_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    barangay = __barangay_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    type_of_place = __type_of_place_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    latitude = __latitude_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    longitude = __longitude_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)
    case_status = __case_status_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records)

def __headers_report(raw_csv_records, cleaned_csv_records, cleaned_pkl_records):
    for 

def __load_records(raw_csv_path, cleaned_csv_path, cleaned_pkl_path):
    with (
        open(raw_csv_path, newline="") as raw_csv_file,
        open(cleaned_csv_path, newline="") as cleaned_csv_file,
        open(cleaned_pkl_path, "rb") as cleaned_pkl_file,
    ):
        raw_csv_reader = csv.DictReader(raw_csv_file)
        raw_csv_records = list(raw_csv_reader)

        cleaned_csv_reader = csv.DictReader(cleaned_csv_file)
        cleaned_csv_records = list(cleaned_csv_reader)

        cleaned_pkl_records = pickle.load(cleaned_pkl_file)

    return raw_csv_records, cleaned_csv_records, cleaned_pkl_records


report_file_path = write_cleaning_report(
    raw_csv_path, cleaned_csv_path, cleaned_pkl_path
)

# TODO: In header cleaning, barangay cleaning, and such, save the pairing results in a file so it can be used for cleaning report