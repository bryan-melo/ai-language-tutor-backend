from pydantic import BaseModel, ConfigDict
from enum import Enum


class SupportedLanguages(str, Enum):
   english = "English"
   spanish = "Spanish"


class CourseDifficulty(str, Enum):
   easy = "Beginner"
   medium = "Intermediate"
   advanced = "Advanced"
   
   def __str__(self):
        return self.value
     
     
class CourseCategories(str, Enum):
   pronunciation_phonetics = "Pronunciation & Phonetics"
   grammar_sentence_structure = "Grammar & Sentence Structure"
   vocabulary_building = "Vocabulary Building"
   listening_speaking = "Listening & Speaking"
   reading_writing = "Reading & Writing"


class CourseCreate(BaseModel):
   title: str
   author: str
   description: str
   num_of_lessons: int
   category: CourseCategories
   difficulty: CourseDifficulty


class CourseResponse(BaseModel):
   id: int
   title: str
   author: str
   description: str
   num_of_lessons: int
   category: CourseCategories
   difficulty: CourseDifficulty
   
   model_config = ConfigDict(from_attributes=True)
   