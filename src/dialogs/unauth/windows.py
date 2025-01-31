from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format, Const

from .getters import get_user
from .states import UnauthState


def unauthorized_window():
    return Window(
        Format('Вы не авторизованы\.'),
        Format('Ваш id: `{user_id}` 👈'),
        parse_mode='MarkdownV2',
        state=UnauthState.unauth,
        getter=get_user,
    )


def no_units():
    return Window(
        Const('У вас нет доступа к кассам.'),
        Const('Обратитесь к администратору.'),
        state=UnauthState.no_units,
    )