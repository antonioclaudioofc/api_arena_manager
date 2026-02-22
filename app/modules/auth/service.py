from app.modules.auth.secutiry import create_access_token
from app.modules.email_client.service import EmailClient
from app.shared.enums import UserRole
from app.shared.exceptions import EmailAlreadyExistsException, UnathorizedException, UsernameAlreadyExistsException
from app.models.user import User
from app.core.security import bcrypt_context, generate_email_verification_token, hash_password
from datetime import datetime, timedelta, timezone


class AuthService:

    def __init__(self, user_repo):
        self.user_repo = user_repo

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
                "id": user.id,
                "role": user.role
            },
            expires_delta=timedelta(minutes=20)
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    async def register(self, data, background_tasks):
        if self.user_repo.get_by_email(data.email):
            raise EmailAlreadyExistsException()

        if self.user_repo.get_by_username(data.username):
            raise UsernameAlreadyExistsException()

        token = generate_email_verification_token()

        user_model = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_password(data.password),
            created_at=datetime.now(timezone.utc),
            role=UserRole.client,
            is_email_verified=False,
            email_verification_token=token
        )

        user = self.user_repo.create(user_model)

        background_tasks.add_task(
            EmailClient.send_verification_email,
            user.email,
            token
        )

        return user
