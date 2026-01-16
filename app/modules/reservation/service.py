from datetime import datetime, timezone
from app.models.reservation import Reservations
from app.modules.reservation.repository import ReservationRepository
from app.modules.schedule.repository import ScheduleRepository
from app.shared.exceptions import BadRequestException, NotFoundException, UnathorizedException


class ReservationService:

    @staticmethod
    def list_my_reservations(user: dict, db):
        if not user:
            raise UnathorizedException("Usuário não autenticado")

        return ReservationRepository.get_by_user(user["id"], db)

    @staticmethod
    def list_all(db):
        return ReservationRepository.get_all(db)

    @staticmethod
    def get(db, reservation_id: int):
        reservation = ReservationRepository.get_by_id(
            db,
            reservation_id
        )

        if not reservation:
            raise NotFoundException("Reserva não encontrada")

        return reservation

    @staticmethod
    def create(user: dict, db, reservation):
        if not user:
            raise UnathorizedException("Usuário não autenticado")

        schedule = ScheduleRepository.get_by_id(db, reservation.schedule_id)

        if not schedule:
            raise NotFoundException("Horário não encontrado")

        active_reservation = ReservationRepository.exists_active_by_schedule(
            db, reservation.schedule_id
        )

        if active_reservation:
            raise BadRequestException("Horário já está ocupado")

        reservation = Reservations(
            **reservation.model_dump(),
            user_id=user["id"],
            status="Ocupado",
            created_at=datetime.now(timezone.utc)
        )

        return ReservationRepository.create(reservation, db)

    @staticmethod
    def delete(user: dict, db, reservation_id: int):
        if not user:
            raise UnathorizedException("Usuário não autenticado")

        reservation = ReservationRepository.get_by_owner(
            user["id"],
            db,
            reservation_id
        )

        if not reservation:
            raise NotFoundException("Reserva não encontrada")

        ReservationRepository.delete(reservation, db)
