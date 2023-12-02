import pytest
from app.core.config import TEST_DATABASE_URL
from app.db.base import Base
from app.main import app
from app.models.user import get_user_model, create_user_model
from app.schemas.user import UserCreateSchema, UserLoginSchema
from app.schemas.desk import DeskSchema
from factory import Factory, Faker, SubFactory
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.urls import UserURLS

from app.core.security import pwd_context

register_url = UserURLS.register_url
login_url = UserURLS.login_url
user_data_url = UserURLS.user_data_url


@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db(tables, engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    client = AsyncClient(app=app, base_url="https://test.com")
    return client


class UserFactory(Factory):
    class Meta:
        model = UserCreateSchema

    username = Faker("word")
    email = Faker("email")
    password = Faker("password")


@pytest.fixture
async def get_user_data():
    user = UserFactory()
    return user.dict()


@pytest.fixture
async def get_user(db, client, get_user_data):
    register_data = await get_user_data

    db_user = get_user_model(register_data.get("username"), db)
    if not db_user:
        hashed_password = pwd_context.hash(register_data.get("password"))
        create_user_model(
            username=register_data.get("username"), email=register_data.get("email"), password=hashed_password, db=db
        )

    return register_data


@pytest.fixture
async def get_token(db, client, get_user):
    user_data = await get_user
    login_data = UserLoginSchema(**user_data)
    login_data = login_data.dict()

    response = await client.post(login_url, json=login_data)
    response_json = response.json()

    token = f"{response_json.get('type')} {response_json.get('token')}"

    return token


# class DeskFactory(Factory):
#     class Meta:
#         model = DeskSchema
#
#     title = Faker("word")
#     user_id = SubFactory(UserFactory)
#
#
# @pytest.fixture
# async def get_desk_data():
#     desk = DeskFactory()
#     return desk.dict()
#
#
# @pytest.fixture
# async def get_desk(db, get_desk_data):
#     desk_data = await get_desk_data
#     return desk_data


