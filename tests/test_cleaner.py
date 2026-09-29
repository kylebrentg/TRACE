from utils.cleaning.header_cleaner import normalize_headers

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
