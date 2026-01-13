from datetime import datetime, timezone
from app.models.court import Courts
from app.shared.exceptions import NotFoundException
from app.modules.court.repository import CourtRepository


class CourtService:

    @staticmethod
    def get_by_id(db, court_id: int):
        court_model = CourtRepository.get_by_id(db, court_id)

        if not court_model:
            raise NotFoundException("Quadra não encontrada")

        return court_model

    @staticmethod
    def list_all(db):
        return CourtRepository.list_all(db)

    @staticmethod
    def create(db, user: dict, court_model):

        court_model = Courts(
            **court_model.model_dump(),
            owner_id=user["id"],
            created_at=datetime.now(timezone.utc)
        )

        return CourtRepository.create(db, court_model)

    @staticmethod
    def update(db, data, court_id: int):

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

        CourtRepository.update(db, court_model)

    @staticmethod
    def delete(db, court_id: int):

        court_model = CourtRepository.get_by_id(db, court_id)
        if not court_model:
            raise NotFoundException("Quadra não encontrada")

        CourtRepository.delete(db, court_model)
