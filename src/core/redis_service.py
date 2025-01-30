import json
import logging
from redis.asyncio.client import Redis

logger = logging.getLogger(__name__)


class RedisService:
    def __init__(
        self,
        redis_client: Redis,
        handbook_exp_seconds: int = 300,
        lock_exp_seconds: int = 60,
        separator: str = ':',
    ):
        self.redis = redis_client
        self.separator = separator
        self.handbook_exp_seconds = handbook_exp_seconds
        self.lock_exp_seconds = lock_exp_seconds
