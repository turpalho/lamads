import asyncio
import logging
from typing import Any, Dict

from aiogram import Bot, types
from aiogram_dialog import Dialog, DialogManager, LaunchMode, Window
from aiogram_dialog.widgets.input import MessageInput, BaseInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

# from services.broadcaster import broadcast_media_group, broadcast_plus
from infrastructure.database.models import media
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.helpers.utils import create_absolute_path, remove_temporary_files
from tgbot.helpers.process_video import process_video
from ....common.buttons import back_btn, close_dialog_back_btn
from . import states


async def save_post_text(message: types.Message,
                         message_input: MessageInput,
                         dialog_manager: DialogManager):
    dialog_manager.dialog_data['message'] = message
    await dialog_manager.next()


async def save_post_file(message: types.Message,
                         message_input: MessageInput,
                         dialog_manager: DialogManager):
    album = dialog_manager.middleware_data.get("album")
    if not album:
        album = [message]

    ct = types.ContentType
    media_group_types = [ct.PHOTO, ct.VIDEO]
    file_type = album[0].content_type

    if file_type not in media_group_types:
        await message.answer("❗️ На данный момент к загрузке доступны: "
                                "фото и видео.")
        return

    while True:
        for el in album:
            # Getting media file from message
            message_file = ((el.photo[-1], ct.PHOTO)
                            if el.content_type == ct.PHOTO
                            else (el.video, ct.VIDEO))

            bot: Bot = dialog_manager.middleware_data.get("bot")
            file_id = message_file[0].file_id

            loader = "—"
            stories_message = await message.answer(loader)
            caption = dialog_manager.dialog_data['message'].text
            try:
                stories_ads = await message.answer_video(file_id, caption=caption)
            except:
                stories_ads = await message.answer_photo(file_id, caption=caption)

            count = 0
            while count < 15:
                loader += "—"
                await stories_message.edit_text(loader)
                count += 1
                await asyncio.sleep(0.5)

            await stories_message.delete()
            await stories_ads.delete()

    dialog_manager.dialog_data['album'] = album
    await dialog_manager.next()


async def confirm_post_data(call, button, dialog_manager: DialogManager):
    album = dialog_manager.dialog_data['album']
    message = dialog_manager.dialog_data['message']

    # repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    await dialog_manager.next()


posts_main_dialog = Dialog(
    Window(
        Const(text="Отправьте текст вашего поста:"),
        MessageInput(func=save_post_text),
        close_dialog_back_btn,
        state=states.PostStates.ADD_POST_TEXT,
    ),
    Window(
        Const(text="Отправьте файл для вашего поста:"),
        MessageInput(func=save_post_file,
                    #  content_types=[
                    #      types.ContentType.PHOTO,
                    #      types.ContentType.VIDEO,
                    #      types.ContentType.ANIMATION,
                    #      types.ContentType.DOCUMENT
                    #      ]
                    ),
        back_btn,
        state=states.PostStates.ADD_POST_FILE,
    ),
    Window(
        Const(text="Ваш пост готов!"),
        Button(text=Const("🟢 Подтвердить данные"),
               id="posts_main__confirm_post_data",
               on_click=confirm_post_data),
        back_btn,
        state=states.PostStates.CONFIRM_POST,
    ),
    Window(
        Const(text="Ваш пост сохранен!"),
        close_dialog_back_btn,
        state=states.PostStates.SAVED_POST,
    ),
)