import inspect

from google import genai
from google.genai.errors import APIError

from utils.constants import CSVStandard, GeminiConstants
from utils.helper.string_values_cleaner import general_string_values_cleaning
from utils.loading.init_gemini import initialize_gemini_api
from utils.schemas import OffenseNameCleaningResponse
from utils.types import ListOfRecords


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
    match_values_data = clean_with_gemini(unique_values, client)

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


def clean_with_gemini(
    values_to_be_cleaned: list[str],
    client: genai.Client,
) -> OffenseNameCleaningResponse:

    prompt = inspect.cleandoc(f"""
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

    models = GeminiConstants.FLASH_LITE_MODELS
    failure: APIError | ValueError

    for model_index, model_name in enumerate(models):
        try:
            interaction = client.interactions.create(
                model=model_name,
                system_instruction=(
                    "You are a Philippine criminal law data cleaning assistant."
                ),
                input=prompt,
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": OffenseNameCleaningResponse.model_json_schema(),
                },
                generation_config={
                    "temperature": GeminiConstants.TEMPERATURE,
                },
            )

            output_text = interaction.output_text

            if not isinstance(output_text, str) or not output_text:
                raise ValueError(
                    f"The model {model_name} returned an empty response "
                    "or output was blocked."
                )

            return OffenseNameCleaningResponse.model_validate_json(output_text)

        except APIError as error:
            failure = error
            error_details = (
                f"status={error.status!r}, code={error.code}, message={error.message!r}"
            )

        except ValueError as error:
            failure = error
            error_details = f"response validation failed: {error}"

        print(f"Model {model_name} failed: {error_details}")

        if model_index == len(models) - 1:
            raise RuntimeError(
                f"All Gemini fallback models failed after trying {len(models)} models."
            ) from failure

        next_model = models[model_index + 1]
        print(f"Switching from {model_name} to {next_model}.")

    raise RuntimeError("Gemini model loop exited unexpectedly.")
