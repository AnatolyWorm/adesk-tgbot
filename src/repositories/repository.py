import logging

from src.core.sheet_configs import UsersConfigs
from src.core.settings import SpreadsheetBool
from src.repositories.base_gs_repository import BaseGSRepository
from src.repositories.base_redis_repository import BaseRedisRepository
from src.schemas.user import User

from adaptix import Retort

logger = logging.getLogger(__name__)


INCOME_ITEMS = ["Носки", "Чай", "Ремонт утюга"]


class Repository:
    _users_hash_name = "users"
    _income_items_key = "income_items"

    def __init__(
        self,
        retort: Retort,
        google_repo: BaseGSRepository,
        redis_repo: BaseRedisRepository,
    ):
        self.google_repo = google_repo
        self.redis_repo = redis_repo

    async def get_user(self, user_id: int) -> User | None:
        user = await self.redis_repo.get_model_by_key_from_hash(
            self._users_hash_name, user_id, User
        )
        if not user:
            await self.update_users(self._users_hash_name)
            user = await self.redis_repo.get_model_by_key_from_hash(
                self._users_hash_name, user_id, User
            )
        return user

    async def get_income_items(self, key: str):
        return await self.redis_repo.get_list(key)

    async def update_users(self, hash: str):
        users_rows = self.google_repo.get_rows(
            UsersConfigs.sheet_name,
            UsersConfigs.START_COL,
            UsersConfigs.END_COL,
            UsersConfigs.START_ROW,
        )
        users = [
            User(
                id=int(row[UsersConfigs.id_index]),
                name=(row[UsersConfigs.name_index]),
                is_active=SpreadsheetBool.yes == (row[UsersConfigs.active_index]),
            )
            for row in users_rows
        ]
        users_dict = {}
        for user in users:
            users_dict[user.id] = user
        await self.redis_repo.save_models_by_hash(hash, users_dict)

    async def update_income_items(self, key: str = _income_items_key):
        await self.redis_repo.save_list(key, INCOME_ITEMS)

    async def update_db(self):
        await self.update_users(self._users_hash_name)
        await self.update_income_items(self._income_items_key)