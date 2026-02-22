from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.dependencies import get_auth_service
from app.schemas.user import RequestUser, UserLogin
from app.schemas.token import Token
from starlette import status
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RequestUser,
    background_tasks: BackgroundTasks,
    auth_service=Depends(get_auth_service)
):
    await auth_service.register(payload, background_tasks)

    return {
        "message": "Usuário criado com sucesso"
    }


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service=Depends(get_auth_service)
):
    payload = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return auth_service.login(payload)


@router.get("/verify-email", response_model=MessageResponse)
def verify_email(
    token: str,
    auth_service=Depends(get_auth_service)
):
    auth_service.verify_email(token)

    return {
        "message": "E-mail verificado com sucesso"
    }
