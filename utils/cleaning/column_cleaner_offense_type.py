from codecs import raw_unicode_escape_decode

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.viewer_data import view_column_values, view_list_items, view_records
from utils.types import ListOfRecords


def clean_column_offense_type(
    raw_records_headers_cleaned: ListOfRecords,
) -> ListOfRecords:
    offense_type_raw_values = [
        record[CSVStandard.OFFENSE_TYPE] for record in raw_records_headers_cleaned
    ]

    values_cleaned = general_string_values_cleaning(offense_type_raw_values)
    values_cleaned = [value.title() for value in values_cleaned]

    cleaned_values_for_offense_type: ListOfRecords = [
        {**record, CSVStandard.OFFENSE_TYPE: value}
        for record, value in zip(raw_records_headers_cleaned, values_cleaned)
    ]

    return cleaned_values_for_offense_type
