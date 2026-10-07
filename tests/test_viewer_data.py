from utils.helper.viewer_data import (
    view_barangay_fuzzy_matching_results,
    view_fuzzy_barangay_matching_results,
    view_fuzzy_header_matching_results,
    view_fuzzy_matching_results,
    view_header_fuzzy_matching_results,
)
from utils.types import BarangayMatchingScorer, HeaderMatchingScorer


def test_view_fuzzy_header_matching_results(capsys):
    results: list[HeaderMatchingScorer] = [
        {"raw_header": "offense_typ", "official_header": "offense_type", "rapidfuzz_score": 95.0},
        {"raw_header": "barangy", "official_header": "barangay", "rapidfuzz_score": 93.33},
    ]
    view_fuzzy_header_matching_results(results, title="Header Matching Test")
    captured = capsys.readouterr().out

    assert "Table Title: Header Matching Test" in captured
    assert "raw_header" in captured
    assert "official_header" in captured
    assert "rapidfuzz_score" in captured
    assert "offense_typ" in captured
    assert "barangy" in captured


def test_view_fuzzy_barangay_matching_results(capsys):
    results: list[BarangayMatchingScorer] = [
        {"raw_barangay": "Sto Rosario", "official_barangay": "Santo Rosario (Población)", "rapidfuzz_score": 90.0},
        {"raw_barangay": "Malabanias", "official_barangay": "Malabañas (Malabanias)", "rapidfuzz_score": 92.5},
    ]
    view_fuzzy_barangay_matching_results(results, title="Barangay Matching Test")
    captured = capsys.readouterr().out

    assert "Table Title: Barangay Matching Test" in captured
    assert "raw_barangay" in captured
    assert "official_barangay" in captured
    assert "rapidfuzz_score" in captured
    assert "Sto Rosario" in captured
    assert "Santo Rosario (Población)" in captured
    assert "Malabanias" in captured


def test_view_fuzzy_barangay_matching_results_unique(capsys):
    results: list[BarangayMatchingScorer] = [
        {"raw_barangay": "Balibago", "official_barangay": "Balibago", "rapidfuzz_score": 100.0},
        {"raw_barangay": "Balibago", "official_barangay": "Balibago", "rapidfuzz_score": 100.0},
    ]
    view_fuzzy_barangay_matching_results(results, unique=True)
    captured = capsys.readouterr().out

    # Should only appear once in data rows
    assert captured.count("Balibago") == 2  # raw and official in a single row


def test_backward_compatibility_aliases():
    assert view_fuzzy_matching_results is view_fuzzy_header_matching_results
    assert view_header_fuzzy_matching_results is view_fuzzy_header_matching_results
    assert view_barangay_fuzzy_matching_results is view_fuzzy_barangay_matching_results
