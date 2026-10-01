import pytest

from utils.cleaning.header_cleaner import (
    instant_header_matching,
    manual_header_matching_step,
    normalize_headers,
    rapidfuzz_header_matching,
)
from utils.types import HeaderMatchingScorer

# --- normalize_headers ---


def test_lowercases_headers():
    raw = [{"offenseType": "Crimes Against Property"}]
    assert normalize_headers(raw) == [{"offensetype": "Crimes Against Property"}]


def test_replaces_spaces_with_underscores():
    raw = [{"stage of felony": "CONSUMMATED"}]
    assert normalize_headers(raw) == [{"stage_of_felony": "CONSUMMATED"}]


def test_strips_leading_and_trailing_whitespace():
    raw = [{"  barangay  ": "CAPAY"}]
    assert normalize_headers(raw) == [{"barangay": "CAPAY"}]


def test_applies_all_transformations_together():
    raw = [{"  Type of Place  ": "Residential area"}]
    assert normalize_headers(raw) == [{"type_of_place": "Residential area"}]


def test_already_normalized_headers_are_unchanged():
    raw = [{"barangay": "AMSIC"}]
    assert normalize_headers(raw) == [{"barangay": "AMSIC"}]


def test_values_are_not_modified():
    raw = [{"casestatus": "  Under Investigation  "}]
    result = normalize_headers(raw)
    assert result[0]["casestatus"] == "  Under Investigation  "


def test_normalizes_all_records():
    raw = [
        {"offenseType": "Crimes Against Property", "casestatus": "Cleared"},
        {"offenseType": "Crimes Against Persons", "casestatus": "Solved"},
        {"offenseType": "Republic Act", "casestatus": "Under Investigation"},
    ]
    assert normalize_headers(raw) == [
        {"offensetype": "Crimes Against Property", "casestatus": "Cleared"},
        {"offensetype": "Crimes Against Persons", "casestatus": "Solved"},
        {"offensetype": "Republic Act", "casestatus": "Under Investigation"},
    ]


def test_returns_empty_list_when_given_empty_list():
    assert normalize_headers([]) == []


# --- instant_header_matching ---


def test_instant_matches_exact_official_headers():
    records = [
        {
            "offense_type": "Crimes Against Property",
            "barangay": "BALIBAGO",
            "stn": "Police Station 1",
        }
    ]
    result = instant_header_matching(records)

    matched_raw = {r["raw_header"] for r in result}
    assert "offense_type" in matched_raw
    assert "barangay" in matched_raw
    assert "stn" not in matched_raw


def test_instant_all_scores_are_100():
    records = [
        {
            "offense_type": "Crimes Against Persons",
            "case_status": "Cleared",
        }
    ]
    result = instant_header_matching(records)

    for match in result:
        assert match["rapidfuzz_score"] == 100.00


def test_instant_raw_and_official_are_equal():
    records = [{"offense_type": "Republic Act", "latitude": "15.155854"}]
    result = instant_header_matching(records)

    for match in result:
        assert match["raw_header"] == match["official_header"]


def test_instant_returns_empty_when_no_headers_match():
    records = [
        {
            "stn": "Police Station 3",
            "pro": "PRO 3",
            "ppo": "ANGELES CPO",
        }
    ]
    assert instant_header_matching(records) == []


def test_instant_matches_all_official_headers_when_all_present():
    records = [
        {
            "offense_type": "Crimes Against Property",
            "offense_name": "Qualified trespass to dwelling",
            "date_committed": "2022-04-23",
            "time_committed": "19:36:00",
            "barangay": "ANUNAS",
            "type_of_place": "Residential (house/condo)",
            "latitude": "15.150541",
            "longitude": "120.575012",
            "case_status": "Solved",
        }
    ]
    result = instant_header_matching(records)
    assert len(result) == 9


# --- rapidfuzz_header_matching ---


def test_rapidfuzz_matches_similar_headers():
    """Headers close enough to official ones (score >= 90) should be matched."""
    records = [
        {
            "offense_typ": "Crimes Against Chastity",
            "barangy": "MARGOT",
            "victimcount": "1",
        }
    ]
    already_matched: list[HeaderMatchingScorer] = []

    result = rapidfuzz_header_matching(records, already_matched)

    matched_raw = {r["raw_header"] for r in result}
    assert "offense_typ" in matched_raw


def test_rapidfuzz_skips_already_matched_raw_headers():
    records = [
        {
            "offense_type": "Crimes Against Persons",
            "barangay": "SAPANGBATO",
        }
    ]
    already_matched: list[HeaderMatchingScorer] = [
        {
            "raw_header": "offense_type",
            "official_header": "offense_type",
            "rapidfuzz_score": 100.00,
        }
    ]

    result = rapidfuzz_header_matching(records, already_matched)

    matched_raw = [r["raw_header"] for r in result]
    assert "offense_type" not in matched_raw


