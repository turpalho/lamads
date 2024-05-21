import logging
from typing import Union

from aiogram import Bot
from aiogram.types import FSInputFile

from infrastructure.database.repo.requests import RequestsRepo


async def post_stories(
    chat_id: Union[int, str],
    bot: Bot,
    repo: RequestsRepo,
) -> bool:
    loader = "—"
    await bot.send_message(text=loader)
    count = 0
    while count < 25:
        loader += "—"
        count += 1
        await bot.edit_message_text(text=loader)
