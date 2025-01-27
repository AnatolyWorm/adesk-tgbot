from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from .keyboards import main_menu
from .selected import on_chosen_menu
from .states import Menu


def menu_window():
    return Window(
        Const('Выберите раздел меню'),
        main_menu(on_click=on_chosen_menu),
        state=Menu.choose_scenario,
        markup_factory=ReplyKeyboardFactory(),
    )
