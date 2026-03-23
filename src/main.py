from fastapi import FastAPI, status
from fastapi_swagger import patch_fastapi
from contextlib import asynccontextmanager

from src.rate_limiter.store.redis import RedisStore, create_redis_client
from src.rate_limiter.strategy.sliding_window import SlidingWindowStrategy
from src.rate_limiter.strategy.token_bucket import TokenBucketStrategy
from src.rate_limiter.limiter import RateLimiter
from src.rate_limiter.middleware import RateLimitMiddleware
from src.rate_limiter.key_generator import ip_key

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await create_redis_client()
    store = RedisStore(redis)
    strategy = TokenBucketStrategy(
        store,
        capacity=10,
        refill_rate=1
    )
    limiter = RateLimiter(strategy, ip_key)
    app.state.limiter = limiter
    app.state.redis = redis
    yield
    await redis.close()

app = FastAPI(
    title="FastAPI Rate limiter",
    description="Custom Rate Limiter using strategy pattern & Redis",
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
    lifespan=lifespan
)
patch_fastapi(app, docs_url="/docs")
app.add_middleware(RateLimitMiddleware)

@app.get("/limited")
async def limited_endpoint():
    return {
        "message": "limited endpoint",
        "status_code": status.HTTP_200_OK
    }
