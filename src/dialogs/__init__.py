from aiogram import Dispatcher

from . import menu, unauth


def include_dialogs(dp: Dispatcher):
    for dialog in [
        *menu.menu_dialog(),
        *unauth.menu_dialog(),
    ]:
        dp.include_router(dialog)
