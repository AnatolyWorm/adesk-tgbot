import logging
from dependency_injector.wiring import inject

from src.core.containers import container
from src.repositories.repository import Repository
from src.schemas.user import User

logger = logging.getLogger(__name__)


class AuthorizeUser:
    user_id_col = 0
    user_name_col = 1
    user_active_col = 2

    @inject
    def __init__(
        self,
        repository: Repository = container.repository()
    ):
        self.repository = repository

    async def get_user(self, id: int) -> User | None:
        user = await self.repository.get_user(id)
        return user
