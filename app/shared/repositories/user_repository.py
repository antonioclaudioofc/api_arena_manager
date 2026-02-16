from app.models.user import User


class UserRepository:

    def __init__(self, db):
        self.db = db

    def create(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_id(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_email_verification_token(self, token):
        return self.db.query(User).filter(User.email_verification_token == token).first()

    def update(self, user):
        self.db.commit()
        self.db.refresh(user)

    def delete(self, user):
        self.db.delete(user)
        self.db.commit()
