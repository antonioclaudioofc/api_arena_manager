import httpx

from app.core.config import EMAIL_API_URL


class EmailClient:

    @staticmethod
    async def _send(url: str, payload: dict):
        if not EMAIL_API_URL:
            return

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    url,
                    json=payload,
                    headers={
                        "x-api-key": EMAIL_API_URL
                    }
                )
        except httpx.HTTPError:
            return

    @staticmethod
    async def send_verification_email(email: str, token: str):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/verification"

        await EmailClient._send(url, {
            "email": email,
            "token": token
        })

    async def send_promote_to_owner(user, arena):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/owner-promotion"

        await EmailClient._send(url, {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
            "arena": {
                "id": arena.id,
                "name": arena.name,
            }
        })

    async def send_create_new_court(user, arena, court):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/new-court"

        await EmailClient._send(url, {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
            "arena": {
                "id": arena.id,
                "name": arena.name,
            },
            "court": {
                "id": court.id,
                "name": court.name,
            }
        })

    async def send_reservation_created(owner, client, schedule, reservation):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/reservation-created"

        payload = {
            "reservation": {
                "id": reservation.id,
                "status": reservation.status,
                "date": schedule.date,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
            },
            "arena": {
                "id": schedule.court.arena.id,
                "name": schedule.court.arena.name,
            },
            "court": {
                "id": schedule.court.id,
                "name": schedule.court.name,
            },
            "owner": {
                "id": owner.id,
                "name": owner.name,
                "email": owner.email,
            },
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
            }
        }

        await EmailClient._send(url, {
            **payload,
            "recipient": "owner"
        })
        await EmailClient._send(url, {
            **payload,
            "recipient": "client"
        })

    async def send_reservation_cancelled(owner, client, schedule, reservation):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/reservation-cancelled"

        payload = {
            "reservation": {
                "id": reservation.id,
                "status": reservation.status,
                "date": schedule.date,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "cancelled_at": (
                    reservation.cancelled_at.isoformat()
                    if reservation.cancelled_at else None
                )
            },
            "arena": {
                "id": schedule.court.arena.id,
                "name": schedule.court.arena.name,
            },
            "court": {
                "id": schedule.court.id,
                "name": schedule.court.name,
            },
            "owner": {
                "id": owner.id,
                "name": owner.name,
                "email": owner.email,
            },
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
            }
        }

        await EmailClient._send(url, {
            **payload,
            "recipient": "owner"
        })
        await EmailClient._send(url, {
            **payload,
            "recipient": "client"
        })
