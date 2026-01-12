from datetime import timedelta
from app.modules.auth.secutiry import create_access_token


def get_auth_headers(user):
    token = create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
            "role": user.role,
        },
        expires_delta=timedelta(minutes=20)
    )

    return {
        "Authorization": f"Bearer {token}"
    }
