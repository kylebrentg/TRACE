import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

from utils.constants import GeminiConstants
from utils.schemas import OffenseNameCleaningResponse


def initialize_gemini_api() -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key, http_options={"api_version": "v1"})
    return client


def clean_values_with_gemini(
    prompt: str,
    client: genai.Client | None = None,
) -> OffenseNameCleaningResponse:
    if client is None:
        client = initialize_gemini_api()

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
