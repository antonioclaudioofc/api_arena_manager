from datetime import datetime, timezone
import re
import traceback
from uuid import uuid4
from app.models.arena import Arena
from app.shared.enums.user import UserRole
from app.shared.exceptions import ForbiddenException, NotFoundException


class ArenaService:

    def __init__(
        self,
        arena_repo,
        user_service
    ):
        self.arena_repo = arena_repo
        self.user_service = user_service

    def _generate_unique_slug(self, court_name: str, arena_id) -> str:
        base_slug = re.sub(r"[^a-z0-9]+", "-", court_name.lower()).strip("-")
        if not base_slug:
            base_slug = "court"

        return f"{base_slug}-{str(arena_id)[:8]}-{uuid4().hex[:8]}"

    def create(self, user, data):
        try:
            payload = data.model_dump()
            print(f"[ArenaService.create] user_id={user.id}", flush=True)
            print(f"[ArenaService.create] payload={payload}", flush=True)

            arena = Arena(
                **payload,
                owner_id=user.id,
                slug=self._generate_unique_slug(data.name, uuid4())
            )

            print("[ArenaService.create] promoting user to owner", flush=True)
            self.user_service.promote_to_owner(user, arena)

            print("[ArenaService.create] persisting arena", flush=True)
            self.arena_repo.create(arena)
            print("[ArenaService.create] success", flush=True)
        except Exception as exc:
            print(f"[ArenaService.create] error={exc}", flush=True)
            traceback.print_exc()
            raise

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

        if user.role != UserRole.OWNER and arena.owner_id != user.id:
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

        if user.role != UserRole.OWNER and arena.owner_id != user.id:
            raise ForbiddenException("Sem premissão")

        self.arena_repo.delete(arena)

    def list_all(self):
        return self.arena_repo.list_all()
