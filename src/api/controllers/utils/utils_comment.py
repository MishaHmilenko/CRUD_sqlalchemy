from fastapi import HTTPException

from src.api.dependencies import DBSession
from src.db import User
from src.db.queries import queries_comment


async def is_comment_exist(comment_id, db: DBSession):
    if await queries_comment.get_comment_by_id(comment_id, db) is None:
        raise HTTPException(
            status_code=404,
            detail='The comment was not found'
        )


async def is_owner(comment_id, user: User, db: DBSession):
    print(user.id, 'user')
    if await queries_comment.get_owner_id_by_comment_id(comment_id, db) != user.id:
        raise HTTPException(
            status_code=403,
            detail='You are not the owner of the comment'
        )
