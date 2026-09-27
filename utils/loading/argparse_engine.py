import argparse


def parse_args() -> argparse.Namespace:
    """Parses command line arguments for the raw CSV file and optional clean flag.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()


    parser.add_argument("raw_csv_file_cli_input")

    args: argparse.Namespace = parser.parse_args()
    
    return args