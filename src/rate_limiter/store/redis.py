import redis.asyncio as aioredis

from .base import RateLimitStore
from src.setttings import settings

class RedisStore(RateLimitStore):

    def __init__(self, redis):
        self.redis = redis

    async def incr(self, key: str, expire: int) -> int:
        value = await self.redis.incr(key)
        if value == 1:
            await self.redis.expire(key, expire)
        return value

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: int, expire: int):
        await self.redis.set(key, value, ex=expire)

    async def zadd(self, key: str, score: float, member: str):
        await self.redis.zadd(key, {member: score})

    async def zremrangebyscore(self, key: str, min_score: float, max_score: float):
        await self.redis.zremrangebyscore(key, min_score, max_score)

    async def zcard(self, key: str):
        return await self.redis.zcard(key)

async def create_redis_client():
    client = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
    return client
