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
    type_id: typing.Union[None, int]
    title: str
    description: typing.Union[None, str]
    date_to: datetime


class CreateTaskSchema(BaseModel):
    desk_id: int
    title: str
    date_to: datetime
    type_id: typing.Union[None, int]
    description: typing.Union[None, str]
