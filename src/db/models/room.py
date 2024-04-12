from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.main import Base

if TYPE_CHECKING:
    from .users import User
    from .comment import Comment


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    comments: Mapped[List['Comment']] = relationship(back_populates='room', cascade='all, delete-orphan')

    creator: Mapped['User'] = relationship(back_populates='created_rooms')
