from fastapi import APIRouter, Depends
from uuid import UUID
from app.modules.auth.dependencies import get_current_user
from app.modules.court.dependencies import get_court_service
from app.schemas.court import RequestCourt, ResponseCourt, UpdateCourt
from starlette import status
from app.shared.schemas import MessageResponse


router = APIRouter(
    prefix="/courts",
    tags=["courts"]
)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: RequestCourt,
    user=Depends(get_current_user),
    court_service=Depends(get_court_service)
):
    court_service.create(user, data)

    return {
        "message": "Quadra criada com sucesso"
    }


@router.get("/{arena_id}", response_model=list[ResponseCourt])
def list_by_arena(
    arena_id: UUID,
    user=Depends(get_current_user),
    court_service=Depends(get_court_service),
):
    return court_service.list_by_arena(user, arena_id)


@router.put("/{court_id}", response_model=MessageResponse)
def update(
    court_id: UUID,
    data: UpdateCourt,
    user=Depends(get_current_user),
    court_service=Depends(get_court_service)
):
    court_service.update(user, data, court_id)

    return {
        "message": "Quadra atualizada com sucesso"
    }


@router.delete("/{court_id}", response_model=MessageResponse)
def delete(
    court_id: UUID,
    user=Depends(get_current_user),
    court_service=Depends(get_court_service)
):
    court_service.delete(user, court_id)

    return {
        "message": "Quadra deletada com sucesso"
    }
