from fastapi import APIRouter, HTTPException, Query
from app import database
from app.models.trainee_model import Trainee

router = APIRouter()

def clean(doc):
    doc.pop("_id", None)
    return doc


@router.post("/trainees/")
async def adding_new_trainee_in_the_institude(trainee: Trainee):

    for existing in database.trainee.find():
        if existing["trainee_email"] == trainee.trainee_email:
            raise HTTPException(status_code=400, detail="Email already registered in this institution.")

    global_id = database.trainee_id_counter
    database.trainee_id_counter += 1
    new_trainee = {
        "trainee_id": global_id,
        "trainee_name": trainee.trainee_name,
        "trainee_age": trainee.trainee_age,
        "trainee_email": trainee.trainee_email,
        "trainee_phone": trainee.trainee_phone,
        "city": trainee.city,
        "skills": trainee.skills
    }
    database.trainee.insert_one(new_trainee)

    return {
        "message": "Trainee added to the institution database successfully",
        "trainee": clean(new_trainee)   # FIX: strip _id before returning
    }


@router.get("/trainees/{trainee_id}")
async def get_trainee_by_using_trainee_id(trainee_id: int):
    trainee = database.trainee.find_one({"trainee_id": trainee_id})
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found in the institution database please check the ID and try again.")
    return trainee   # FIX: strip _id before returning


# FIX: renamed path param to avoid clash with /{trainee_id} above
@router.get("/trainees/city/{city}")
async def get_trainees_by_using_the_registered_city(city: str):
    trainees_in_city = []
    for trainee in database.trainee.find():
        if trainee["city"].lower() == city.lower():
            trainees_in_city.append(clean(trainee))   # FIX: strip _id

    if not trainees_in_city:
        raise HTTPException(status_code=404, detail="No trainees found in the specified city.")
    return trainees_in_city