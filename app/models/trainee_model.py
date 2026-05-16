from pydantic import BaseModel, EmailStr
from typing import List

class Trainee(BaseModel):

    trainee_name: str
    trainee_age: int
    trainee_email: EmailStr
    trainee_phone: str
    city: str
    skills: List[str]