from fastapi import APIRouter, Depends, Path, Query
from app.schemas.auth import ResponseUser
from app.schemas.reservation import ReservationResponseAdmin
from app.schemas.schedule import ScheduleCreate
from app.dependencies import db_dependency
from starlette import status
from typing import Annotated
from app.modules.auth.service import AuthService
from app.schemas.court import RequestCourt, UpdateCourt
from app.modules.admin.service import AdminService
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

user_dependency = Annotated[dict, Depends(AuthService.get_current_user)]


@router.get("/reservations", response_model=list[ReservationResponseAdmin], status_code=status.HTTP_200_OK)
def list_reservations(
    user: user_dependency,
    db: db_dependency
):
    return AdminService.list_reservations(user, db)


@router.get("/users", response_model=list[ResponseUser], status_code=status.HTTP_200_OK)
def list_users(
    user: user_dependency,
    db: db_dependency
):
    return AdminService.list_users(user, db)


@router.post("/courts", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_court(
    db: db_dependency,
    user: user_dependency,
    court_request: RequestCourt,
):
    AdminService.create_court(db, user, court_request)

    return {
        "message": "Quadra criada com sucesso"
    }


@router.put("/courts/{court_id}", response_model=MessageResponse)
def update_court(
    db: db_dependency,
    user: user_dependency,
    data: UpdateCourt,
    court_id: int
):
    AdminService.update_court(db, user, data, court_id)

    return {
        "message": "Quadra atualizada com sucesso"
    }


@router.delete("/courts/{court_id}", response_model=MessageResponse)
def delete_court(
    db: db_dependency,
    user: user_dependency,
    court_id: int = Path(gt=0)
):
    AdminService.delete_court(db, user, court_id)

    return {
        "message": "Quadra deletada com sucesso"
    }


@router.post("/schedules", status_code=status.HTTP_201_CREATED)
def create_schedule(
        user: user_dependency,
        schedule_request: ScheduleCreate,
        db: db_dependency
):
    AdminService.create_schedule(user, schedule_request, db)


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(user: user_dependency, db: db_dependency, schedule_id: int = Path(gt=0)):
    AdminService.delete_schedule(user, db, schedule_id)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user: user_dependency,
    db: db_dependency,
    user_id: int = Path(gt=0)
):
    AdminService.delete_user(user, db, user_id)
