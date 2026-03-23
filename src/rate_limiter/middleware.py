from fastapi.responses import JSONResponse
from fastapi import status

from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        limiter = request.app.state.limiter
        result = await limiter.check(request)
        if not result.allowed:
            return JSONResponse(
                {"detail": "Rate limit exceeded"},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )
        response = await call_next(request)
        return response
