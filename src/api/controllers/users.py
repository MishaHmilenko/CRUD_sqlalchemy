from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.controllers.utils.utils_users import validate_password
from src.api.dependencies import get_db, get_current_user
from src.db.queries import queries_user
from src.db.schemes.schemes_user import UserCreate, User, UserBase, LoginUser

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/sign-up', response_model=User)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    user_db = await queries_user.get_user_by_email(user.email, db)
    if user_db:
        raise HTTPException(status_code=400, detail='User already exist')
    user = await queries_user.create_user(user, db)
    await queries_user.create_user_token(user, db)
    return user


@router.post('/login', response_model=User)
async def login(user: LoginUser, db: Annotated[AsyncSession, Depends(get_db)]):
    user_db = await queries_user.get_user_by_email(user.email, db)

    if not user_db:
        raise HTTPException(status_code=404, detail='User does not exist')

    if not validate_password(user.password, user_db.password):
        raise HTTPException(status_code=400, detail='Password does not match')

    await queries_user.create_user_token(user_db, db)
    return user_db


@router.get('/me', response_model=UserBase)
async def get_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get('/by-id/{user_id}', response_model=UserBase)
async def get_user_by_id(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await queries_user.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@router.get('/by-email/{email}', response_model=UserBase)
async def get_user_by_email(email: str, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await queries_user.get_user_by_email(email, db)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user
