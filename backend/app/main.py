from fastapi import FastAPI

from app.api.routers import router as api_router
from app.db.base import Base
from app.db.session import engine

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключаем роутер API
app.include_router(api_router)


# Создаем таблицы в базе данных при запуске приложения
def init():
    Base.metadata.create_all(bind=engine)


# Инициализируем таблицы
init()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
