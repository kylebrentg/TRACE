from datetime import date, time

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.viewer_data import view_column_values, view_list_items, view_records
from utils.types import ListOfRecords


def clean_column_date_time(raw_records_lat_lng_cleaned: ListOfRecords):
    date_time_tuples = [
        (record[CSVStandard.DATE_COMMITTED], record[CSVStandard.TIME_COMMITTED])
        for record in raw_records_lat_lng_cleaned
    ]
    valid_datetime = []
    invalid_datetime = []
    for i, date_time in enumerate(date_time_tuples, start=1):
        date_str, time_str = date_time
        try:
            date_str, time_str = general_string_values_cleaning([date_str, time_str])
            dt_obj = (
                date.fromisoformat(date_str),
                time.fromisoformat(time_str) if time_str is not None else None,
            )
            valid_datetime.append(dt_obj)
        except (ValueError, TypeError):
            invalid_datetime.append(
                {"Row number": i, "Incorrect date_time or empty": date_time}
            )
            continue

    if invalid_datetime:
        raise ValueError(
            "Incorrect date or time stamp(s). Please fix.", "\n", invalid_datetime
        )

    cleaned_values = [
        {
            **record,
            CSVStandard.DATE_COMMITTED: dt_obj[0],
            CSVStandard.TIME_COMMITTED: dt_obj[1],
        }
        for record, dt_obj in zip(raw_records_lat_lng_cleaned, valid_datetime)
    ]

    return cleaned_values
