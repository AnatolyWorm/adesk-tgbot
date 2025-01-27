import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.dialogs.menu.states import Menu
from src.dialogs.unauth.states import UnauthState
from src.schemas.user import User

logger = logging.getLogger(__name__)
user_router = Router(name=__name__)


@user_router.message(Command('start'))
async def start(message: Message, dialog_manager: DialogManager):
    user: User = dialog_manager.middleware_data.get('user')
    if user is None:
        await dialog_manager.reset_stack(remove_keyboard=True)
        await dialog_manager.start(UnauthState.unauth)
        return

    await message.answer(f"Привет {user.name}")
    await dialog_manager.start(Menu.choose_scenario, mode=StartMode.RESET_STACK)


@user_router.message(Command('myid'))
async def myid(message: Message, dialog_manager: DialogManager):
    await message.answer(f'Ваш id: `{message.from_user.id}` 💠', parse_mode='MarkdownV2')
