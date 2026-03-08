from datetime import time
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.shared.normalizers import normalize_string


class BaseArena(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    @field_validator(
        "name",
        "description",
        "phone",
        "email",
        "city",
        "address",
        "state",
        "zip_code",
        mode="before"
    )
    @classmethod
    def normalize_fiels(cls, value):
        return normalize_string(value)

    @field_validator("opening_time", "closing_time", mode="before")
    @classmethod
    def parse_time_with_timezone(cls, value):
        if value is None or isinstance(value, time):
            return value

        if isinstance(value, str):
            raw_value = value.strip()
            if raw_value.endswith("Z"):
                raw_value = raw_value[:-1] + "+00:00"

            parsed_time = time.fromisoformat(raw_value)
            return parsed_time.replace(tzinfo=None)

        return value


class RequestArena(BaseArena):
    name: str
    phone: str
    city: str
    address: str
    state: str
    zip_code: str


class UpdateArena(BaseArena):
    pass


class ResponseArena(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    phone: str
    email: Optional[str] = None
    city: str
    address: str
    state: str
    zip_code: str
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    model_config = ConfigDict(from_attributes=True)
