from aiogram.fsm.state import StatesGroup, State


class PhotoStates(StatesGroup):
    waiting_for_photo = State()


class EventStates(StatesGroup):
    waiting_for_code = State()
