from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional
from uuid import UUID
from app.shared.enums.user import UserRole
from app.shared.normalizers import normalize_string


class BaseUser(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr] = None

    @field_validator("email", "name", mode="before")
    @classmethod
    def normalize_fields(cls, value):
        return normalize_string(value)


class RequestUser(BaseUser):
    email: EmailStr
    name: str
    password: str = Field(min_length=6)


class UpdateUser(BaseUser):
    pass


class ResponseUser(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
