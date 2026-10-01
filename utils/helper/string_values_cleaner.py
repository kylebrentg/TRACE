import re
import unicodedata

from utils.helper.data_viewer import view_list
from utils.helper.program_tools import exit_now


def general_string_values_cleaning(column_raw_values: list[str]) -> list[str]:
    cleaned_values = []

    for raw_value in column_raw_values:
        cleaned_value = clean_invisible_characters(raw_value)
        cleaned_value = standardize_punctuation(cleaned_value)
        cleaned_value = tidy_spacing(cleaned_value)

        cleaned_values.append(cleaned_value)

    view_list(cleaned_values, representation=True)
    exit_now()

    return cleaned_values


# General Cleaning 1
def clean_invisible_characters(text: str) -> str:
    # Step 1: Turn multi-part or weird font versions of letters into plain keyboard characters.
    # (Example: Merges 'e' + separate accent mark into one standard 'é' so Python sees them as equal).
    text = unicodedata.normalize("NFKC", text)

    # Step 2: Delete characters that take up zero space on screen and serve no purpose in data.
    # (Example: \u200b is an invisible gap; \ufeff is a hidden file watermark from text editors).
    text = text.replace("\u200b", "").replace("\ufeff", "")

    # Step 3: Turn web spaces (&nbsp;), tabs, and line-break Enters into a standard spacebar space.
    # (Example: Stops a multi-line spreadsheet row or website copy-paste from splitting into pieces).
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[\r\n\t]+", " ", text)

    return text


# General Cleaning 2
def standardize_punctuation(text: str) -> str:
    # Step 1: Turn curly single quotes and smart apostrophes into standard straight quotes.
    # (Example: 'O’Connor' or ‘quoted’ becomes plain keyboard 'O\'Connor' or 'quoted').
    text = re.sub(r"[‘’‚‛`]", "'", text)

    # Step 2: Turn curly double quotes into standard straight double quotes.
    # (Example: “Hello” or „Hello” becomes plain keyboard "Hello").
    text = re.sub(r"[“”„‟«»]", '"', text)

    # Step 3: Turn long dashes (em-dash, en-dash, minus signs) into standard hyphens.
    # (Example: Word's auto-formatted 'cost — benefit' becomes 'cost - benefit').
    text = re.sub(r"[–—−֊־᐀‐‑‒–—―]", "-", text)

    return text


# General Cleaning 3
def tidy_spacing(text: str) -> str:
    # Step 1: Collapse repeated spaces between words down to exactly one single space.
    # (Example: 'Hello      world' becomes 'Hello world'. The regex \s+ catches any run of spaces).
    text = re.sub(r"\s+", " ", text)

    # Step 2: Remove spaces from the very beginning and very end of the entire string.
    # (Example: ' Hello world ' becomes 'Hello world').
    text = text.strip()

    return text
