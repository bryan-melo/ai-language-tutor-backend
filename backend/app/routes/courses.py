from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlmodel import select
from app.database.connection import SessionDep
from app.database.schemas import Course

router = APIRouter()


# Route to create a course
@router.post("/create-course", response_model=Course)
def create_course(course: Course, session: SessionDep) -> Course:
   session.add(course)
   session.commit()
   session.refresh(course)
   return course


# Route to get all courses in database
@router.post("/get-all-courses", response_model=list[Course])
def get_all_courses(session: SessionDep) -> list[Course]:
   courses = session.query(Course).all()
   
   if not courses:
      raise HTTPException(status_code=404, detail="No courses found")

   return courses


# Route to get a course using course id
@router.get("/get-course/{course_id}", response_model=Course)
def get_course(course_id: int, session, SessionDep) -> Course:
   course = session.get(Course, course_id)
   if not course:
      raise HTTPException(status_code=404, detail="Course not found")
   return course
