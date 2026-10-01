from utils.constants import CSVStandard
from utils.helper.column_values_viewer import view_column_values
from utils.helper.program_tools import exit_now
from utils.types import ListOfRecords


def clean_column_offense_type(raw_records: ListOfRecords) -> ListOfRecords:
    for header in CSVStandard.SCHEMA:
        if not isinstance(header, str):
            continue

        view_column_values(raw_records, header)
