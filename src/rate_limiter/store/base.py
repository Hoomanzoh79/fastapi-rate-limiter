from abc import ABC,abstractmethod

class RateLimitStore(ABC):

    @abstractmethod
    async def incr(self, key: str, expire: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: int, expire: int):
        raise NotImplementedError

    @abstractmethod
    async def zadd(self, key: str, score: float, member: str):
        raise NotImplementedError

    @abstractmethod
    async def zremrangebyscore(self, key: str, min_score: float, max_score: float):
        raise NotImplementedError

    @abstractmethod
    async def zcard(self, key: str) -> int:
        raise NotImplementedError
