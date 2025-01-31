from pydantic_settings import BaseSettings


class SheetNames(BaseSettings):
    handbook: str = "Справочник"


class UsersConfigs:
    START_COL: str = "A"
    END_COL: str = "C"
    START_ROW: str = 2
