import argparse
from datetime import date, time

import pytest

from project import (
    clean_column_barangay,
    clean_column_case_status,
    clean_column_date_time,
    clean_column_latitude_longitude,
    clean_column_offense_name,
    clean_column_offense_type,
    clean_column_type_of_place,
    clean_csv_file,
    clean_headers,
    load_csv_file,
)


# ---- Function 1: load_csv_file ----
def test_load_csv_file_returns_list_of_dicts(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "barangay,offense,casestatus,lat,lng\n"
        "PANDAN,OTHER LIGHT THREATS - RPC Art. 285,Cleared,15.157139,120.587082\n"
        "MINING,MURDER - RPC Art. 248,Solved,15.148399,120.604561\n"
    )
    args = argparse.Namespace(raw_csv_file_cli_input=str(csv_file))

    records = load_csv_file(args)

    assert isinstance(records, list)
    assert isinstance(records[0], dict)


def test_load_csv_file_reads_correct_values(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "barangay,offense,casestatus,lat,lng\n"
        "PANDAN,OTHER LIGHT THREATS - RPC Art. 285,Cleared,15.157139,120.587082\n"
        "MINING,MURDER - RPC Art. 248,Solved,15.148399,120.604561\n"
    )
    args = argparse.Namespace(raw_csv_file_cli_input=str(csv_file))

    records = load_csv_file(args)

    assert len(records) == 2
    assert records[0] == {
        "barangay": "PANDAN",
        "offense": "OTHER LIGHT THREATS - RPC Art. 285",
        "casestatus": "Cleared",
        "lat": "15.157139",
        "lng": "120.587082",
    }
    assert records[1]["barangay"] == "MINING"


def test_load_csv_file_missing_file(tmp_path):
    args = argparse.Namespace(raw_csv_file_cli_input=str(tmp_path / "nope.csv"))

    with pytest.raises(ValueError):
        load_csv_file(args)


def test_load_csv_file_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    args = argparse.Namespace(raw_csv_file_cli_input=str(csv_file))

    with pytest.raises(ValueError):
        load_csv_file(args)


