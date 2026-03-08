from app.models.reservation import Reservation
from app.models.schedule import Schedule
from sqlalchemy.orm import aliased
from app.shared.enums.reservation import ReservationStatus


class ScheduleRepository:

    def __init__(self, db):
        self.db = db

    def create(self, schedule):
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)

        return schedule

    def bulk_create(self, schedules):
        self.db.add_all(schedules)
        self.db.commit()

    def get_by_id(self, schedule_id):
        return (
            self.db.query(Schedule)
            .filter(Schedule.id == schedule_id)
            .first()
        )

    def list_by_court(self, court_id):
        return (
            self.db.query(Schedule)
            .filter(Schedule.court_id == court_id)
            .all()
        )

    def exists(self, court_id, date, start_time, end_time):
        return (
            self.db.query(Schedule)
            .filter(
                Schedule.court_id == court_id,
                Schedule.date == date,
                Schedule.start_time == start_time,
                Schedule.end_time == end_time
            )
            .first()
            is not None
        )

    def list_with_availability(self, court_id):
        reservation_alias = aliased(Reservation)

        return (
            self.db.query(Schedule, reservation_alias.id)
            .outerjoin(
                reservation_alias,
                (reservation_alias.schedule_id == Schedule.id)
                & (reservation_alias.status == ReservationStatus.CONFIRMED)
            )
            .filter(Schedule.court_id == court_id)
            .all()
        )

    def update(self, schedule):
        self.db.commit()
        self.db.refresh(schedule)

        return schedule

    def delete(self, schedule):
        self.db.delete(schedule)
        self.db.commit()
