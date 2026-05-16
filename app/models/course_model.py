from pydantic import BaseModel
from typing import List

class Course(BaseModel):
    course_name: str
    trainer_name: str
    course_duration: int
    topics: List[str]