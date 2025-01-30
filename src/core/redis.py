from redis.asyncio.client import Redis


class RedisClient:
    def __new__(
        cls,
        redis_url: str,
    ):
        return Redis.from_url(redis_url)
