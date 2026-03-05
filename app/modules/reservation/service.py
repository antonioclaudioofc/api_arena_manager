from datetime import datetime, timezone, date
from app.models.reservation import Reservation
from app.messaging.producer import producer
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

    def create(self, user, data, background_tasks):
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
        reservation = self.reservation_repo.create(reservation)

        owner = schedule.court.arena.owner
        payload = {
            "reservation": {
                "id": reservation.id,
                "status": reservation.status,
                "date": schedule.date,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
            },
            "arena": {
                "id": schedule.court.arena.id,
                "name": schedule.court.arena.name,
            },
            "court": {
                "id": schedule.court.id,
                "name": schedule.court.name,
            },
            "owner": {
                "id": owner.id,
                "name": owner.name,
                "email": owner.email,
            },
            "client": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }
        }

        producer.publish_message('reservation_created', {
            **payload,
            "recipient": "owner"
        })
        producer.publish_message('reservation_created', {
            **payload,
            "recipient": "client"
        })

        return reservation

    def list_all(self):
        return self.reservation_repo.list_all()

    def list_my_reservations(self, user):
        return self.reservation_repo.list_by_client(user.id)

    def list_owner_reservations(self, user):
        if user.role != UserRole.owner:
            raise ForbiddenException(
                "Apenas donos podem visualizar essas reservas")

        reservations = self.reservation_repo.list_by_owner(user.id)

        return [
            {
                "id": reservation.id,
                "status": reservation.status,
                "created_at": reservation.created_at,
                "cancelled_at": reservation.cancelled_at,
                "schedule": {
                    "id": reservation.schedule.id,
                    "date": reservation.schedule.date,
                    "start_time": reservation.schedule.start_time,
                    "end_time": reservation.schedule.end_time,
                },
                "court": {
                    "id": reservation.schedule.court.id,
                    "name": reservation.schedule.court.name,
                },
                "arena": {
                    "id": reservation.schedule.court.arena.id,
                    "name": reservation.schedule.court.arena.name,
                },
                "client": {
                    "id": reservation.client.id,
                    "name": reservation.client.name,
                    "email": reservation.client.email,
                }
            }
            for reservation in reservations
        ]

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

        reservation = self.reservation_repo.update(reservation)

        owner = reservation.schedule.court.arena.owner
        payload = {
            "reservation": {
                "id": reservation.id,
                "status": reservation.status,
                "date": reservation.schedule.date,
                "start_time": reservation.schedule.start_time,
                "end_time": reservation.schedule.end_time,
                "cancelled_at": (
                    reservation.cancelled_at.isoformat()
                    if reservation.cancelled_at else None
                )
            },
            "arena": {
                "id": reservation.schedule.court.arena.id,
                "name": reservation.schedule.court.arena.name,
            },
            "court": {
                "id": reservation.schedule.court.id,
                "name": reservation.schedule.court.name,
            },
            "owner": {
                "id": owner.id,
                "name": owner.name,
                "email": owner.email,
            },
            "client": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }
        }

        producer.publish_message('reservation_cancelled', {
            **payload,
            "recipient": "owner"
        })
        producer.publish_message('reservation_cancelled', {
            **payload,
            "recipient": "client"
        })

        return reservation
