from sqlmodel import Field, SQLModel

# Course Model for Database
class Course(SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True, index=True)
   title: str = Field(unique=True)
   author: str
   description: str
   num_of_lessons: int
   
   
# Lesson Model for Database
class Lesson(SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True, index=True)
   title: str = Field(unique=True)
   lesson_num: int 
   material: str 
   parent_course: int | None = Field(default=None, foreign_key="course.id", index=True)