def test_rapidfuzz_returns_empty_when_nothing_scores_high():
    records = [
        {
            "pro": "PRO 3",
            "ppo": "ANGELES CPO",
            "victimcount": "2",
        }
    ]
    already_matched: list[HeaderMatchingScorer] = []

    result = rapidfuzz_header_matching(records, already_matched)

    high_scores = [r for r in result if r["rapidfuzz_score"] >= 90]
    assert len(high_scores) == 0


def test_rapidfuzz_does_not_duplicate_official_headers():
    """Two raw headers might both map to the same official header.
    Only the higher-scoring one should be kept."""
    records = [
        {
            "offense_typ": "Crimes Against Property",
            "offensetype": "Crimes Against Persons",
        }
    ]
    already_matched: list[HeaderMatchingScorer] = []

    result = rapidfuzz_header_matching(records, already_matched)

    official_headers_in_result = [r["official_header"] for r in result]
    assert len(official_headers_in_result) == len(set(official_headers_in_result))


def test_rapidfuzz_all_scores_are_at_least_90():
    records = [
        {
            "offense_typ": "Crimes Against Property",
            "barangy": "CUAYAN",
            "suspectcount": "1",
        }
    ]
    already_matched: list[HeaderMatchingScorer] = []

    result = rapidfuzz_header_matching(records, already_matched)

    for match in result:
        assert match["rapidfuzz_score"] >= 90


def test_rapidfuzz_returns_empty_when_all_already_matched():
    records = [
        {
            "offense_type": "Crimes Against Persons",
            "barangay": "MINING",
        }
    ]
    already_matched: list[HeaderMatchingScorer] = [
        {
            "raw_header": "offense_type",
            "official_header": "offense_type",
            "rapidfuzz_score": 100.00,
        },
        {
            "raw_header": "barangay",
            "official_header": "barangay",
            "rapidfuzz_score": 100.00,
        },
    ]

    result = rapidfuzz_header_matching(records, already_matched)
    assert result == []


# --- manual_header_matching_step ---


def test_manual_step_returns_empty_when_all_officials_matched():
    records = [
        {
            "offense_type": "Crimes Against Property",
            "barangay": "TABUN",
        }
    ]
    running_matched: list[HeaderMatchingScorer] = [
        {
            "raw_header": header,
            "official_header": header,
            "rapidfuzz_score": 100.00,
        }
        for header in (
            "offense_type",
            "offense_name",
            "modus_operandi",
            "date_committed",
            "time_committed",
            "barangay",
            "latitude",
            "longitude",
            "police_station_number",
            "case_status",
        )
    ]

    result = manual_header_matching_step(records, running_matched)
    assert result == []


def test_manual_step_prompts_for_unmatched_official_headers(monkeypatch):
    """When one official header is unmatched and the user picks raw header 1
    and confirms, the result should contain that match with score 100."""
    records = [
        {"offense_type": "Crimes Against Property", "casestatus": "Cleared"},
        {"offense_type": "Crimes Against Persons", "casestatus": "Solved"},
    ]

    running_matched: list[HeaderMatchingScorer] = [
        {
            "raw_header": header,
            "official_header": header,
            "rapidfuzz_score": 100.00,
        }
        for header in (
            "offense_type",
            "offense_name",
            "date_committed",
            "time_committed",
            "barangay",
            "type_of_place",
            "latitude",
            "longitude",
        )
    ]
    # Only "case_status" is unmatched, and "casestatus" is the only raw header left

    inputs = iter(["1", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = manual_header_matching_step(records, running_matched)

    assert len(result) == 1
    assert result[0]["raw_header"] == "casestatus"
    assert result[0]["official_header"] == "case_status"
    assert result[0]["rapidfuzz_score"] == 100.00


def test_manual_step_retries_on_invalid_then_accepts(monkeypatch):
    """User enters an invalid number, then a valid one, then confirms."""
    records = [
        {"offense_type": "Republic Act", "casestatus": "Under Investigation"},
    ]

    running_matched: list[HeaderMatchingScorer] = [
        {
            "raw_header": header,
            "official_header": header,
            "rapidfuzz_score": 100.00,
        }
        for header in (
            "offense_type",
            "offense_name",
            "modus_operandi",
            "date_committed",
            "time_committed",
            "barangay",
            "latitude",
            "longitude",
            "police_station_number",
        )
    ]

    # "99" is invalid, "1" picks casestatus, "no" rejects, "1" again, "yes" confirms
    inputs = iter(["99", "1", "no", "1", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = manual_header_matching_step(records, running_matched)

    assert len(result) == 1
    assert result[0]["raw_header"] == "casestatus"
    assert result[0]["rapidfuzz_score"] == 100.00
