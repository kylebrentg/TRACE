import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from rich.console import Console

from utils.constants import GeminiConstants
from utils.schemas import OffenseNameCleaningResponse

console = Console()


def initialize_gemini_api(column_name: str) -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    with console.status(
        f"[bold cyan]Initializing Gemini for `{column_name}`...",
        spinner="dots",
    ):
        client = genai.Client(api_key=api_key, http_options={"api_version": "v1"})

    console.print(f"[bold green]Gemini initialized for `{column_name}`.")
    return client


def clean_values_from_json(*, column_name: str) -> OffenseNameCleaningResponse:
    response_file = (
        Path(__file__).resolve().parents[2]
        / "data" / "interim" / f"gemini_{column_name}.json"
    )
    cached_response = json.loads(response_file.read_text(encoding="utf-8"))
    cleaned_values = OffenseNameCleaningResponse.model_validate(
        cached_response["response"]
    )
    console.print(f"[bold green]Using saved Gemini response for `{column_name}`.")
    return cleaned_values


def clean_values_with_gemini(
    prompt: str,
    client: genai.Client | None = None,
    *,
    column_name: str,
) -> OffenseNameCleaningResponse:
    if client is None:
        client = initialize_gemini_api(column_name)

    models = GeminiConstants.FLASH_LITE_MODELS
    failure: APIError | ValueError

    for model_index, model_name in enumerate(models):
        try:
            console.print(
                f"[bold cyan]Sending a `{column_name}` cleaning request to Gemini ({model_name})..."
            )
            with console.status(
                f"[bold cyan]Waiting for Gemini's response for `{column_name}`. Please wait; this may take a while...",
                spinner="dots",
            ):
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

                console.print(
                    f"[bold cyan]Gemini response received for `{column_name}`. Checking the results..."
                )
                output_text = interaction.output_text

                if not isinstance(output_text, str) or not output_text:
                    raise ValueError(
                        f"The model {model_name} returned an empty response "
                        "or output was blocked."
                    )

                cleaned_values = OffenseNameCleaningResponse.model_validate_json(
                    output_text
                )


                console.print(
                    f"[bold green]Gemini results validated for `{column_name}`. Cleaning request complete."
                )
                return cleaned_values

        except APIError as error:
            console.print(
                f"[bold red]Gemini request failed for `{column_name}` using {model_name} (API error): {error}"
            )
            failure = error
            error_details = (
                f"status={error.status!r}, code={error.code}, message={error.message!r}"
            )

        except ValueError as error:
            console.print(f"[bold red]Value error for `{column_name}`: {error}")
            failure = error
            error_details = f"response validation failed: {error}"

        print(f"Model {model_name} failed for `{column_name}`: {error_details}")

        if model_index == len(models) - 1:
            console.print(
                f"[bold red]Gemini cleaning request failed for `{column_name}`. All {len(models)} models failed; no validated results were returned."
            )
            raise RuntimeError(
                f"All Gemini fallback models failed after trying {len(models)} models."
            ) from failure

        next_model = models[model_index + 1]
        console.print(
            f"[bold yellow]Trying another Gemini model for `{column_name}`: switching from {model_name} to {next_model}. Please wait..."
        )

    raise RuntimeError("Gemini model loop exited unexpectedly.")
