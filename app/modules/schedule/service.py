from datetime import date, datetime, timedelta, timezone
from app.models.schedule import Schedule
from app.modules.schedule.exceptions import ConflictException
from app.shared.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException
)


class ScheduleService:

    def __init__(
        self,
        schedule_repo,
        court_service,
    ):
        self.schedule_repo = schedule_repo
        self.court_service = court_service

    def create(self, user, data):
        court = self.court_service.get_by_id(data.court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        if court.arena.owner_id != user.id:
            raise ForbiddenException("Sem permissão")

        schedule_date = date.fromisoformat(data.date)
        today = date.today()

        if schedule_date < today:
            raise BadRequestException(
                "Não é possível criar horários para datas no passado"
            )

        start_time = datetime.strptime(data.start_time, "%H:%M")
        end_time = datetime.strptime(data.end_time, "%H:%M")

        if start_time >= end_time:
            raise BadRequestException(
                "Horário inicial deve ser menor que o horário final"
            )

        schedule = Schedule(
            **data.model_dump(),
            created_at=datetime.now(timezone.utc)
        )

        self.schedule_repo.create(schedule)

    def create_batch(self, user, data):
        court = self.court_service.get_by_id(data.court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        if court.arena.owner_id != user.id:
            raise ForbiddenException("Sem permissão")

        if data.interval_minutes <= 0:
            raise BadRequestException("Intervalo inválido")

        start_date = date.fromisoformat(data.start_date)
        end_date = date.fromisoformat(data.end_date)
        today = date.today()

        if start_date < today:
            raise BadRequestException("Data inicial não pode ser no passado")

        if end_date < start_date:
            raise BadRequestException(
                "Data final deve ser maior que a inicial")

        current_time = datetime.strptime(data.start_time, "%H:%M")
        end_time_limit = datetime.strptime(data.end_time, "%H:%M")

        if current_time >= end_time_limit:
            raise BadRequestException(
                "Horário inicial deve ser menor que o final"
            )

        weekdays = data.weekdays if data.weekdays else [0, 1, 2, 3, 4, 5, 6]

        schedules_to_create = []
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() not in weekdays:
                current_date += timedelta(days=1)
                continue

            current_time = datetime.strptime(data.start_time, "%H:%M")

            while current_time < end_time_limit:
                next_time = current_time + timedelta(
                    minutes=data.interval_minutes
                )

                if next_time > end_time_limit:
                    break

                if self.schedule_repo.exists(
                    court_id=data.court_id,
                    date=current_date.isoformat(),
                    start_time=current_time.strftime("%H:%M"),
                    end_time=next_time.strftime("%H:%M"),
                ):
                    raise ConflictException("Horário já existente")

                schedules_to_create.append(
                    Schedule(
                        court_id=data.court_id,
                        date=current_date.isoformat(),
                        start_time=current_time.strftime("%H:%M"),
                        end_time=next_time.strftime("%H:%M"),
                        created_at=datetime.now(timezone.utc),
                    )
                )

                current_time = next_time

            current_date += timedelta(days=1)

        self.schedule_repo.bulk_create(schedules_to_create)

    def get_by_id(self, schedule_id):
        return self.schedule_repo.get_by_id(schedule_id)

    def list_by_court(self, court_id):
        rows = self.schedule_repo.list_with_availability(court_id)

        courts = []
        for schedule, reservation_id in rows:
            courts.append({
                "id": schedule.id,
                "date": schedule.date,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "court_id": schedule.court_id,
                "is_available": reservation_id is None
            })

        return courts

    def update(self, user, data, schedule_id):
        schedule = self.schedule_repo.get_by_id(schedule_id)

        if not schedule:
            raise NotFoundException("Horário não encontrado")

        court = schedule.court
        if court.arena.owner_id != user.id:
            raise ForbiddenException("Sem permissão")

        if data.date is not None:
            schedule.date = data.date

        if data.start_time is not None:
            schedule.start_time = data.start_time

        if data.end_time is not None:
            schedule.end_time = data.end_time

        schedule.updated_at = datetime.now(timezone.utc)

        self.schedule_repo.update(schedule)

    def delete(self, user, schedule_id):
        schedule = self.schedule_repo.get_by_id(schedule_id)

        if not schedule:
            raise NotFoundException("Horário não encontrado")

        court = schedule.court

        if court.arena.owner_id != user.id:
            raise ForbiddenException("Sem permissão")

        self.schedule_repo.delete(schedule)
