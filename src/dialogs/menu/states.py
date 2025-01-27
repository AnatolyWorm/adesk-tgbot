from aiogram.filters.state import StatesGroup, State


class Menu(StatesGroup):
    choose_scenario = State()
