from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import db_dependency
from app.schemas.auth import AuthCreate
from app.schemas.token import Token
from starlette import status
from app.modules.auth.service import AuthService
from app.shared.schemas import ApiResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/", response_model=ApiResponse[None], status_code=status.HTTP_201_CREATED)
def register(
    user_request: AuthCreate,
    db: db_dependency
):
    AuthService.register(db, user_request)

    return {
        "message": "Usuário criado com sucesso"
    }


@router.post("/token", response_model=ApiResponse[Token])
def login(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    token = AuthService.login(db, form_data)

    return {
        "message": "Login realizado com sucesso",
        "data": token
    }
