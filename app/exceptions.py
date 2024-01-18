from typing import Any, Dict, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.exceptions import HTTPException


class ItemNotFoundException(HTTPException):
    def __init__(
        self,
        status_code: int = 404,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class FileNotFoundException(ItemNotFoundException):
    def __init__(
        self,
        status_code: int = 404,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        detail = "Searching file not found"
        super().__init__(status_code, detail, headers)


class UserNotFoundException(ItemNotFoundException):
    def __init__(
        self,
        status_code: int = 404,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        detail = "Searching user not found"
        super().__init__(status_code, detail, headers)


class InvalidBsonIDException(HTTPException):
    def __init__(
        self,
        status_code: int = 422,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        detail = "Incorrect input id"
        super().__init__(status_code, detail, headers)


def ValidateBsonID(id: str):
    try:
        bson_id = ObjectId(id)
    except (InvalidId, TypeError):
        raise InvalidBsonIDException()
    return bson_id