def test_load_csv_file_header_only(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("barangay,offense,casestatus,lat,lng\n")
    args = argparse.Namespace(raw_csv_file_cli_input=str(csv_file))

    with pytest.raises(ValueError):
        load_csv_file(args)


# ---- Function 2: clean_csv_file ----
def test_clean_csv_file_cleans_every_column():
    raw_records = [
        {
            "offense_type": "crimes against property",
            "offense_name": "MURDER - RPC Art. 248",
            "date_committed": "2025-07-31",
            "time_committed": "02:09:00",
            "barangay": "MINING",
            "type_of_place": "Along the street",
            "latitude": "15.157139",
            "longitude": "120.587082",
            "case_status": "Solved",
        }
    ]

    cleaned_records = clean_csv_file(raw_records)

    assert cleaned_records[0] == {
        "offense_type": "Crimes Against Property",
        "offense_name": "Murder - RPC Art. 248",
        "date_committed": date(2025, 7, 31),
        "time_committed": time(2, 9),
        "barangay": "Mining",
        "type_of_place": "Along the street.",
        "latitude": 15.157139,
        "longitude": 120.587082,
        "case_status": "Solved",
    }


# --- clean_headers ---
def test_clean_headers_orders_columns_to_official_schema():
    records = [
        {
            "case_status": "Solved",
            "offense_type": "Crimes Against Property",
            "offense_name": "Murder - RPC Art. 248",
            "date_committed": "2025-07-31",
            "time_committed": "02:09:00",
            "barangay": "Mining",
            "type_of_place": "Along the street.",
            "latitude": "15.157139",
            "longitude": "120.587082",
        }
    ]

    result = clean_headers(records)

    assert list(result[0].keys()) == [
        "offense_type",
        "offense_name",
        "date_committed",
        "time_committed",
        "barangay",
        "type_of_place",
        "latitude",
        "longitude",
        "case_status",
    ]


def test_clean_headers_drops_columns_that_are_not_official():
    records = [
        {
            "offense_type": "Crimes Against Property",
            "offense_name": "Murder - RPC Art. 248",
            "date_committed": "2025-07-31",
            "time_committed": "02:09:00",
            "barangay": "Mining",
            "type_of_place": "Along the street.",
            "latitude": "15.157139",
            "longitude": "120.587082",
            "case_status": "Solved",
            "stn": "Police Station 1",
        }
    ]

    result = clean_headers(records)

    assert "stn" not in result[0]
    assert result[0]["case_status"] == "Solved"


# --- clean_column_offense_type ---
def test_clean_column_offense_type_title_cases_values():
    records = [{"offense_type": "crimes against property"}]

    assert clean_column_offense_type(records) == [
        {"offense_type": "Crimes Against Property"}
    ]


def test_clean_column_offense_type_turns_n_a_into_none():
    records = [{"offense_type": "N/A"}]

    assert clean_column_offense_type(records) == [{"offense_type": None}]


# --- clean_column_offense_name ---
def test_clean_column_offense_name_fixes_casing():
    records = [{"offense_name": "MURDER - RPC Art. 248"}]

    assert clean_column_offense_name(records) == [
        {"offense_name": "Murder - RPC Art. 248"}
    ]


def test_clean_column_offense_name_joins_split_words():
    records = [{"offense_name": "COMPREHENSI VE DANGEROUS DRUGS ACT OF 2002 - RA 9165"}]

    assert clean_column_offense_name(records) == [
        {"offense_name": "Comprehensive Dangerous Drugs Act of 2002 - RA 9165"}
    ]


# --- clean_column_type_of_place ---
def test_clean_column_type_of_place_expands_street():
    records = [{"type_of_place": "Along the street"}]

    assert clean_column_type_of_place(records) == [
        {"type_of_place": "Along the street."}
    ]


def test_clean_column_type_of_place_expands_hospital():
    records = [{"type_of_place": "Hospital (Gov't/Private)"}]

    assert clean_column_type_of_place(records) == [
        {"type_of_place": "A hospital, whether government or private."}
    ]


# --- clean_column_barangay ---
def test_clean_column_barangay_matches_official_name():
    records = [{"barangay": "MINING"}]

    assert clean_column_barangay(records) == [{"barangay": "Mining"}]


def test_clean_column_barangay_keeps_other_columns():
    records = [{"barangay": "AMSIC", "case_status": "Solved"}]

    assert clean_column_barangay(records) == [
        {"barangay": "Amsic", "case_status": "Solved"}
    ]


# --- clean_column_case_status ---
def test_clean_column_case_status_keeps_official_values():
    records = [
        {"case_status": "Solved"},
        {"case_status": "Cleared"},
        {"case_status": "Under Investigation"},
    ]

    assert clean_column_case_status(records) == records


# --- clean_column_latitude_longitude ---
def test_clean_column_latitude_longitude_converts_to_floats():
    records = [{"latitude": "15.157139", "longitude": "120.587082"}]

    assert clean_column_latitude_longitude(records) == [
        {"latitude": 15.157139, "longitude": 120.587082}
    ]


def test_clean_column_latitude_longitude_turns_missing_into_none():
    records = [{"latitude": "N/A", "longitude": "120.587082"}]

    assert clean_column_latitude_longitude(records) == [
        {"latitude": None, "longitude": None}
    ]


def test_clean_column_latitude_longitude_rounds_to_six_decimals():
    records = [{"latitude": "15.1558549", "longitude": "120.5750129"}]

    assert clean_column_latitude_longitude(records) == [
        {"latitude": 15.155855, "longitude": 120.575013}
    ]


# --- clean_column_date_time ---
def test_clean_column_date_time_converts_strings_to_date_and_time():
    records = [{"date_committed": "2025-07-31", "time_committed": "02:09:00"}]

    assert clean_column_date_time(records) == [
        {"date_committed": date(2025, 7, 31), "time_committed": time(2, 9)}
    ]


def test_clean_column_date_time_turns_missing_time_into_none():
    records = [{"date_committed": "2025-07-31", "time_committed": "N/A"}]

    assert clean_column_date_time(records) == [
        {"date_committed": date(2025, 7, 31), "time_committed": None}
    ]


def test_clean_column_date_time_raises_on_bad_date():
    records = [{"date_committed": "2025-13-01", "time_committed": "02:09:00"}]

    with pytest.raises(ValueError):
        clean_column_date_time(records)
