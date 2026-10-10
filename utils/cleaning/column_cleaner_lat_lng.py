from utils.constants import CSVStandard
from utils.helper.viewer_data import view_column_values
from utils.types import ListOfRecords


def clean_column_latitude_longitude(raw_records_case_status_cleaned: ListOfRecords):
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LATITUDE, unique=True)
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LONGITUDE, unique=True)

    coordinates = [
        (record[CSVStandard.LATITUDE].strip(), record[CSVStandard.LATITUDE].strip())
        for record in raw_records_case_status_cleaned
    ]

    strip_white_spaces()
    remove_invalid_placeholder_values()
    standardize_floats_to_6_decimal_places()
    swap_incorrect_coordinate_order()
    enforce_angeles_city_bounding_box()
