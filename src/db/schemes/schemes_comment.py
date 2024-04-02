from pydantic import BaseModel

from src.db.schemes.schemes_user import UserBase


class CommentBase(BaseModel):
    content: str
    user: UserBase


class CommentCreate(BaseModel):
    content: str
