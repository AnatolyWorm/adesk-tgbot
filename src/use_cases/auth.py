from dependency_injector.wiring import Provide, inject

from src.core.containers import Container, container
from src.repositories.base_gs_repository import BaseGSRepository
from src.repositories.handbook import HandBookRepository
from src.schemas.user import User
from src.core.settings import SpreadsheetBool, settings, SheetNames


import logging
logger = logging.getLogger(__name__)

class AuthorizeUser:
    user_id_col = 0
    user_name_col = 1
    user_active_col = 2

    @inject
    def __init__(
        self,
        handbook_repo: HandBookRepository = container.handbook_repository()
        # handbook_repo: HandBookRepository = Provide[Container.handbook_repository]
        # handbook_repo: HandBookRepository = container.get(HandBookRepository)
    ):
        self.handbook_repo = handbook_repo

    async def get_user(self, id: int) -> User | None:
        users_rows = self.handbook_repo.get_rows("A", "C", 2)
        for row in users_rows:
            if int(row[self.user_id_col]) == id:
                return User(
                    id=id,
                    name=(row[self.user_name_col]),
                    is_active=SpreadsheetBool.yes == (row[self.user_active_col]),
                )
