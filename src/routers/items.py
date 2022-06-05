from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, ORJSONResponse
from fastapi.encoders import jsonable_encoder

from src.config.settings import db
from src.models.items import ItemModel, UpdateItemModel


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

item_collection = db.get_collection("items")


@router.get("/", response_description="List Items", response_model=list[ItemModel])
async def list_items():
    items = await item_collection.find().to_list(10)
    return items


@router.post("/", response_description="Add New Items", response_model=ItemModel)
async def create_item(item: ItemModel = Body(..., embed=True)):
    item = jsonable_encoder(item)
    new_item = await item_collection.insert_one(item)
    created_item = await item_collection.find_one({"_id": new_item.inserted_id})
    return ORJSONResponse(status_code=status.HTTP_201_CREATED, content=created_item)


@router.get("/{item_id}", response_description="Get Item", response_model=ItemModel)
async def retrieve_item(item_id: str):
    if (item := await item_collection.find_one({"_id": item_id})) is not None:
        return item

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.put("/{item_id}", response_description="Update Item", response_model=ItemModel)
async def update_item(item_id: str, item: UpdateItemModel = Body(...)):
    item = {k: v for k, v in item.dict().items() if v is not None}

    if 1 <= len(item):
        updated_item = await item_collection.update_one({"_id": item_id}, {"$set": item})

        if (updated_item.modified_count == 1):
            if (updated_item := await item_collection.find_one({"_id": item_id})) is not None:
                return updated_item

    if (exist_item := await item_collection.find_one({"_id": item_id})) is not None:
        return exist_item

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.delete("/{item_id}", response_description="Delete Item")
async def delete_item(item_id: str):
    delete_result = await item_collection.delete_one({"_id": item_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
