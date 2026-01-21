from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from app.shared.normalizers import normalize_string


class BaseCourt(BaseModel):
    name: Optional[str] = None
    sports_type: Optional[str] = None
    price_per_hour: Optional[Decimal] = None

    @field_validator("name", "sports_type", mode="before")
    @classmethod
    def normalize_fields(cls, value):
        return normalize_string(value)


class RequestCourt(BaseCourt):
    arena_id: int
    name: str
    sports_type: str
    price_per_hour: Decimal


class UpdateCourt(BaseCourt):
    pass


class ResponseCourt(BaseModel):
    id: int
    arena_id: int
    name: str
    sports_type: str

    model_config = ConfigDict(from_attributes=True)
