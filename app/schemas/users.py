from datetime import date
import datetime
from pydantic import BaseModel, model_validator
import json
from pydantic import ConfigDict, BaseModel, Field, EmailStr, field_validator, validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from typing import Optional, List
from schemas.images import ImageModel
from pydantic import BaseModel

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=2)
    surname: str = Field(..., min_length=3)
    age: int = Field(..., ge=18)
    birthdate: datetime.datetime = Field(...)

    # Для перевода объекта в тело body для передачи по json вместе с файлом при пост запросе
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserWithImage(UserModel):
    image: Optional[ImageModel]


class UserCollection(BaseModel):
    users: List[UserWithImage]


class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    birthdate: Optional[date] = None
