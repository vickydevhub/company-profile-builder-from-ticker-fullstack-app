from typing import Any, List, Optional

from pydantic import BaseModel


class Candidate(BaseModel):
    value: str
    source: str
    source_url: str
    confidence: float


class ProfileFieldResponse(BaseModel):
    section: str
    field: str
    label: str

    value: Optional[Any] = None

    source: Optional[str] = None
    source_url: Optional[str] = None
    source_date: Optional[str] = None

    confidence: Optional[float] = None

    note: Optional[str] = None

    conflict: Optional[bool] = False
    candidates: Optional[List[Candidate]] = None


class ProfileResponse(BaseModel):
    status: str
    progress: int
    profile: Optional[List[ProfileFieldResponse]] = None
    error: Optional[str] = None