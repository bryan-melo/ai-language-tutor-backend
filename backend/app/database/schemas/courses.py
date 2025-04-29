from sqlmodel import Field, SQLModel
from typing import List, Optional
from sqlalchemy import Column, JSON


# Course Schema
class Course(SQLModel, table=True):
   id: Optional[int] = Field(
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
   difficulty: str = Field(
      description="Difficulty of a course ranging from Beginner, Intermediate, and Expert"
   )
   
   
# Lesson Schema
class Lesson(SQLModel, table=True):
   id: Optional[int] = Field(
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
   material: List[str] = Field(
      sa_column=Column(JSON),
      description="Main content or material of the lesson"
    )
   parent_course: int | None = Field(
      default=None, 
      foreign_key="course.id", 
      index=True,
      description="Foreign key linking to the parent course"
   )