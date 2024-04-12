from datetime import datetime

from pydantic import BaseModel

from src.business_logic.user.dto import UserBase


class RoomBase(BaseModel):
    id: int
    name: str
    creator: UserBase
    description: str


class RoomCreate(BaseModel):
    name: str
    description: str


class RoomUpdate(RoomCreate):
    ...


class Room(RoomBase):
    created_at: datetime
    creator: UserBase
