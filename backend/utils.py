from typing import List, Type, TypeVar
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Grade, Student, Module, Tutor
from schemas import StudentResponse, ModuleResponse, TutorResponse, GradeResponse

T = TypeVar('T')

def get_or_404(db: Session, model: Type[T], **filters) -> T:
    """Get a record by filters or raise 404 if not found."""
    instance = db.query(model).filter_by(**filters).first()
    if not instance:
        model_name = model.__name__
        raise HTTPException(status_code=404, detail=f"{model_name} not found")
    return instance

def check_exists(db: Session, model: Type[T], **filters) -> bool:
    """Check if a record exists with the given filters."""
    return db.query(model).filter_by(**filters).first() is not None

def get_classification(avg: float) -> str:
    if avg >= 0.7:
        return "Distinction"
    elif avg >= 0.6:
        return "Merit"
    elif avg >= 0.4:
        return "Pass"
    else:
        return "Fail"

def calculate_average_grade(grades: List[Grade]) -> float:
    if not grades:
        return 0
    return round(sum(grade.score for grade in grades) / len(grades), 2)

def build_student_response(student: Student) -> StudentResponse:
    """Build a consistent StudentResponse from a Student model."""
    avg = calculate_average_grade(student.grades)
    classification = get_classification(avg)
    
    return StudentResponse(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        dob=student.dob,
        personal_tutor_id=student.personal_tutor_id,
        average_grade=avg,
        classification=classification
    )

def build_module_response(module: Module) -> ModuleResponse:
    """Build a consistent ModuleResponse from a Module model."""
    return ModuleResponse(
        id=module.id,
        title=module.title,
        module_tutor_id=module.module_tutor_id
    )

def build_tutor_response(tutor: Tutor) -> TutorResponse:
    """Build a consistent TutorResponse from a Tutor model."""
    return TutorResponse(
        id=tutor.id,
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
        title=tutor.title
    )

def build_grade_response(grade: Grade) -> GradeResponse:
    """Build a consistent GradeResponse from a Grade model."""
    return GradeResponse(
        student_id=grade.student_id,
        module_id=grade.module_id,
        score=grade.score
    )

def get_grade_or_404(db: Session, student_id: str, module_id: int) -> Grade:
    """Get a grade by student_id and module_id or raise 404 if not found."""
    return get_or_404(db, Grade, student_id=student_id, module_id=module_id)

def check_grade_exists(db: Session, student_id: str, module_id: int) -> bool:
    """Check if a grade exists for the given student and module."""
    return check_exists(db, Grade, student_id=student_id, module_id=module_id) 