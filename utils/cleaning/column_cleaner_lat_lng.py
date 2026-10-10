from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.viewer_data import view_column_values, view_list_items
from utils.types import ListOfRecords

_ListOfCoordinates = list[tuple[str | float, str | float]]


def clean_column_latitude_longitude(raw_records_case_status_cleaned: ListOfRecords):
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LATITUDE, unique=True)
    # view_column_values(raw_records_case_status_cleaned, CSVStandard.LONGITUDE, unique=True)

    coordinates = [
        (record[CSVStandard.LATITUDE].strip(), record[CSVStandard.LATITUDE].strip())
        for record in raw_records_case_status_cleaned
    ]

    updated_coordinates = _standardize_stringified_float_values(coordinates)
    updated_coordinates = _update_invalid_placeholder_values(updated_coordinates)
    view_list_items(updated_coordinates, representation=True)
    updated_coordinates = _update_types_from_string_to_float(updated_coordinates)
    view_list_items(updated_coordinates, representation=True)

    # updated_coordinates = _standardize_coordinate_to_6_decimal_places(updated_coordinates)
    # swap_incorrect_coordinate_order()
    # enforce_angeles_city_bounding_box()


def _update_types_from_string_to_float(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    updated_records: _ListOfCoordinates = []
    for coordinate in coordinates:
        lat, lng = coordinate
        if lat == "None" or lng == "None":
            updated_records.append((lat, lng))
            continue
        updated_records.append((float(lat), float(lng)))

    return updated_records


# def _standardize_coordinate_to_6_decimal_places(updated_coordinates: _ListOfCoordinates):


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
    updated_records = []
    for coordinate in coordinates:
        lat, lng = coordinate
        if isinstance(lat, str) and isinstance(lng, str):
            updated_records.append((lat.strip().lower(), lng.strip().lower()))

    return updated_records
