from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.schemas.court import ResponseCourt


class BaseSchedule(BaseModel):
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class RequestSchedule(BaseSchedule):
    court_id: UUID
    date: str
    start_time: str
    end_time: str


class UpdateSchedule(BaseSchedule):
    pass


class ResponseSchedule(BaseSchedule):
    id: UUID
    court_id: UUID
    date: str
    start_time: str
    end_time: str
    court: ResponseCourt

    model_config = ConfigDict(from_attributes=True)


class ResponseScheduleWithAvailability(ResponseSchedule):
    available: bool


class RequestScheduleBatch(BaseModel):
    court_id: UUID
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    interval_minutes: int
    weekdays: List[int]
