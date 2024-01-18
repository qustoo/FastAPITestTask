from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from utils import DataWriter
from dao import MongoDAO

router = APIRouter(prefix="/export")


@router.get("/")
async def export_data(filename: str = "data.xlsx"):
    data = await MongoDAO.get_data()
    columns = await MongoDAO.get_columns()
    try:
        with DataWriter(columns, filename) as dw:
            dw.write_columns()
            dw.write_values(data)
    except Exception as err:
        return HTTPException(status_code=400, detail=str(err))
