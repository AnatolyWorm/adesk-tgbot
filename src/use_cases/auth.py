import json
import logging
from dependency_injector.wiring import Provide, inject

from src.core.containers import container
from src.repositories.base_gs_repository import BaseGSRepository
from src.repositories.base_redis_repository import BaseRedisRepository
from src.repositories.users_repository import UsersRedisRepository
from src.repositories.handbook import HandBookGSRepository
from src.schemas.user import User
from src.core.settings import SpreadsheetBool
from src.core.sheet_configs import UsersConfigs

logger = logging.getLogger(__name__)


class AuthorizeUser:
    user_id_col = 0
    user_name_col = 1
    user_active_col = 2

    @inject
    def __init__(
        self,
        handbook_repo: HandBookGSRepository = container.handbook_repository(),
        redis_repo: UsersRedisRepository = container.users_repository()
    ):
        self.handbook_repo = handbook_repo
        self.redis_repo = redis_repo

    async def get_user(self, id: int) -> User | None:
        user = await self.redis_repo.get_user_from_redis(id)
        if not user:
            users = await self.handbook_repo.get_users()
            await self.redis_repo.put_users_in_redis(users)
        user = await self.redis_repo.get_user_from_redis(id)
        return user
