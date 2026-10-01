from utils.types import ListOfRecords


def view_column_values(records: ListOfRecords, column_name: str) -> None:
    print("=" * 50)
    print(f"Column: {column_name}")
    print("-" * 25)
    column_values = list(frozenset(record[column_name] for record in records))

    for index, value in enumerate(column_values[:20], start=1):
        if value in ("", "", " ", None):
            print(f"{index}. ''")
            continue
        print(f"{index}. {value}")

    if len(column_values) > 50:
        print(f"...omitting {len(column_values) - 50}")
    print("-" * 25)
