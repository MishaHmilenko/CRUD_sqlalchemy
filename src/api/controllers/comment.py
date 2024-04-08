from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.api.controllers.utils.utils_comment import is_comment_exist, is_owner
from src.api.dependencies import DBSession, CurrentUser
from src.db.queries import queries_comment, queries_user
from src.db.schemes.schemes_comment import CommentBase, CommentUpdate

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
            await queries_comment.add_comment(user.id, room_id, content, db)    # Create comment
            await manager.send_comment(content, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get('/', response_model=list[CommentBase])   # get comments by room_id
async def get_comments(
        room_id: int, db: DBSession, skip: int = 0, limit: int = 5,
):
    comments = await queries_comment.get_comments(room_id, skip, limit, db)
    return comments


@router.put('/{comment_id}')
async def update_comment(
        comment_id: int, comment_data: CommentUpdate, user: CurrentUser, db: DBSession
):
    await is_comment_exist(comment_id, db)
    await is_owner(comment_id, user, db)

    updated_comment = await queries_comment.update_comment_by_id(comment_id, comment_data, user, db)
    return updated_comment


@router.delete('/{comment_id}')
async def delete_comment(comment_id: int, user: CurrentUser, db: DBSession):
    await is_comment_exist(comment_id, db)
    await is_owner(comment_id, user, db)

    await queries_comment.delete_comment_by_id(comment_id, user, db)
    return {'status_code': 204, 'detail': 'Deleted successfully'}
