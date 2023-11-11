
from pydantic import BaseModel, EmailStr
from src.database.models import UserRole





class RequestRole(BaseModel):
    email: EmailStr
    role: UserRole


class CommentSchema(BaseModel):
    text: str = "some text"
    photo_id: int


class CommentList(BaseModel):
    limit: int = 10
    offset: int = 0
    photo_id: int


class CommentUpdateSchems(BaseModel):
    id: int
    text: str


class CommentResponse(BaseModel):
    username: str
    text: str
    photo_id: int


class CommentRemoveSchema(BaseModel):
    id: int
