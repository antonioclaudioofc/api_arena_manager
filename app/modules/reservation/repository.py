from app.models.reservation import Reservation
from app.models.schedule import Schedule
from app.models.court import Court
from app.models.arena import Arena
from app.shared.enums.reservation import ReservationStatus


class ReservationRepository:

    def __init__(self, db):
        self.db = db

    def create(self, reservation):
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)

        return reservation

    def get_by_id(self, reservation_id):
        return (
            self.db.query(Reservation)
            .filter(Reservation.id == reservation_id)
            .first()
        )

    def get_active_by_schedule(self, schedule_id):
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.schedule_id == schedule_id,
                Reservation.status == ReservationStatus.CONFIRMED
            )
            .first()
        )

    def list_by_client(self, user_id):
        return (
            self.db.query(Reservation)
            .filter(Reservation.user_id == user_id)
            .all()
        )

    def list_all(self):
        return self.db.query(Reservation).all()

    def list_by_owner(self, owner_id):
        return (
            self.db.query(Reservation)
            .join(Schedule, Schedule.id == Reservation.schedule_id)
            .join(Court, Court.id == Schedule.court_id)
            .join(Arena, Arena.id == Court.arena_id)
            .filter(Arena.owner_id == owner_id)
            .all()
        )

    def update(self, reservation):
        self.db.commit()
        self.db.refresh(reservation)

        return reservation
