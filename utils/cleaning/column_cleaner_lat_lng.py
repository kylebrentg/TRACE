from utils.constants import CSVStandard
from utils.helper.viewer_data import view_column_values
from utils.types import ListOfRecords

_ListOfCoordinates = list[tuple[str, str]]

def clean_column_latitude_longitude(raw_records_case_status_cleaned: ListOfRecords):
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LATITUDE, unique=True)
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LONGITUDE, unique=True)

    coordinates = [
        (record[CSVStandard.LATITUDE].strip(), record[CSVStandard.LATITUDE].strip())
        for record in raw_records_case_status_cleaned
    ]

    updated_coordinates = _strip_white_spaces(coordinates)
    updated_coordinates = update_invalid_placeholder_values(updated_coordinates)
    # standardize_floats_to_6_decimal_places()
    # swap_incorrect_coordinate_order()
    # enforce_angeles_city_bounding_box()


def _update_invalid_placeholder_values(coordinates: _ListOfCoordinates) -> _ListOfCoordinates:
  ...

def _strip_white_spaces(coordinates: _ListOfCoordinates) -> _ListOfCoordinates:
    return [
        (coordinate[0].strip(), coordinate[1].strip()) for coordinate in coordinates
    ]
