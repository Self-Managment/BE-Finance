from app.schemas.base import _BaseModel, BaseReturnSchema
from pydantic import BaseModel


class UserSchema(_BaseModel):
    id: int
    username: str
    email: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    token: str
    type: str
