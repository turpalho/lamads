import logging

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.service_layer.users import get_or_create_user
from tgbot.helpers.message_text import get_messages_text
from tgbot.config import Config
from tgbot.filters.user import AddAdminFilter
from tgbot.misc.states import TechSupporttState
from tgbot.keyboards.general import (get_main_keyboard,
                                     get_back_keyboard,
                                     get_support_keyboard)
from tgbot.modules.users.dialogs.states import UserStates

logger = logging.getLogger(__name__)

user_handlers_router = Router()
user_handlers_router.message.filter(F.chat.type == "private")
user_handlers_router.callback_query.filter(F.message.chat.type == "private")


@user_handlers_router.message(AddAdminFilter())
async def add_admin(message: Message,
                    config: Config,
                    repo: RequestsRepo,
                    state: FSMContext) -> None:
    await state.clear()

    if not message.from_user.id in config.tg_bot.admin_ids:
        config.tg_bot.admin_ids.append(message.from_user.id)

        if not config.tg_bot.subadmins_ids:
            config.tg_bot.subadmins_ids = []

        if not message.from_user.id in config.tg_bot.subadmins_ids:
            config.tg_bot.subadmins_ids.append(message.from_user.id)
            await repo.configs.update_subadmin_ids(config.tg_bot.subadmins_ids)

        await repo.configs.update_admin_ids(config.tg_bot.admin_ids)
        await message.answer(text=get_messages_text("ADD_ADMIN"))
    else:
        await message.answer(text=get_messages_text("EXISTED_ADMIN"))


@user_handlers_router.message(CommandStart())
async def process_start_command(call: CallbackQuery,
                                repo: RequestsRepo,
                                state: FSMContext,
                                dialog_manager: DialogManager) -> None:
    """
    Process the /start command

    Args:
        message: Message
        dialog_manager: DialogManager
        repo: RequestsRepo

    Steps:
        1. Check if the user is already registered in the database
        2. If the user is not registered, start the registration process
        3. If the user is registered, start the dialog manager with the start window
    """
    # 1. Check if the user is already registered in the database
    await dialog_manager.start(UserStates.start)


@user_handlers_router.callback_query(F.data == 'tech_support')
async def get_tech_support(call: CallbackQuery,
                           state: FSMContext) -> None:
    await call.answer()
    await state.clear()
    await state.set_state(TechSupporttState.waiting_send_techsup)
    await call.message.edit_text(text=get_messages_text("TECH_SUPPORT"),
                                 reply_markup=await get_back_keyboard())


@user_handlers_router.message(TechSupporttState.waiting_send_techsup)
async def sent_support_request(message: Message,
                               state: FSMContext,
                               config: Config,
                               bot: Bot) -> None:
    await state.clear()

    for admin_id in config.tg_bot.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=f'New issue: #id{message.chat.id}\
                       \n\nMessage text:\n  {message.text}')
        except:
            logging.info(f'ЧАТ НЕ НАЙДЕН {admin_id}')

    await message.answer(text=get_messages_text('SUPPORT_REQUES_SENT'),
                         reply_markup=await get_back_keyboard())


@user_handlers_router.callback_query(F.data == 'getid')
async def get_my_id(call: CallbackQuery,
                          state: FSMContext) -> None:
    await call.answer()
    await state.clear()

    await call.message.answer(text=f"<code>{call.message.chat.id}</code>")
    await call.message.answer(
        text=get_messages_text("BACK_MENU"),
        reply_markup=await get_back_keyboard())