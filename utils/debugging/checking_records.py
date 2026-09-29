from utils.types import ListOfRecords


def check_records(raw_records: ListOfRecords) -> None:
    """Prints the first 5 records in the raw records."""
    print("-" * 50)
    for i, record in enumerate(raw_records[:5]):
        print(f"Record {i + 1}: {record}", "\n")
    print("-" * 50)


def view_headers_only(raw_records: ListOfRecords) -> None:
    """Prints the headers of the first record in the raw records."""
    print("-" * 50)
    for record in raw_records:
        print(record.keys())
        break
    print("-" * 50)
