
import argparse

from utils.loading.loader import does_csv_file_exists, initialize_argparse_engine


def main():
  args: argparse.Namespace = initialize_argparse_engine()
  raw_records: list[dict] = load_csv_file(args)
  

def load_csv_file(args: argparse.Namespace) -> list[dict]:

  if not does_csv_file_exists(args.raw_csv_file_cli_input):
    raise ValueError(f"CSV file not found: {args.raw_csv_file_cli_input}")
    

def func_2():
  ...

def func_3():
  ...

if __name__ == "__main__":
  main()