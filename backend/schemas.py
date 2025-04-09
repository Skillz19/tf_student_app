from pydantic import BaseModel, validator
from datetime import date
from typing import Optional
import re

# Tutor Schemas
class TutorBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    title: Optional[str] = None

class TutorCreate(TutorBase):
    pass

class TutorResponse(TutorBase):
    id: int
    class Config:
        from_attributes = True

# Module Schemas
class ModuleBase(BaseModel):
    title: str
    module_tutor_id: int

class ModuleResponse(ModuleBase):
    id: int
    class Config:
        from_attributes = True

# Student Schemas
class StudentBase(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    dob: date
    personal_tutor_id: int

    @validator('student_id')
    @classmethod
    def validate_student_id(cls, v):
        if not re.match(r'^[0-9]{6}[A-Z]$', v):
            raise ValueError(
                'Student ID must be 6 numbers followed by 1 uppercase letter'
            )
        return v

    @validator('dob')
    @classmethod
    def dob_in_past(cls, v):
        if v >= date.today():
            raise ValueError('Date of birth must be in the past')
        return v

class StudentResponse(StudentBase):
    average_grade: float
    classification: str
    class Config:
        from_attributes = True

# Grade Schemas
class GradeBase(BaseModel):
    student_id: str
    module_id: int
    score: float

    @validator('score')
    @classmethod
    def validate_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Score must be between 0 and 1')
        return v

class GradeResponse(GradeBase):
    class Config:
        from_attributes = True
        orm_mode = True 
