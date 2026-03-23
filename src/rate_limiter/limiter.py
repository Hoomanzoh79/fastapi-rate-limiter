class RateLimiter:

    def __init__(self, strategy, key_func):
        self.strategy = strategy
        self.key_func = key_func

    async def check(self, request):
        key = self.key_func(request)
        return await self.strategy.check(key)
