from fastapi import APIRouter, Depends
from typing import Annotated
from starlette import status

from app.dependencies import db_dependency
from app.modules.auth.service import AuthService
from app.modules.user.service import UserService
from app.schemas.auth import ResponseUser, UpdateUser, UserVerification
from app.shared.schemas import ApiResponse, MessageResponse

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

user_dependency = Annotated[dict, Depends(AuthService.get_current_user)]


@router.put("/me", response_model=MessageResponse)
def update_profile(
    db: db_dependency,
    user: user_dependency,
    data: UpdateUser
):
    user = UserService.update_profile(db, user["id"], data)

    return {
        "message": "Perfil atualizado com sucesso",
    }


@router.get("/me", response_model=ResponseUser)
def get_user(
    db: db_dependency,
    user: user_dependency
):
    user_model = UserService.get_profile(db, user["id"])

    return user_model


@router.put("/change-password", response_model=MessageResponse)
def change_password(
    db: db_dependency,
    user: user_dependency,
    user_verification: UserVerification
):
    UserService.change_password(db, user["id"], user_verification)

    return {
        "message": "Senha atualizado com sucesso"
    }


@router.delete("/account", response_model=MessageResponse)
def delete_account(
    db: db_dependency,
    user: user_dependency
):
    UserService.delete_account(db, user["id"])

    return {
        "message": "Conta deletada com sucesso"
    }
