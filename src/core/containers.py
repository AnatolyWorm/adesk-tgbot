from adaptix import Retort
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dependency_injector import containers, providers

from src.core.redis import RedisClient
from src.core.settings import settings

from repositories.base_gs_repository import BaseGSRepository
from repositories.base_redis_repository import BaseRedisRepository
from repositories.repository import Repository

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

    adaptix_retort = providers.Singleton(Retort)

    base_redis_repository = providers.Singleton(
        BaseRedisRepository,
        redis_client=redis,
        retort=adaptix_retort,
    )

    base_gs_repository = providers.Singleton(
        BaseGSRepository,
        creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
        sheet_id=settings.GOOGLE_SPREADSHEET_ID,
    )

    repository = providers.Singleton(
        Repository,
        retort=adaptix_retort,
        google_repo=base_gs_repository,
        redis_repo=base_redis_repository,
    )


container = Container()
