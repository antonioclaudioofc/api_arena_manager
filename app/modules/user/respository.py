from app.models.auth import Users


class UserRepository:

    @staticmethod
    def get_by_id(db, user_id: int):
        return db.query(Users).filter(Users.id == user_id).first()

    @staticmethod
    def delete(db, user):
        db.delete(user)
        db.commit()
        db.refresh(user)
