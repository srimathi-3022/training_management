from pydantic import BaseModel
from datetime import datetime


class Registration(BaseModel):
    course_id: int
    trainee_id: int
   
    registration_date: datetime = datetime.now()
