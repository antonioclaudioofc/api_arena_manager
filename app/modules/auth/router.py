from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import db_dependency
from app.modules.auth.service import AuthService
from app.schemas.user import RequestUser
from app.schemas.token import Token
from starlette import status
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_request: RequestUser,
    db: db_dependency
):
    AuthService.register(db, user_request)

    return {
        "message": "Usuário criado com sucesso"
    }


@router.post("/login", response_model=Token)
def login(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    token = AuthService.login(db, form_data)

    return token
