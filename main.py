from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import course_routes, trainee_routes, registration_routes, attendance_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course_routes.router)
app.include_router(trainee_routes.router)
app.include_router(registration_routes.router)
app.include_router(attendance_routes.router)
