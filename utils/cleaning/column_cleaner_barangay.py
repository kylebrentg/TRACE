from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.viewer_data import view_list_items, view_records
from utils.types import ListOfRecords


def clean_column_barangay(
    raw_records_type_of_place_cleaned: ListOfRecords,
) -> ListOfRecords:
    barangay_raw_values: list[str] = [
        record[CSVStandard.BARANGAY] for record in raw_records_type_of_place_cleaned
    ]

    # return cleaned_values
