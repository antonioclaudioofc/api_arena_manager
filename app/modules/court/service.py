from datetime import datetime, timezone
from app.models.court import Court
from app.modules.arena.repository import ArenaRepository
from app.shared.enums import UserRole
from app.shared.exceptions import ForbiddenException, NotFoundException
from app.modules.court.repository import CourtRepository


class CourtService:

    def __init__(self, court_repo: CourtRepository, arena_repo: ArenaRepository):
        self.court_repo = court_repo
        self.arena_repo = arena_repo

    def create(self, user, data):
        arena = self.arena_repo.get_by_id(data.arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão")

        court = Court(
            **data.model_dump(),
            created_at=datetime.now(timezone.utc)
        )

        return self.court_repo.create(court)

    def list_by_arena(self, user, arena_id):
        arena = self.arena_repo.get_by_id(arena_id)

        if not arena or arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão")

        return self.court_repo.get_by_arena(arena_id)

    def update(self, user, data, court_id):
        court = self.court_repo.get_by_id(court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        arena = self.arena_repo.get_by_id(court.arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão para editar esta quadra")

        if data.name:
            court.name = data.name

        if data.sports_type:
            court.sports_type = data.sports_type

        if data.price_per_hour:
            court.price_per_hour = data.price_per_hour

        court.update_at = datetime.now(timezone.utc)

        self.court_repo.update(court)

    def delete(self, user, court_id):
        court = self.court_repo.get_by_id(court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        arena = self.arena_repo.get_by_id(court.arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão para remover esta quadra")

        self.court_repo.delete(court)
