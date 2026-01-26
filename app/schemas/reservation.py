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
    created_at: str

    model_config = ConfigDict(from_attributes=True)



class ResponseReservationEnriched(BaseModel):
    id: int
    status: ReservationStatus
    created_at: str
    cancelled_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    client: ResponseUser
    
    schedule: ResponseSchedule
    
    court: ResponseCourt
    
    arena_name: str
    arena_city: str
    arena_address: str

    model_config = ConfigDict(from_attributes=True)

