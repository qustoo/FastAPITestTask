from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class ImageModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    filename: str
    length: int
    uploadDate: datetime
