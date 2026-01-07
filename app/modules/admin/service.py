from datetime import datetime, timezone
from fastapi import Depends
from app.modules.admin.repository import AdminRepository
from app.modules.schedule.repository import ScheduleRepository
from app.models.schedule import Schedules
from app.modules.schedule.service import ScheduleService
from app.shared.repositories.user_repository import UserRepository
from app.modules.court.repository import CourtRepository
from app.models.court import Courts
from app.modules.admin.exceptions import AdminOnlyException
from app.shared.exceptions import NotFoundException


class AdminService:

    @staticmethod
    def ensure_admin(user: dict):
        if not user or user.get("user_role") != "admin":
            raise AdminOnlyException()

    @staticmethod
    def create_court(db, user: dict, court_model):
        AdminService.ensure_admin(user)

        court_model = Courts(
            **court_model.model_dump(),
            owner_id=user["id"],
            created_at=datetime.now(timezone.utc)
        )

        return CourtRepository.create(db, court_model)

    @staticmethod
    def update_court(db, user: dict, data, court_id: int):
        AdminService.ensure_admin(user)

        court_model = CourtRepository.get_by_id(db, court_id)

        if not court_model:
            raise NotFoundException("Quadra não encontrada")

        if data.name is not None:
            court_model.name = data.name

        if data.sports_type is not None:
            court_model.sports_type = data.sports_type

        if data.description is not None:
            court_model.description = data.description

        court_model.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(court_model)

    @staticmethod
    def delete_court(db, user: dict, court_id: int):
        AdminService.ensure_admin(user)

        court_model = CourtRepository.get_by_id(db, court_id)
        if not court_model:
            raise NotFoundException("Quadra não encontrada")

        CourtRepository.delete(db, court_model)

    @staticmethod
    def create_schedule(db, user: dict, schedule_request):
        AdminService.ensure_admin(user)

        court = CourtRepository.get_by_id(db, schedule_request.court_id)

        if not court:
            raise NotFoundException("Quadra não encontrado")

        schedule_model = Schedules(
            **schedule_request.model_dump(),
            owner_id=user["id"],
            created_at=datetime.now(timezone.utc)
        )

        return ScheduleRepository.create(db, schedule_model)

    @staticmethod
    def create_schedules(db, user: dict, data):
        AdminService.ensure_admin(user)

        court = CourtRepository.get_by_id(db, data.court_id)
        if not court:
            raise NotFoundException("Quadra não encontrada")

        ScheduleService.create_batch(db, data)

    @staticmethod
    def update_schedule(db, user: dict, data, schedule_id: int):
        AdminService.ensure_admin(user)

        schedule = ScheduleRepository.get_by_id(db, schedule_id)

        if not schedule:
            raise NotFoundException("Horário não encontrado")

        if data.date is not None:
            schedule.date = data.date

        if data.start_time is not None:
            schedule.start_time = data.start_time

        if data.end_time is not None:
            schedule.end_time = data.end_time

        if data.available is not None:
            schedule.available = data.available

        if data.court_id is not None:
            schedule.court_id = data.court_id

        schedule.updated_at = datetime.now(timezone.utc)

        db.commit()

    @staticmethod
    def delete_schedule(db, user: dict, schedule_id: int):
        AdminService.ensure_admin(user)

        schedule_model = ScheduleRepository.get_by_id(db, schedule_id)
        if not schedule_model:
            raise NotFoundException("Horário não encontrado")

        ScheduleRepository.delete(db, schedule_model)

    @staticmethod
    def delete_user(db, user: dict, user_id: int):
        AdminService.ensure_admin(user)

        user_model = UserRepository.get_by_id(db, user_id)
        if not user_model:
            raise NotFoundException("Usuário não encontrado!")

        UserRepository.delete(db, user_model)

    @staticmethod
    def list_reservations(user: dict, db):
        AdminService.ensure_admin(user)
        return AdminRepository.list_all_reservations(db)

    @staticmethod
    def list_users(user: dict, db):
        AdminService.ensure_admin(user)
        return AdminRepository.list_all_users(db)
