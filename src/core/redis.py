from redis.asyncio.client import Redis

from src.core.settings import settings

redis_client = Redis.from_url(settings.REDIS)
