from fastapi import APIRouter, HTTPException
from app.database.connection import SessionDep
from app.database.schemas import Course
from sqlmodel import select

router = APIRouter()


# Route to create a course
@router.post("/create/create-course", response_model=Course)
def create_course(course: Course, session: SessionDep) -> Course:
   session.add(course)
   session.commit()
   session.refresh(course)
   return Course.model_validate(course.model_dump())


# Route to get all courses in database
@router.get("/get-all-courses", response_model=list[Course])
def get_all_courses(session: SessionDep) -> list[Course]:
   statement = select(Course)
   courses = session.exec(statement).all()
   
   if not courses:
      raise HTTPException(status_code=404, detail="No courses found")

   return [Course.model_validate(course.model_dump()) for course in courses]


# Route to get a course using course id
@router.get("/get-course/{course_id}", response_model=Course)
def get_course(course_id: int, session: SessionDep) -> Course:
   course = session.get(Course, course_id)
   if not course:
      raise HTTPException(status_code=404, detail="Course not found")
   return Course.model_validate(course.model_dump())


# Route to delete an existing course
@router.delete("/delete/delete-course/{course_id}")
def delete_course(course_id: int, session: SessionDep):
   course = session.get(Course, course_id)
   if not course:
      raise HTTPException(status_code=404, detail="Course not found")
   session.delete(course)
   session.commit()
   return {"ok": True}
