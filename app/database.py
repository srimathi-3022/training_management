from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client =MongoClient(MONGO_URI)
db = client["training_db"]
trainee = db["trainees"]
course = db["courses"]
registration = db["registrations"]
attendance = db["attendances"]

trainee_id_counter = 1
course_id_counter = 1
registration_id_counter = 1
attendance_id_counter = 1