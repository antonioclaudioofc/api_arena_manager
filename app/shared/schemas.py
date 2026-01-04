from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None


class MessageResponse(BaseModel):
    message: str
