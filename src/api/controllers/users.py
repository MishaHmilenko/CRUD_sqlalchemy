from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_db
from src.db.queries import queries_user
from src.db.schemes.schemes_for_user import UserCreate

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/sign-up')
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    user_db = await queries_user.get_user_by_email(db, user.email)
    if user_db:
        raise HTTPException(status_code=400, detail='User already exist')
    user = await queries_user.create_user(db, user)
    user.token = await queries_user.create_user_token(db, user)
    return user
