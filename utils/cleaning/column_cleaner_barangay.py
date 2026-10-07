from rapidfuzz import fuzz, process, utils

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.viewer_data import (
    view_fuzzy_barangay_matching_results,
    view_list_items,
    view_records,
)
from utils.types import BarangayMatchingScorer, ListOfRecords


def clean_column_barangay(
    raw_records_type_of_place_cleaned: ListOfRecords,
) -> ListOfRecords:

    official_barangay_values = list(CSVStandard.BARANGAY_NAMES)

    raw_barangay_values: list[str] = list(
        {record[CSVStandard.BARANGAY] for record in raw_records_type_of_place_cleaned}
    )

    match_values = rapidfuzz_barangay_matching(
        raw_barangay_values, official_barangay_values
    )

    # return cleaned_values


def rapidfuzz_barangay_matching(
    raw_barangay_values: list[str], official_barangay_values: list[str]
):
    # raw_barangay_values = [
    #     barangay_value.title() for barangay_value in raw_barangay_values
    # ]

    rapidfuzz_results: list[BarangayMatchingScorer] = []

    for raw_barangay in raw_barangay_values:
        result_rapidfuzz = process.extractOne(
            raw_barangay, official_barangay_values, scorer=fuzz.WRatio, processor=utils.default_process
        )

        matching_official_barangay, score, _ = result_rapidfuzz

        rapidfuzz_results.append(
            {
                "raw_barangay": raw_barangay,
                "official_barangay": matching_official_barangay,
                "rapidfuzz_score": round(score, 2),
            }
        )

    view_fuzzy_barangay_matching_results(
        rapidfuzz_results, "Barangay Matching RapidFuzz Result"
    )
