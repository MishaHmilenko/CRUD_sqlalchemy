from typing import Annotated, AsyncGenerator

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine
from starlette.staticfiles import StaticFiles

from src.api.controllers.main import setup_controllers
from src.api.stub import Stub
from src.business_logic.comment.main import CommentBusinessLogicService
from src.business_logic.room.main import RoomBusinessLogicService
from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.comment_dao import CommentDAO
from src.db.dao.room_dao import RoomDAO
from src.db.dao.user_dao import UserDAO
from src.db.main import engine_factory, sa_session_factory, DBConfig


def factory_user_dao(session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]) -> UserDAO:
    return UserDAO(session=session)


def factory_user_logic_service(dao: Annotated[UserDAO, Depends(Stub(UserDAO))]) -> UserBusinessLogicService:
    return UserBusinessLogicService(dao=dao)


def factory_room_dao(session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]) -> RoomDAO:
    return RoomDAO(session=session)


def factory_room_logic_service(dao: Annotated[RoomDAO, Depends(Stub(RoomDAO))]) -> RoomBusinessLogicService:
    return RoomBusinessLogicService(dao=dao)


def factory_comment_dao(session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]) -> CommentDAO:
    return CommentDAO(session=session)


def factory_comment_logic_service(
        dao_comment: Annotated[CommentDAO, Depends(Stub(CommentDAO))],
        dao_room: Annotated[RoomDAO, Depends(Stub(RoomDAO))],
        dao_user: Annotated[UserDAO, Depends(Stub(UserDAO))]
) -> CommentBusinessLogicService:
    return CommentBusinessLogicService(dao_comment=dao_comment, dao_room=dao_room, dao_user=dao_user)


async def session_provider(
        sessionmaker: async_sessionmaker[AsyncSession] = Depends(Stub(async_sessionmaker[AsyncSession]))
) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session


def build_app():
    app = FastAPI(title='CRUD')

    setup_controllers(app=app)

    engine = engine_factory(DBConfig())
    sessionmaker = sa_session_factory(engine)

    add_pagination(app)
    app.mount('/static', StaticFiles(directory='static'), name='static')

    app.dependency_overrides.update({
        Stub(AsyncEngine): lambda: engine,
        Stub(async_sessionmaker[AsyncSession]): lambda: sessionmaker,
        Stub(AsyncSession): session_provider,
        Stub(UserDAO): factory_user_dao,
        Stub(UserBusinessLogicService): factory_user_logic_service,
        Stub(RoomDAO): factory_room_dao,
        Stub(RoomBusinessLogicService): factory_room_logic_service,
        Stub(CommentDAO): factory_comment_dao,
        Stub(CommentBusinessLogicService): factory_comment_logic_service
    })

    return app
