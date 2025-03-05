import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models import *

app = FastAPI()

# Define allowed origins for Cross-Origin Resource Sharing (CORS)
origins = [
    "http://localhost:3000/courses"     # Allow requests from frontend running on localhost:3000
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Connected to the database!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
