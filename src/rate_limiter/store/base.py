from typing import Protocol

class RateLimitStore(Protocol):

    async def incr(self, key: str, expire: int) -> int:
        ...

    async def get(self, key: str):
        ...

    async def set(self, key: str, value: int, expire: int):
        ...

    async def zadd(self, key: str, score: float, member: str):
        ...

    async def zremrangebyscore(self, key: str, min_score: float, max_score: float):
        ...

    async def zcard(self, key: str) -> int:
        ...
