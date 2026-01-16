from datetime import datetime, timezone
from app.core.security import hash_password
from app.models.user import Users


def user_factory(
    db,
    *,
    email="user@test.com",
    username="user",
    password="123456",
    role="client",
):
    user = Users(
        email=email,
        username=username,
        first_name="Test",
        last_name="User",
        hashed_password=hash_password(password),
        role=role,
        created_at=datetime.now(timezone.utc)
    )

    db.add(user)
    db.commit()
    db.refresh

    return user
