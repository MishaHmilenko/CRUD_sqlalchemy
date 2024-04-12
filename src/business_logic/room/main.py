from typing import Annotated

from fastapi import Depends

from src.api.stub import Stub
from src.business_logic.room.dto import RoomCreate, RoomUpdate
from src.business_logic.room.exceptions import RoomNotExist, NotOwnerOfRoom
from src.db import User, Room
from src.db.dao.room_dao import RoomDAO


class RoomBusinessLogicService:
    def __init__(self, dao: RoomDAO):
        self._dao = dao

    async def create_room(self, room_data: RoomCreate, user: User) -> Room:
        room = await self._dao.create_room(room_data, user)
        return room

    async def get_all_own_rooms(self, user: User) -> list[Room]:
        rooms = await self._dao.get_rooms_by_user_id(user)
        return rooms

    async def get_all_rooms(self) -> list[Room]:
        rooms = await self._dao.get_all_rooms()
        return rooms

    async def update_room_by_id(self, room_id: int, room_data: RoomUpdate, user: User) -> Room:
        room = await self._dao.update_room_by_id(room_id, room_data, user)

        if await self._dao.get_room_by_id(room_id) is None:
            raise RoomNotExist()

        if await self._dao.get_owner_by_room_id(room_id) != user.id:
            raise NotOwnerOfRoom()

        return room

    async def delete_room_by_id(self, room_id: int, user: User):

        if await self._dao.get_room_by_id(room_id) is None:
            raise RoomNotExist()

        if await self._dao.get_owner_by_room_id(room_id) != user.id:
            raise NotOwnerOfRoom()

        await self._dao.delete_room_by_id(room_id, user)


RoomLogicService = Annotated[RoomBusinessLogicService, Depends(Stub(RoomBusinessLogicService))]
