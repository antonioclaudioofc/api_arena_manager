from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from app.shared.normalizers import normalize_string


class BaseArena(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

    @field_validator("name", "city", "address", mode="before")
    @classmethod
    def normalize_fiels(cls, value):
        return normalize_string(value)


class RequestArena(BaseArena):
    name: str
    city: str
    address: str


class UpdateArena(BaseArena):
    pass


class ResponseArena(BaseModel):
    id: int
    owner_id: int
    name: str
    city: str
    address: str

    model_config = ConfigDict(from_attributes=True)
