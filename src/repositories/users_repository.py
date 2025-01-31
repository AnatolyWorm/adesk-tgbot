import json
import logging

from src.schemas.user import User
from .base_redis_repository import BaseRedisRepository


logger = logging.getLogger(__name__)


class UsersRedisRepository(BaseRedisRepository):
    _hash_name = "users"

    async def put_users_in_redis(self, user_models: list[User]):
        for model in user_models:
            await self.redis_client.hset(
                self._hash_name,
                str(model.id),
                json.dumps(self.convert_to_dict(model)),
            )
        await self.redis_client.expire(
            name=self._hash_name, time=self.expire_seconds
        )

    async def get_user_from_redis(self, id: int) -> User | None:
        data = await self.redis_client.hget(self._hash_name, str(id))
        if data:
            return self.convert_to_model(
                json.loads(data),
                User,
            )
