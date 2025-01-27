from aiogram_dialog import Dialog

from .windows import menu_window


def menu_dialog() -> list[Dialog]:
    return [
        Dialog(menu_window()),
    ]
