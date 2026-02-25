from app.schemas.user import ResponseUser
from pydantic import ConfigDict
from app.schemas.schedule import ResponseSchedule
from app.schemas.court import ResponseCourt
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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


class ResponseReservationOwnerClient(BaseModel):
    id: int
    name: str
    email: str


class ResponseReservationOwnerArena(BaseModel):
    id: int
    name: str


class ResponseReservationOwnerCourt(BaseModel):
    id: int
    name: str


class ResponseReservationOwnerSchedule(BaseModel):
    id: int
    date: str
    start_time: str
    end_time: str


class ResponseOwnerReservation(BaseModel):
    id: int
    status: ReservationStatus
    created_at: datetime | None
    cancelled_at: datetime | None
    schedule: ResponseReservationOwnerSchedule
    court: ResponseReservationOwnerCourt
    arena: ResponseReservationOwnerArena
    client: ResponseReservationOwnerClient
