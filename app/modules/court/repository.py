from app.models.court import Courts


class CourtRepository:

    @staticmethod
    def get_by_id(db, court_id):
        return db.query(Courts).filter(Courts.id == court_id).first()

    @staticmethod
    def list_all(db):
        return db.query(Courts).all()

    @staticmethod
    def create(db, court):
        db.add(court)
        db.commit()
        db.refresh(court)

        return court

    @staticmethod
    def delete(db, court):
        db.delete(court)
        db.commit()
