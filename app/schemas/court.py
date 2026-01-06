from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from app.shared.normalizers import normalize_string


class BaseCourt(BaseModel):
    name: Optional[str] = None
    sports_type: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name", "sports_type", "description", mode="before")
    @classmethod
    def normalize_fields(cls, value):
        if value is None:
            return value
        return normalize_string(value)


class RequestCourt(BaseCourt):
    name: str
    sports_type: str
    description: Optional[str] = None


class UpdateCourt(BaseCourt):
    pass


class ResponseCourt(BaseModel):
    id: int
    name: str
    sports_type: str
    description: Optional[str]
    created_at: str
    updated_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
