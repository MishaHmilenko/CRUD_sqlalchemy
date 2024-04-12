from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.business_logic.comment.dto import CommentUpdate
from src.db import Comment, User
from src.db.dao.main import BaseDAO


class CommentDAO(BaseDAO):
    async def create_comment(self, content: str, room_id: int, user: User) -> Comment:
        db_comment = Comment(
            content=content,
            user_id=user.id,
            room_id=room_id,
            created_at=datetime.utcnow(),
            user=user
        )

        self._session.add(db_comment)
        await self._session.commit()
        await self._session.refresh(db_comment)
        return db_comment

    async def get_comments(self, room_id: int, skip: int, limit: int) -> list[Comment]:
        query = (
            select(Comment)
            .where(Comment.room_id == room_id)
            .offset(skip)
            .limit(limit)
            .order_by(Comment.created_at)
            .options(selectinload(Comment.user))
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        query = select(Comment).where(Comment.id == comment_id)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_user_id_by_comment_id(self, comment_id: int):
        query = select(Comment.user_id).where(Comment.id == comment_id)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def update_comment_by_id(self, comment_id: int, comment_data: CommentUpdate, user: User) -> Comment:
        query = (
            update(Comment)
            .values(content=comment_data.content)
            .where(Comment.id == comment_id)
            .where(Comment.user_id == user.id)
            .returning(Comment)
        )

        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def delete_comment_by_id(self, comment_id: int, user: User):
        query = delete(Comment).where(Comment.id == comment_id).where(Comment.user_id == user.id)
        await self._session.execute(query)
        await self._session.commit()
