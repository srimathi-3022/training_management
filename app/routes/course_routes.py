from fastapi import APIRouter, HTTPException
from app import database
from app.models.course_model import Course

router = APIRouter()

def clean(doc):
    doc.pop("_id", None)
    return doc


@router.post("/courses/")
async def adding_new_course_in_the_institude(course: Course):

    global_id = database.course_id_counter
    database.course_id_counter += 1

    new_course = {
        "course_id": global_id,
        "course_name": course.course_name,
        "trainer_name": course.trainer_name,
        "course_duration": course.course_duration,
        "topics": course.topics
    }
    database.course.insert_one(new_course)
    return {
        "message": "Course added to the institution database successfully",
        "course": clean(new_course)  
    }


@router.get("/courses/{course_id}")
async def get_course_by_using_course_id(course_id: int):
    course = database.course.find_one({"course_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found in the institution database please check the ID and try again.")
    return clean(course)