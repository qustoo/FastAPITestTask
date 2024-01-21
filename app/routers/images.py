from bson import ObjectId
from dao.grid_fs_mongo_dao import MongoImagesDAO
from database import get_mongo_database
from dependecies import validate_file_id
from exceptions import FileNotFoundException
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from schemas.images import ImageModel

router = APIRouter(prefix="/files", tags=["Images"])


@router.get("/information/{file_id}", response_model=ImageModel)
async def get_file_information(
    database: MongoImagesDAO = Depends(get_mongo_database),
    file_id: ObjectId = Depends(validate_file_id),
):
    if file := await database.get_file_information(file_id):
        return file
    raise FileNotFoundException()


@router.get("/download_file/{file_id}")
async def download_file(
    database: MongoImagesDAO = Depends(get_mongo_database),
    file_id: ObjectId = Depends(validate_file_id),
):
    if file := await database.get_file_object(file_id):
        return StreamingResponse(
            database.download_stream(file_id), media_type="image/png"
        )
    else:
        raise FileNotFoundException()
