import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.config import settings
from app.dao import MongoImagesDAO

if settings.DB_TYPE == "LOCAL":
    DATABASE_URL = settings.LOCAL_DATABASE_URL
else:
    DATABASE_URL = settings.REMOTE_DATABASE_URL


client = AsyncIOMotorClient(DATABASE_URL)
client.get_io_loop = asyncio.get_event_loop
db = client[settings.DB_BOX]
collection = db.get_collection(settings.DB_COLLECTION)
image_collection = db.get_collection("Images")
image_information_collect = db.get_collection("fs.files")
fs = AsyncIOMotorGridFSBucket(db)
fs.get_io_loop = asyncio.get_event_loop


async def get_mongo_database():
    return MongoImagesDAO(collection, image_collection, image_information_collect, fs)
