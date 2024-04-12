from typing import Any

from fastapi import HTTPException


class UserNotExists(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='User not exist',
            headers=headers
        )


class UserNotAuthenticated(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=401,
            detail='Invalid authentication credentials',
            headers={"WWW-Authenticate": "Bearer"}
        )


class UserAlreadyExists(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=400,
            detail='User already exists',
            headers=headers
        )


class PasswordsDoNotMatch(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=400,
            detail='Passwords do not match',
            headers=headers
        )
