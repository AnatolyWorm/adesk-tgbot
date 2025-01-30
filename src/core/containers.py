from dishka import provide, Scope, Provider, make_container
from redis.asyncio.client import Redis
from adaptix import Retort
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dependency_injector import containers, providers

from src.core.google_sheets_api import GoogleSheetsApiService
from src.core.redis_service import RedisService
from src.core.redis import RedisClient
from src.core.settings import SheetNames, Settings, settings

from repositories.handbook import HandBookRepository
from repositories.base_gs_repository import BaseGSRepository
from repositories.base_redis_repository import BaseRedisRepository

import logging
logger = logging.getLogger(__name__)

# class Container(Provider):

#     @provide(scope=Scope.APP)
#     def get_google_sheet(self) -> GoogleSheetsApiService:
#         return GoogleSheetsApiService(
#             creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
#             sheet_id=settings.GOOGLE_SPREADSHEET_ID,
#         )

#     @provide(scope=Scope.REQUEST, provides=GoogleSheetsApiService)
#     def get_handbook_repo(self) -> HandBookRepository:
#         return HandBookRepository(
#             spread_sheet_name=settings.GOOGLE_SPREADSHEET_NAMES.handbook,
#             workbook=google_sheets_api_service,
#         )


# container = make_container(Container())


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

    redis_repository = providers.Factory(
        BaseRedisRepository,
        redis_client=redis,
        retort=adaptix_retort,
    )

    google_api_service = providers.Singleton(
        GoogleSheetsApiService,
        creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
        sheet_id=settings.GOOGLE_SPREADSHEET_ID,
    )

    handbook_repository = providers.Factory(
        HandBookRepository,
        spread_sheet_name=settings.GOOGLE_SPREADSHEET_NAMES.handbook,
        workbook=google_api_service,
    )


container = Container()
