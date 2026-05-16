from fastapi import FastAPI
from app.routes import course_routes, trainee_routes, registration_routes, attendance_routes

app = FastAPI()

app.include_router(course_routes.router)
app.include_router(trainee_routes.router)
app.include_router(registration_routes.router)
app.include_router(attendance_routes.router)
