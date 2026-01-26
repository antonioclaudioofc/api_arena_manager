from app.models.reservation import Reservation
from app.shared.enums import ReservationStatus


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
                Reservation.status == ReservationStatus.active
            )
            .first()
        )

    def list_by_client(self, client_id):
        return (
            self.db.query(Reservation)
            .filter(Reservation.client_id == client_id)
            .all()
        )

    def list_all(self):
        return self.db.query(Reservation).all()

    def update(self, reservation):
        self.db.commit()
        self.db.refresh(reservation)

        return reservation
