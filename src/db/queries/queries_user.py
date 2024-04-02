from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.controllers.utils.utils_users import hash_password, get_random_string
from src.db import User, UserToken
from src.db.schemes.schemes_user import UserCreate


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_token(token: str, db: AsyncSession):
    query = (
        select(UserToken)
        .where(UserToken.token == token)
        .options(joinedload(UserToken.user))
    )

    result = await db.execute(query)
    token = result.scalars().first()
    return token.user


async def create_user(user: UserCreate, db: AsyncSession) -> User:

    salt = await get_random_string()
    hashed_password = await hash_password(user.password)

    db_user = User(name=user.name, email=user.email, password=f'{salt}${hashed_password}')
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_user_token(user: User, db: AsyncSession) -> User:
    db_token = UserToken(user=user, expires=datetime.now() + timedelta(weeks=2))
    db.add(db_token)
    user.token = db_token
    await db.commit()
    await db.refresh(db_token)
    return db_token
