from datetime import datetime, timezone
import uuid
from app.core.security import hash_password
from app.models.user import User
from app.shared.enums import UserRole


def user_factory(db, role=UserRole.client, password="123456"):
    unique = uuid.uuid4().hex[:8]

    user = User(
        email=f"user_{unique}@test.com",
        username=f"user_{unique}",
        name=f"User{unique}",
        hashed_password=hash_password(password),
        role=role,
        created_at=datetime.now(timezone.utc)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
