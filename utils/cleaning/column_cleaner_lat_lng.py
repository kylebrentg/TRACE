from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.viewer_data import view_column_values, view_list_items
from utils.types import ListOfRecords

_ListOfCoordinates = list[tuple[str, str]]


def clean_column_latitude_longitude(raw_records_case_status_cleaned: ListOfRecords):
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LATITUDE, unique=True)
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LONGITUDE, unique=True)

    coordinates = [
        (record[CSVStandard.LATITUDE].strip(), record[CSVStandard.LATITUDE].strip())
        for record in raw_records_case_status_cleaned
    ]

    updated_coordinates = _standardize_stringified_float_values(coordinates)
    updated_coordinates = _update_invalid_placeholder_values(updated_coordinates)

    # standardize_floats_to_6_decimal_places()
    # swap_incorrect_coordinate_order()
    # enforce_angeles_city_bounding_box()


def _update_invalid_placeholder_values(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    # Sentinel Values: `0.0, 0.0`, `""`, `"N/A"`, or `None`.
    updated_records: _ListOfCoordinates = []
    sentinel_values = {"0.0", "''", '""', "n/a", "none"}
    for coordinate in coordinates:
        lat, lng = coordinate
        if lat in sentinel_values or lng in sentinel_values:
            updated_records.append(("None", "None"))
            continue
        updated_records.append((lat, lng))

    return updated_records


def _standardize_stringified_float_values(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    return [
        (coordinate[0].strip().lower(), coordinate[1].strip().lower())
        for coordinate in coordinates
    ]
