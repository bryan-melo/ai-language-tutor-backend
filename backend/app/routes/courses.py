from sqlmodel import select
from fastapi import APIRouter, HTTPException, status

from app.database.connection import SessionDep
from app.database.schemas import Course
from app.models.course_models import CourseCreate, CourseResponse



router = APIRouter()


# Route to create a course
@router.post("/create/create-course", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, session: SessionDep) -> Course:
   # Check for existing course
   existing = session.exec(
      select(Course).where(
         (Course.title == course.title)
      )
   ).first()
   
   if existing:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="A course with that title already exists."
      )
      
   db_course = Course(**course.model_dump(mode="json"))
   session.add(db_course)
   session.commit()
   session.refresh(db_course)
   return Course.model_validate(db_course)


# Route to get all courses in database
@router.get("/get-all-courses", response_model=list[CourseResponse], status_code=status.HTTP_200_OK)
def get_all_courses(session: SessionDep) -> list[Course]:
   courses = session.exec(
      select(Course)
   )

   return [Course.model_validate(course) for course in courses]


# Route to get a course using course id
@router.get("/get-course/{course_id}", response_model=Course, status_code=status.HTTP_200_OK)
def get_course(course_id: int, session: SessionDep) -> Course:
   course = session.get(Course, course_id)
   if not course:
      raise HTTPException(status_code=404, detail="Course not found")
   return Course.model_validate(course.model_dump())


# Route to delete an existing course
@router.delete("/delete/delete-course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, session: SessionDep):
   course = session.get(Course, course_id)
   if not course:
      raise HTTPException(status_code=404, detail="Course not found")
   session.delete(course)
   session.commit()
   return
