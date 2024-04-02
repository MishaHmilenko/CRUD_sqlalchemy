from typing import Annotated

from fastapi import APIRouter, Header
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.api.dependencies import DBSession, CurrentUser
from src.db.queries import queries_comment, queries_user
from src.db.schemes import schemes_comment
from src.db.schemes.schemes_comment import CommentCreate

router = APIRouter(prefix='/comment', tags=['comment'])


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_comment(self, comment: str, websocket: WebSocket):
        await websocket.send_text(comment)


manager = WebSocketManager()


@router.websocket('/ws/user-token/{user_token}/room-id/{room_id}')
async def websocket_endpoint(
        user_token: str, room_id: int, websocket: WebSocket, db: DBSession
):
    await manager.connect(websocket)
    try:
        while True:
            content = await websocket.receive_text()
            user = await queries_user.get_user_by_token(user_token, db)
            await queries_comment.add_comment(user.id, room_id, content, db)
            await manager.send_comment(content, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


