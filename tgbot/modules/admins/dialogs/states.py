from aiogram.fsm.state import State, StatesGroup


class AdminMain(StatesGroup):
    start = State()
    settings = State()
    data = State()
