from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

import os
from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
config_path = 'config/settings.json'
config_file = os.path.join(PROJECT_ROOT, config_path)
config = json.loads(open(config_file).read())
for key, value in config.items():
    setattr(sys.modules[__name__], key, value)


app = FastAPI()
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client.college

from fastapi import Body, HTTPException, status
from fastapi.responses import Response, ORJSONResponse
from fastapi.encoders import jsonable_encoder

from app import app, db
from models import StudentModel, UpdateStudentModel


@app.post("/", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await db["students"].insert_one(student)
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return ORJSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@app.get("/", response_description="List all students", response_model=list[StudentModel])
async def list_students():
    students = await db["students"].find().to_list(1000)
    return students


@app.get("/{id}", response_description="Get a single student", response_model=StudentModel)
async def show_student(id: str):
    if (student := await db["students"].find_one({"_id": id})) is not None:
        return student
    
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if 1 <= len(student):
        updated_student = await db["students"].update_one({"_id": id}, {"$set": student})

        if (updated_student.modified_count == 1):
            if (updated_student := await db["students"].find_one({"_id": id})) is not None:
                return updated_student

    if (existing_student := await db["students"].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await db["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")
