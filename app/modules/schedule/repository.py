from sqlalchemy import and_
from app.models.reservation import Reservations
from app.models.schedule import Schedules


class ScheduleRepository:

    @staticmethod
    def create(db, schedule):
        db.add(schedule)
        db.commit()
        db.refresh(schedule)

        return schedule

    @staticmethod
    def get_by_id(db, schedule_id):
        return db.query(Schedules).filter(Schedules.id == schedule_id).first()

    @staticmethod
    def list_with_status(db):
        return (
            db.query(
                Schedules,
                Reservations.id.label("reservation_id")
            )
            .outerjoin(
                Reservations,
                and_(
                    Reservations.schedule_id == Schedules.id,
                    Reservations.status == "Ocupado"
                )
            )
            .all()
        )

    @staticmethod
    def exists(db, court_id: int, date: str, start_time: str, end_time: str):
        return (
            db.query(Schedules)
            .filter(
                Schedules.court_id == court_id,
                Schedules.date == date,
                Schedules.start_time == start_time,
                Schedules.end_time == end_time
            ).first()
            is not None
        )

    @staticmethod
    def bulk_create(db, schedules: list[Schedules]):
        db.add_all(schedules)
        db.commit()

    @staticmethod
    def update(db, schedule):
        db.commit()
        db.refresh(schedule)

    @staticmethod
    def delete(db, schedule):
        db.delete(schedule)
        db.commit()
