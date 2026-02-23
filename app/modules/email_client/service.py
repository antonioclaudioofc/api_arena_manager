import httpx

from app.core.config import EMAIL_API_URL


class EmailClient:

    @staticmethod
    async def send_verification_email(email: str, token: str):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/verification"

        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                url,
                json={
                    "email": email,
                    "token": token
                },
                headers={
                    "x-api-key": EMAIL_API_URL
                }
            )

    async def send_promote_to_owner(user, arena):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/owner-promotion"

        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                url,
                json={
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                    },
                    "arena": {
                        "id": arena.id,
                        "name": arena.name,
                    }
                },
                headers={
                    "x-api-key": EMAIL_API_URL
                }
            )

    async def send_create_new_court(user, arena, court):
        url = f"{EMAIL_API_URL}/notifications/arena-manager/new-court"

        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                url,
                json={
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
                },
                headers={
                    "x-api-key": EMAIL_API_URL
                }
            )
