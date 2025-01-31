import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from use_cases.auth import AuthorizeUser
# from repositories.user import Repository
from schemas.user import User

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        chat_id = event.from_user.id
        try:
            user: User | None = await AuthorizeUser().get_user(chat_id)
        except Exception as exc:
            logger.exception(exc)
            user = None
        data.update({'user': user, 'user_id': chat_id})
        return await handler(event, data)
