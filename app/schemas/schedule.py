from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.court import ResponseCourt


class BaseSchedule(BaseModel):
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class RequestSchedule(BaseSchedule):
    court_id: int
    date: str
    start_time: str
    end_time: str


class UpdateSchedule(BaseSchedule):
    pass


class ResponseSchedule(BaseSchedule):
    id: int
    court_id: int
    date: str
    start_time: str
    end_time: str

    model_config = ConfigDict(from_attributes=True)


class ResponseScheduleWithAvailability(ResponseSchedule):
    available: bool
