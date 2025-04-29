import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import create_db_and_tables
from app.routes import all_routers

app = FastAPI()

# Include all Routes
all_routers(app)

# Define allowed origins for Cross-Origin Resource Sharing (CORS)
origins = [
    "http://localhost:3000/courses",
    "http://localhost:3000/signup",
    "http://localhost:3000/login"   
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create Database and Tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the AI Language Tutor API",
        "version": "1.0",
        "routes": {
            "courses": {
                "Get course": "/courses/get-course/{course_id}",
                "Get all courses": "/courses/get-all-courses",
            },
            "lessons": {
                "Get lesson": "/lessons/get-lesson/{lesson_id}",
                "Get all lessons": "/lessons/get-all-lessons",
            }
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
