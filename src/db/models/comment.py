from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.main import Base

if TYPE_CHECKING:
    from .room import Room
    from .users import User


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user: Mapped['User'] = relationship(back_populates='comments')

    room: Mapped['Room'] = relationship()
