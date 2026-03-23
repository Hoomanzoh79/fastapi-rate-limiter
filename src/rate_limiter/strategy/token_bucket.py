import time

from src.rate_limiter.models import RateLimitResult
from src.rate_limiter.store.base import RateLimitStore

class TokenBucketStrategy:

    def __init__(self, store:RateLimitStore, capacity: int, refill_rate: float):
        self.store = store
        self.capacity = capacity
        self.refill_rate = refill_rate

    async def check(self, key: str):
        redis_key = f"bucket:{key}"
        data = await self.store.get(redis_key)
        now = time.time()
        
        if not data:
            tokens = self.capacity
            last = now
        else:
            tokens, last = map(float, data.split(":"))
            tokens = min(
                self.capacity,
                tokens + (now - last) * self.refill_rate
            )

        if tokens < 1:
            await self.store.set(redis_key, f"{tokens}:{now}", 3600)
            return RateLimitResult(False, 0, 1)

        tokens -= 1

        await self.store.set(redis_key, f"{tokens}:{now}", 3600)

        return RateLimitResult(True, int(tokens), 1)
