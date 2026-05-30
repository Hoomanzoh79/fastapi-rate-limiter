# FastAPI Rate Limiter

A customizable and extensible rate limiting solution built with FastAPI and Redis. The project implements multiple rate limiting algorithms using the Strategy Pattern and provides a pluggable storage layer through Abstract Base Classes (ABC), allowing Redis to be replaced with any compatible backend with minimal changes.

## Features

- Multiple rate limiting algorithms:
  - Fixed Window
  - Sliding Window
  - Token Bucket
- Strategy Pattern for algorithm selection
- Pluggable storage layer using Python ABCs
- Redis-backed implementation
- FastAPI middleware integration
- IP-based request limiting
- Asynchronous implementation using `redis.asyncio`
- Easily extendable with custom strategies and storage providers

## Technologies
<div >
	<img src="https://skillicons.dev/icons?i=python"/>
	<img src="https://skillicons.dev/icons?i=fastapi"/>
	<img src="https://skillicons.dev/icons?i=redis"/>
	<img src="https://skillicons.dev/icons?i=docker"/>
</div>
  

## Architecture

The project is designed around two abstraction layers:

### Rate Limiting Strategies

All algorithms implement a common interface:

```python
class RateLimitStrategy(ABC):
    @abstractmethod
    async def check(self, key: str):
        pass
```

Current implementations:

- `FixedWindowStrategy`
- `SlidingWindowStrategy`
- `TokenBucketStrategy`

This allows switching algorithms without changing application code.

### Storage Layer

The storage layer is abstracted through the `RateLimitStore` interface:

```python
class RateLimitStore(ABC):
    async def incr(...)
    async def get(...)
    async def set(...)
    async def zadd(...)
    async def zremrangebyscore(...)
    async def zcard(...)
```

Current implementation:

- `RedisStore`

Additional backends (Memcached, DynamoDB, MongoDB, etc.) can be added by implementing the same interface.

## Supported Algorithms

### Fixed Window

Uses a counter within a fixed time window.

Example:

- Limit: 10 requests
- Window: 60 seconds

Once the counter exceeds the limit, requests are rejected until the next window begins.

### Sliding Window

Stores request timestamps in a Redis sorted set.

Advantages:

- More accurate limiting
- Prevents bursts at window boundaries

### Token Bucket

Maintains a bucket of tokens that refill over time.

Advantages:

- Smooth request distribution
- Supports burst traffic
- Commonly used in production systems

## Configuration Example

```python
strategy = TokenBucketStrategy(
    store=store,
    capacity=10,
    refill_rate=1
)
```

Meaning:

- Bucket capacity: 10 tokens
- Refill rate: 1 token/second

## Usage

### Create Redis Store

```python
redis = await create_redis_client()
store = RedisStore(redis)
```

### Select a Strategy

```python
strategy = TokenBucketStrategy(
    store=store,
    capacity=10,
    refill_rate=1
)
```

### Create Rate Limiter

```python
limiter = RateLimiter(
    strategy=strategy,
    key_func=ip_key
)
```

### Register Middleware

```python
app.add_middleware(RateLimitMiddleware)
```

## Rate Limiting Key

By default, requests are limited based on:

```python
client_ip + request_path
```

Example:

```text
192.168.1.10:/limited
```

Custom key generators can easily be implemented.

## Example Response

When the limit is exceeded:

```json
{
  "detail": "Rate limit exceeded"
}
```

Response Status:

```http
429 Too Many Requests
```

## Running the Project

### Clone the Repository

```bash
git clone https://github.com/Hoomanzoh79/fastapi-rate-limiter.git
cd fastapi-rate-limiter
```

### Configure Environment Variables

Create a `.env` file and provide the required Redis configuration:

```env
REDIS_URL=redis://redis:6379/0
RATE_LIMIT_REQUESTS=60 (configure as needed)
RATE_LIMIT_WINDOW_SECONDS=60  (configure as needed)
```

### Start the Application

```bash
docker-compose up -d
```

This will start:

* FastAPI application
* Redis instance

### Verify Containers

```bash
docker ps
```

### Access the API

Swagger UI:

```text
http://localhost:8000/docs
```

Example endpoint:

```http
GET /limited
```

### Stop the Application

```bash
docker-compose down
```


## Extending the Project

### Add a New Strategy

```python
class LeakyBucketStrategy(RateLimitStrategy):
    async def check(self, key: str):
        ...
```

### Add a New Storage Backend

```python
class MongoStore(RateLimitStore):
    ...
```

No changes are required in the middleware or application layer.


