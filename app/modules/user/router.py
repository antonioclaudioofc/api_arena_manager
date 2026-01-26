from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import get_current_user, get_user_service
from app.modules.user.service import UserService
from app.schemas.user import ResponseUser, UpdateUser, UserVerification
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/me", response_model=ResponseUser)
def get_profile(
    user=Depends(get_current_user)
):
    return user


@router.put("/me", response_model=MessageResponse)
def update_profile(
    data: UpdateUser,
    user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.update(user, data)

    return {
        "message": "Perfil atualizado com sucesso",
    }


@router.put("/change-password", response_model=MessageResponse)
def change_password(
    user_verification: UserVerification,
    user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.change_password(user, user_verification)

    return {
        "message": "Senha atualizado com sucesso"
    }


@router.delete("/account", response_model=MessageResponse)
def delete_account(
    user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete(user)

    return {
        "message": "Conta deletada com sucesso"
    }
