from rapidfuzz import fuzz, process, utils

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.user_facing import manual_barangay_matching
from utils.helper.viewer_data import (
    view_column_values,
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

    rapidfuzz_results = rapidfuzz_barangay_matching(
        raw_barangay_values, official_barangay_values
    )

    updated_records = match_high_rapidfuzz_result(
        rapidfuzz_results, raw_records_type_of_place_cleaned
    )

    cleaned_values = manual_barangay_matching(updated_records, rapidfuzz_results)

    return cleaned_values


def match_high_rapidfuzz_result(
    rapidfuzz_results: list[BarangayMatchingScorer], raw_records: ListOfRecords
) -> ListOfRecords:
    updated_records: ListOfRecords = []

    for record in raw_records:
        for result in rapidfuzz_results:
            if record[CSVStandard.BARANGAY] != result["raw_barangay"]:
                continue

            if result["rapidfuzz_score"] >= 90:
                record = {**record, CSVStandard.BARANGAY: result["official_barangay"]}

            break

        updated_records.append(record)

    return updated_records


def rapidfuzz_barangay_matching(
    raw_barangay_values: list[str], official_barangay_values: list[str]
) -> list[BarangayMatchingScorer]:

    rapidfuzz_results: list[BarangayMatchingScorer] = []

    for raw_barangay in raw_barangay_values:
        result_rapidfuzz = process.extractOne(
            raw_barangay,
            official_barangay_values,
            scorer=fuzz.WRatio,
            processor=utils.default_process,
        )

        matching_official_barangay, score, _ = result_rapidfuzz

        rapidfuzz_results.append(
            {
                "raw_barangay": raw_barangay,
                "official_barangay": matching_official_barangay,
                "rapidfuzz_score": round(score, 2),
            }
        )
    return rapidfuzz_results
