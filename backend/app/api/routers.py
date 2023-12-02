from app.api.endpoints import user, desk
from fastapi import APIRouter
from app.api.urls import UserURLS, DeskURLS

router = APIRouter()

router.include_router(user.router, prefix=UserURLS.base_url, tags=["user"])
router.include_router(desk.router, prefix=DeskURLS.base_url, tags=["desc"])
