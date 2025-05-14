from fastapi import APIRouter, HTTPException
from app.database.connection import SessionDep
from app.database.schemas import Lesson

router = APIRouter()


# Route to create a lesson
@router.post("/create/create-lesson", response_model=Lesson)
def create_lesson(lesson: Lesson, session: SessionDep) -> Lesson:
   session.add(lesson)
   session.commit()
   session.refresh(lesson)
   return lesson


# Route to get all lessons for a specific course
@router.get("/get-lessons-by-course/{course_id}", response_model=list[Lesson])
def get_lessons_by_course(course_id: int, session: SessionDep) -> list[Lesson]:
    lessons = session.query(Lesson).filter(Lesson.parent_course == course_id).all()
    
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this course")
    
    return lessons


# Route to get a lesson using lesson id
@router.get("/get-lesson/{lesson_id}", response_model=Lesson)
def get_lesson(lesson_id: int, session: SessionDep) -> Lesson:
   lesson = session.get(Lesson, lesson_id)
   if not lesson:
      raise HTTPException(status_code=404, detail="Lesson not found")
   return lesson


# Route to delete an existing lesson
@router.delete("/delete/delete-lesson/{lesson_id}")
def delete_lesson(lesson_id: int, session: SessionDep):
   lesson = session.get(Lesson, lesson_id)
   if not lesson:
      raise HTTPException(status_code=404, detail="Lesson not found")
   session.delete(lesson)
   session.commit()
   return {"ok": True}
