from utils.constants import CSVStandard
from utils.debugging.checking_records import view_headers_only
from utils.types import ListOfRecords

# --- cleaning csv headers ---


def normalize_headers(raw_records: ListOfRecords) -> ListOfRecords:
    """Normalizes the headers of the raw records.

    Args:
        raw_records (RawRecords): The raw records to normalize.

    Returns:
        RawRecords: The raw records with normalized headers."""
    return [
        {
            header.strip().lower().replace(" ", "_"): value
            for header, value in record.items()
        }
        for record in raw_records
    ]


def instant_header_match(normalized_raw_records: ListOfRecords) -> set:
    normalized_headers = next(iter(normalized_raw_records)).keys()
    official_headers = CSVStandard.HEADERS
    return normalized_headers & official_headers
