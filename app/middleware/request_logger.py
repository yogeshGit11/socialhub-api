import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        end = time.time() - start
        print(f"{request.method} {request.url.path} ---> {response.status_code} ({end:.3f}s)")
        return response