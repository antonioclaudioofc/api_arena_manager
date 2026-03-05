from datetime import datetime, timezone
from app.messaging.producer import producer
from app.shared.enums.user import UserRole
from app.shared.exceptions import (
    EmailAlreadyExistsException,
    ForbiddenException,
    UsernameAlreadyExistsException
)
from app.core.security import bcrypt_context


class UserService:

    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_profile(self, user):
        return user

    def update(self, user, data):
        if data.email and data.email != user.email:
            if self.user_repo.get_by_email(data.email):
                raise EmailAlreadyExistsException()
            user.email = data.email

        if data.username and data.username != user.username:
            if self.user_repo.get_by_username(data.username):
                raise UsernameAlreadyExistsException()
            user.username = data.username

        if data.name:
            user.name = data.name

        user.updated_at = datetime.now(timezone.utc)

        self.user_repo.update(user)

    def change_password(self, user, data):
        if not bcrypt_context.verify(data.password, user.hashed_password):
            raise ForbiddenException("Senha atual incorreta")

        if data.password == data.new_password:
            raise ForbiddenException(
                "A nova senha deve ser diferente da atual"
            )

        user.hashed_password = bcrypt_context.hash(data.new_password)
        user.updated_at = datetime.now(timezone.utc)

        self.user_repo.update(user)

    def delete(self, user):
        self.user_repo.delete(user)

    def promote_to_owner(self, user, arena):
        if user.role == UserRole.PLAYER:
            user.role = UserRole.OWNER
            user.updated_at = datetime.now(timezone.utc)

            producer.publish_message('owner_promotion', {
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                },
                'arena': {
                    'id': arena.id,
                    'name': arena.name,
                }
            })

            self.user_repo.update(user)

        return user
