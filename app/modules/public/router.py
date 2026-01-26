from fastapi import APIRouter, Depends
from app.modules.arena.dependencies import get_arena_service
from app.modules.court.dependencies import get_court_service
from app.modules.schedule.dependencies import get_schedule_service
from app.schemas.arena import ResponseArena
from app.schemas.court import ResponseCourt
from app.shared.exceptions import NotFoundException

router = APIRouter(
    prefix="/public",
    tags=["public"]
)


@router.get("/arenas", response_model=list[ResponseArena])
def list_arenas(
    arena_service=Depends(get_arena_service)
):
    return arena_service.list_all()


@router.get("/arenas/{arena_id}", response_model=ResponseArena)
def get_arena(
    arena_id: int,
    arena_service=Depends(get_arena_service)
):
    arena = arena_service.get_by_id(arena_id)
    if not arena:
        raise NotFoundException("Arena não encontrada")
    return arena


@router.get("/arenas/{arena_id}/courts", response_model=list[ResponseCourt])
def list_courts_by_arena(
    arena_id: int,
    court_service=Depends(get_court_service),
    arena_service=Depends(get_arena_service)
):
    arena = arena_service.get_by_id(arena_id)
    if not arena:
        raise NotFoundException("Arena não encontrada")

    return court_service.list_all(arena_id)


@router.get("/courts/{court_id}/schedules", response_model=list[dict])
def list_available_schedules(
    court_id: int,
    schedule_service=Depends(get_schedule_service),
    court_service=Depends(get_court_service)
):
    court = court_service.get_by_id(court_id)
    if not court:
        raise NotFoundException("Quadra não encontrada")

    return schedule_service.list_by_court(court_id)
