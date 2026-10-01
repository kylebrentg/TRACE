import argparse
import sys

import pytest

from project import load_csv_file
from utils.loading.init_argparse import does_csv_file_exists, initialize_argparse_engine

# --- initialize_argparse_engine ---


def test_valid_csv_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "data.csv"])
    args = initialize_argparse_engine()
    assert args.raw_csv_file_cli_input == "data.csv"


def test_valid_csv_file_with_path(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "path/to/my_file.csv"])
    args = initialize_argparse_engine()
    assert args.raw_csv_file_cli_input == "path/to/my_file.csv"


def test_invalid_extension_raises_value_error(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "data.txt"])
    with pytest.raises(ValueError, match="raw_csv_file_cli_input must be a CSV file"):
        initialize_argparse_engine()


def test_no_extension_raises_value_error(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "data"])
    with pytest.raises(ValueError, match="raw_csv_file_cli_input must be a CSV file"):
        initialize_argparse_engine()


def test_missing_argument_raises_system_exit(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit):
        initialize_argparse_engine()


# --- does_csv_file_exists ---


def test_returns_true_when_file_exists(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("col1,col2\n1,2\n")
    assert does_csv_file_exists(str(csv_file)) is True


def test_returns_false_when_file_does_not_exist(tmp_path):
    csv_file = tmp_path / "missing.csv"
    assert does_csv_file_exists(str(csv_file)) is False


def test_returns_false_for_nonexistent_path():
    assert does_csv_file_exists("/nonexistent/path/file.csv") is False


def test_returns_true_for_directory(tmp_path):
    assert does_csv_file_exists(str(tmp_path)) is True


def test_returns_false_for_empty_string():
    assert does_csv_file_exists("") is False


# --- load_csv_file ---


def test_load_csv_file_raises_when_file_has_no_data_rows(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("col1,col2\n")  # header only, no data rows
    args = argparse.Namespace(raw_csv_file_cli_input=str(csv_file))
    with pytest.raises(ValueError, match="is empty"):
        load_csv_file(args)
