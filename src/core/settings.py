from enum import StrEnum
from pydantic_settings import BaseSettings

from src.core.sheet_configs import SheetNames


class DatesSettings(StrEnum):
    date_format = "%d.%m.%Y"
    time_format = "%H:%M"
    datetime_format = "%d.%m.%Y %H:%M:%S"


class SpreadsheetBool(StrEnum):
    yes = 'Да'
    no = 'Нет'


class LoggerSettings(BaseSettings):
    LEVEL: str = 'INFO'


class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    NOTIFY_CHANNEL_ID: str

    LOGGER: LoggerSettings = LoggerSettings()

    REDIS: str = 'redis://redis:6379/1'

    GOOGLE_SPREADSHEET_ID: str
    GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH: str
    GOOGLE_SPREADSHEET_NAMES: SheetNames = SheetNames()


settings = Settings()
