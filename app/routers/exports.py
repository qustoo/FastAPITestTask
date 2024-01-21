from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.dao import MongoImagesDAO
from app.database import get_mongo_database
from app.logger import logger
from app.utils import DataWriter

router = APIRouter(prefix="/export", tags=["Exports"])


@router.get("/")
async def export_data(
    database: MongoImagesDAO = Depends(get_mongo_database), filename: str = "data.xlsx"
):
    data = await database.get_data()
    columns = await database.get_columns()
    try:
        with DataWriter(columns, filename) as dw:
            dw.write_columns()
            dw.write_values(data)
    except Exception as err:
        logger.error("Cannot export data to xsls format", exc_info=str(err))
        return HTTPException(status_code=400, detail=str(err))
    return JSONResponse("data.xsls was created")
