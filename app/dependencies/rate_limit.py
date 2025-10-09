import redis.asyncio as redis
from fastapi import Depends, HTTPException
from app.core.config import settings
from app.schemas import user as user_schema
from app.dependencies.user_deps import get_current_user

LOGIN_REDIS_PREFIX = settings.LOGIN_REDIS_PREFIX
LOGIN_TIME_WINDOW = settings.LOGIN_TIME_WINDOW
LOGIN_ATTEMPTS_LIMIT = settings.LOGIN_ATTEMPTS_LIMIT


async def get_redis():
    rds = redis.Redis.from_url(settings.REDIS_URL)
    return rds

# login Attempts limiting for Users
async def limit_login_attempts(
    redis=Depends(get_redis),
    payload: user_schema.UserLogin = None
):

    user_email = payload.email
    redis_key = f"{LOGIN_REDIS_PREFIX}{user_email}"
    attempts = await redis.incr(redis_key)

    # Set expiration only on the first attempt
    if attempts == 1:
        await redis.expire(redis_key, LOGIN_TIME_WINDOW)

    if attempts > LOGIN_ATTEMPTS_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please try again later."
        )
    return True

# prfile download rate limiting
async def limit_profile_downloads(
    redis=Depends(get_redis),
    current_user=Depends(get_current_user)
):
    user_email = current_user.email
    redis_key = f"profile_downloads:{user_email}"
    downloads = await redis.incr(redis_key)

    if downloads == 1:
        await redis.expire(redis_key, 60)

    if downloads > 2:
        raise HTTPException(
            status_code=429,
            detail="Too many profile download requests. Please try again later."
        )
    return True