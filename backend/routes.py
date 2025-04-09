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
from utils import (
    build_student_response,
    build_module_response,
    build_tutor_response,
    build_grade_response,
    get_or_404,
    check_exists
)

router = APIRouter()

# Students Endpoints
@router.post("/students/", response_model=StudentResponse)
def create_student(student: StudentBase, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return build_student_response(db_student)

@router.get("/students/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [build_student_response(student) for student in students]

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = get_or_404(db, Student, student_id=student_id)
    return build_student_response(student)

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
    return build_module_response(db_module)

@router.get("/modules/", response_model=List[ModuleResponse])
def get_all_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).all()
    return [build_module_response(module) for module in modules]

@router.get("/modules/{module_id}", response_model=ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db)):
    module = get_or_404(db, Module, id=module_id)
    return build_module_response(module)

# Tutors Endpoints
@router.post("/tutors/", response_model=TutorResponse)
def create_tutor(tutor: TutorBase, db: Session = Depends(get_db)):
    db_tutor = Tutor(**tutor.dict())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return build_tutor_response(db_tutor)

@router.get("/tutors/", response_model=List[TutorResponse])
def get_all_tutors(db: Session = Depends(get_db)):
    tutors = db.query(Tutor).all()
    return [build_tutor_response(tutor) for tutor in tutors]

@router.get("/tutors/{tutor_id}", response_model=TutorResponse)
def get_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = get_or_404(db, Tutor, id=tutor_id)
    return build_tutor_response(tutor)

# Grades Endpoints
@router.post("/grades/", response_model=GradeResponse)
def create_grade(grade: GradeBase, db: Session = Depends(get_db)):
    if check_exists(db, Grade, student_id=grade.student_id, module_id=grade.module_id):
        error_msg = (
            f"Grade for student {grade.student_id} "
            f"in module {grade.module_id} already exists"
        )
        raise HTTPException(status_code=400, detail=error_msg)
    
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return build_grade_response(db_grade)

@router.get("/grades/module/{module_id}", response_model=List[GradeResponse])
def get_module_grades(module_id: int, db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.module_id == module_id).all()
    return [build_grade_response(grade) for grade in grades]

@router.put("/grades/{student_id}/{module_id}", response_model=GradeResponse)
def update_grade(
    student_id: str, 
    module_id: int, 
    grade: GradeBase, 
    db: Session = Depends(get_db)
):
    db_grade = get_or_404(db, Grade, student_id=student_id, module_id=module_id)
    
    for key, value in grade.dict().items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return build_grade_response(db_grade)