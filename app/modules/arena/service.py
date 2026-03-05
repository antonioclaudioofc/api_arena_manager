from datetime import datetime, timezone
from app.models.arena import Arena
from app.shared.enums import UserRole
from app.shared.exceptions import ForbiddenException, NotFoundException


class ArenaService:

    def __init__(
        self,
        arena_repo,
        user_service
    ):
        self.arena_repo = arena_repo
        self.user_service = user_service

    def create(self, user, data):

        arena = Arena(
            **data.model_dump(),
            owner_id=user.id,
            created_at=datetime.now(timezone.utc)
        )

        self.user_service.promote_to_owner(user, arena)

        self.arena_repo.create(arena)

    def get_by_id(self, arena_id):
        return self.arena_repo.get_by_id(arena_id)

    def list_my_arenas(self, user):
        if not self.arena_repo.exists_by_owner(user.id):
            raise ForbiddenException("Usuário não possui arenas")

        return self.arena_repo.get_by_owner(user.id)

    def update(self, user, data, arena_id):
        arena = self.arena_repo.get_by_id(arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if user.role != UserRole.owner and arena.owner_id != user.id:
            raise ForbiddenException("Sem premissão")

        if data.name:
            arena.name = data.name

        if data.city:
            arena.city = data.city

        if data.address:
            arena.address = data.address

        arena.updated_at = datetime.now(timezone.utc)

        self.arena_repo.update(arena)

    def delete(self, user, arena_id):
        arena = self.arena_repo.get_by_id(arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if user.role != UserRole.owner and arena.owner_id != user.id:
            raise ForbiddenException("Sem premissão")

        self.arena_repo.delete(arena)

    def list_all(self):
        return self.arena_repo.list_all()
