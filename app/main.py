from fastapi import FastAPI
from routers import users_router, export_router, image_router
import uvicorn

app = FastAPI(title="Test Task", version="0.0.1", debug=True)

app.include_router(users_router)
app.include_router(export_router)
app.include_router(image_router)


# REDIS
# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
