import datetime
import json
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from pydantic.functional_validators import BeforeValidator
from schemas.images import ImageModel
from typing_extensions import Annotated

from .sorts import SortValues

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=2)
    surname: str = Field(..., min_length=3)
    age: int = Field(default=18, ge=18)
    birthdate: datetime.datetime = Field(...)
    vote_value: int = Field(default=0, ge=0, le=10)

    # Для перевода объекта в тело body для передачи по json вместе с файлом при пост запросе
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserWithImage(UserModel):
    image: Optional[ImageModel] = None


class UserOutputModel(UserWithImage):
    # Для моделей, в который счетчик превысил значения 10
    vote_value: int


class UserCollection(BaseModel):
    users: Optional[List[UserOutputModel]] = None  # List[UserWithImage]


class UserUpdateModel(BaseModel):
    name: str = Field(..., min_length=2)
    surname: str = Field(..., min_length=3)
    age: int = Field(default=18, ge=18)
    birthdate: datetime.datetime = Field(...)
    vote_value: int = Field(default=0, ge=0, le=10)


class UserPartialUpdateModel(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    surname: Optional[str] = Field(None, min_length=3)
    age: Optional[int] = Field(None, ge=18)
    birthdate: Optional[datetime.datetime] = Field(None)
    vote_value: Optional[int] = Field(None, ge=0, le=10)


class SortUserModel(BaseModel):
    name: Optional[SortValues] = None
    surname: Optional[SortValues] = None
    age: Optional[SortValues] = None
    birthdate: Optional[SortValues] = None
