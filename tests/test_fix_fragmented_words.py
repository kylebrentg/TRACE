"""Tests for fix_fragmented_words in string_values_cleaner."""

import pytest

from utils.helper.string_values_cleaner import (
    fix_fragmented_words,
    general_string_values_cleaning,
)


# --- Core fragmented-word cases from the task ---


class TestFragmentedWordsFromTaskData:
    """Every fragmented example mentioned in the original task."""

    def test_comprehensi_ve(self):
        assert fix_fragmented_words("COMPREHENSI VE") == "COMPREHENSIVE"

    def test_manufactur_e(self):
        assert fix_fragmented_words("MANUFACTUR E") == "MANUFACTURE"

    def test_malversatio_n(self):
        assert fix_fragmented_words("MALVERSATIO N") == "MALVERSATION"

    def test_paraphernali_a(self):
        assert fix_fragmented_words("PARAPHERNALI A") == "PARAPHERNALIA"

    def test_lasciviousne_ss(self):
        assert fix_fragmented_words("LASCIVIOUSNE SS") == "LASCIVIOUSNESS"

    def test_discriminati_on(self):
        assert fix_fragmented_words("DISCRIMINATI ON") == "DISCRIMINATION"


# --- Full offense_name strings from the task ---


class TestFullOffenseNameStrings:
    """End-to-end on realistic multi-word strings."""

    def test_comprehensive_law_on_firearms(self):
        inp = "COMPREHENSI VE LAW ON FIREARMS AND AMMUNITION - RA 10591 (covers RA 9516, RA 8294, PD 1866)"
        exp = "COMPREHENSIVE LAW ON FIREARMS AND AMMUNITION - RA 10591 (covers RA 9516, RA 8294, PD 1866)"
        assert fix_fragmented_words(inp) == exp

    def test_malversation_with_trailing_period(self):
        inp = "MALVERSATIO N OF PUBLIC FUNDS OR PROPERTY; PRESUMPTION OF MALVERSATIO N. - RPC Art. 217"
        exp = "MALVERSATION OF PUBLIC FUNDS OR PROPERTY; PRESUMPTION OF MALVERSATION. - RPC Art. 217"
        assert fix_fragmented_words(inp) == exp

    def test_comprehensive_drugs_and_paraphernalia(self):
        inp = (
            "COMPREHENSI VE DANGEROUS DRUGS ACT OF 2002 - POSSESSION OF EQUIPMENT, "
            "INSTRUMENT, APPARATUS AND OTHER PARAPHERNALI A FOR DANGEROUS DRUGS "
            "DURING PARTIES, SOCIAL GATHERINGS OR MEETINGS - RA 9165 Article II Section 14"
        )
        exp = (
            "COMPREHENSIVE DANGEROUS DRUGS ACT OF 2002 - POSSESSION OF EQUIPMENT, "
            "INSTRUMENT, APPARATUS AND OTHER PARAPHERNALIA FOR DANGEROUS DRUGS "
            "DURING PARTIES, SOCIAL GATHERINGS OR MEETINGS - RA 9165 Article II Section 14"
        )
        assert fix_fragmented_words(inp) == exp

    def test_acts_of_lasciviousness(self):
        inp = "ACTS OF LASCIVIOUSNE SS - RPC Art. 336"
        exp = "ACTS OF LASCIVIOUSNESS - RPC Art. 336"
        assert fix_fragmented_words(inp) == exp

    def test_discrimination_act(self):
        inp = "SPECIAL PROTECTION OF CHILDREN AGAINST CHILD ABUSE, EXPLOITATION AND DISCRIMINATI ON ACT. (ANTI- CHILD ABUSE LAW) - RA 7610"
        exp = "SPECIAL PROTECTION OF CHILDREN AGAINST CHILD ABUSE, EXPLOITATION AND DISCRIMINATION ACT. (ANTI- CHILD ABUSE LAW) - RA 7610"
        assert fix_fragmented_words(inp) == exp

    def test_comprehensive_dangerous_drugs_act(self):
        inp = "COMPREHENSI VE DANGEROUS DRUGS ACT OF 2002 - RA 9165"
        exp = "COMPREHENSIVE DANGEROUS DRUGS ACT OF 2002 - RA 9165"
        assert fix_fragmented_words(inp) == exp


# --- Strings that should NOT be modified ---


