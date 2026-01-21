from fastapi import APIRouter, Depends
from app.modules.auth.dependencies import get_current_user
from app.modules.court.dependencies import get_court_service
from app.schemas.court import RequestCourt, ResponseCourt, UpdateCourt
from starlette import status
from app.shared.schemas import MessageResponse


router = APIRouter(
    prefix="/courts",
    tags=["courts"]
)


@router.get("/", response_model=list[ResponseCourt])
def list_by_arena(
    arena_id: int,
    user=Depends(get_current_user),
    court_service = Depends(get_court_service),
):
    return court_service.list_by_arena(user, arena_id)


@router.post("/{arena_id}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: RequestCourt,
    user=Depends(get_current_user),
    court_service = Depends(get_court_service)
):
    court_service.create(user, data)

    return {
        "message": "Quadra criada com sucesso"
    }


@router.put("/{court_id}", response_model=MessageResponse)
def update(
    court_id: int,
    data: UpdateCourt,
    user=Depends(get_current_user),
    court_service = Depends(get_court_service)
):
    court_service.update(user, data, court_id)

    return {
        "message": "Quadra atualizada com sucesso"
    }


@router.delete("/{court_id}", response_model=MessageResponse)
def delete(
    court_id: int,
    user=Depends(get_current_user),
    court_service = Depends(get_court_service)
):
    court_service.delete(user, court_id)

    return {
        "message": "Quadra deletada com sucesso"
    }
