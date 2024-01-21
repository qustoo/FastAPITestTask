from fastapi import status
from fastapi.exceptions import HTTPException


class ItemNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundException(ItemNotFoundException):
    detail = "User not found"


class FileNotFoundException(ItemNotFoundException):
    detail = "File not found"


class InvalidBsonIDException(HTTPException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Incorrect input id"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectVoteValueException(HTTPException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "incorrect vote value(less then 0 or greaten then 10)"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
