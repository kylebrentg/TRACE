from datetime import date, time
from typing import ClassVar


class CSVStandard:
    # Column names
    OFFENSE_TYPE = "offense_type"
    OFFENSE_NAME = "offense_name"
    MODUS_OPERANDI = "modus_operandi"
    DATE_COMMITTED = "date_committed"
    TIME_COMMITTED = "time_committed"
    BARANGAY = "barangay"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    POLICE_STATION_NUMBER = "police_station_number"
    CASE_STATUS = "case_status"

    HEADERS: ClassVar[tuple[str, ...]] = (
        OFFENSE_TYPE,
        OFFENSE_NAME,
        MODUS_OPERANDI,
        DATE_COMMITTED,
        TIME_COMMITTED,
        BARANGAY,
        LATITUDE,
        LONGITUDE,
        POLICE_STATION_NUMBER,
        CASE_STATUS,
    )

    HEADERS_LENGTH: ClassVar[int] = len(HEADERS)

    SCHEMA: ClassVar[dict[str, type]] = {
        OFFENSE_TYPE: str,
        OFFENSE_NAME: str,
        MODUS_OPERANDI: str,
        DATE_COMMITTED: date,
        TIME_COMMITTED: time,
        BARANGAY: str,
        LATITUDE: float,
        LONGITUDE: float,
        POLICE_STATION_NUMBER: str,
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
