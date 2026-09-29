import random
import textwrap
from typing import Any

from tabulate import tabulate

from utils.helper.program_tools import exit_now
from utils.types import ListOfRecords


def display_raw_headers_remaining(
    raw_headers_matched: list[str], raw_records: ListOfRecords
) -> None:
    table_headers = ["No.", "Raw Header", "Samples Values"]
    table_data: list[tuple[int, str, str]] = []

    all_raw_headers = next(iter(raw_records)).keys()

    pos = 0
    for header in all_raw_headers:
        if header in raw_headers_matched:
            continue

        header_all_values = list(
            dict.fromkeys(record[header] for record in raw_records)
        )

        header_random_values: list[str | Any] = random.sample(
            header_all_values, k=min(5, len(header_all_values))
        )

        values_string: str = ", ".join(str(header) for header in header_random_values)

        wrapped_values = textwrap.fill(values_string, width=50)

        pos += 1

        table_data.append((pos, header, wrapped_values))

    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    exit_now()
