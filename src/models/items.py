from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

from src.models.common import PyObjectId


class ItemModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(min_length=2, max_length=50)
    price: int = Field(...)
    quantity: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_typeds_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "bag",
                "price": 1000,
                "quantity": 10,
            }
        }

class UpdateItemModel(BaseModel):
    name: Optional[str]
    price: Optional[int]
    quantity: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "bag1",
                "price": 2000,
                "quantity": 5,
            }
        }
