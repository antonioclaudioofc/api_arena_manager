import datetime
from app.schemas.user import ResponseUser
from pydantic import ConfigDict
from app.schemas.schedule import ResponseSchedule
from pydantic import BaseModel
from typing import Optional

from app.shared.enums import ReservationStatus


class RequestReservation(BaseModel):
    schedule_id: int


class UpdateReservation(BaseModel):
    status: ReservationStatus


class ResponseReservation(BaseModel):
    id: int
    schedule_id: int
    client_id: int
    status: ReservationStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponseReservationAdmin(BaseModel):
    id: int
    status: str
    schedule: ResponseSchedule
    user: ResponseUser
    created_at: str
    updated_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
