from datetime import date, time
from typing import ClassVar


class CSVStandard:
    # Column names
    OFFENSE_TYPE = "offense_type"
    OFFENSE_NAME = "offense_name"
    DATE_COMMITTED = "date_committed"
    TIME_COMMITTED = "time_committed"
    BARANGAY = "barangay"
    TYPE_OF_PLACE = "type_of_place"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    CASE_STATUS = "case_status"

    HEADERS: ClassVar[tuple[str, ...]] = (
        OFFENSE_TYPE,
        OFFENSE_NAME,
        DATE_COMMITTED,
        TIME_COMMITTED,
        BARANGAY,
        TYPE_OF_PLACE,
        LATITUDE,
        LONGITUDE,
        CASE_STATUS,
    )

    HEADERS_LENGTH: ClassVar[int] = len(HEADERS)

    SCHEMA: ClassVar[dict[str, type]] = {
        OFFENSE_TYPE: str,
        OFFENSE_NAME: str,
        DATE_COMMITTED: date,
        TIME_COMMITTED: time,
        BARANGAY: str,
        TYPE_OF_PLACE: str,
        LATITUDE: float,
        LONGITUDE: float,
        CASE_STATUS: str,
    }

    BARANGAY_NAMES: ClassVar[frozenset[str]] = frozenset(
        {
            "Agapito del Rosario",
            "Amsic",
            "Anunas",
            "Balibago",
            "Capaya",
            "Claro M. Recto",
            "Cuayan",
            "Cutcut",
            "Cutud",
            "Lourdes North West",
            "Lourdes Sur",
            "Lourdes Sur East",
            "Malabañas (Malabanias)",
            "Margot",
            "Marisol (Ninoy Aquino)",
            "Mining",
            "Pampang (Santo Niño)",
            "Pandan",
            "Pulung Bulu",
            "Pulung Cacutud",
            "Pulung Maragul",
            "Salapungan",
            "San José",
            "San Nicolas",
            "Santa Teresita",
            "Santa Trinidad",
            "Santo Cristo",
            "Santo Domingo",
            "Santo Rosario (Población)",
            "Sapalibutad",
            "Sapangbato",
            "Tabun",
            "Virgen Delos Remedios",
        }
    )

    CASE_CRIME_STATUS: ClassVar[frozenset[str]] = frozenset(
        {
            "Solved",
            "Cleared",
            "Under Investigation",
        }
    )

    NULL_VALUE_PLACEHOLDERS: ClassVar[frozenset[str]] = frozenset(
        {
            "",
            "nan",
            "null",
            "none",
            "n/a",
            "na",
            "n.a.",
            "not available",
            "not applicable",
            "not reported",
            "not stated",
            "not provided",
            "undefined",
            "unknown",
            "?",
            "-",
            "--",
            "---",
        }
    )


class GeminiConstants:
    # 1. Flagship / Complex reasoning & heavy development
    PRO_MODELS: ClassVar[frozenset[str]] = frozenset(
        {
            "gemini-3.1-pro-preview",
        }
    )

    # 2. Ultra-low latency & cost-efficient batch processing
    FLASH_LITE_MODELS: ClassVar[tuple[str, ...]] = (
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
    )

    # 3. Standard workhorse models (balanced speed, intelligence, & context)
    FLASH_MODELS: ClassVar[frozenset[str]] = frozenset(
        {
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-3-flash-preview",
        }
    )

    # Combined text-only generation bucket
    TEXT_MODELS_BUCKET: ClassVar[frozenset[str]] = (
        PRO_MODELS | frozenset(FLASH_LITE_MODELS) | FLASH_MODELS
    )

    TEMPERATURE: ClassVar[float] = 0.0
    MAX_RETRIES: ClassVar[int] = 2
