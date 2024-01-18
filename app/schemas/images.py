from pydantic import BaseModel
from datetime import datetime
from pydantic.functional_validators import BeforeValidator
from pydantic import ConfigDict, BaseModel, Field
from typing_extensions import Annotated
from typing import Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]


class ImageModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    filename: str
    length: int
    uploadDate: datetime
