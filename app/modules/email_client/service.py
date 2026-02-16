import httpx

from app.core.config import EMAIL_API_URL


class EmailClient:

    @staticmethod
    async def send_verification_email(email: str, token: str):
        url = f"{EMAIL_API_URL}/email/"

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
