from aiogram_dialog import Dialog

from .windows import unauthorized_window, no_units


def menu_dialog() -> list[Dialog]:
    return [
        Dialog(
            unauthorized_window(),
            no_units(),
        ),
    ]
