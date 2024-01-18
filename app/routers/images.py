from fastapi import APIRouter, Depends, Path
from exceptions import FileNotFoundException
from exceptions import ValidateBsonID
from dao.grid_fs_mongo_dao import MongoImagesDAO
from schemas.images import ImageModel
from database import collection, image_collection, fs, image_information_collect

router = APIRouter(prefix="/files")


async def get_mongo_database():
    return MongoImagesDAO(collection, image_collection, image_information_collect, fs)


@router.get("/information/{file_id}", response_model=ImageModel)
async def get_info(
    database: MongoImagesDAO = Depends(get_mongo_database), file_id: str = Path(...)
):
    file_id = ValidateBsonID(file_id)
    file = await database.get_information(file_id)
    if file:
        return file
    raise FileNotFoundException()
