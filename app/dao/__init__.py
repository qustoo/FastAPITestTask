from .mongo_dao import MongoDAO
from .base_dao import NoSQLDAO, NoSQLInterface
from .grid_fs_mongo_dao import MongoImagesDAO
from database import collection, image_collection, fs, image_information_collect


async def get_mongo_database():
    return MongoImagesDAO(collection, image_collection, image_information_collect, fs)
