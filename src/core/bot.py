from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage

from middlewares import AuthMiddleware
from src.core.settings import settings


def create_bot() -> Bot:
    return Bot(token=settings.TG_BOT_TOKEN)


def create_dispatcher(
    bot: Bot,
    storage: BaseStorage | None = None,
) -> Dispatcher:
    dp = Dispatcher(
            bot=bot,
            storage=storage,
        )
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    return dp
