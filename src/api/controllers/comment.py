from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.api.dependencies import CurrentUser
from src.business_logic.comment.dto import CommentBase, CommentUpdate
from src.business_logic.comment.main import CommentLogicService

router = APIRouter(prefix='/comment', tags=['comment'])


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.remove(websocket)

    async def send_comment(self, comment: str, websocket: WebSocket):
        await websocket.send_text(comment)


manager = WebSocketManager()


@router.websocket('/ws/user-token/{user_token}/room-id/{room_id}')
async def websocket_endpoint(
        user_token: str, room_id: int, websocket: WebSocket, service: CommentLogicService
):
    await manager.connect(websocket)
    try:
        while True:
            content = await websocket.receive_text()
            await service.create_comment(content, room_id, user_token)
            await manager.send_comment(content, websocket)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@router.get('/{room_id}', response_model=list[CommentBase])
async def get_comments(room_id: int, service: CommentLogicService, skip: int = 0, limit: int = 5):
    return await service.get_comments(room_id, skip, limit)


@router.put('/{comment_id}', response_model=CommentBase)
async def update_comment(
        comment_id: int, comment_data: CommentUpdate, user: CurrentUser, service: CommentLogicService
):
    return await service.update_comment(comment_id, comment_data, user)


@router.delete('/{comment_id}')
async def delete_comment(comment_id: int, user: CurrentUser, service: CommentLogicService):
    await service.delete_comment(comment_id, user)
    return {'status_code': 204, 'detail': 'Deleted successfully'}
