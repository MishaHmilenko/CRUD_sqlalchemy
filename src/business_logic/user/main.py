from typing import Annotated

from fastapi import HTTPException, Depends

from src.api.controllers.utils.utils_users import validate_password
from src.api.stub import Stub
from src.business_logic.user.dto import UserBase, UserCreate, User, LoginUser
from src.business_logic.user.exceptions import UserNotExists, UserNotAuthenticated, UserAlreadyExists, PasswordsDoNotMatch
from src.db.dao.user_dao import UserDAO


class UserBusinessLogicService:
    def __init__(self, dao: UserDAO) -> None:
        self._dao = dao

    async def get_user_by_id(self, user_id: int) -> UserBase:
        user = await self._dao.get_user_by_id(user_id)

        if user is None:
            raise UserNotExists()

        return UserBase(id=user.id, name=user.name, email=user.email)

    async def get_user_by_email(self, email: str) -> UserBase:
        user = await self._dao.get_user_by_email(email)

        if user is None:
            raise UserNotExists()

        return UserBase(id=user.id, name=user.name, email=user.email)

    async def get_user_by_token(self, token: str) -> User:
        user = await self._dao.get_user_by_token(token)

        if user is None:
            raise UserNotAuthenticated()

        return user

    async def create_user(self, user: UserCreate) -> User:
        user_db = await self._dao.get_user_by_email(user.email)

        if user_db:
            raise UserAlreadyExists()

        user = await self._dao.create_user(user)
        await self._dao.create_user_token(user)
        return user

    async def authentication(self, user: LoginUser) -> User:
        user_db = await self._dao.get_user_by_email(user.email)

        if user_db is None:
            raise UserNotExists()

        # if not validate_password(user.password, user_db.password):
        #     raise PasswordsDoNotMatch()

        user_token = await self._dao.create_user_token(user_db)
        user = await self._dao.get_user_by_token(user_token.token)
        return user


UserLogicService = Annotated[UserBusinessLogicService, Depends(Stub(UserBusinessLogicService))]
