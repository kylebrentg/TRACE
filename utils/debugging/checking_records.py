from typing import Any


def check_records(raw_records: list[dict[str | Any, str | Any]]) -> None:
    for i, record in enumerate(raw_records[:5]):
        print(f"Record {i + 1}: {record}", "\n")
