import httpx
from fastapi.encoders import jsonable_encoder
from app.core.config import settings


ROUTE_MAP = {
    "verification": "/api/arena-manager/verification",
    "password_reset": "/api/arena-manager/password-reset",
    "owner_promotion": "/api/arena-manager/owner-promotion",
    "new_court": "/api/arena-manager/new-court",
    "reservation_created": "/api/arena-manager/reservation-created",
    "reservation_cancelled": "/api/arena-manager/reservation-cancelled",
}


class ArenaManagerProducer:

    def publish_message(self, message_type: str, data: dict):
        path = ROUTE_MAP.get(message_type)
        if not path:
            raise ValueError(f"Unknown message type: {message_type}")

        url = f"{settings.NOTIFY_API_URL}{path}"

        httpx.post(
            url,
            json=jsonable_encoder(data),
            headers={"X-API-Key": settings.NOTIFY_API_KEY},
            timeout=10,
        )


producer = ArenaManagerProducer()
