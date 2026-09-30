from rapidfuzz import fuzz, process

from utils.constants import CSVStandard
from utils.helper.data_viewer import view_list, view_rapid_fuzz_results, view_records
from utils.helper.program_tools import exit_now
from utils.helper.user_facing import manual_header_matching
from utils.types import HeaderMatchingScorer, ListOfRecords

# --- cleaning csv headers ---


def normalize_headers(raw_records: ListOfRecords) -> ListOfRecords:
    """Normalizes the headers of the raw records.

    Args:
        raw_records (RawRecords): The raw records to normalize.

    Returns:
        RawRecords: The raw records with normalized headers."""
    return [
        {
            header.strip().lower().replace(" ", "_"): value
            for header, value in record.items()
        }
        for record in raw_records
    ]


def instant_header_matching(raw_records: ListOfRecords) -> list[HeaderMatchingScorer]:
    raw_headers = next(iter(raw_records)).keys()
    official_headers = CSVStandard.HEADERS

    headers_matched = list(raw_headers & official_headers)
    return [
        {"raw_header": header, "official_header": header, "rapidfuzz_score": 100.00}
        for header in headers_matched
    ]


def rapidfuzz_header_matching(
    raw_records: ListOfRecords,
    running_headers_matched: list[HeaderMatchingScorer],
) -> list[HeaderMatchingScorer]:

    # 1. Prepare data needed
    raw_headers = list(next(iter(raw_records)).keys())
    official_headers = CSVStandard.HEADERS

    raw_headers_matched: list[str] = [
        header["raw_header"] for header in running_headers_matched
    ]
    official_headers_matched = [
        header["raw_header"] for header in running_headers_matched
    ]

    headers_ready_for_matching: list[HeaderMatchingScorer] = []

    # 2. Perform RapidFuzz process
    rapidfuzz_results: list[HeaderMatchingScorer] = []

    for header in raw_headers:
        if header in raw_headers_matched:
            continue

        result_rapidfuzz = process.extractOne(
            header, official_headers, scorer=fuzz.WRatio
        )

        matching_official_header, score, _ = result_rapidfuzz

        rapidfuzz_results.append(
            {
                "raw_header": header,
                "official_header": matching_official_header,
                "rapidfuzz_score": round(score, 2),
            }
        )

    # 3. Only choose the high scores (>= 90) from the result
    high_score_results: list[HeaderMatchingScorer] = []
    for result in sorted(
        rapidfuzz_results, key=lambda x: x["rapidfuzz_score"], reverse=True
    ):
        if result["official_header"] in [
            high_score["official_header"] for high_score in high_score_results
        ]:
            continue

        if not result["rapidfuzz_score"] >= 90:
            continue

        high_score_results.append(result)
        raw_headers_matched.append(result["raw_header"])
        official_headers_matched.append(result["official_header"])

    headers_ready_for_matching.extend(high_score_results)

    return headers_ready_for_matching


def manual_header_matching_step(
    raw_records: ListOfRecords,
    running_headers_matched: list[HeaderMatchingScorer],
) -> list[HeaderMatchingScorer]:
    """Manually match any official headers that weren't matched by prior steps."""
    official_headers = CSVStandard.HEADERS

    raw_headers_matched = [header["raw_header"] for header in running_headers_matched]
    official_headers_matched = [
        header["official_header"] for header in running_headers_matched
    ]

    official_headers_remaining = [
        header for header in official_headers if header not in official_headers_matched
    ]

    return manual_header_matching(
        official_headers_remaining, raw_headers_matched, raw_records
    )


def update_records_headers(
    raw_records: ListOfRecords, headers_to_match: list[HeaderMatchingScorer]
) -> ListOfRecords:

    raw_and_official_headers: dict[str, str] = {
        header["raw_header"]: header["official_header"] for header in headers_to_match
    }

    records_with_headers_updated = [
        {
            raw_and_official_headers[header]: record[header]
            for header in record
            if header in raw_and_official_headers
        }
        for record in raw_records
    ]

    # Rearranging headers to abide to the schema
    official_headers_in_order: tuple = CSVStandard.HEADERS

    records_with_headers_arranged = [
        {
            official_header: record[official_header]
            for official_header in official_headers_in_order
            for header in record
            if official_header == header
        }
        for record in records_with_headers_updated
    ]

    return records_with_headers_arranged
