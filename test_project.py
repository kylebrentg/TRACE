import argparse

import pytest

from project import load_csv_file


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
