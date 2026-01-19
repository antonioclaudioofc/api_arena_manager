from app.models.arena import Arena


class ArenaRepository:

    def __init__(self, db):
        self.db = db

    def create(self, arena):
        self.db.add(arena)
        self.db.commit()
        self.db.refresh(arena)

        return arena

    def get_by_id(self, arena_id):
        return (
            self.db.query(Arena)
            .filter(Arena.id == arena_id)
            .first()
        )

    def get_by_owner(self, owner_id):
        return (
            self.db.query(Arena)
            .filter(Arena.owner_id == owner_id)
            .all()
        )

    def update(self, arena):
        self.db.commit()
        self.db.refresh(arena)

        return arena

    def delete(self, arena):
        self.db.delete(arena)
        self.db.commit()

    def list_all(self):
        return self.db.query(Arena).all()
