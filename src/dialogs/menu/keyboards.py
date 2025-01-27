from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const

from .schemas import MenuButton


def main_menu(on_click):
    return Column(
        Button(Const('🚀 Начать смену'), id=MenuButton.open_shift, on_click=on_click),
        Button(Const('✍️ Внести запись'), id=MenuButton.make_entry, on_click=on_click),
        Button(Const('🏁 Закрыть смену'), id=MenuButton.close_shift, on_click=on_click),
    )
