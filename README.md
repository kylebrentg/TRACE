# T.R.A.C.E. (Text Repair & Angeles Crime Evaluation)

#### Video Demo: TODO (add the YouTube URL before submission)

#### Description:

T.R.A.C.E. is my CS50P final project: a Python command-line application for cleaning crime records obtained through FOI Philippines (Freedom of Information). Its cleaning rules target the structure and text problems in these records, including inconsistent headers and OCR-damaged words. It takes a CSV and exports a cleaned CSV and a Python pickle file. The application handles data preparation, not crime lookup or safety reporting; it doesn't extract text from scanned documents itself.

The tool isn't tied to a particular year. You can supply records from 2015 or 2023, for example, provided they contain the fields the pipeline needs. The current workflow handles one year's records in one CSV per run; it doesn't offer year-range processing such as `2015–2022` or combine annual files. The built-in barangay references target Angeles City, Philippines, so using records from another locality requires updating the reference list in `utils/constants.py`.

Common problems include broken words such as `Commercial/B usiness Establishment`, abbreviated barangay names, and inconsistent capitalization. Rather than retaining every source column, the tool produces these nine output fields:

```text
offense_type, offense_name, date_committed, time_committed, barangay,
type_of_place, latitude, longitude, case_status
```

The pipeline first normalizes headers, matches them to these fields, and asks for help when it can't resolve a match. It drops columns outside this schema. Field cleaners then format offense categories, repair offense names and place descriptions, match barangays and case statuses, check coordinates, and parse dates and times. For example, `MINING` becomes `Mining`, while the place-description repair expands `Hospital (Gov't/Private)` into readable English. The pipeline preserves row order; it doesn't remove duplicate incidents.

### Design choices

Different fields need different repair methods. Python's standard library handles CSV files and predictable text cleanup without a dataframe (like Pandas) dependency. RapidFuzz compares noisy labels against reference values, including 33 barangay names and the statuses `Solved`, `Cleared`, and `Under Investigation`. Uncertain matches go to terminal review rather than silently accepting the nearest spelling. Skipping a barangay or status correction retains its original value, so users still need to inspect the output.

Offense names can contain legal references and word splits that a short lookup table can't cover. Gemini handles these names and expands place descriptions. Each request contains distinct normalized strings from one column rather than complete records, avoiding repeated work for repeated values. Pydantic checks the response structure, but it can't establish whether a legal reference or correction is accurate.

Both cleaners send new requests to Gemini each time you run the pipeline; they don't automatically reuse results from earlier runs. The `clean_values_from_json()` helper can read a Gemini response you have saved in `data/interim/`, but it is only used for debugging. Calls to that helper are commented out in both cleaners, so using it requires manually changing the cleaner code. There is no command-line option to reuse saved responses or run these cleaning steps offline.

CSV supports spreadsheet inspection, while pickle preserves Python date/time objects and numeric values. Missing dates or invalid date/time strings stop processing; invalid or incomplete coordinate pairs become empty values, although nonnumeric coordinate text raises an error. Coordinate checks enforce global bounds, not Angeles City boundaries.

I chose uv to manage the Python environment and dependencies because I want to keep using it in future projects, and this project gives me a place to practice that workflow. CS50P doesn't require uv; `requirements.txt` keeps the usual pip-based setup available. The uv workflow uses `uv.lock` to keep dependency versions consistent.

### Project files

`project.py` contains `main()` and the top-level functions `load_csv_file()`, `clean_csv_file()`, and `save_cleaned_records()`. These separate file loading, pipeline execution, and output writing. `test_project.py` tests these functions and basic cleaner behavior.

The helper modules divide the remaining work by responsibility:

```text
utils/
├── constants.py                    Output fields, reference values, API settings
├── schemas.py                      Pydantic models for Gemini responses
├── types.py                        Record and matching-result type definitions
├── cleaning/
│   ├── header_cleaner.py            Header normalization and matching
│   ├── column_cleaner_offense_type.py   Category text formatting
│   ├── column_cleaner_offense_name.py   Gemini offense repair and prompt
│   ├── column_cleaner_type_of_place.py  Gemini place-description repair
│   ├── column_cleaner_barangay.py   Barangay matching and review
│   ├── column_cleaner_case_status.py    Status matching and review
│   ├── column_cleaner_lat_lng.py    Coordinate conversion and bounds checks
│   └── column_cleaner_date_time.py  ISO date/time parsing and error collection
├── helper/
│   ├── string_values_cleaner.py     Shared Unicode, whitespace, and null cleanup
│   ├── user_facing.py               Interactive matching menus
│   ├── viewer_data.py               Diagnostic tables and value displays
│   └── program_tools.py             Success messages and debugging helpers
└── loading/
    ├── init_argparse.py             CSV argument parsing and existence checks
    ├── init_gemini.py               API setup, model fallback, saved-JSON reader
    └── pickle.py                    Pickle loading and saving
