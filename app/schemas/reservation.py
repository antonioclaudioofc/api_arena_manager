from app.schemas.auth import ResponseUser
from pydantic import ConfigDict
from app.schemas.schedule import ResponseSchedule
from pydantic import BaseModel
from typing import Optional


class BaseReservation(BaseModel):
    schedule_id: Optional[int] = None


class RequestReservation(BaseReservation):
    schedule_id: int


class UpdateReservation(BaseReservation):
    pass


class ResponseReservation(BaseReservation):
    status: str
    schedule: ResponseSchedule
    created_at: str
    updated_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ResponseReservationAdmin(BaseModel):
    id: int
    status: str
    schedule: ResponseSchedule
    user: ResponseUser
    created_at: str
    updated_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
