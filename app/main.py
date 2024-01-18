import shutil
from fastapi import FastAPI, File, Form, HTTPException, Path, UploadFile
from routers import users_router, export_router, image_router
import uvicorn

app = FastAPI(title="Test Task", version="0.0.1", debug=True)

app.include_router(users_router)
app.include_router(export_router)
app.include_router(image_router)


@app.post("/photos", status_code=201)
async def create_upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


# REDIS
# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
