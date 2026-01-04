from app.models.auth import Users


class UserRepository:

    @staticmethod
    def get_by_id(db, user_id: int):
        return db.query(Users).filter(Users.id == user_id).first()

    @staticmethod
    def get_by_username(db, username: str):
        return db.query(Users).filter(Users.username == username).first()

    @staticmethod
    def get_by_email(db, email: str):
        return db.query(Users).filter(Users.email == email).first()

    @staticmethod
    def create(db, user):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete(db, user):
        db.delete(user)
        db.commit()
        db.refresh(user)
