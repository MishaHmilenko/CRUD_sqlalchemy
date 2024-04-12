from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.business_logic.user.main import UserLogicService
from src.db import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
        service: UserLogicService, token: str = Depends(oauth2_scheme),
) -> User:
    return await service.get_user_by_token(token)


CurrentUser = Annotated[AsyncSession, Depends(get_current_user)]