class TestNoFalsePositives:
    """Legitimate word sequences must not be merged."""

    def test_of_public_stays_separate(self):
        assert fix_fragmented_words("OF PUBLIC") == "OF PUBLIC"

    def test_on_firearms_stays_separate(self):
        assert fix_fragmented_words("ON FIREARMS") == "ON FIREARMS"

    def test_anti_dash_carnapping_unchanged(self):
        inp = "NEW ANTI- CARNAPPING ACT OF 2016 - MC - RA 10883 (repealed RA 6539)"
        assert fix_fragmented_words(inp) == inp

    def test_murder_unchanged(self):
        assert fix_fragmented_words("MURDER - RPC Art. 248") == "MURDER - RPC Art. 248"

    def test_robbery_unchanged(self):
        inp = "ROBBERY WITH VIOLENCE AGAINST OR INTIMIDATION OF PERSONS - RPC Art. 294"
        assert fix_fragmented_words(inp) == inp

    def test_safe_spaces_act_unchanged(self):
        inp = "SAFE SPACES ACT (GENDER BASED SEXUAL HARASSMENT) - RA 11313"
        assert fix_fragmented_words(inp) == inp

    def test_cybercrime_unchanged(self):
        inp = "CYBERCRIME PREVENTION ACT OF 2012 - RA 10175"
        assert fix_fragmented_words(inp) == inp


# --- Edge cases ---


class TestEdgeCases:

    def test_empty_string(self):
        assert fix_fragmented_words("") == ""

    def test_single_word(self):
        assert fix_fragmented_words("MURDER") == "MURDER"

    def test_single_unknown_word(self):
        # A lone unknown word with no neighbor cannot be merged.
        assert fix_fragmented_words("COMPREHENSI") == "COMPREHENSI"

    def test_only_numbers(self):
        assert fix_fragmented_words("10591 9165") == "10591 9165"

    def test_number_next_to_word(self):
        assert fix_fragmented_words("RA 10591") == "RA 10591"

    def test_multiple_spaces_collapsed_and_merged(self):
        # str.split() collapses runs of whitespace, so double-space still merges.
        assert fix_fragmented_words("COMPREHENSI  VE") == "COMPREHENSIVE"

    def test_all_caps_and_lowercase_both_work(self):
        assert fix_fragmented_words("comprehensi ve") == "comprehensive"
        assert fix_fragmented_words("COMPREHENSI VE") == "COMPREHENSIVE"

    def test_mixed_case_realistic(self):
        # In practice the data is all-uppercase, but test title-case fragments
        assert fix_fragmented_words("Comprehensi ve") == "Comprehensive"

    def test_punctuation_on_right_token(self):
        assert fix_fragmented_words("MALVERSATIO N.") == "MALVERSATION."

    def test_three_fragment_chain(self):
        # If a word were split into 3 parts, we can only merge pairwise left-to-right.
        # "COMPREHEN SI VE" -> first pass merges "COMPREHEN"+"SI" if valid,
        # otherwise tries "SI"+"VE". Neither "comprehensi" nor "sive" is a word.
        # This is an inherent limitation; 3-way splits are not observed in the data.
        result = fix_fragmented_words("COMPREHEN SI VE")
        # None of the pairs form a valid word, so nothing merges
        assert result == "COMPREHEN SI VE"


# --- Pipeline integration ---


class TestPipelineIntegration:
    """fix_fragmented_words is called inside general_string_values_cleaning."""

    def test_full_pipeline_fixes_fragments(self):
        raw = ["COMPREHENSI VE LAW ON FIREARMS"]
        cleaned = general_string_values_cleaning(raw)
        assert cleaned == ["COMPREHENSIVE LAW ON FIREARMS"]

    def test_full_pipeline_fragments_and_spacing(self):
        # Invisible chars + extra spaces + fragment
        raw = ["COMPREHENSI\u00a0 VE  LAW"]
        cleaned = general_string_values_cleaning(raw)
        assert cleaned == ["COMPREHENSIVE LAW"]

    def test_full_pipeline_fragments_with_fake_null(self):
        raw = ["nan"]
        cleaned = general_string_values_cleaning(raw)
        assert cleaned == [None]

    def test_full_pipeline_preserves_clean_strings(self):
        raw = ["MURDER - RPC Art. 248"]
        cleaned = general_string_values_cleaning(raw)
        assert cleaned == ["MURDER - RPC Art. 248"]
