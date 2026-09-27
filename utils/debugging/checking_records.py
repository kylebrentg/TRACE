from utils.types import RawRecords


def check_records(raw_records: RawRecords) -> None:
    for i, record in enumerate(raw_records[:5]):
        print(f"Record {i + 1}: {record}", "\n")
