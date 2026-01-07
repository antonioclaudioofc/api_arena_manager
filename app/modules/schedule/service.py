from datetime import date, datetime, timedelta, timezone
from app.models.schedule import Schedules
from app.modules.schedule.exceptions import ConflictException
from app.modules.schedule.repository import ScheduleRepository
from app.modules.court.repository import CourtRepository
from app.shared.exceptions import NotFoundException, BadRequestException


class ScheduleService:

    @staticmethod
    def create_batch(db, schedules):

        court = CourtRepository.get_by_id(db, schedules.court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        if schedules.interval_minutes <= 0:
            raise BadRequestException("Intervalo inválido")

        schedules_to_create = []

        start_date = date.fromisoformat(schedules.start_date)
        end_date = date.fromisoformat(schedules.end_date)

        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() not in schedules.weekdays:
                current_date += timedelta(days=1)
                continue

            current_time = datetime.strptime(
                schedules.start_time, "%H:%M"
            )
            end_time_limit = datetime.strptime(
                schedules.end_time, "%H:%M"
            )

            if current_time >= end_time_limit:
                raise BadRequestException(
                    "Horário inicial deve ser menor que o final"
                )

            while current_time < end_time_limit:
                next_time = current_time + timedelta(
                    minutes=schedules.interval_minutes
                )

                if next_time > end_time_limit:
                    break

                if ScheduleRepository.exists(
                    db=db,
                    court_id=schedules.court_id,
                    date=current_date.isoformat(),
                    start_time=current_time.strftime("%H:%M"),
                    end_time=next_time.strftime("%H:%M"),
                ):
                    raise ConflictException()

                schedules_to_create.append(
                    Schedules(
                        court_id=schedules.court_id,
                        date=current_date.isoformat(),
                        start_time=current_time.strftime("%H:%M"),
                        end_time=next_time.strftime("%H:%M"),
                        available=True,
                        created_at=datetime.now(timezone.utc),
                    )
                )

                current_time = next_time

            current_date += timedelta(days=1)

        ScheduleRepository.bulk_create(db, schedules_to_create)

    @staticmethod
    def list_all(db):
        return ScheduleRepository.list_all(db)

    @staticmethod
    def get_by_id(db, schedule_id: int):
        schedule_model = ScheduleRepository.get_by_id(db, schedule_id)

        if not schedule_model:
            raise NotFoundException("Horário não encontrado")

        return schedule_model
