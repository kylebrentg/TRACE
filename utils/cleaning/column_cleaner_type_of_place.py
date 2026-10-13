import inspect

from utils.constants import CSVStandard
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.loading.init_gemini import clean_values_with_gemini, initialize_gemini_api
from utils.types import ListOfRecords


def _type_of_place_cleaning_prompt(values_to_be_cleaned: list[str]) -> str:
    return inspect.cleandoc(f"""
        You are standardizing raw 'type_of_place' strings from Philippine police crime reports.
        Input strings contain OCR errors (split words, irregular slashes) and raw parenthetical notes.

        Task:
        Transform each raw string into a readable, grammatically correct English sentence or elaborated description that preserves the full context and specific examples (e.g., sub-types, vehicle types, facility types).

        Guidelines:
        1. Fix OCR splits (e.g., "unocc upied" -> "unoccupied", "b usiness" -> "business", "co nd" -> "condo", "mosq ue" -> "mosque").
        2. Expand abbreviations and slashes into natural English (e.g., "fx" -> "FX", "jeep" -> "jeepney", "bldg" -> "building").
        3. Retain all contextual details and examples, weaving them naturally into a complete, readable sentence or elaborated phrase rather than leaving awkward raw parentheticals or trailing checklists.
        4. Use proper capitalization and sentence punctuation.
        5. Return one mapping per input. Keep the exact raw input in 'original' and the elaborated English text in 'cleaned'.

        Input values:
        {values_to_be_cleaned}
    """)


def clean_column_type_of_place(
    raw_records_offense_name_cleaned: ListOfRecords,
) -> ListOfRecords:
    type_of_place_raw_values: list[str] = [
        record[CSVStandard.TYPE_OF_PLACE] for record in raw_records_offense_name_cleaned
    ]

    # view_list_items(type_of_place_raw_values, "type_of_place Raw Values", unique=True)

    unique_values = list(
        {
            value.lower()
            for value in general_string_values_cleaning(type_of_place_raw_values)
            if value
        }
    )

    client = initialize_gemini_api()
    prompt = _type_of_place_cleaning_prompt(unique_values)
    match_values_data = clean_values_with_gemini(prompt, client)

    match_values_mapping = {
        match_value.original.strip().lower(): match_value.cleaned
        for match_value in match_values_data.items
    }

    for original, cleaned in match_values_mapping.items():
        print(f"('original', '{original}'): ('cleaned', '{cleaned}')")

    cleaned_values: ListOfRecords = [
        {
            **record,
            CSVStandard.TYPE_OF_PLACE: match_values_mapping.get(
                record[CSVStandard.TYPE_OF_PLACE].strip().lower(),
                record[CSVStandard.TYPE_OF_PLACE],
            )
            if general_string_values_cleaning([record[CSVStandard.TYPE_OF_PLACE]])[0] is not None
            else None,
        }
        for record in raw_records_offense_name_cleaned
    ]

    return cleaned_values
