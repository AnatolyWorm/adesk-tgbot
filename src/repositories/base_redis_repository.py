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

    # def key_builder(self, keys: list[str]) -> str | None:
    #     return self.separator.join([str(k) for k in keys])

    # async def get_data(self, key: list[str]) -> dict | None:
    #     data = await self.redis_client.get(self.key_builder(key))
    #     return json.loads(data) if data else None

    # async def set_data(self, key: list[str], data: dict) -> bool:
    #     return await self.redis_client.set(
    #         self.key_builder(key),
    #         json.dumps(data),
    #         ex=self.expire_seconds,
    #     )

    def convert_to_model(self, data: dict, model: Any) -> Any:
        return self.retort.load(data, model)

    def convert_to_dict(self, model: Any) -> dict:
        return self.retort.dump(model)

    async def save_models_by_hash(
        self,
        hash_name: str,
        data: dict[str, Any],
    ) -> bool:
        try:
            for key, model in data.items():
                await self.redis_client.hset(
                    hash_name,
                    key,
                    json.dumps(self.convert_to_dict(model)),
                )
            await self.redis_client.expire(
                name=hash_name, time=self.expire_seconds
            )
            return True
        except Exception as exc:
            logger.error(exc)
            return False

    async def get_model_by_key_from_hash(
        self,
        hash_name: str,
        key: str,
        model: Any,
    ) -> Any | None:
        data = await self.redis_client.hget(hash_name, key)
        if data:
            return self.convert_to_model(
                json.loads(data),
                model,
            )

    async def save_list(
        self,
        list_name: str,
        data_list: list[str],
    ) -> int:
        await self.redis_client.delete(list_name)
        qty_saved = await self.redis_client.rpush(
            list_name, *[json.dumps(data) for data in data_list]
        )
        return qty_saved

    async def get_list(
        self,
        list_name: str,
    ) -> list[str]:
        data_json = await self.redis_client.lrange(list_name, 0, -1)
        return [json.loads(el) for el in data_json]
