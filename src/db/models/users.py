import uuid
from datetime import datetime

from sqlalchemy.dialects import postgresql

from sqlalchemy import String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import force_auto_coercion, EmailType, PasswordType

from src.db.main import Base

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


class UserToken(Base):
    __tablename__ = 'user_token'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[UUID] = mapped_column(UUID, default=uuid.uuid4)
    expires: Mapped[datetime] = mapped_column()

    user: Mapped['User'] = relationship(
        'User',
        back_populates='token',
    )
