from datetime import datetime

from pydantic import BaseModel

from src.db.schemes.schemes_for_user import UserBase


class RoomBase(BaseModel):
    id: int
    name: str
    description: str


class RoomCreate(BaseModel):
    name: str
    description: str


class Room(RoomBase):
    created_at: datetime
    creator: UserBase
