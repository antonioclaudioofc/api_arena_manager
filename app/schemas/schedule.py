from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.court import ResponseCourt


class BaseSchedule(BaseModel):
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    available: Optional[bool] = None
    court_id: Optional[int] = None


class RequestSchedule(BaseSchedule):
    date: str
    start_time: str
    end_time: str
    available: bool
    court_id: int


class UpdateSchedule(BaseSchedule):
    pass


class ResponseSchedule(BaseSchedule):
    id: int
    date: str
    start_time: str
    end_time: str
    available: bool
    court: ResponseCourt
    created_at: str
    updated_at: str | None

    model_config = ConfigDict(from_attributes=True)
