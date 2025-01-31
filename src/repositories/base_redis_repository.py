import json
import logging
from typing import Any
from adaptix import Retort
from redis.asyncio.client import Redis


logger = logging.getLogger(__name__)


class BaseRedisRepository:

    def __init__(
        self,
        redis_client: Redis,
        retort: Retort,
        expire_seconds: int = 300,
        lock_exp_seconds: int = 60,
        separator: str = ':',
    ):
        self.redis_client = redis_client
        self.retort = retort
        self.separator = separator
        self.expire_seconds = expire_seconds
        self.lock_exp_seconds = lock_exp_seconds

    def key_builder(self, keys: list[str]) -> str | None:
        return self.separator.join([str(k) for k in keys])

    def convert_to_model(self, data: dict, model: Any) -> Any:
        return self.retort.load(data, model)

    def convert_to_dict(self, model: Any) -> dict:
        return self.retort.dump(model)

    async def get_data(self, key: list[str]) -> dict | None:
        data = await self.redis_client.get(self.key_builder(key))
        return json.loads(data) if data else None

    async def set_data(self, key: list[str], data: dict) -> bool:
        return await self.redis_client.set(
            self.key_builder(key),
            json.dumps(data),
            ex=self.expire_seconds,
        )
