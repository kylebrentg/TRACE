from rapidfuzz import fuzz, process

from utils.constants import CSVStandard
from utils.helper.data_viewer import view_list, view_rapid_fuzz_results
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
