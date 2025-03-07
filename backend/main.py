import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.database.connection import create_db_and_tables
from app.routes import account

app = FastAPI()

app.include_router(account.router)

# Define allowed origins for Cross-Origin Resource Sharing (CORS)
origins = [
    "http://localhost:3000/courses"    
]

# Add CORS middleware
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
    return {"message": "Hello world!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
