from fastapi import APIRouter, HTTPException
from app import database
from app.models.attendance_model import MarkAttendance, AddScore

router = APIRouter()

def clean(doc):
    doc.pop("_id", None)
    return doc


def find_attendance(trainee_id: int, course_id: int):
    return database.attendance.find_one({"trainee_id": trainee_id, "course_id": course_id})


def check_registration(trainee_id: int, course_id: int):
    return database.registration.find_one(
        {"trainee_id": trainee_id, "course_id": course_id}
    ) is not None


def calculate_percentage(attended: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((attended / total) * 100, 2)


def get_result(score: float) -> str:
    return "Pass" if score >= 50 else "Fail"


# ─── Mark attendance for a date ───────────────────────────────────────────────
@router.post("/attendance/mark", status_code=201)
def mark_attendance(data: MarkAttendance):

    if not check_registration(data.trainee_id, data.course_id):
        raise HTTPException(
            status_code=404,
            detail="Registration not found. Please register the trainee for this course first."
        )

    record = find_attendance(data.trainee_id, data.course_id)

    if record is None:
        new_record = {
            "trainee_id": data.trainee_id,
            "course_id": data.course_id,
            "total_classes": data.total_classes,
            "attended_dates": [data.date],  # add date immediately on creation
            "score": 0.0
        }
        database.attendance.insert_one(new_record)
        attended_count = 1
        total = data.total_classes
    else:
        # Check if date already marked
        if data.date in record["attended_dates"]:
            raise HTTPException(status_code=400, detail=f"Attendance for date '{data.date}' is already marked.")

        # FIX: persist changes back to MongoDB using update_one
        database.attendance.update_one(
            {"trainee_id": data.trainee_id, "course_id": data.course_id},
            {"$push": {"attended_dates": data.date}, "$set": {"total_classes": data.total_classes}}
        )
        attended_count = len(record["attended_dates"]) + 1
        total = data.total_classes

    percentage = calculate_percentage(attended_count, total)

    return {
        "success": True,
        "message": f"Attendance marked for {data.date}.",
        "data": {
            "trainee_id": data.trainee_id,
            "course_id": data.course_id,
            "attended_classes": attended_count,
            "total_classes": total,
            "attendance_percentage": percentage
        }
    }


# ─── Add assessment score ─────────────────────────────────────────────────────
@router.post("/attendance/score", status_code=201)
def add_score(data: AddScore):

    if not check_registration(data.trainee_id, data.course_id):
        raise HTTPException(
            status_code=404,
            detail="Registration not found. Please register the trainee for this course first."
        )

    record = find_attendance(data.trainee_id, data.course_id)

    if record is None:
        new_record = {
            "trainee_id": data.trainee_id,
            "course_id": data.course_id,
            "total_classes": 0,
            "attended_dates": [],
            "score": data.score
        }
        database.attendance.insert_one(new_record)
    else:
        # FIX: persist score back to MongoDB using update_one
        database.attendance.update_one(
            {"trainee_id": data.trainee_id, "course_id": data.course_id},
            {"$set": {"score": data.score}}
        )

    return {
        "success": True,
        "message": "Score updated successfully.",
        "data": {
            "trainee_id": data.trainee_id,
            "course_id": data.course_id,
            "score": data.score,
            "result": get_result(data.score)
        }
    }


# ─── Progress report ──────────────────────────────────────────────────────────
@router.get("/attendance/progress/{trainee_id}/{course_id}")
def get_progress_report(trainee_id: int, course_id: int):

    trainee = database.trainee.find_one({"trainee_id": trainee_id})
    if not trainee:
        raise HTTPException(status_code=404, detail=f"Trainee with ID {trainee_id} not found.")

    course = database.course.find_one({"course_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found.")

    record = find_attendance(trainee_id, course_id)
    if not record:
        raise HTTPException(status_code=404, detail="No attendance record found for this trainee and course.")

    percentage = calculate_percentage(len(record["attended_dates"]), record["total_classes"])
    result = get_result(record["score"])

    return {
        "success": True,
        "data": {
            "trainee": {
                "trainee_id": trainee["trainee_id"],
                "trainee_name": trainee["trainee_name"],
                "email": trainee["trainee_email"],
                "city": trainee["city"],
                "skills": trainee["skills"]
            },
            "course": {
                "course_id": course["course_id"],
                "course_name": course["course_name"],           # FIX: was course_title
                "trainer_name": course["trainer_name"],
                "course_duration": course["course_duration"]    # FIX: was duration
            },
            "attendance": {
                "total_classes": record["total_classes"],
                "attended_classes": len(record["attended_dates"]),
                "attendance_percentage": percentage
            },
            "assessment": {
                "score": record["score"],
                "result": result
            }
        }
    }