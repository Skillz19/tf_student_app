from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Student, Module, Tutor, Grade
from schemas import *
from database import get_db
from typing import List

router = APIRouter()

# Students Endpoints
@router.post("/students/", response_model=StudentResponse)
def create_student(student: StudentBase, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    result = []
    
    for student in students:
        # Calculate average and classification
        grades = [grade.score for grade in student.grades]
        avg = round(sum(grades) / len(grades), 2) if grades else 0
        
        result.append({
            **student.__dict__,
            "average_grade": avg,
            "classification": "Distinction" if avg >= 0.7 else "Merit" if avg >= 0.6 else "Pass" if avg >= 0.4 else "Fail"
        })
    
    return result

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Calculate average and classification
    grades = [grade.score for grade in student.grades]
    avg = round(sum(grades) / len(grades), 2) if grades else 0
    
    return {
        **student.__dict__,
        "average_grade": avg,
        "classification": "Distinction" if avg >= 0.7 else "Merit" if avg >= 0.6 else "Pass" if avg >= 0.4 else "Fail"
    }

@router.get("/students/{student_id}/grades", response_model=List[GradeResponse])
def get_student_grades(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student.grades

# Modules Endpoints
@router.post("/modules/", response_model=ModuleResponse)
def create_module(module: ModuleBase, db: Session = Depends(get_db)):
    db_module = Module(**module.model_dump())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.get("/modules/", response_model=List[ModuleResponse])
def get_all_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).all()
    return modules

@router.get("/modules/{module_id}", response_model=ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

# Tutors Endpoints
@router.post("/tutors/", response_model=TutorResponse)
def create_tutor(tutor: TutorBase, db: Session = Depends(get_db)):
    db_tutor = Tutor(**tutor.model_dump())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

@router.get("/tutors/", response_model=List[TutorResponse])
def get_all_tutors(db: Session = Depends(get_db)):
    tutors = db.query(Tutor).all()
    return tutors

@router.get("/tutors/{tutor_id}", response_model=TutorResponse)
def get_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return tutor

# Grades Endpoints
@router.post("/grades/", response_model=GradeBase)
def create_grade(grade: GradeBase, db: Session = Depends(get_db)):
    db_grade = Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade