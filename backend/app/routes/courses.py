from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlmodel import select
from app.database.connection import SessionDep
from app.database.schemas import Course, Lesson

router = APIRouter()


''' Routes for Courses '''
# Route to create a course
@router.post("/create-course", response_model=Course)
def create_course(course: Course, session: SessionDep) -> Course:
   session.add(course)
   session.commit()
   session.refresh(course)
   return course


# Route to get a course using course id
@router.get("/get-course/{course_id}", response_model=Course)
def get_course(course_id: int, session, SessionDep) -> Course:
   course = session.get(Course, course_id)
   if not course:
      raise HTTPException(status_code=404, detail="Course not found")
   return course



''' Routes for Lessons '''
# Route to create a lesson
@router.post("/create-lesson", response_model=Lesson)
def create_lesson(lesson: Lesson, session: SessionDep) -> Lesson:
   session.add(lesson)
   session.commit()
   session.refresh(lesson)
   return lesson


# Route to get a lesson using lesson id
@router.get("/get-lesson/{lesson_id}", response_model=Lesson)
def get_lesson(lesson_id: int, session, SessionDep) -> Lesson:
   lesson = session.get(Lesson, lesson_id)
   if not lesson:
      raise HTTPException(status_code=404, detail="Lesson not found")
   return Lesson