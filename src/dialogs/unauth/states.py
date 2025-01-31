from aiogram.filters.state import StatesGroup, State


class UnauthState(StatesGroup):
    unauth = State()
    no_units = State()
