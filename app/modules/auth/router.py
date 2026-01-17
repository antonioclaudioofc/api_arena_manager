from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.dependencies import get_auth_service
from app.modules.auth.service import AuthService
from app.schemas.user import RequestUser
from app.schemas.token import Token
from starlette import status
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_request: RequestUser,
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.register(user_request)

    return {
        "message": "Usuário criado com sucesso"
    }


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login(form_data)
