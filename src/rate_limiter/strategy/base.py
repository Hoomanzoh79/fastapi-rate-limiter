from typing import Protocol

from src.rate_limiter.models import RateLimitResult

class RateLimitStrategy(Protocol):

    async def check(self, key: str) -> RateLimitResult:
        ...
