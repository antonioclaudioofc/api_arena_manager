from fastapi import APIRouter, Depends
from app.modules.auth.dependencies import get_current_user
from app.modules.reservation.dependencies import get_reservation_service
from app.schemas.reservation import RequestReservation
from starlette import status

from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
def create(
    data: RequestReservation,
    user=Depends(get_current_user),
    reservation_service=Depends(get_reservation_service),
):
    reservation_service.create(user, data)

    return {
        "message": "Reserva criada com sucesso"
    }


@router.get("/")
def list_all(
    reservation_service=Depends(get_reservation_service)
):
    return reservation_service.list_all()


@router.get("/me")
def list_my_reservations(
    user=Depends(get_current_user),
    reservation_service=Depends(get_reservation_service),
):
    return reservation_service.list_my_reservations(user)


@router.delete("/{reservation_id}", response_model=MessageResponse)
def cancel(
    reservation_id: int,
    user=Depends(get_current_user),
    reservation_service=Depends(get_reservation_service),
):
    reservation_service.cancel(user, reservation_id)

    return {
        "message": "Reserva cancelada com sucesso"
    }
