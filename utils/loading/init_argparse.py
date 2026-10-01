import argparse
import os


def initialize_argparse_engine() -> argparse.Namespace:
    """Parses command line arguments for the raw CSV file and optional clean flag.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("raw_csv_file_cli_input")

    args: argparse.Namespace = parser.parse_args()

    if not args.raw_csv_file_cli_input.endswith(".csv"):
        raise ValueError("raw_csv_file_cli_input must be a CSV file")

    return args


def does_csv_file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)
