from app.models.auth import Users


class AuthRepository:

    @staticmethod
    def get_by_email(db, email: str):
        return db.query(Users).filter(Users.email == email).first()

    @staticmethod
    def get_by_username(db, username: str):
        return db.query(Users).filter(Users.username == username).first()

    @staticmethod
    def create(db, user_model: Users):
        db.add(user_model)
        db.commit()
        db.refresh(user_model)

        return user_model
