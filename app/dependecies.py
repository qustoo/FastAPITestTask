from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Path
from typing_extensions import Annotated

from FastAPITestTask.app.exceptions import InvalidBsonIDException


async def validate_id(user_id: Annotated[str, Path()]):
    try:
        bson_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        raise InvalidBsonIDException()
    return bson_id


async def validate_file_id(file_id: Annotated[str, Path()]):
    try:
        bson_id = ObjectId(file_id)
    except (InvalidId, TypeError):
        raise InvalidBsonIDException()
    return bson_id
