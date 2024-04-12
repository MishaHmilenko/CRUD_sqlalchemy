from typing import Any

from fastapi import HTTPException


class RoomNotExist(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='Room not exist',
            headers=headers
        )


class NotOwnerOfRoom(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=403,
            detail='You are not the owner of the room',
            headers=headers
        )
