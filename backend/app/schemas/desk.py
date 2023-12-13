import typing
from datetime import datetime

from app.schemas.base import _BaseModel
from pydantic import BaseModel


class DeskSchema(_BaseModel):
    id: int
    title: str
    user_id: int


class CreateDeskSchema(BaseModel):
    title: str


class TaskTypeSchema(_BaseModel):
    id: int
    user_id: int
    title: str
    color: str
    is_show: bool


class CreateTaskTypeSchema(BaseModel):
    title: str
    color: str


class TaskSchema(_BaseModel):
    id: int
    desk_id: int
    type_id: typing.Optional[int]
    title: str
    description: typing.Optional[str]
    date_to: typing.Optional[datetime]


class CreateTaskSchema(BaseModel):
    desk_id: int
    title: str
    date_to: typing.Optional[datetime]
    type_id: typing.Optional[int]
    description: typing.Optional[str]
