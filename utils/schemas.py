from pydantic import BaseModel


class OffenseNameMapping(BaseModel):
    """A single original → cleaned offense name mapping."""
    original: str
    cleaned: str


class OffenseNameCleaningResponse(BaseModel):
    """The expected JSON structure returned by Gemini for offense name cleaning."""
    items: list[OffenseNameMapping]
