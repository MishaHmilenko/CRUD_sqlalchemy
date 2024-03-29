from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Room, User
from src.db.schemes.schemes_room import RoomCreate, RoomUpdate


async def create_room(user: User, room: RoomCreate, db: AsyncSession):
    db_room = Room(
        name=room.name,
        description=room.description,
        created_at=datetime.utcnow(),
        creator_id=user.id,
        creator=user
    )

    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room


async def get_room_by_id(room_id, db: AsyncSession):
    query = select(Room).where(Room.id == room_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_own_rooms(user: User, db: AsyncSession):
    query = select(Room).where(Room.creator_id == user.id)
    results = await db.execute(query)
    return results.scalars().all()


async def get_owner_id_by_room_id(room_id: int, db: AsyncSession):
    query = select(Room.creator_id).where(Room.id == room_id)
    result = await db.execute(query)
    return result.scalars().first()


async def update_room_by_id(room_id: int, room_data: RoomUpdate, user: User, db: AsyncSession):
    query = (
        update(Room)
        .values(name=room_data.name, description=room_data.description)
        .where(Room.id == room_id)
        .where(Room.creator_id == user.id)
        .returning(Room)
    )

    result = await db.execute(query)
    await db.commit()
    return result.scalars().first()


async def delete_room_by_id(room_id: int, db: AsyncSession):
    query = delete(Room).where(Room.id == room_id)
    await db.execute(query)
    await db.commit()
