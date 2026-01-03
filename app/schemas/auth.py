from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.shared.enums import UserRole
from app.shared.normalizers import normalize_string


class AuthCreate(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: UserRole

    @field_validator("email", "username", mode="before")
    @classmethod
    def normalize_auth_fields(cls, value):
        return normalize_string(value)

    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, value):
        if " " in value:
            raise ValueError("Username não pode conter espaços")

        return value

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def normalize_names(cls, value):
        return normalize_string(value)


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    created_at: str
    updated_at: str | None

    model_config = ConfigDict(from_attributes=True)
