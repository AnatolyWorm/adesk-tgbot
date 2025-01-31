from adaptix import Retort
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dependency_injector import containers, providers

from src.core.google_sheets_api import GoogleSheetsApiService
from src.core.redis import RedisClient
from src.core.settings import settings

from repositories.handbook import HandBookGSRepository
from src.repositories.users_repository import UsersRedisRepository

import logging
logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    redis = providers.Singleton(
        RedisClient,
        redis_url=settings.REDIS,
    )

    storage = providers.Singleton(
        RedisStorage,
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    adaptix_retort = providers.Factory(Retort)

    users_repository = providers.Factory(
        UsersRedisRepository,
        redis_client=redis,
        retort=adaptix_retort,
    )

    google_api_service = providers.Singleton(
        GoogleSheetsApiService,
        creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
        sheet_id=settings.GOOGLE_SPREADSHEET_ID,
    )

    handbook_repository = providers.Factory(
        HandBookGSRepository,
        spread_sheet_name=settings.GOOGLE_SPREADSHEET_NAMES.handbook,
        workbook=google_api_service,
    )


container = Container()
