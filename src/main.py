import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from src.core.bot import create_bot, create_dispatcher
from dependency_injector.wiring import inject
from src.core.containers import container
from src.core.settings import settings
from src.dialogs import include_dialogs
from src.handlers import user_router

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=settings.LOGGER.LEVEL,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)


def register_all_handlers(dp: Dispatcher):
    dp.include_router(user_router)


@inject
async def main():
    logger.info('Creating bot...')
    bot: Bot = create_bot()
    await bot.delete_webhook()
    logger.info('Creating dispatcher...')
    dp: Dispatcher = create_dispatcher(
                        bot=bot,
                        storage=container.storage(),
                    )

    logger.info('Registering handlers...')
    register_all_handlers(dp)

    logger.info('Setup dialogs...')
    include_dialogs(dp)
    setup_dialogs(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped!')
