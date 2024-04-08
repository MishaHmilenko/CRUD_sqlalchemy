from fastapi import HTTPException

from src.db.queries import queries_room


async def is_room_exist(room_id, db):
    if await queries_room.get_room_by_id(room_id, db) is None:
        raise HTTPException(
            status_code=404,
            detail='The room was not found'
        )


async def is_owner(room_id, user, db):
    if await queries_room.get_owner_id_by_room_id(room_id, db) != user.id:
        raise HTTPException(
            status_code=403,
            detail='You are not the owner of the room'
        )
