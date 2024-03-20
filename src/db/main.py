from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.config import db_user, db_password, db_host, db_port, db_name

full_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_async_engine(full_url, echo=True)

SessionLocal = async_sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


Base = declarative_base()
