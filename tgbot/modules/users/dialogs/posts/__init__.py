from aiogram import Router

from .posts_main import posts_main_dialog

post_router = Router(name=__name__)
post_router.include_routers(
    posts_main_dialog,
)