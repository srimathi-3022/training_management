from pydantic import BaseModel, Field
class MarkAttendance(BaseModel):
    trainee_id: int
    course_id: int
    date: str            
    total_classes: int


class AddScore(BaseModel):
    trainee_id: int
    course_id: int
    score: float = Field(..., ge=0, le=100) 