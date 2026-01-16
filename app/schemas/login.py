from pydantic import BaseModel, EmailStr


class RequestLogin(BaseModel):
    email: EmailStr
    password: str
