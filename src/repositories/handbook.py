from src.core.sheet_configs import UsersConfigs
from src.core.settings import SpreadsheetBool
from src.schemas.user import User

from .base_gs_repository import BaseGSRepository


class HandBookGSRepository(BaseGSRepository):
    user_id_col = 0
    user_name_col = 1
    user_active_col = 2

    async def get_users(self) -> list[User]:
        users_rows = self.get_rows(
            UsersConfigs.START_COL,
            UsersConfigs.END_COL,
            UsersConfigs.START_ROW,
        )
        users = [
            User(
                id=int(row[self.user_id_col]),
                name=(row[self.user_name_col]),
                is_active=SpreadsheetBool.yes == (row[self.user_active_col]),
            )
            for row in users_rows
        ]
        return users
