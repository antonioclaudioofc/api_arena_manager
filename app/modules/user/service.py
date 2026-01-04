from datetime import datetime, timezone
from app.shared.repositories.user_repository import UserRepository
from app.shared.exceptions import (
    EmailAlreadyExistsException,
    ForbiddenException,
    NotFoundException
)
from app.core.security import bcrypt_context


class UserService:

    @staticmethod
    def get_profile(db, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise NotFoundException("Usuário não encontrado")

        return user

    @staticmethod
    def update_profile(db, user_id: int, data):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise NotFoundException("Usuário não encontrado")

        if data.email and data.email != user.email:
            if UserRepository.get_by_email(db, data.email):
                raise EmailAlreadyExistsException()

            user.email = data.email

        if data.first_name:
            user.first_name = data.first_name

        if data.last_name:
            user.last_name = data.last_name

        user.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def change_password(db, user_id: int, data):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise NotFoundException("Usuário não encontrado")

        if not bcrypt_context.verify(data.password, user.hashed_password):
            raise ForbiddenException("Senha atual incorreta")

        if data.password == data.new_password:
            raise ForbiddenException(
                "A nova senha deve ser diferente da atual"
            )

        user.hashed_password = bcrypt_context.hash(data.new_password)
        user.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

    @staticmethod
    def delete_account(db, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise NotFoundException("Usuário não encontrado")

        db.delete(user)
        db.commit()
