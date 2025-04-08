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
def setup_data(db):
    # Create a tutor
    tutor = Tutor(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        title="Dr."
    )
    db.add(tutor)
    db.commit()

    # Create a student
    student = Student(
        student_id="123456S",
        first_name="Jane",
        last_name="Smith",
        dob=date(2000, 1, 1),
        personal_tutor_id=tutor.id
    )
    db.add(student)
    db.commit()

    # Create a module
    module = Module(
        title="Test Module",
        module_tutor_id=tutor.id
    )
    db.add(module)
    db.commit()

    return {
        "student": student,
        "module": module,
        "tutor": tutor
    }

def test_create_grade(client, setup_data):
    # Create initial grade
    response = client.post(
        "/grades/",
        json={
            "student_id": setup_data["student"].student_id,
            "module_id": setup_data["module"].id,
            "score": 0.85
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == setup_data["student"].student_id
    assert data["module_id"] == setup_data["module"].id
    assert data["score"] == 0.85

    # Try to create a duplicate grade
    response = client.post(
        "/grades/",
        json={
            "student_id": setup_data["student"].student_id,
            "module_id": setup_data["module"].id,
            "score": 0.90
        }
    )
    assert response.status_code == 400
    error_detail = response.json()["detail"].lower()
    assert "already exists" in error_detail
    assert setup_data["student"].student_id.lower() in error_detail
    assert str(setup_data["module"].id) in error_detail

def test_get_student_grades(client, setup_data, db):
    # Create a grade first
    grade = Grade(
        student_id=setup_data["student"].student_id,
        module_id=setup_data["module"].id,
        score=0.85
    )
    db.add(grade)
    db.commit()

    # Test getting student grades
    response = client.get(f"/grades/student/{setup_data['student'].student_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["student_id"] == setup_data["student"].student_id
    assert data[0]["module_id"] == setup_data["module"].id
    assert data[0]["score"] == 0.85

def test_get_module_grades(client, setup_data, db):
    # Create a grade first
    grade = Grade(
        student_id=setup_data["student"].student_id,
        module_id=setup_data["module"].id,
        score=0.85
    )
    db.add(grade)
    db.commit()

    # Test getting module grades
    response = client.get(f"/grades/module/{setup_data['module'].id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["student_id"] == setup_data["student"].student_id
    assert data[0]["module_id"] == setup_data["module"].id
    assert data[0]["score"] == 0.85

def test_update_grade(client, setup_data, db):
    # Create a grade first
    grade = Grade(
        student_id=setup_data["student"].student_id,
        module_id=setup_data["module"].id,
        score=0.75
    )
    db.add(grade)
    db.commit()

    # Update the grade
    response = client.put(
        f"/grades/{setup_data['student'].student_id}/{setup_data['module'].id}",
        json={
            "student_id": setup_data["student"].student_id,
            "module_id": setup_data["module"].id,
            "score": 0.90
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == setup_data["student"].student_id
    assert data["module_id"] == setup_data["module"].id
    assert data["score"] == 0.90 