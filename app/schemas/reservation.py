from pydantic import ConfigDict
from app.schemas.schedule import ResponseSchedule
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.shared.enums.reservation import ReservationStatus


class RequestReservation(BaseModel):
    schedule_id: UUID


class UpdateReservation(BaseModel):
    status: ReservationStatus


class ResponseReservation(BaseModel):
    id: UUID
    schedule_id: UUID
    user_id: UUID
    status: ReservationStatus
    schedule: ResponseSchedule

    model_config = ConfigDict(from_attributes=True)


class ResponseReservationOwnerClient(BaseModel):
    id: UUID
    name: str
    email: str


class ResponseReservationOwnerArena(BaseModel):
    id: UUID
    name: str


class ResponseReservationOwnerCourt(BaseModel):
    id: UUID
    name: str


class ResponseReservationOwnerSchedule(BaseModel):
    id: UUID
    date: str
    start_time: str
    end_time: str


class ResponseOwnerReservation(BaseModel):
    id: UUID
    status: ReservationStatus
    created_at: datetime | None
    cancelled_at: datetime | None
    schedule: ResponseReservationOwnerSchedule
    court: ResponseReservationOwnerCourt
    arena: ResponseReservationOwnerArena
    client: ResponseReservationOwnerClient
