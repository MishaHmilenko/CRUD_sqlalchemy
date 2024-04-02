from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Comment
from src.db.schemes.schemes_comment import CommentCreate


async def add_comment(user_id: int, room_id: int, comment: str, db: AsyncSession):
    query = insert(Comment).values(content=comment, user_id=user_id, room_id=room_id)

    await db.execute(query)
    await db.commit()
