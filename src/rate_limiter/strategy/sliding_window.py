import time

from .base import RateLimitStrategy
from src.rate_limiter.models import RateLimitResult
from src.rate_limiter.store.base import RateLimitStore

class SlidingWindowStrategy(RateLimitStrategy):

    def __init__(self, store:RateLimitStore, limit: int, window: int):
        self.store = store
        self.limit = limit
        self.window = window

    async def check(self, key: str) -> RateLimitResult:
        now = time.time()
        window_start = now - self.window
        redis_key = f"rate:{key}"
        
        await self.store.zremrangebyscore(redis_key, 0, window_start)
        count = await self.store.zcard(redis_key)

        if count >= self.limit:
            return RateLimitResult(False, 0, self.window)

        await self.store.zadd(redis_key, now, str(now))

        remaining = self.limit - (count + 1)

        return RateLimitResult(True, remaining, self.window)
