from fastapi import Depends
from app.modules.reservation.repository import ReservationRepository
from app.dependencies import db_dependency
from app.modules.reservation.service import ReservationService
from app.modules.schedule.dependencies import get_schedule_service


def get_reservation_repository(db: db_dependency):
    return ReservationRepository(db)


def get_reservation_service(
    reservation_repo=Depends(get_reservation_repository),
    schedule_service=Depends(get_schedule_service)
):
    return ReservationService(reservation_repo, schedule_service)
