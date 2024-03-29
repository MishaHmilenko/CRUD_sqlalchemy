import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import force_auto_coercion

from src.db.main import Base

if TYPE_CHECKING:
    from .comment import Comment
    from .room import Room

force_auto_coercion()


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    token: Mapped['UserToken'] = relationship(
        'UserToken',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    created_rooms: Mapped[List['Room']] = relationship(back_populates='creator')

    comments: Mapped[List['Comment']] = relationship(back_populates='user')


class UserToken(Base):
    __tablename__ = 'user_token'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    expires: Mapped[datetime] = mapped_column()

    user: Mapped['User'] = relationship(back_populates='token')