```

Most of my testing effort so far is in `test_project.py`. The focused tests in `tests/` are incomplete practice tests for selected cleaning columns and supporting functions. They help me check that those functions work, but they don't cover every helper function, subfunction, or edge case. Neither test location provides comprehensive coverage yet; I plan to improve that in a future iteration.

`requirements.txt` lists pip dependencies; `pyproject.toml` defines project metadata and Python requirements, while `uv.lock` records dependency versions for uv. `.gitignore` excludes credentials and local artifacts. Local `data/`, `context_files/`, and `my_notes/` hold datasets and development references; Git excludes them, so a fresh clone needs its own input CSV.

### Setup and usage

Use Python 3.13 or newer and run the project commands from the repository root. These instructions use macOS/Linux shell syntax and focus on uv.

#### Set up the environment with uv

Follow uv's [official installation guide](https://docs.astral.sh/uv/getting-started/installation/) to install it. The guide includes Homebrew, which I used on macOS, as well as other installation methods. Once the `uv` command is available, install Python and the project dependencies:

```sh
uv python install 3.13
uv sync --locked --python 3.13
```

`uv sync` creates the project's `.venv` environment and installs dependencies from `uv.lock`. `uv run` runs a command inside that environment, so you don't need to activate it manually.

`--locked` tells uv to check that `uv.lock` exists and is up to date with the project's dependency declarations in `pyproject.toml`. If the lockfile is missing or needs to change, uv stops with an error instead of creating or updating it. This keeps setup tied to the dependency versions recorded in the repository; it doesn't prevent uv from downloading or installing those packages. The same check applies when you add `--locked` to `uv run`.

#### Prepare the input and run

Create the data directories:

```sh
mkdir -p data/raw data/processed
```

Create a root `.env` file containing your own credential:

```dotenv
GEMINI_API_KEY=your_api_key
```

Save one year's FOI crime records as `data/raw/crime_records.csv`. The filename doesn't select the year; the dates in your records determine it. The CSV needs columns that map to all nine output fields, with dates and times in ISO format, such as `2023-07-31` and `02:09:00`.

Run the pipeline with uv:

```sh
uv run --locked python project.py data/raw/crime_records.csv
```

Follow any matching prompts. Successful completion writes `data/processed/crime_records_CLEANED.csv` and `.pkl`. Output directories must already exist, and repeated runs overwrite these files. You can use a year-specific input filename to keep outputs separate. The path builder replaces every `raw` substring with `processed`; use the directory layout above to avoid unexpected filenames.

Gemini requires network access and may incur charges or hit quotas. Requests send offense and place strings to Google; only process data you have permission to share, and keep credentials out of version control.

### Tests

Run the main test file from the repository root:

```sh
uv run pytest test_project.py
```

This runs pytest inside uv's project environment and selects only `test_project.py`. To also require an up-to-date lockfile without allowing uv to change it, use:

```sh
uv run --locked pytest test_project.py
```

These tests check file loading and saving, the cleaning pipeline, and basic behavior for each cleaning column. They are not comprehensive coverage of every underlying function or edge case.

Some tests call Gemini directly, including the full-pipeline test and tests for offense-name and place-description cleaning. They require `GEMINI_API_KEY` in your `.env` file and network access, may incur API usage, and can fail if the service is unavailable or returns an unexpected correction.
