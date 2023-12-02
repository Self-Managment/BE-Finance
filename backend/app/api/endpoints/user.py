from app.api.urls import UserURLS
from app.core.security import get_current_user
from app.core.security import pwd_context, create_access_token
from app.db.session import get_db
from app.models.user import User, create_user_model, get_user_model, get_user_schema
from app.schemas.user import UserCreateSchema, UserLoginSchema, UserSchema, TokenSchema
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(UserURLS.register, status_code=status.HTTP_201_CREATED)
def user_register(user: UserCreateSchema, db: Session = Depends(get_db)):
    """
    Эндпоинт регистрации юзера
    """
    username = user.username
    email = user.email
    password = user.password

    db_user = get_user_model(username, db)
    if db_user:
        raise HTTPException(status_code=403, detail=f"Пользователь {username} уже существует")

    hashed_password = pwd_context.hash(password)
    user = create_user_model(username=username, email=email, password=hashed_password, db=db)
    if not user:
        raise HTTPException(status_code=500, detail="Произошла неизвестная ошибка")
    access_token = create_access_token(data={"sub": username})

    return_data = TokenSchema(
        token=access_token,
        type="bearer",
    )

    return return_data


@router.post(UserURLS.login, status_code=status.HTTP_200_OK)
def user_login(user: UserLoginSchema, db: Session = Depends(get_db)):
    """
    Логин
    """
    db_user = get_user_model(user.username, db)
    if db_user and pwd_context.verify(user.password, db_user.password):
        access_token = create_access_token(data={"sub": db_user.username})

        return_data = TokenSchema(
            token=access_token,
            type="bearer",
        )

        return return_data

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get(UserURLS.user_data, status_code=status.HTTP_200_OK)
def get_private_data(current_user: User = Depends(get_current_user)):
    return get_user_schema(current_user)
