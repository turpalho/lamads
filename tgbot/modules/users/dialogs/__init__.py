from aiogram import Router

from .user_main import users_main_dialog
from .posts import post_router

user_dialogs_router = Router(name=__name__)
user_dialogs_router.include_routers(
    users_main_dialog,
    post_router,
)