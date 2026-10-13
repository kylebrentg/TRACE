import re
import unicodedata

from utils.constants import CSVStandard
from utils.helper.program_tools import exit_now
from utils.helper.viewer_data import view_list_items

# --- General String Values Cleaning ---


def general_string_values_cleaning(column_raw_values: list[str | None]) -> list[str | None]:
    cleaned_values = []

    for raw_value in column_raw_values:
        if raw_value is None:
            cleaned_values.append(None)
            continue
        cleaned_value = clean_invisible_characters(raw_value)
        cleaned_value = standardize_punctuation(cleaned_value)
        cleaned_value = tidy_spacing(cleaned_value)
        cleaned_value = convert_fake_nulls(cleaned_value)

        cleaned_values.append(cleaned_value)

    return cleaned_values


# General Cleaning 1
def clean_invisible_characters(text):
    if not isinstance(text, str):
        return text

    text = unicodedata.normalize("NFKC", text)

    # Drop all invisible format (Cf) and control (Cc) characters,
    # but keep whitespace so the next step can handle it.
    text = "".join(
        ch
        for ch in text
        if ch.isspace() or unicodedata.category(ch) not in ("Cf", "Cc")
    )

    # Collapse any run of Unicode whitespace into a single space and strip the ends.
    return " ".join(text.split())


# General Cleaning 2
def standardize_punctuation(text: str) -> str:
    text = re.sub(r"[‘’‚‛`]", "'", text)
    text = re.sub(r"[“”„‟«»]", '"', text)
    text = re.sub(r"[–—−֊־᐀‐‑‒–—―]", "-", text)

    return text


# General Cleaning 3
def tidy_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


# General Cleaning 4
def convert_fake_nulls(text: str | None) -> str | None:
    # Step 1: If already None, keep it as None
    if text is None:
        return None

    # Step 2: Strip whitespace and check if lowercased text is a placeholder
    if text.strip().lower() in CSVStandard.NULL_VALUE_PLACEHOLDERS:
        return None

    return text
