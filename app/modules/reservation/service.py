from datetime import datetime, timezone, date
from app.models.reservation import Reservation
from app.shared.enums import ReservationStatus, UserRole
from app.shared.exceptions import BadRequestException, ForbiddenException, NotFoundException


class ReservationService:

    def __init__(
        self,
        reservation_repo,
        schedule_service,
    ):
        self.reservation_repo = reservation_repo
        self.schedule_service = schedule_service

    def create(self, user, data):
        if user.role != UserRole.client:
            raise ForbiddenException("Apenas clientes podem fazer reservas")

        schedule = self.schedule_service.get_by_id(data.schedule_id)

        if not schedule:
            raise NotFoundException("Horário não encontrado")

        schedule_date = date.fromisoformat(schedule.date)
        today = date.today()

        if schedule_date < today:
            raise BadRequestException(
                "Não é possível reservar horários passados"
            )

        active_reservation = self.reservation_repo.get_active_by_schedule(
            data.schedule_id
        )

        if active_reservation:
            raise BadRequestException("Horário já está reservado")

        reservation = Reservation(
            schedule_id=data.schedule_id,
            client_id=user.id,
            status=ReservationStatus.active,
            created_at=datetime.now(timezone.utc),
        )

        return self.reservation_repo.create(reservation)

    def list_all(self):
        return self.reservation_repo.list_all()

    def list_my_reservations(self, user):
        return self.reservation_repo.list_by_client(user.id)

    def cancel(self, user, reservation_id: int):
        reservation = self.reservation_repo.get_by_id(reservation_id)

        if not reservation:
            raise NotFoundException("Reserva não encontrada")

        if (reservation.client_id != user.id):
            raise ForbiddenException("Sem permissão")

        if reservation.status == ReservationStatus.cancelled:
            raise BadRequestException("Reserva já cancelada")

        reservation.status = ReservationStatus.cancelled
        reservation.cancelled_at = datetime.now(timezone.utc)
        reservation.updated_at = datetime.now(timezone.utc)

        return self.reservation_repo.update(reservation)
