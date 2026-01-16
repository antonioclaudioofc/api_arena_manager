from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional
from app.shared.enums import UserRole
from app.shared.normalizers import normalize_string


class BaseUser(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("email", "username", "first_name", "last_name", mode="before")
    @classmethod
    def normalize_fields(cls, value):
        if value is None:
            return value
        return normalize_string(value)

    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, value):
        if value and " " in value:
            raise ValueError("Username não pode conter espaços")
        return value


class RequestUser(BaseUser):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str = Field(min_length=6)
    role: UserRole


class UpdateUser(BaseUser):
    pass


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class ResponseUser(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
