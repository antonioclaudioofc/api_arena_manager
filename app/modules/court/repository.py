from app.models.court import Court


class CourtRepository:

    def __init__(self, db):
        self.db = db

    def create(self, court):
        self.db.add(court)
        self.db.commit()
        self.db.refresh(court)

        return court

    def list_all(self, arena_id):
        return (
            self.db.query(Court)
            .filter(Court.arena_id == arena_id)
            .all()
        )

    def get_by_id(self, court_id):
        return (
            self.db.query(Court)
            .filter(Court.id == court_id)
            .first()
        )

    def update(self, court):
        self.db.commit()
        self.db.refresh(court)

        return court

    def delete(self, court):
        self.db.delete(court)
        self.db.commit()

