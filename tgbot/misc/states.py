from aiogram.fsm.state import State, StatesGroup


class AddPostState(StatesGroup):
    waiting_send_post = State()


class TechSupporttState(StatesGroup):
    waiting_send_techsup = State()


class AdminState(StatesGroup):
    waiting_set_new_payment_sum = State()
