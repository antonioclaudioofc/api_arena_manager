from fastapi import Depends
from app.dependencies import db_dependency
from app.modules.arena.dependencies import get_arena_service
from app.modules.court.repository import CourtRepository
from app.modules.court.service import CourtService


def get_court_repository(db: db_dependency):
    return CourtRepository(db)


def get_court_service(
    court_repo=Depends(get_court_repository),
    arena_service=Depends(get_arena_service)
):
    return CourtService(court_repo, arena_service)
