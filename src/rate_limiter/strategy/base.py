from abc import ABC,abstractmethod

from src.rate_limiter.models import RateLimitResult

class RateLimitStrategy(ABC):

    @abstractmethod
    async def check(self, key: str) -> RateLimitResult:
        raise NotImplementedError
