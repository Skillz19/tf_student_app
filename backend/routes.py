from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Student, Module, Tutor, Grade
from schemas import (
    StudentBase, StudentResponse,
    ModuleBase, ModuleResponse,
    TutorBase, TutorResponse,
    GradeBase, GradeResponse
)
from database import get_db
from typing import List

router = APIRouter()

# Students Endpoints
@router.post("/students/", response_model=StudentResponse)
def create_student(student: StudentBase, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    # Calculate average grade and classification
    grades = [grade.score for grade in db_student.grades]
    avg = round(sum(grades) / len(grades), 2) if grades else 0
    classification = (
        "Distinction" if avg >= 0.7 
        else "Merit" if avg >= 0.6 
        else "Pass" if avg >= 0.4 
        else "Fail"
    )
    
    return {
        "student_id": db_student.student_id,
        "first_name": db_student.first_name,
        "last_name": db_student.last_name,
        "dob": db_student.dob,
        "personal_tutor_id": db_student.personal_tutor_id,
        "average_grade": avg,
        "classification": classification
    }

@router.get("/students/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    result = []
    
    for student in students:
        grades = [grade.score for grade in student.grades]
        avg = round(sum(grades) / len(grades), 2) if grades else 0
        
        result.append({
            **student.__dict__,
            "average_grade": avg,
            "classification": (
                "Distinction" if avg >= 0.7 
                else "Merit" if avg >= 0.6 
                else "Pass" if avg >= 0.4 
                else "Fail"
            )
        })
    
    return result

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    grades = [grade.score for grade in student.grades]
    avg = round(sum(grades) / len(grades), 2) if grades else 0
    
    return {
        **student.__dict__,
        "average_grade": avg,
        "classification": (
            "Distinction" if avg >= 0.7 
            else "Merit" if avg >= 0.6 
            else "Pass" if avg >= 0.4 
            else "Fail"
        )
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
    db_module = Module(**module.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return {
        "id": db_module.id,
        "title": db_module.title,
        "module_tutor_id": db_module.module_tutor_id
    }

@router.get("/modules/", response_model=List[ModuleResponse])
def get_all_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).all()
    return [
        {
            "id": module.id,
            "title": module.title,
            "module_tutor_id": module.module_tutor_id
        }
        for module in modules
    ]

@router.get("/modules/{module_id}", response_model=ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return {
        "id": module.id,
        "title": module.title,
        "module_tutor_id": module.module_tutor_id
    }

# Tutors Endpoints
@router.post("/tutors/", response_model=TutorResponse)
def create_tutor(tutor: TutorBase, db: Session = Depends(get_db)):
    db_tutor = Tutor(**tutor.dict())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return {
        "id": db_tutor.id,
        "first_name": db_tutor.first_name,
        "last_name": db_tutor.last_name,
        "email": db_tutor.email,
        "title": db_tutor.title
    }

@router.get("/tutors/", response_model=List[TutorResponse])
def get_all_tutors(db: Session = Depends(get_db)):
    tutors = db.query(Tutor).all()
    return [
        {
            "id": tutor.id,
            "first_name": tutor.first_name,
            "last_name": tutor.last_name,
            "email": tutor.email,
            "title": tutor.title
        }
        for tutor in tutors
    ]

@router.get("/tutors/{tutor_id}", response_model=TutorResponse)
def get_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return {
        "id": tutor.id,
        "first_name": tutor.first_name,
        "last_name": tutor.last_name,
        "email": tutor.email,
        "title": tutor.title
    }

# Grades Endpoints
@router.post("/grades/", response_model=GradeResponse)
def create_grade(grade: GradeBase, db: Session = Depends(get_db)):
    existing_grade = db.query(Grade).filter(
        Grade.student_id == grade.student_id,
        Grade.module_id == grade.module_id
    ).first()
    
    if existing_grade:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Grade for student {grade.student_id} "
                f"in module {grade.module_id} already exists"
            )
        )
    
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/grades/module/{module_id}", response_model=List[GradeResponse])
def get_module_grades(module_id: int, db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.module_id == module_id).all()
    return grades

@router.put("/grades/{student_id}/{module_id}", response_model=GradeResponse)
def update_grade(
    student_id: str, 
    module_id: int, 
    grade: GradeBase, 
    db: Session = Depends(get_db)
):
    db_grade = db.query(Grade).filter(
        Grade.student_id == student_id,
        Grade.module_id == module_id
    ).first()
    
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    for key, value in grade.dict().items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade