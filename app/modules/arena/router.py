from fastapi import APIRouter, Depends

from app.modules.arena.dependencies import get_arena_service
from app.modules.arena.service import ArenaService
from app.modules.auth.dependencies import get_current_user
from app.schemas.arena import RequestArena, ResponseArena, UpdateArena
from app.shared.schemas import MessageResponse


router = APIRouter(
    prefix="/arenas",
    tags=["arenas"]
)


@router.get("/", response_model=list[ResponseArena])
def list(
    user=Depends(get_current_user),
    arena_service: ArenaService = Depends(get_arena_service)
):
    return arena_service.list_my_arenas(user)


@router.post("/", response_model=MessageResponse)
def create(
    data: RequestArena,
    user=Depends(get_current_user),
    arena_service: ArenaService = Depends(get_arena_service)
):
    arena_service.create(user, data)

    return {
        "message": "Arena criada com sucesso"
    }


@router.put("/{arena_id}", response_model=MessageResponse)
def update(
    arena_id: int,
    data: UpdateArena,
    user=Depends(get_current_user),
    arena_service: ArenaService = Depends(get_arena_service),
):
    arena_service.update(user, data, arena_id)

    return {
        "message": "Arena atualizada com sucesso"
    }


@router.delete("/{arena_id}", response_model=MessageResponse)
def delete(
    arena_id: int,
    user=Depends(get_current_user),
    arena_service: ArenaService = Depends(get_arena_service)
):
    arena_service.delete(user, arena_id)

    return {
        "message": "Arena deletada com sucesso"
    }
