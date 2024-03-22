from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Room, User
from src.db.schemes.schemes_room import RoomCreate


async def create_room(user: User, room: RoomCreate, db: AsyncSession):
    db_room = Room(
        name=room.name,
        description=room.description,
        created_at=datetime.utcnow(),
        creator_id=user.id,
        creator=user
    )

    db.add(db_room)
    user.created_rooms.append(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room
