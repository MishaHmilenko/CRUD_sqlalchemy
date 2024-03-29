from fastapi import APIRouter, HTTPException

from src.api.controllers.utils.utils_rooms import is_room_exist, is_owner
from src.api.dependencies import CurrentUser, DBSession
from src.db.queries import queries_room
from src.db.schemes.schemes_room import RoomCreate, RoomBase, RoomUpdate

router = APIRouter(prefix='/rooms', tags=['room'])


@router.post('/create-room', response_model=RoomBase)
async def create_room(room_data: RoomCreate, user: CurrentUser, db: DBSession):
    room = await queries_room.create_room(user, room_data, db)
    return room


@router.get('/own')
async def get_all_own_rooms(user: CurrentUser, db: DBSession):
    return await queries_room.get_own_rooms(user, db)


@router.put('/update/{room_id}')
async def update_room(
        room_id: int, room_data: RoomUpdate, user: CurrentUser, db: DBSession
):
    await is_room_exist(room_id, db)
    await is_owner(room_id, user, db)

    updated_room = await queries_room.update_room_by_id(room_id, room_data, user, db)
    return updated_room


@router.delete('/delete/{room_id}')
async def delete_room(room_id: int, user: CurrentUser, db: DBSession):
    await is_room_exist(room_id, db)
    await is_owner(room_id, user, db)

    await queries_room.delete_room_by_id(room_id, db)
    return {'status_code': 204, 'detail': 'Deleted successfully'}
