from datetime import datetime

from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.business_logic.room.dto import RoomCreate, RoomUpdate, RoomBase
from src.db import Room, User
from src.db.dao.main import BaseDAO


class RoomDAO(BaseDAO):
    async def create_room(self, room: RoomCreate, user: User) -> Room:

        db_room = Room(
            name=room.name,
            description=room.description,
            created_at=datetime.utcnow(),
            creator_id=user.id,
            creator=user
        )

        self._session.add(db_room)
        await self._session.commit()
        await self._session.refresh(db_room)
        return db_room

    async def get_all_rooms(self) -> Page[RoomBase]:
        query = select(Room).options(selectinload(Room.creator))
        return await paginate(self._session, query)

    async def get_room_by_id(self, room_id: int) -> Room:
        query = select(Room).where(Room.id == room_id)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_rooms_by_user_id(self, user: User) -> Page[RoomBase]:
        query = select(Room).where(Room.creator_id == user.id)
        return await paginate(self._session, query)

    async def get_owner_id_by_room_id(self, room_id: int) -> int:
        query = select(Room.creator_id).where(Room.id == room_id)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def update_room_by_id(self, room_id: int, room_data: RoomUpdate, user: User) -> Room:
        query = (
            update(Room)
            .values(name=room_data.name, description=room_data.description)
            .where(Room.id == room_id)
            .where(Room.creator_id == user.id)
            .returning(Room).options(selectinload(Room.creator))
        )

        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def delete_room_by_id(self, room_id: int, user: User):
        query = delete(Room).where(Room.id == room_id).where(User.id == user.id)

        await self._session.execute(query)
        await self._session.commit()
