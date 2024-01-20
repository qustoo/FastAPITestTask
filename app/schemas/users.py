import datetime
from pydantic import BaseModel, model_validator
import json
from .sorts import SortValues
from pydantic import BaseModel, Field, EmailStr, field_validator, validator
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
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    birthdate: Optional[datetime.datetime] = None
    vote_value: Optional[int] = None


class SortUserModel(BaseModel):
    name: Optional[SortValues] = None
    surname: Optional[SortValues] = None
    age: Optional[SortValues] = None
    birthdate: Optional[SortValues] = None
