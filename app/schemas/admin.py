from typing import List

from pydantic import BaseModel, field_validator

from app.shared.normalizers import normalize_string


class RequestScheduleBatch(BaseModel):
    court_id: int
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    interval_minutes: int
    weekdays: List[int]
    months: List[int]

    @field_validator("start_time", "end_time", "start_date", "end_date", mode="before")
    @classmethod
    def normalize_fiels(cls, value):
        return normalize_string(value)
