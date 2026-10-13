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
    rapidfuzz_ambiguous: bool


class CaseStatusMatchingScorer(TypedDict):
    raw_case_status: str
    official_case_status: str
    rapidfuzz_score: float


Coordinate = tuple[float | None, float | None]
ListOfCoordinates = list[Coordinate]
