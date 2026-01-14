from fastapi import APIRouter, Depends, Query, Path
from app.schemas.reservation import ResponseReservation, RequestReservation
from app.modules.auth.service import AuthService
from app.modules.reservation.service import ReservationService
from app.dependencies import db_dependency
from typing import Annotated
from starlette import status

from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

user_dependency = Annotated[dict, Depends(AuthService.get_current_user)]


@router.get("/me", response_model=list[ResponseReservation],  status_code=status.HTTP_200_OK)
def my_reservations(
    user: user_dependency,
    db: db_dependency
):
    return ReservationService.list_my_reservations(user, db)


@router.get("/", response_model=list[ResponseReservation], status_code=status.HTTP_200_OK)
def list_reservations(
    db: db_dependency
):
    return ReservationService.list_all(db)


@router.get("/{reservation_id}", response_model=ResponseReservation, status_code=status.HTTP_200_OK)
def get_reservation(
    db: db_dependency,
    reservation_id: int = Path(gt=0)
):
    return ReservationService.get(db, reservation_id)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    user: user_dependency,
    db: db_dependency,
    reservation_schedule: RequestReservation
):
    ReservationService.create(user, db, reservation_schedule)

    return {
        "message": "Reserva criada com sucesso"
    }


@router.delete("/{reservation_id}", response_model=MessageResponse)
def delete_reservation(
    user: user_dependency,
    db: db_dependency,
    reservation_id: int = Path(gt=0)
):
    ReservationService.delete(user, db, reservation_id)

    return {
        "message": "Reserva deletada com sucesso"
    }
