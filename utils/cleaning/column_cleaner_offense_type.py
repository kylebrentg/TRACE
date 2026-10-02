from utils.constants import CSVStandard
from utils.helper.column_values_viewer import view_column_values
from utils.helper.data_viewer import view_list, view_records
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.types import ListOfRecords


def clean_column_offense_type(
    raw_records_headers_cleaned: ListOfRecords,
) -> ListOfRecords:
    offense_type_raw_values = [
        record[CSVStandard.OFFENSE_TYPE] for record in raw_records_headers_cleaned
    ]

    view_list(offense_type_raw_values, "Raw Values before General String Cleaning")

    values_cleaned = general_string_values_cleaning(offense_type_raw_values)
    values_cleaned = [value.title() for value in values_cleaned]

    view_list(
        values_cleaned, "New Values after General String Cleaning", representation=True
    )
