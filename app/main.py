# import uvicorn
# from fastapi import FastAPI
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
#
#
# from routers import export_router
# from app.routers import export_router, image_router, users_router
#
# app = FastAPI(title="Test Task", version="0.0.1", debug=True)
#
# app.include_router(users_router)
# app.include_router(export_router)
# app.include_router(image_router)
#

def recursive_sum(my_list: list, total_sum=0) -> int:
    if not my_list:
        return 0
    for item in my_list:
        if type(item) == list:
            total_sum += recursive_sum(item, 0)
        elif type(item) == int:
            total_sum += item
    return total_sum
if __name__ == "__main__":
    my_list = [1, [4, 4,[10]]]
    print(recursive_sum(my_list))
    # uvicorn.run("main:app", reload=True)
