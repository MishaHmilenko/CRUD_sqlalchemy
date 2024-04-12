from pydantic import BaseModel

from src.business_logic.user.dto import UserBase


class CommentBase(BaseModel):
    id: int
    content: str
    user: UserBase


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str
