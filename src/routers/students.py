from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, ORJSONResponse
from fastapi.encoders import jsonable_encoder

from ..config.settings import db
from ..models.students import StudentModel, UpdateStudentModel

router = APIRouter(
    prefix="/students",
    tags=["students"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)

student_collection = db.get_collection("students")

@router.post("/", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await student_collection.insert_one(student)
    created_student = await student_collection.find_one({"_id": new_student.inserted_id})
    return ORJSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@router.get("/", response_description="List all students", response_model=list[StudentModel])
async def list_students():
    students = await student_collection.find().to_list(1000)
    return students


@router.get("/{id}", response_description="Get a single student", response_model=StudentModel)
async def retrieve_student(id: str):
    if (student := await student_collection.find_one({"_id": id})) is not None:
        return student
    
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if 1 <= len(student):
        updated_student = await student_collection.update_one({"_id": id}, {"$set": student})

        if (updated_student.modified_count == 1):
            if (updated_student := await student_collection.find_one({"_id": id})) is not None:
                return updated_student

    if (existing_student := await student_collection.find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await student_collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")
