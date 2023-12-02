from app.db.base import Base
from sqlalchemy import Column, Integer, String

from app.db.session import get_db
from sqlalchemy.orm import Session, relationship
from fastapi import Depends
from app.schemas.base import Schema

from app.schemas.user import UserSchema


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    desks = relationship("Desk", back_populates="user")


def create_user_model(username: str, email: str, password: str, db: Session = Depends(get_db)) -> User:
    db_user = User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_model(username: str, db: Session = Depends(get_db)) -> User:
    db_user = db.query(User).filter(User.username == username).first()
    return db_user


def get_user_schema(user: User) -> UserSchema:
    return Schema(UserSchema, user)
