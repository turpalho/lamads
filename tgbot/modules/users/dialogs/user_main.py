from aiogram import Bot, types
from aiogram_dialog import Dialog, DialogManager, LaunchMode, Window
from aiogram_dialog.widgets.kbd import Button, Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from ...common.buttons import back_btn, close_dialog_back_btn
from .states import UserStates
from .posts.states import PostStates


async def get_channels(call, button, dialog_manager: DialogManager):
    await dialog_manager.start(state=PostStates.ADD_POST_TEXT)

async def add_post_start(call, button, dialog_manager: DialogManager):
    await dialog_manager.start(state=PostStates.ADD_POST_TEXT)


users_main_dialog = Dialog(
    Window(
        Const("Главное меню:"),
        Button(text=Const("Мои каналы"),
               id="view_channels",
               on_click=get_channels),
        Button(text=Const("Добавить пост"),
               id="add_post",
               on_click=add_post_start),
        state=UserStates.start,
    ),
)