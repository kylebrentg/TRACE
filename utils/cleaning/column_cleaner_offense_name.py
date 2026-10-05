from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.viewer_data import view_column_values, view_list_items
from utils.types import ListOfRecords


def clean_column_offense_name(raw_records_offense_type_cleaned: ListOfRecords):
    offense_name_raw_values: list[str] = [
        record[CSVStandard.OFFENSE_NAME] for record in raw_records_offense_type_cleaned
    ]

    generally_cleaned_values = general_string_values_cleaning(offense_name_raw_values)
    values_cleaned: list[str] = [value.lower() for value in generally_cleaned_values]

    view_list_items(values_cleaned, unique=True)
    exit_now()

def clean_with_gemini(values_to_be_cleaned: list[str]) -> list[str]:
  
  


