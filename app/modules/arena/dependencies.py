from fastapi import Depends
from app.dependencies import db_dependency
from app.modules.arena.repository import ArenaRepository
from app.modules.arena.service import ArenaService
from app.modules.auth.dependencies import get_user_service


def get_arena_repository(db: db_dependency):
    return ArenaRepository(db)


def get_arena_service(
    arena_repo=Depends(get_arena_repository),
    user_service=Depends(get_user_service)
):
    return ArenaService(arena_repo, user_service)
