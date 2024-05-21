from aiogram.fsm.state import State, StatesGroup


class PostStates(StatesGroup):
    ADD_POST_TEXT = State()
    ADD_POST_FILE = State()
    CONFIRM_POST = State()
    SAVED_POST = State()