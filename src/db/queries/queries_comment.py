from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import Comment, User
from src.db.schemes.schemes_comment import CommentUpdate


async def add_comment(user_id: int, room_id: int, comment: str, db: AsyncSession):
    query = insert(Comment).values(content=comment, user_id=user_id, room_id=room_id)

    await db.execute(query)
    await db.commit()


async def get_comments(room_id: int, skip: int, limit: int, db: AsyncSession):
    query = select(Comment).where(Comment.room_id == room_id).offset(skip).limit(limit).order_by(Comment.created_at).options(selectinload(Comment.user))    #!!!!!!!!!!!!!!!

    result = await db.execute(query)
    return result.scalars().all()


async def get_comment_by_id(comment_id: int, db: AsyncSession):
    query = select(Comment).where(Comment.id == comment_id)

    result = await db.execute(query)
    return result.scalars().first()


async def get_owner_id_by_comment_id(comment_id: int, db: AsyncSession):
    query = select(Comment.user_id).where(Comment.id == comment_id)

    result = await db.execute(query)
    return result.scalars().first()


async def update_comment_by_id(comment_id, comment_data: CommentUpdate, user: User, db: AsyncSession):
    query = (
        update(Comment)
        .values(content=comment_data.content)
        .where(Comment.id == comment_id)
        .where(Comment.user_id == user.id)
        .returning(Comment))

    result = await db.execute(query)
    await db.commit()
    return result.scalars().first()


async def delete_comment_by_id(comment_id, user: User, db: AsyncSession):
    query = delete(Comment).where(Comment.id == comment_id).where(Comment.user_id == user.id)

    await db.execute(query)
    await db.commit()
