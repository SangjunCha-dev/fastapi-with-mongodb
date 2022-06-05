from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional

from src.models.common import PyObjectId


class UserModel(BaseModel):
    user_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=2, max_length=20)
    email: EmailStr = Field(...)
    age: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "tester1",
                "email": "tester@example.com",
                "age": 22,
            }
        }

class UpdateUserModel(BaseModel):
    name: Optional[str]
    age: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "tester2",
                "email": "tester2@example.com",
                "age": 33,
            }
        }
