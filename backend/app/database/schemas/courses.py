from sqlmodel import Field, SQLModel

# Course Schema
class Course(SQLModel, table=True):
   id: int | None = Field(
      default=None, 
      primary_key=True, 
      index=True,
      description="Unique course identifier"
   )
   title: str = Field(
      unique=True,
      description="Title of the course"
   )
   author: str = Field(
      description="The name of the author that created this course"
   )
   description: str = Field(
      description="A brief summary or description of the course content"
   )
   num_of_lessons: int = Field(
      description="The number of lessons included in the course"
   )
   category: str = Field(
      description="Category to which the course belongs to (e.g, Pronunciation & Phonetics, Vocabulary, etc.)"
   )
   progress: int = Field(
      default=0,
      description="A percentage related to the number of lessons completed within the course"
   )
   
   
# Lesson Schema
class Lesson(SQLModel, table=True):
   id: int | None = Field(
      default=None, 
      primary_key=True, 
      index=True,
      description="Unique lesson identifier"
   )
   title: str = Field(
      unique=True,
      description="Title of the lesson"
   )
   lesson_num: int = Field(
      description="Lesson number within the course"
   )
   material: str = Field(
      description="Main content or material of the lesson"
   )
   parent_course: int | None = Field(
      default=None, 
      foreign_key="course.id", 
      index=True,
      description="Foreign key linking to the parent course"
   )