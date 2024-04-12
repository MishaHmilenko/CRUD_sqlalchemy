from dataclasses import dataclass

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base, DeclarativeBase

from src.config import db_user, db_password, db_host, db_port, db_name


class Base(DeclarativeBase):
    pass


@dataclass
class DBConfig:
    user: str = db_user
    password: str = db_password
    database: str = db_name
    host: str = db_host
    port: int = db_port

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


def engine_factory(config: DBConfig) -> AsyncEngine:
    return create_async_engine(
        url=config.url,
        echo=True
    )


def sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
