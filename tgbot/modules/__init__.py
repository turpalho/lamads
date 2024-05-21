# flake8: noqa
from aiogram import Router

# from .admins.dialogs import admin_dialogs_router
from .users.user_handlers import user_handlers_router
from .users.dialogs import user_dialogs_router
from .chats.chats_hanlers import chats_handler_router

common_router = Router()
common_router.include_routers(
    # admin_handlers_router,
    chats_handler_router,
    user_handlers_router,
    user_dialogs_router,
    # admin_dialogs_router,
)
