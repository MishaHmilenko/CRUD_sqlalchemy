from fastapi import APIRouter

from src.api.dependencies import CurrentUser
from src.business_logic.user.dto import User, UserCreate, LoginUser, UserBase
from src.business_logic.user.main import UserLogicService


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/sign-up', response_model=User)
async def create_user(user: UserCreate, service: UserLogicService):
    return await service.create_user(user)


@router.post('/login', response_model=User)
async def login(user: LoginUser, service: UserLogicService):
    return await service.authentication(user)


@router.get('/me', response_model=UserBase)
async def get_current_user(user: CurrentUser):
    return user


@router.get('/by-id/{user_id}', response_model=UserBase)
async def get_user_by_id(
        user_id: int, service: UserLogicService
):
    return await service.get_user_by_id(user_id)


@router.get('/by-email/{email}', response_model=UserBase)
async def get_user_by_email(
        email: str, service: UserLogicService
) -> UserBase:
    return await service.get_user_by_email(email)
