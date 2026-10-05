import inspect
import json
import sys

from data.interim.offense_name_match_values import MATCH_VALUES_3
from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.helper.viewer_data import view_column_values, view_list_items, view_records
from utils.loading.init_gemini import initialize_gemini_api
from utils.types import ListOfRecords


def clean_column_offense_name(raw_records_offense_type_cleaned: ListOfRecords):
    offense_name_raw_values: list[str] = [
        record[CSVStandard.OFFENSE_NAME] for record in raw_records_offense_type_cleaned
    ]
    generally_cleaned_values = general_string_values_cleaning(offense_name_raw_values)
    generally_cleaned_values: list[str] = [
        value.lower() for value in generally_cleaned_values
    ]

    unique_values = list(set(generally_cleaned_values))
    match_values_json = clean_with_gemini(unique_values)
    match_values_data: list[dict[str, str]] = json.loads(match_values_json)
    match_values_mapping = {
        match_value["original"]: match_value["cleaned"]
        for match_value in match_values_data
    }

    """
    Goal: Update the values of the offense_name column based on the match_values_data_mapping
    1. I need to iterate over each record in the raw_records
    2. Then once I have a record or many dict[str, str] pairs, I am focusing only on the offense_name column and retaining the other pairs of that record
    3. (Mapping) On the current value of the current record for the offense_name, I will use that as a key
    """

    # view_column_values(
    #     raw_records_offense_type_cleaned, CSVStandard.OFFENSE_NAME, unique=True
    # )

    cleaned_values: ListOfRecords = [
        {
            **record,
            CSVStandard.OFFENSE_NAME: match_values_mapping[
                record[CSVStandard.OFFENSE_NAME].lower()
            ],
        }
        for record in raw_records_offense_type_cleaned
    ]

    # view_column_values(cleaned_values, CSVStandard.OFFENSE_NAME, unique=True)
    return cleaned_values


def clean_with_gemini(values_to_be_cleaned: list[str]):

    prompt = inspect.cleandoc(f"""
        You are a Philippine criminal law data cleaning assistant. You will be given a Python list of raw offense name strings extracted from a crime records database. These strings may contain:
        - Fragmented words caused by OCR errors (e.g., "manufactur e", "paraphernali a", "lasciviousne ss") — rejoin them into the correct word
        - Irregular spacing around hyphens
        - Inconsistent casing
        Your task is to return a cleaned version of each offense name. Apply these rules:
        1. Fix all fragmented words by merging them into their correct spelling
        2. Standardize the format as: "<Offense Name> - <Legal Basis>" (e.g., "Reckless Imprudence Resulting to Multiple Physical Injuries - RPC Art. 365")
        3. Use title case for the offense name portion
        4. Keep legal basis references uppercase and abbreviated (e.g., "RPC", "RA", "PD", "BP")
        5. Do not add, remove, or invent any offense — only clean what is given
        6. Remove grammatically incorrect commas inherited from OCR
           (e.g., commas before prepositions like ", of" or ", by").
           Do NOT remove hyphens — compound modifiers (e.g., "gender-based",
           "anti-child") must retain or gain their hyphen.
        7. Any bare act number (e.g., "3815") that refers to a Philippine law
           must be written as "Act No. 3815".
        8. The phrase "as amended by" should always be lowercase and not subject
           to title casing.
        9. Return ONLY a valid JSON array of objects, one per input value, with this exact structure:
        [
          {{
            "original": "<the original string>",
            "cleaned": "<the cleaned string>"
          }},
          ...
        ]
        Here are the values to clean:
        {values_to_be_cleaned}
    """)

    try:
        client = initialize_gemini_api()
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt,
            response_format={"type": "text", "mime_type": "application/json"},
        )

        if not interaction.output_text:
            raise ValueError(
                "The model returned an empty response or output was blocked."
            )

        print(interaction.output_text)
        return interaction.output_text
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
