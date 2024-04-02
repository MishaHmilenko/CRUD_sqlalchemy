from datetime import datetime

from pydantic import BaseModel, constr, UUID4, Field, field_validator, EmailStr


class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8)


class TokenBase(BaseModel):
    token: UUID4 = Field(alias='access_token')
    expires: datetime
    token_type: str | None = 'bearer'

    class Config:
        from_attributes = True
        populate_by_name = True

    @field_validator('token')
    def hexlify_token(cls, value):
        return value.hex


class User(UserBase):
    token: TokenBase | None = None

    class Config:
        from_attributes = True


class LoginUser(BaseModel):
    email: str
    password: str
