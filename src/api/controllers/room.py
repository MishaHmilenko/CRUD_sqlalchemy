from fastapi import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.api.dependencies import CurrentUser
from src.business_logic.room.dto import RoomBase, RoomCreate, RoomUpdate
from src.business_logic.room.main import RoomLogicService
from src.db import Room

router = APIRouter(prefix='/rooms', tags=['room'])
templates = Jinja2Templates(directory="static/templates")


@router.post('/create-room', response_model=RoomBase)
async def create_room(room_data: RoomCreate, user: CurrentUser, service: RoomLogicService):
    return await service.create_room(room_data, user)


@router.get('/own', response_model=Page[RoomBase])
async def get_all_own_rooms(user: CurrentUser, service: RoomLogicService):
    return await service.get_all_own_rooms(user)


# For test websocket
@router.get('/{room_id}')
async def get_room(room_id: int, request: Request):
    return templates.TemplateResponse(
        request=request, name='chat.html'
    )


@router.get('/', response_model=Page[RoomBase])
async def get_rooms(service: RoomLogicService):
    return await service.get_all_rooms()


@router.put('/update/{room_id}', response_model=RoomBase)
async def update_room(
        room_id: int, room_data: RoomUpdate, user: CurrentUser, service: RoomLogicService
):
    return await service.update_room_by_id(room_id, room_data, user)


@router.delete('/delete/{room_id}')
async def delete_room(
        room_id: int, user: CurrentUser, service: RoomLogicService
):
    await service.delete_room_by_id(room_id, user)
    return {'status_code': 204, 'detail': 'Deleted successfully'}
