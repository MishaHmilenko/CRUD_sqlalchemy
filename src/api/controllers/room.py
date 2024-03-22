from fastapi import APIRouter

from src.api.dependencies import CurrentUser, DBSession
from src.db.queries import queries_room
from src.db.schemes.schemes_room import RoomCreate

router = APIRouter(prefix='/rooms', tags=['room'])


@router.post('/create-room')
async def create_room(room_data: RoomCreate, user: CurrentUser, db: DBSession):
    room = await queries_room.create_room(user, room_data, db)
    return room
