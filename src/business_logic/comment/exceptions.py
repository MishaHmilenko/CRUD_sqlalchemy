from typing import Any

from fastapi import HTTPException


class CommentNotExist(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='Comment not exist',
            headers=headers
        )


class NotOwnerOfComment(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=403,
            detail='You are not the owner of the comment',
            headers=headers
        )
