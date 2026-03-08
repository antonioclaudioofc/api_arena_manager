from datetime import datetime, timezone
import re
from uuid import uuid4
from app.models.court import Court
from app.messaging.producer import producer
from app.shared.exceptions import ForbiddenException, NotFoundException


class CourtService:

    def __init__(self, court_repo, arena_service):
        self.court_repo = court_repo
        self.arena_service = arena_service

    def _generate_unique_slug(self, court_name: str, arena_id) -> str:
        base_slug = re.sub(r"[^a-z0-9]+", "-", court_name.lower()).strip("-")
        if not base_slug:
            base_slug = "court"

        return f"{base_slug}-{str(arena_id)[:8]}-{uuid4().hex[:8]}"

    def create(self, user, data):
        arena = self.arena_service.get_by_id(data.arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão")

        court = Court(
            **data.model_dump(),
            slug=self._generate_unique_slug(data.name, data.arena_id),
            created_at=datetime.now(timezone.utc)
        )

        producer.publish_message('new_court', {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'arena': {
                'id': arena.id,
                'name': arena.name,
            },
            'court': {
                'id': court.id,
                'name': court.name,
            }
        })

        return self.court_repo.create(court)

    def get_by_id(self, court_id):
        return self.court_repo.get_by_id(court_id)

    def list_all(self, arena_id):
        return self.court_repo.list_all(arena_id)

    def list_by_arena(self, user, arena_id):
        arena = self.arena_service.get_by_id(arena_id)

        if not arena or arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão")

        return self.court_repo.list_all(arena_id)

    def update(self, user, data, court_id):
        court = self.court_repo.get_by_id(court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        arena = self.arena_service.get_by_id(court.arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão para editar esta quadra")

        if data.name:
            court.name = data.name

        if data.sport_type:
            court.sport_type = data.sport_type

        if data.name:
            court.slug = self._generate_unique_slug(data.name, court.arena_id)

        if data.price_per_hour:
            court.price_per_hour = data.price_per_hour

        court.updated_at = datetime.now(timezone.utc)

        self.court_repo.update(court)

    def delete(self, user, court_id):
        court = self.court_repo.get_by_id(court_id)

        if not court:
            raise NotFoundException("Quadra não encontrada")

        arena = self.arena_service.get_by_id(court.arena_id)

        if not arena:
            raise NotFoundException("Arena não encontrada")

        if arena.owner_id != user.id:
            raise ForbiddenException("Sem premisão para remover esta quadra")

        self.court_repo.delete(court)
