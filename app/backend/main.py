import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define allowed origins for Cross-Origin Resource Sharing (CORS)
origins = [
    "http://localhost:5174"     # Allow requests from frontend running on localhost:3000
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, Wordl!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)