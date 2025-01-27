from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from src.core.redis import redis_client

storage = RedisStorage(redis_client, key_builder=DefaultKeyBuilder(with_destiny=True))
