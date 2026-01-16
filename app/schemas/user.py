from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional
from app.shared.enums import UserRole
from app.shared.normalizers import normalize_string


class BaseUser(BaseModel):
    name: Optional[str]
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("email", "username", "name", mode="before")
    @classmethod
    def normalize_fields(cls, value):
        return normalize_string(value)

    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, value):
        if value and " " in value:
            raise ValueError("Usuário não pode conter espaços")
        return value


class RequestUser(BaseUser):
    email: EmailStr
    username: str
    name: str
    password: str = Field(min_length=6)
    role: UserRole


class UpdateUser(BaseUser):
    pass


class ResponseUser(BaseModel):
    email: EmailStr
    username: str
    name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
