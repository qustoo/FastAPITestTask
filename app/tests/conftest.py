import asyncio
from app.config import settings
import pytest
from httpx import AsyncClient
from main import app as fastapi_app
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@pytest.fixture(scope="function", autouse=True)
async def async_client():
    """Return instance of async client and yield it"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        yield async_client


# Taken from pytest-asyncio doc
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def create_cache():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST:}", encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="test_task_cache")
