from typing import Annotated

from fastapi import Depends
from fastapi_pagination import Page

from src.api.stub import Stub
from src.business_logic.room.dto import RoomCreate, RoomUpdate, RoomBase
from src.business_logic.room.exceptions import RoomNotExist, NotOwnerOfRoom
from src.business_logic.user.dto import UserBase
from src.db import User
from src.db.dao.room_dao import RoomDAO
from src.db.dao.user_dao import UserDAO


class RoomBusinessLogicService:
    def __init__(self, dao_room: RoomDAO, dao_user: UserDAO):
        self._dao_room = dao_room
        self._dao_user = dao_user

    async def create_room(self, room_data: RoomCreate, user: UserBase) -> RoomBase:
        user = await self._dao_user.get_user_by_id(user.id)
        room = await self._dao_room.create_room(room_data, user)
        return RoomBase(
            id=room.id,
            name=room.name,
            creator=UserBase(id=user.id, name=user.name, email=user.email),
            description=room.description
        )

    async def get_all_own_rooms(self, user: User) -> Page[RoomBase]:
        return await self._dao_room.get_rooms_by_user_id(user)

    async def get_all_rooms(self) -> Page[RoomBase]:
        return await self._dao_room.get_all_rooms()

    async def update_room_by_id(self, room_id: int, room_data: RoomUpdate, user: User) -> RoomBase:
        room = await self._dao_room.update_room_by_id(room_id, room_data, user)

        if await self._dao_room.get_room_by_id(room_id) is None:
            raise RoomNotExist()

        if await self._dao_room.get_owner_id_by_room_id(room_id) != user.id:
            raise NotOwnerOfRoom()

        return RoomBase(
            id=room.id,
            name=room.name,
            creator=UserBase(id=room.creator.id, name=room.creator.name, email=room.creator.email),
            description=room.description
        )

    async def delete_room_by_id(self, room_id: int, user: User):

        if await self._dao_room.get_room_by_id(room_id) is None:
            raise RoomNotExist()

        if await self._dao_room.get_owner_id_by_room_id(room_id) != user.id:
            raise NotOwnerOfRoom()

        await self._dao_room.delete_room_by_id(room_id, user)


RoomLogicService = Annotated[RoomBusinessLogicService, Depends(Stub(RoomBusinessLogicService))]
