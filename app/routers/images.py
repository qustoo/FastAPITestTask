from bson import ObjectId
from fastapi import APIRouter, Depends, Path
from exceptions import FileNotFoundException
from exceptions import ValidateBsonID
from dao.grid_fs_mongo_dao import MongoImagesDAO
from schemas.images import ImageModel
from database import get_mongo_database
from fastapi.responses import StreamingResponse
from database import fs

router = APIRouter(prefix="/files", tags=["Images"])


@router.get("/information/{file_id}", response_model=ImageModel)
async def get_file_information(
    database: MongoImagesDAO = Depends(get_mongo_database), file_id: str = Path(...)
):
    file_id = ValidateBsonID(file_id)
    file = await database.get_file_information(file_id)
    if file:
        return file
    raise FileNotFoundException()


@router.get("/download_file/{file_id}")
async def download_file(
    database: MongoImagesDAO = Depends(get_mongo_database), file_id: str = Path(...)
):
    file_id = ValidateBsonID(file_id)
    file = await database.get_file_object(file_id)
    if file:
        return StreamingResponse(
            database.download_stream(file_id), media_type="image/png"
        )
    else:
        raise FileNotFoundException()
