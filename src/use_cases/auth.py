import json
import logging
from dependency_injector.wiring import Provide, inject
from adaptix import Retort

from src.core.containers import Container, container
from src.repositories.base_gs_repository import BaseGSRepository
from src.repositories.base_redis_repository import BaseRedisRepository
from src.repositories.handbook import HandBookRepository
from src.schemas.user import User
from src.core.settings import SpreadsheetBool
from src.core.sheet_configs import UsersConfigs

retort = Retort()

logger = logging.getLogger(__name__)

class AuthorizeUser:
    user_id_col = 0
    user_name_col = 1
    user_active_col = 2

    @inject
    def __init__(
        self,
        handbook_repo: HandBookRepository = container.handbook_repository(),
        redis_repo: BaseRedisRepository = container.redis_repository()
    ):
        self.handbook_repo = handbook_repo
        self.redis_repo = redis_repo

    async def get_user(self, id: int) -> User | None:
        user = await self.redis_repo.get_data(["user", str(id)])
        logger.info(user)
        if not user:
            logger.info("Go to GoogleSheets")
            users_rows = self.handbook_repo.get_rows(
                UsersConfigs.START_COL,
                UsersConfigs.END_COL,
                UsersConfigs.START_ROW,
            )
            for row in users_rows:
                if int(row[self.user_id_col]) == id:
                    user = User(
                        id=int(row[self.user_id_col]),
                        name=(row[self.user_name_col]),
                        is_active=SpreadsheetBool.yes == (row[self.user_active_col]),
                    )

                    logger.info("Set new user")
                    await self.redis_repo.set_data(["user", str(user.id)], self.redis_repo.convert_to_dict(user))
                    return user
        return self.redis_repo.convert_to_model(user, User)
