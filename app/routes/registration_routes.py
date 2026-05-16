from fastapi import APIRouter, HTTPException
from app import database
from app.models.registration_model import Registration

router = APIRouter()

def clean(doc):
    doc.pop("_id", None)
    return doc


@router.post("/registrations/")
async def adding_new_registration_in_the_institude(registration: Registration):

    # Check if the course exists
    course = database.course.find_one({"course_id": registration.course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found in the institution database please check the ID and try again.")

    # Check if the trainee exists
    trainee = database.trainee.find_one({"trainee_id": registration.trainee_id})
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found in the institution database please check the ID and try again.")

    # Check for duplicate registration
    existing_registration = database.registration.find_one(
        {"course_id": registration.course_id, "trainee_id": registration.trainee_id}
    )
    if existing_registration:
        raise HTTPException(status_code=400, detail="Trainee is already registered for this course. No need to register again.")

    global_id = database.registration_id_counter
    database.registration_id_counter += 1
    new_registration = {
        "registration_id": global_id,
        "course_id": registration.course_id,
        "trainee_id": registration.trainee_id,
        "registration_date": registration.registration_date.isoformat()  # FIX: make datetime JSON-safe
    }

    database.registration.insert_one(new_registration)
    return {
        "message": "Registration added to the institution database successfully",
        "registration": clean(new_registration)   # FIX: strip _id before returning
    }