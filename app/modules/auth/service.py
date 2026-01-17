from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.secutiry import create_access_token
from app.shared.enums import UserRole
from app.shared.repositories.user_repository import UserRepository
from app.shared.exceptions import EmailAlreadyExistsException, UnathorizedException, UsernameAlreadyExistsException
from app.models.user import User
from app.core.security import bcrypt_context, hash_password
from datetime import datetime, timedelta, timezone


class AuthService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(
        self,
        username: str,
        password: str
    ):

        user = self.user_repo.get_by_username(username)

        if not user:
            raise UnathorizedException("Usuário inexistente")

        if not bcrypt_context.verify(password, user.hashed_password):
            raise UnathorizedException("Usuário ou senha inválida")

        return user

    def login(
        self,
        form_data: OAuth2PasswordRequestForm
    ):

        user = self.authenticate(
            form_data.username,
            form_data.password,
        )

        token = create_access_token(
            data={
                "sub": user.username,
                "id": user.id,
                "role": user.role
            },
            expires_delta=timedelta(minutes=20)
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def register(
        self,
        data
    ):
        if self.user_repo.get_by_email(data.email):
            raise EmailAlreadyExistsException()

        if self.user_repo.get_by_username(data.username):
            raise UsernameAlreadyExistsException()

        user_model = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_password(data.password),
            created_at=datetime.now(timezone.utc),
            role=UserRole.client,
        )

        return self.user_repo.create(user_model)
