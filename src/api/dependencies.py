from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import User
from src.db.main import SessionLocal
from src.db.queries.queries_user import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_current_user(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    print(token)
    user = await get_user_by_token(token, db)
    print(user)

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Invalid authentication credentials',
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user
