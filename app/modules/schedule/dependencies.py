from fastapi import Depends
from app.modules.court.dependencies import get_court_service
from app.modules.schedule.repository import ScheduleRepository
from app.modules.schedule.service import ScheduleService
from app.dependencies import db_dependency


def get_schedule_repository(db: db_dependency):
    return ScheduleRepository(db)


def get_schedule_service(
        schedule_repo=Depends(get_schedule_repository),
        court_service=Depends(get_court_service)
):
    return ScheduleService(schedule_repo, court_service)
