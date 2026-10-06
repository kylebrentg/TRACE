import inspect

from utils.constants import CSVStandard
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.loading.init_gemini import clean_values_with_gemini, initialize_gemini_api
from utils.types import ListOfRecords


def offense_name_cleaning_prompt(values_to_be_cleaned: list[str]) -> str:
    return inspect.cleandoc(f"""
        You will be given a Python list of raw offense name strings extracted from
        a crime records database. These strings may contain:

        - Fragmented words caused by OCR errors (e.g., "manufactur e",
          "paraphernali a", "lasciviousne ss") — rejoin them into the correct word
        - Irregular spacing around hyphens
        - Inconsistent casing

        Your task is to return a cleaned version of each offense name.

        Apply these rules:

        1. Fix all fragmented words by merging them into their correct spelling.
        2. Standardize the format as:
           "<Offense Name> - <Legal Basis>"
           Example:
           "Reckless Imprudence Resulting to Multiple Physical Injuries - RPC Art. 365"
        3. Use title case for the offense name portion.
        4. Keep legal basis references uppercase and abbreviated
           (e.g., "RPC", "RA", "PD", "BP").
        5. Do not add, remove, or invent any offense. Only clean what is given.
        6. Remove grammatically incorrect commas inherited from OCR
           (e.g., commas before prepositions like ", of" or ", by").
           Do NOT remove hyphens. Compound modifiers such as
           "gender-based" and "anti-child" must retain or gain their hyphen.
        7. Any bare act number (e.g., "3815") that refers to a Philippine law
           must be written as "Act No. 3815".
        8. The phrase "as amended by" should always be lowercase and should not
           be subject to title casing.
        9. Return one mapping for every input value.
        10. Preserve each original input string exactly in the "original" field.
        11. Put the cleaned offense name in the "cleaned" field.

        Here are the values to clean:
        {values_to_be_cleaned}
    """)


def clean_column_offense_name(raw_records_offense_type_cleaned: ListOfRecords):
    offense_name_raw_values: list[str] = [
        record[CSVStandard.OFFENSE_NAME] for record in raw_records_offense_type_cleaned
    ]
    unique_values = list(
        {
            value.lower()
            for value in general_string_values_cleaning(offense_name_raw_values)
        }
    )

    client = initialize_gemini_api()
    prompt = offense_name_cleaning_prompt(unique_values)
    match_values_data = clean_values_with_gemini(prompt, client)

    match_values_mapping = {
        match_value.original: match_value.cleaned
        for match_value in match_values_data.items
    }

    cleaned_values: ListOfRecords = [
        {
            **record,
            CSVStandard.OFFENSE_NAME: match_values_mapping[
                record[CSVStandard.OFFENSE_NAME].lower()
            ],
        }
        for record in raw_records_offense_type_cleaned
    ]

    return cleaned_values
