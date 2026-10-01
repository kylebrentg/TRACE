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
