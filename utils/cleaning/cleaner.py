from utils.types import RawRecords


def normalize_headers(raw_records: RawRecords) -> RawRecords:
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
