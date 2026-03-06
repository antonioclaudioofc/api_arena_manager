from typing import Annotated
from uuid import UUID

from jose import JWTError
from app.modules.auth.service import AuthService
from app.modules.user.service import UserService
from app.shared.exceptions import UnathorizedException
from app.shared.repositories.user_repository import UserRepository
from app.modules.auth.secutiry import decode_token, oauth2_bearer
from fastapi import Depends
from app.dependencies import db_dependency


def get_user_repository(db: db_dependency):
    return UserRepository(db)


def get_auth_service(user_repo=Depends(get_user_repository)):
    return AuthService(user_repo)


def get_user_service(user_repo=Depends(get_user_repository)):
    return UserService(user_repo)


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    user_repo=Depends(get_user_repository)
):
    try:
        payload = decode_token(token)
        raw_user_id = payload.get("id")

        if not raw_user_id:
            raise UnathorizedException("Token inválido")

        try:
            user_id = UUID(str(raw_user_id))
        except (ValueError, TypeError):
            raise UnathorizedException("Token inválido")

        user = user_repo.get_by_id(user_id)

        if not user:
            raise UnathorizedException("Usuário não encontrado")

        return user

    except JWTError:
        raise UnathorizedException("Token inválido")
