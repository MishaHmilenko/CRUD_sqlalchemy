from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import User, UserToken
from src.db.schemes.schemes_for_user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_user_token(db: AsyncSession, user: User) -> UserToken:
    print('starts create_user_token')
    db_token = UserToken(user=user, expires=datetime.now() + timedelta(weeks=2))
    print('db_token ', db_token)
    db.add(db_token)
    print('Add db_token')
    await db.commit()
    print('commit')
    await db.refresh(db_token)
    print('refresh', db_token.token)
    return str(db_token.token)
