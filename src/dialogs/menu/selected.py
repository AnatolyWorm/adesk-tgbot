from aiogram_dialog.widgets.kbd import Button

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram import Bot

from .schemas import MenuButton
from .states import Menu
# from src.dialogs.dds.states import DDS
# from src.dialogs.open_shift.states import OpenShift
# from src.dialogs.close_shift.states import CloseShift
from src.schemas.user import User


async def on_chosen_menu(c: CallbackQuery, widget: Button, manager: DialogManager):
    if widget.widget_id == MenuButton.open_shift:
        await manager.start(Menu.choose_scenario, mode=StartMode.RESET_STACK)
        return

    if widget.widget_id == MenuButton.make_entry:
        # user: User = manager.middleware_data.get('user')
        # if len(user.units) == 1:
        #     bot: Bot = manager.middleware_data.get('bot')
        #     await bot.send_message(
        #         chat_id=c.from_user.id,
        #         text=f'`{user.units[0].title}({user.units[0].brand}) г.{user.units[0].city}`',
        #         parse_mode='MarkdownV2'
        #     )
        #     await manager.start(DDS.select_initial_cashbox, mode=StartMode.RESET_STACK)
        #     return
        await manager.start(Menu.choose_scenario, mode=StartMode.RESET_STACK)
        return

    # if widget.widget_id == MenuButton.close_shift:
    #     await manager.start(CloseShift.select_unit, mode=StartMode.RESET_STACK)
    #     return
    await manager.switch_to(Menu.choose_scenario)
