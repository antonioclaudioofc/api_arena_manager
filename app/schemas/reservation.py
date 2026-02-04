from app.schemas.user import ResponseUser
from pydantic import ConfigDict
from app.schemas.schedule import ResponseSchedule
from app.schemas.court import ResponseCourt
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
    schedule: ResponseSchedule


    model_config = ConfigDict(from_attributes=True)


