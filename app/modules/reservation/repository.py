from app.models.reservation import Reservations


class ReservationRepository:

    @staticmethod
    def get_all(db):
        return db.query(Reservations).all()

    @staticmethod
    def get_by_id(db, reservation_id: int):
        return db.query(Reservations).filter(Reservations.id == reservation_id).first()

    @staticmethod
    def get_by_user(user_id: int, db):
        return (
            db.query(Reservations)
            .filter(Reservations.user_id == user_id)
            .all()
        )

    @staticmethod
    def exists_active_by_schedule(db, schedule_id: int):
        return (
            db.query(Reservations)
            .filter(
                Reservations.schedule_id == schedule_id,
                Reservations.status == "Ocupado"
            )
            .first()
        )

    @staticmethod
    def get_by_owner(user_id: id, db, reservation_id: int):
        return db.query(Reservations).filter(Reservations.id == reservation_id, Reservations.user_id == user_id).first()

    @staticmethod
    def create(reservation, db):
        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def delete(reservation, db):
        db.delete(reservation)
        db.commit()
