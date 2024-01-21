import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.config import settings
from app.routers import export_router, image_router, users_router

app = FastAPI(title="Test Task", version="0.0.1", debug=True)

app.include_router(users_router)
app.include_router(export_router)
app.include_router(image_router)


# REDIS
@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST:}", encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="test_task_cache")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
