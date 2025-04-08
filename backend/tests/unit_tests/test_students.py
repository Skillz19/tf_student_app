import pytest
from datetime import date
from tests.test_client import get_test_client
from tests.test_db import get_test_db, init_test_db
from models import Student, Module, Tutor, Grade

@pytest.fixture(autouse=True)
def init_db():
    init_test_db()

@pytest.fixture
def client():
    return get_test_client()

@pytest.fixture
def db():
    db = next(get_test_db())
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_tutor(db):
    tutor = Tutor(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        title="Dr."
    )
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor

@pytest.fixture
def sample_module(db, sample_tutor):
    module = Module(
        title="Test Module",
        module_tutor_id=sample_tutor.id
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module

def test_create_student(client, sample_tutor):
    response = client.post(
        "/students/",
        json={
            "student_id": "S001",
            "first_name": "Jane",
            "last_name": "Smith",
            "dob": "2000-01-01",
            "personal_tutor_id": sample_tutor.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "S001"
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"

def test_get_student(client, db, sample_tutor):
    # Create a student first
    student = Student(
        student_id="S002",
        first_name="Bob",
        last_name="Wilson",
        dob=date(2000, 2, 2),
        personal_tutor_id=sample_tutor.id
    )
    db.add(student)
    db.commit()

    # Test getting the student
    response = client.get(f"/students/{student.student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "S002"
    assert data["first_name"] == "Bob"

def test_get_all_students(client, db, sample_tutor):
    # Create multiple students
    students = [
        Student(
            student_id="S003",
            first_name="Alice",
            last_name="Brown",
            dob=date(2000, 3, 3),
            personal_tutor_id=sample_tutor.id
        ),
        Student(
            student_id="S004",
            first_name="Charlie",
            last_name="Davis",
            dob=date(2000, 4, 4),
            personal_tutor_id=sample_tutor.id
        )
    ]
    for student in students:
        db.add(student)
    db.commit()

    # Test getting all students
    response = client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    student_ids = [s["student_id"] for s in data]
    assert "S003" in student_ids
    assert "S004" in student_ids

def test_student_classification(client, db, sample_tutor, sample_module):
    # Create a student
    student = Student(
        student_id="S005",
        first_name="Eve",
        last_name="Johnson",
        dob=date(2000, 5, 5),
        personal_tutor_id=sample_tutor.id
    )
    db.add(student)
    db.commit()

    # Create a second module
    module2 = Module(
        title="Test Module 2",
        module_tutor_id=sample_tutor.id
    )
    db.add(module2)
    db.commit()

    # Add grades for different modules
    grades = [
        Grade(student_id=student.student_id, module_id=sample_module.id, score=0.85),
        Grade(student_id=student.student_id, module_id=module2.id, score=0.90)
    ]
    for grade in grades:
        db.add(grade)
    db.commit()

    # Test student classification
    response = client.get(f"/students/{student.student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "Distinction"  # Average grade is 0.875 