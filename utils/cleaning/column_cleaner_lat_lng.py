from utils.constants import CSVStandard
from utils.helper.string_values_cleaner import clean_invisible_characters
from utils.types import ListOfRecords

_ListOfCoordinates = list[tuple[str | float | None, str | float | None]]


def clean_column_latitude_longitude(raw_records_case_status_cleaned: ListOfRecords):

    coordinates = [
        (record[CSVStandard.LATITUDE], record[CSVStandard.LONGITUDE])
        for record in raw_records_case_status_cleaned
    ]

    updated_coordinates = _standardize_stringified_float_values(coordinates)
    updated_coordinates = _update_invalid_placeholder_values(updated_coordinates)
    updated_coordinates = _update_types_from_string_to_float(updated_coordinates)
    updated_coordinates = _standardize_coordinate_to_6_decimal_places(
        updated_coordinates
    )
    updated_coordinates = _validate_lat_lng_boundary(updated_coordinates)

    cleaned_records = [
        {
            **record,
            CSVStandard.LATITUDE: lat,
            CSVStandard.LONGITUDE: lng,
        }
        for record, (lat, lng) in zip(
            raw_records_case_status_cleaned, updated_coordinates
        )
    ]

    return cleaned_records


def _validate_lat_lng_boundary(coordinates: _ListOfCoordinates) -> _ListOfCoordinates:
    updated_coordinates: _ListOfCoordinates = []
    lat_north: float = 90.000000
    lat_south: float = -90.000000
    lng_east: float = 180.000000
    lng_west: float = -180.000000

    for coordinate in coordinates:
        lat, lng = coordinate
        if __check_none_value(lat, lng):
            updated_coordinates.append((lat, lng))
            continue

        if not isinstance(lat, float) or not isinstance(lng, float):
            raise TypeError("lat or lng must be of float type")

        if not (lat <= lat_north and lat >= lat_south) or not (
            lng <= lng_east and lng >= lng_west
        ):
            updated_coordinates.append((None, None))

            continue

        updated_coordinates.append((lat, lng))

    return updated_coordinates


def _standardize_coordinate_to_6_decimal_places(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    updated_coordinates: _ListOfCoordinates = []

    for coordinate in coordinates:
        lat, lng = coordinate
        if __check_none_value(lat, lng):
            updated_coordinates.append((lat, lng))
            continue

        if isinstance(lat, float) and isinstance(lng, float):
            updated_coordinates.append(
                (
                    round(lat, 6),
                    round(lng, 6),
                )
            )
    return updated_coordinates


def _update_types_from_string_to_float(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    updated_coordinates: _ListOfCoordinates = []
    for coordinate in coordinates:
        lat, lng = coordinate
        if lat is None or lng is None:
            updated_coordinates.append((lat, lng))
            continue
        updated_coordinates.append((float(lat), float(lng)))

    return updated_coordinates


def _update_invalid_placeholder_values(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    # If either coordinate is missing, the entire pair is unavailable.
    updated_coordinates: _ListOfCoordinates = []
    sentinel_values = CSVStandard.NULL_VALUE_PLACEHOLDERS
    for coordinate in coordinates:
        lat, lng = coordinate
        if lat is None or lng is None or lat in sentinel_values or lng in sentinel_values:
            updated_coordinates.append((None, None))
            continue
        updated_coordinates.append((lat, lng))

    return updated_coordinates


def _standardize_stringified_float_values(
    coordinates: _ListOfCoordinates,
) -> _ListOfCoordinates:
    updated_coordinates = []
    for coordinate in coordinates:
        lat, lng = coordinate
        updated_coordinates.append(
            (
                clean_invisible_characters(lat).lower() if isinstance(lat, str) else lat,
                clean_invisible_characters(lng).lower() if isinstance(lng, str) else lng,
            )
        )

    return updated_coordinates


# --- Helper Functions ---
def __check_none_value(lat, lng) -> bool:
    return lat is None or lng is None
