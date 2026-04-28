import time

from .base import RateLimitStrategy
from src.rate_limiter.models import RateLimitResult
from src.rate_limiter.store.base import RateLimitStore

class FixedWindowStrategy(RateLimitStrategy):

    def __init__(self, store:RateLimitStore, limit: int, window: int):
        self.store = store
        self.limit = limit
        self.window = window

    async def check(self, key: str):
        window_id = int(time.time()) // self.window
        redis_key = f"rate:{key}:{window_id}"

        count = await self.store.incr(redis_key, self.window)

        if count > self.limit:
            return RateLimitResult(False, 0, self.window)

        remaining = self.limit - count

        return RateLimitResult(True, remaining, self.window)
