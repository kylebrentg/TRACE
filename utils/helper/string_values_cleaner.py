import re
import unicodedata

from utils.constants import CSVStandard
from utils.helper.viewer_data import view_list_items
from utils.helper.program_tools import exit_now

# --- General String Values Cleaning ---


def general_string_values_cleaning(column_raw_values: list[str]) -> list[str]:
    cleaned_values = []

    for raw_value in column_raw_values:
        cleaned_value = clean_invisible_characters(raw_value)
        cleaned_value = standardize_punctuation(cleaned_value)
        cleaned_value = tidy_spacing(cleaned_value)
        cleaned_value = fix_fragmented_words(cleaned_value)
        cleaned_value = convert_fake_nulls(cleaned_value)

        cleaned_values.append(cleaned_value)

    # view_list(cleaned_values, representation=True)
    # exit_now()

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
def fix_fragmented_words(text: str) -> str:
    """Rejoin words that were incorrectly split mid-word.

    Walks adjacent token pairs and merges them when:
      - The left token (letters only) is NOT a known dictionary word, AND
      - Concatenating the two tokens' letters IS a known dictionary word.

    Examples:
        "COMPREHENSI VE"   -> "COMPREHENSIVE"
        "MALVERSATIO N."   -> "MALVERSATION."
        "LASCIVIOUSNE SS"  -> "LASCIVIOUSNESS"
    """
    tokens = text.split()
    if len(tokens) <= 1:
        return text

    result: list[str] = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens):
            left = tokens[i]
            right = tokens[i + 1]

            # Extract only the alphabetic characters from each token.
            left_alpha = re.sub(r"[^a-zA-Z]", "", left)
            right_alpha = re.sub(r"[^a-zA-Z]", "", right)

            if left_alpha and right_alpha:
                joined_alpha = left_alpha + right_alpha
                left_is_known = bool(_spell.known([left_alpha.lower()]))
                joined_is_known = bool(_spell.known([joined_alpha.lower()]))

                if not left_is_known and joined_is_known:
                    # Preserve any trailing punctuation from the right token.
                    # e.g. right="N." -> right_alpha="N", trailing="."
                    trailing_punct = right[len(right_alpha):]
                    result.append(left + right_alpha + trailing_punct)
                    i += 2
                    continue

        result.append(tokens[i])
        i += 1

    return " ".join(result)


# General Cleaning 5
def convert_fake_nulls(text: str | None) -> str | None:
    # Step 1: If already None, keep it as None
    if text is None:
        return None

    # Step 2: Strip whitespace and check if lowercased text is a placeholder
    if text.strip().lower() in CSVStandard.NULL_VALUE_PLACEHOLDERS:
        return None

    return text
