from app.modules.auth.secutiry import create_access_token
from app.messaging.producer import producer
from app.shared.enums.user import UserRole
from app.shared.exceptions import EmailAlreadyExistsException, UnathorizedException
from app.models.user import User
from app.core.security import (
    bcrypt_context,
    generate_email_verification_token,
    generate_password_reset_token,
    hash_password
)
from datetime import datetime, timedelta, timezone


class AuthService:

    def __init__(self, user_repo):
        self.user_repo = user_repo

    @staticmethod
    def _to_utc(dt):
        if dt is None:
            return None

        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    def authenticate(
        self,
        email,
        password
    ):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise UnathorizedException("Usuário inexistente")

        if not bcrypt_context.verify(password, user.hashed_password):
            raise UnathorizedException("Usuário ou senha inválida")

        if not user.is_email_verified:
            raise UnathorizedException("E-mail não verificado")

        return user

    def verify_email(self, token):
        user = self.user_repo.get_by_email_verification_token(token)

        if not user:
            raise UnathorizedException("Token inválido")

        user.is_email_verified = True
        user.email_verification_token = None

        self.user_repo.update(user)

    def login(
        self,
        user_model
    ):
        user = self.authenticate(
            user_model.email,
            user_model.password,
        )

        token = create_access_token(
            data={
                "sub": user.email,
                "id": str(user.id),
                "role": user.role
            },
            expires_delta=timedelta(minutes=20)
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def register(self, data):
        if self.user_repo.get_by_email(data.email):
            raise EmailAlreadyExistsException()

        token = generate_email_verification_token()

        user_model = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_password(data.password),
            role=UserRole.PLAYER,
            is_email_verified=False,
            email_verification_token=token
        )

        user = self.user_repo.create(user_model)

        producer.publish_message('verification', {
            'email': user.email,
            'token': token
        })

        return user

    def forgot_password(self, email):
        user = self.user_repo.get_by_email(email)

        if not user:
            return

        token = generate_password_reset_token()

        user.reset_password_token = token
        user.reset_password_token_expires_at = datetime.now(
            timezone.utc) + timedelta(hours=1)

        self.user_repo.update(user)

        producer.publish_message('password_reset', {
            'email': user.email,
            'token': token
        })

    def validate_password_reset_token(self, token):
        user = self.user_repo.get_by_reset_password_token(token)

        if not user:
            raise UnathorizedException("Token inválido")

        expires_at = self._to_utc(user.reset_password_token_expires_at)

        if not expires_at or expires_at < datetime.now(timezone.utc):
            raise UnathorizedException("Token expirado")

        return user

    def reset_password(self, token, new_password):
        user = self.validate_password_reset_token(token)

        user.hashed_password = hash_password(new_password)
        user.reset_password_token = None
        user.reset_password_token_expires_at = None

        self.user_repo.update(user)
