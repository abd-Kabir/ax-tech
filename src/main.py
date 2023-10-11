from fastapi import FastAPI

from src.users.base_config import fastapi_users, auth_backend
from src.users.router import router as user_router
from src.users.schemas import UserRead, UserCreate

app = FastAPI(
    title='AX-Technology'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(user_router)
