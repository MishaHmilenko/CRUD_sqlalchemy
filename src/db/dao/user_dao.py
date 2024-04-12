from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.api.controllers.utils.utils_users import get_random_string, hash_password
from src.business_logic.user.dto import UserCreate
from src.db import User, UserToken
from src.db.dao.main import BaseDAO


class UserDAO(BaseDAO):
    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_user_by_token(self, token: str) -> User:
        query = (
            select(UserToken)
            .where(UserToken.token == token)
            .options(joinedload(UserToken.user))
        )

        result = await self._session.execute(query)
        token = result.scalars().first()
        return token.user

    async def create_user(self, user: UserCreate) -> User:
        salt = get_random_string()
        hashed_password = hash_password(user.password)

        db_user = User(name=user.name, email=user.email, password=f'{salt}${hashed_password}')
        self._session.add(db_user)
        await self._session.commit()
        await self._session.refresh(db_user)
        return db_user

    async def create_user_token(self, user: User) -> UserToken:
        db_token = UserToken(user=user, expires=datetime.now() + timedelta(weeks=2))
        self._session.add(db_token)
        await self._session.commit()
        await self._session.refresh(db_token)
        return db_token
