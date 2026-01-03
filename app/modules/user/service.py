from datetime import datetime, timezone
from app.modules.user.respository import UserRepository
from app.shared.exceptions import ForbiddenException, NotFoundException
from app.core.security import bcrypt_context


class UserService:

    @staticmethod
    def get_profile(db, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise NotFoundException("Usuário não encontrado")

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
                "A nova senha deve ser diferente da atual")

        user.hashed_password = bcrypt_context.hash(data.new_password)
        user.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        return {"message": "Senha alterada com sucesso"}
