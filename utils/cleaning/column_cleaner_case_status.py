from rapidfuzz import fuzz, process, utils

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.user_facing import ListOfRecords
from utils.helper.viewer_data import (
    view_case_status_fuzzy_matching_results,
    view_column_values,
    view_fuzzy_barangay_matching_results,
    view_list_items,
)
from utils.types import CaseStatusMatchingScorer


def clean_column_case_status(raw_records_barangay_cleaned: ListOfRecords):
    official_case_status_values = list(CSVStandard.CASE_CRIME_STATUS)
    raw_case_status_values = list(
        {record[CSVStandard.CASE_STATUS] for record in raw_records_barangay_cleaned}
    )

    rapidfuzz_results = rapidfuzz_case_status_matching(
        raw_case_status_values, official_case_status_values
    )


def rapidfuzz_case_status_matching(
    raw_case_status_values: list[str], official_case_status_values: list[str]
):
    rapidfuzz_results: list[CaseStatusMatchingScorer] = []

    for raw_case_status in raw_case_status_values:
        result_rapidfuzz = process.extractOne(
            raw_case_status,
            official_case_status_values,
            scorer=fuzz.WRatio,
            processor=utils.default_process,
        )

        matching_official_case_status, score, _ = result_rapidfuzz

        rapidfuzz_results.append(
            {
                "raw_case_status": raw_case_status,
                "official_case_status": matching_official_case_status,
                "rapidfuzz_score": round(score, 2),
            }
        )

    view_case_status_fuzzy_matching_results(rapidfuzz_results)
    exit_now()
    return rapidfuzz_results
