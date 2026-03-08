from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from uuid import UUID
from app.shared.normalizers import normalize_string


class BaseCourt(BaseModel):
    name: Optional[str] = None
    sport_type: Optional[str] = None
    surface_type: Optional[str] = None
    price_per_hour: Optional[Decimal] = None

    @field_validator("name", "sport_type", "surface_type", mode="before")
    @classmethod
    def normalize_fields(cls, value):
        return normalize_string(value)


class RequestCourt(BaseCourt):
    arena_id: UUID
    name: str
    sport_type: str
    price_per_hour: Decimal


class UpdateCourt(BaseCourt):
    pass


class ResponseCourt(BaseModel):
    id: UUID
    slug: Optional[str] = None
    name: str
    arena_id: UUID
    sport_type: str
    surface_type: str
    price_per_hour: Decimal

    model_config = ConfigDict(from_attributes=True)
