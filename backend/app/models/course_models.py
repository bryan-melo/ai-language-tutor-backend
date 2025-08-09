from pydantic import BaseModel, ConfigDict
from enum import Enum


class SupportedLanguages(str, Enum):
   English = "English"
   Spanish = "Spanish"


class CourseDifficulty(str, Enum):
   Beginner = "Beginner"
   Intermediate = "Intermediate"
   Advanced = "Advanced"
     
     
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
   
   model_config = ConfigDict(from_attributes=True)


class CourseResponse(BaseModel):
   id: int
   title: str
   author: str
   description: str
   num_of_lessons: int
   category: CourseCategories
   difficulty: CourseDifficulty
   
   model_config = ConfigDict(from_attributes=True)
   