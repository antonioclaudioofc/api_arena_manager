from app.modules.admin.repository import AdminRepository
from app.modules.court.service import CourtService
from app.modules.schedule.service import ScheduleService
from app.shared.repositories.user_repository import UserRepository
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

        return CourtService.create(db, user, court_model)

    @staticmethod
    def update_court(db, user: dict, data, court_id: int):
        AdminService.ensure_admin(user)

        CourtService.update(db, data, court_id)

    @staticmethod
    def delete_court(db, user: dict, court_id: int):
        AdminService.ensure_admin(user)

        CourtService.delete(db, court_id)

    @staticmethod
    def create_schedule(db, user: dict, schedule_request):
        AdminService.ensure_admin(user)

        return ScheduleService.create(db, user, schedule_request)

    @staticmethod
    def create_schedules(db, user: dict, data):
        AdminService.ensure_admin(user)

        ScheduleService.create_batch(db, data)

    @staticmethod
    def update_schedule(db, user: dict, data, schedule_id: int):
        AdminService.ensure_admin(user)

        ScheduleService.update(db, data, schedule_id)

    @staticmethod
    def delete_schedule(db, user: dict, schedule_id: int):
        AdminService.ensure_admin(user)

        ScheduleService.delete(db, schedule_id)

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
