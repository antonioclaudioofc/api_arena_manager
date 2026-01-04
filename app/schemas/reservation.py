from pydantic import BaseModel, ConfigDict
from app.schemas.auth import ResponseUser
from app.schemas.schedule import ScheduleResponse


class ReservationCreate(BaseModel):
    status: str
    schedule_id: int
    owner_id: int

    created_at: str
    updated_at: str | None


class ReservationResponse(BaseModel):
    id: int
    status: str
    schedule: ScheduleResponse
    created_at: str
    updated_at: str | None

    model_config = ConfigDict(from_attributes=True)


class ReservationResponseAdmin(BaseModel):
    id: int
    status: str
    schedule: ScheduleResponse
    user: ResponseUser
    created_at: str
    updated_at: str | None

    model_config = ConfigDict(from_attributes=True)
