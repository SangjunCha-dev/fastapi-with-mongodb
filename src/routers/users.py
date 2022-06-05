from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, ORJSONResponse
from fastapi.encoders import jsonable_encoder

from src.config.settings import db
from src.models.users import UserModel, UpdateUserModel


router = APIRouter(
    prefix="/users",
    tags=['users'],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)

user_collection = db.get_collection("users")


@router.get("/", response_description="List Users", response_model=list[UserModel])
async def list_users():
    users = await user_collection.find().to_list(10)
    return users


@router.post("/", response_description="Add New User", response_model=UserModel)
async def create_user(user: UserModel = Body(..., embed=True)):
    user = jsonable_encoder(user)
    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return ORJSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get("/{user_id}", response_description="Get User", response_model=UserModel)
async def retrieve_user(user_id: str):
    if (user := await user_collection.find_one({"_id": user_id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.put("/{user_id}", response_description="Update User", response_model=UserModel)
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if 1 <= len(user):
        updated_user = await user_collection.update_one({"_id": user_id}, {"$set": user})

        if (updated_user.modified_count == 1):
            if (updated_user := await user_collection.find_one({"_id": user_id})) is not None:
                return updated_user

    if (exist_user := await user_collection.find_one({"_id": user_id})) is not None:
        return exist_user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.delete("/{user_id}", response_description="Delete user")
async def delete_user(user_id: str):
    delete_result = await user_collection.delete_one({"_id": user_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")
