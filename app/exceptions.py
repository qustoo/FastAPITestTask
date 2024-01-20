from bson import ObjectId
from bson.errors import InvalidId
from fastapi.exceptions import HTTPException
from fastapi import status


class ItemNotFoundException(HTTPException):
    status_code = 404
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundException(ItemNotFoundException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class FileNotFoundException(ItemNotFoundException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "File not found"


class InvalidBsonIDException(HTTPException):
    status_code: int = 422
    detail: str = "Incorrect input id"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectVoteValueException(HTTPException):
    status_code: int = (404,)
    detail: str = ("incorrect vote value(less then 0 or greaten then 10)",)

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


def ValidateBsonID(id: str):
    try:
        bson_id = ObjectId(id)
    except (InvalidId, TypeError):
        raise InvalidBsonIDException()
    return bson_id
