from typing import Any, TypedDict

ListOfRecords = list[dict[str | Any, str | Any]]

class HeaderMatchingScorer(TypedDict):
    raw_header: str
    official_header: str
    rapidfuzz_score: float

class BarangayMatchingScorer(TypedDict):
    raw_barangay: str
    official_barangay: str
    rapidfuzz_score: float
