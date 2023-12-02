from app.api.urls import DeskURLS
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.models.desk import Desk, TaskType

from app.schemas.desk import (
    CreateDeskSchema,
    CreateTaskTypeSchema,
    CreateTaskSchema,
)
from app.models.desk import (
    create_desk_model,
    get_desk_models_list_by_user_id,
    get_desk_schema,
    create_task_type_model,
    get_task_type_models_list_by_user_id,
    get_task_type_schema,
    create_task_model,
    get_task_schema,
    get_task_models_list_by_user_id
)

import typing


router = APIRouter()


"""
##########
## DESK ##
##########
"""


@router.post(DeskURLS.create_desk, status_code=status.HTTP_201_CREATED)
def create_desk(desk: CreateDeskSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_desk: Desk = create_desk_model(user_id=current_user.id, title=desk.title, db=db)
    return get_desk_schema(db_desk)


@router.get(DeskURLS.get_desk_list, status_code=status.HTTP_200_OK)
def get_desk_list(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    desk_models_list = get_desk_models_list_by_user_id(user_id=current_user.id, db=db)
    return desk_models_list


"""
###############
## TASK_TYPE ##
###############
"""


@router.post(DeskURLS.create_type, status_code=status.HTTP_201_CREATED)
def create_type(
        task_type: CreateTaskTypeSchema,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_task_type: TaskType = create_task_type_model(
        user_id=current_user.id, title=task_type.title, color=task_type.color, is_show=True, db=db
    )
    return get_task_type_schema(db_task_type)


@router.get(DeskURLS.get_task_type_list, status_code=status.HTTP_200_OK)
def get_task_type_list(
        is_show: typing.Union[None, bool] = None,
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    task_type_models_list = get_task_type_models_list_by_user_id(user_id=current_user.id, is_show=is_show, db=db)
    return task_type_models_list


"""
##########
## TASK ##
##########
"""


@router.post(DeskURLS.create_task, status_code=status.HTTP_201_CREATED)
def create_task(
        task: CreateTaskSchema,
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    db_task = create_task_model(
        desk_id=task.desk_id,
        type_id=task.type_id,
        title=task.title,
        description=task.description,
        date_to=task.date_to,
        db=db,
    )
    return get_task_schema(db_task)


@router.get(DeskURLS.get_task_list, status_code=status.HTTP_200_OK)
def get_task_list(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task_models_list = get_task_models_list_by_user_id(user_id=current_user.id, db=db)
    return task_models_list
