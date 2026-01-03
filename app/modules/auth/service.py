from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from app.modules.auth.repository import AuthRepository
from app.modules.auth.secutiry import create_access_token, decode_token
from app.shared.exceptions import EmailAlreadyExistsException, UnathorizedException, UsernameAlreadyExistsException
from app.models.auth import Users
from app.core.security import bcrypt_context, hash_password
from datetime import datetime, timedelta, timezone
from .secutiry import oauth2_bearer


class AuthService:

    @staticmethod
    def authenticate(db, username: str, password: str):

        user = AuthRepository.get_by_username(db, username)

        if not user or not bcrypt_context.verify(password, user.hashed_password):
            raise UnathorizedException("Usuário ou senha inválidos")

        return user

    @staticmethod
    def login(form_data: OAuth2PasswordRequestForm, db):
        user = AuthService.authenticate(
            db,
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

    @staticmethod
    def register(data, db):
        if AuthRepository.get_by_email(db, data.email):
            raise EmailAlreadyExistsException()
        
        if AuthRepository.get_by_username(db, data.username):
            raise UsernameAlreadyExistsException()
        
        user_model = Users(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_password(data.password),
            created_at=datetime.now(timezone.utc)
        )

        return AuthRepository.create(db, user_model)

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_bearer)):
        try:
            payload = decode_token(token)
            return {
                "id": payload["id"],
                "username": payload["sub"],
                "user_role": payload["role"]
            }
        except JWTError:
            raise UnathorizedException("Token inválido!")
