from datetime import date, time

import pytest

from utils.cleaning.column_cleaner_date_time import clean_column_date_time
from utils.constants import CSVStandard


@pytest.mark.parametrize(
    "date_str, time_str, expected_date, expected_time",
    [
        ("2026-10-13", "14:30:45", date(2026, 10, 13), time(14, 30, 45)),
        ("2024-02-29", "23:59:59", date(2024, 2, 29), time(23, 59, 59)),
        ("2026-01-01", "00:00:00", date(2026, 1, 1), time(0, 0, 0)),
        ("2026-12-31", "23:59:59", date(2026, 12, 31), time(23, 59, 59)),
        ("2026-10-13", "14:30", date(2026, 10, 13), time(14, 30)),
        ("2026-10-13", "", date(2026, 10, 13), None),
        ("2026-10-13", None, date(2026, 10, 13), None),
        ("2026-10-13", " N/A ", date(2026, 10, 13), None),
        (
            "2026-10-13",
            "14:30:45.123456",
            date(2026, 10, 13),
            time(14, 30, 45, 123456),
        ),
    ],
)
def test_converts_valid_iso_strings_to_date_and_time(
    date_str, time_str, expected_date, expected_time
):
    records = [
        {CSVStandard.DATE_COMMITTED: date_str, CSVStandard.TIME_COMMITTED: time_str}
    ]

    assert clean_column_date_time(records) == [
        {
            CSVStandard.DATE_COMMITTED: expected_date,
            CSVStandard.TIME_COMMITTED: expected_time,
        }
    ]


@pytest.mark.parametrize(
    "date_str, time_str",
    [
        ("2023-02-29", "12:00:00"),
        ("2026-02-30", "12:00:00"),
        ("2026-13-01", "12:00:00"),
        ("2026-00-01", "12:00:00"),
        ("13/10/2026", "12:00:00"),
        ("", "12:00:00"),
        (None, "12:00:00"),
        ("2026-10-13", "24:00:00"),
        ("2026-10-13", "12:60:00"),
        ("2026-10-13", "12:00:60"),
        ("2026-10-13", "not-a-time"),
    ],
)
def test_rejects_invalid_values_and_reports_the_row(date_str, time_str):
    records = [
        {CSVStandard.DATE_COMMITTED: date_str, CSVStandard.TIME_COMMITTED: time_str}
    ]

    with pytest.raises(ValueError, match="Incorrect date or time") as exc_info:
        clean_column_date_time(records)

    assert exc_info.value.args[2] == [
        {"Row number": 1, "Incorrect date_time or empty": (date_str, time_str)}
    ]


def test_reports_all_invalid_rows_using_one_based_row_numbers():
    records = [
        {
            CSVStandard.DATE_COMMITTED: "2026-10-13",
            CSVStandard.TIME_COMMITTED: "12:00:00",
        },
        {
            CSVStandard.DATE_COMMITTED: "2023-02-29",
            CSVStandard.TIME_COMMITTED: "12:00:00",
        },
        {
            CSVStandard.DATE_COMMITTED: "2026-10-14",
            CSVStandard.TIME_COMMITTED: "13:00:00",
        },
        {
            CSVStandard.DATE_COMMITTED: "2026-10-15",
            CSVStandard.TIME_COMMITTED: "24:00:00",
        },
    ]
    original = [record.copy() for record in records]

    with pytest.raises(ValueError) as exc_info:
        clean_column_date_time(records)

    assert exc_info.value.args[2] == [
        {"Row number": 2, "Incorrect date_time or empty": ("2023-02-29", "12:00:00")},
        {"Row number": 4, "Incorrect date_time or empty": ("2026-10-15", "24:00:00")},
    ]
    assert records == original


def test_preserves_record_order_other_columns_and_original_input():
    records = [
        {
            CSVStandard.DATE_COMMITTED: "2026-10-14",
            CSVStandard.TIME_COMMITTED: "13:00:00",
            "case_status": "Solved",
        },
        {
            CSVStandard.DATE_COMMITTED: "2026-10-13",
            CSVStandard.TIME_COMMITTED: "12:00:00",
            "case_status": "Cleared",
        },
    ]
    original = [record.copy() for record in records]

    result = clean_column_date_time(records)

    assert result == [
        {
            CSVStandard.DATE_COMMITTED: date(2026, 10, 14),
            CSVStandard.TIME_COMMITTED: time(13, 0),
            "case_status": "Solved",
        },
        {
            CSVStandard.DATE_COMMITTED: date(2026, 10, 13),
            CSVStandard.TIME_COMMITTED: time(12, 0),
            "case_status": "Cleared",
        },
    ]
    assert records == original
    assert result is not records
    assert all(cleaned is not raw for cleaned, raw in zip(result, records))


def test_handles_empty_input():
    assert clean_column_date_time([]) == []


@pytest.mark.parametrize(
    "missing_column", [CSVStandard.DATE_COMMITTED, CSVStandard.TIME_COMMITTED]
)
def test_missing_required_column_raises_key_error(missing_column):
    record = {
        CSVStandard.DATE_COMMITTED: "2026-10-13",
        CSVStandard.TIME_COMMITTED: "12:00:00",
    }
    del record[missing_column]

    with pytest.raises(KeyError) as exc_info:
        clean_column_date_time([record])

    assert exc_info.value.args == (missing_column,)
