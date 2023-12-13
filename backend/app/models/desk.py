import typing
from datetime import datetime

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.desk import DeskSchema, TaskTypeSchema, TaskSchema
from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship, joinedload


class Desk(Base):
    __tablename__ = "desk"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String, index=True, nullable=False)

    user = relationship("User", back_populates="desks")
    tasks = relationship("Task", back_populates="desk")


class TaskType(Base):
    __tablename__ = "task_type"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    color = Column(String, nullable=False)
    is_show = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="type")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    desk_id = Column(Integer, ForeignKey("desk.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("task_type.id"), nullable=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    date_to = Column(DateTime, default=datetime.utcnow)

    desk = relationship("Desk", back_populates="tasks")
    type = relationship("TaskType", back_populates="tasks")


"""
##########
## DESK ##
##########
"""


def create_desk_model(user_id: int, title: str, db: Session = Depends(get_db)) -> Desk:
    db_desc = Desk(title=title, user_id=user_id)
    db.add(db_desc)
    db.commit()
    db.refresh(db_desc)

    return db_desc


def get_desk_models_list_by_user_id(user_id: int, db: Session = Depends(get_db)) -> typing.List[DeskSchema]:
    db_desk_list = db.query(Desk).filter(Desk.user_id == user_id)
    result_list = [
        get_desk_schema(desk) for desk in db_desk_list
    ]
    return result_list


def get_desk_model_by_id(desk_id: int, db: Session = Depends(get_db)) -> Desk:
    db_desk = db.query(Desk).filter(Desk.id == desk_id).first()
    return db_desk


def check_belong_desk_to_user(desk_id: int, user_id: int, db: Session = Depends(get_db)) -> bool:
    db_desk = get_desk_model_by_id(desk_id, db)

    if db_desk and db_desk.user.id == user_id:
        return True
    return False

def get_desk_schema(desk: Desk) -> DeskSchema:
    return Schema(DeskSchema, desk)


"""
###############
## TASK_TYPE ##
###############
"""


def create_task_type_model(
        user_id: int, title: str, color: str, is_show: bool, db: Session = Depends(get_db)
) -> TaskType:
    db_task_type = TaskType(user_id=user_id, title=title, color=color, is_show=is_show)
    db.add(db_task_type)
    db.commit()
    db.refresh(db_task_type)

    return db_task_type


def get_task_type_models_list_by_user_id(
        user_id: int, is_show: typing.Union[bool, None] = None, db: Session = Depends(get_db)
) -> typing.List[TaskTypeSchema]:
    db_task_type_list = db.query(TaskType).filter(TaskType.user_id == user_id)

    if is_show is not None:
        db_task_type_list = db_task_type_list.filter(TaskType.is_show == is_show)

    result_list = [get_task_type_schema(task_type) for task_type in db_task_type_list]

    return result_list


def get_task_type_schema(task_type: TaskType) -> TaskTypeSchema:
    return Schema(TaskTypeSchema, task_type)


"""
##########
## TASK ##
##########
"""


def create_task_model(
        desk_id: int,
        title: str,
        date_to: datetime,
        type_id: typing.Union[None, str] = None,
        description: typing.Union[None, int] = None,
        db: Session = Depends(get_db)
) -> Task:
    db_task = Task(desk_id=desk_id, type_id=type_id, title=title, description=description, date_to=date_to)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_task_models_list_by_user_id(user_id: int, db: Session = Depends(get_db)) -> typing.List[TaskSchema]:
    db_task_list = db.query(Task).join(Desk, Task.desk_id == Desk.id).filter(Desk.user_id == user_id) \
        .options(joinedload(Task.desk))
    result_list = [get_task_schema(task) for task in db_task_list]
    return result_list


def get_task_schema(task: Task) -> TaskSchema:
    return Schema(TaskSchema, task)
