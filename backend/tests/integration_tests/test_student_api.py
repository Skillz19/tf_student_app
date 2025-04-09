import pytest
from ..test_client import get_test_client
from ..test_db import init_test_db

@pytest.fixture(autouse=True)
def setup_database():
    init_test_db()
    yield

def test_create_student():
    client = get_test_client()
    
    # Create a tutor first (since student requires a tutor)
    tutor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@university.edu"
    }
    tutor_response = client.post("/tutors/", json=tutor_data)
    assert tutor_response.status_code == 200
    tutor_id = tutor_response.json()["id"]
    
    # Test data
    student_data = {
        "student_id": "123456A",
        "first_name": "John",
        "last_name": "Doe",
        "dob": "2000-01-01",
        "personal_tutor_id": tutor_id
    }
    
    # Create student
    response = client.post("/students/", json=student_data)
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == student_data["student_id"]
    assert data["first_name"] == student_data["first_name"]
    assert data["last_name"] == student_data["last_name"]
    assert data["average_grade"] == 0  # No grades yet
    assert data["classification"] == "Fail"  # Default classification with no grades

def test_get_all_students():
    client = get_test_client()
    
    # Create a tutor first
    tutor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@university.edu"
    }
    tutor_response = client.post("/tutors/", json=tutor_data)
    assert tutor_response.status_code == 200
    tutor_id = tutor_response.json()["id"]
    
    # Create multiple students
    students = [
        {
            "student_id": "123456A",
            "first_name": "John",
            "last_name": "Doe",
            "dob": "2000-01-01",
            "personal_tutor_id": tutor_id
        },
        {
            "student_id": "234567B",
            "first_name": "Jane",
            "last_name": "Doe",
            "dob": "2000-02-01",
            "personal_tutor_id": tutor_id
        }
    ]
    
    for student in students:
        client.post("/students/", json=student)
    
    # Get all students
    response = client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["student_id"] == "123456A"
    assert data[1]["student_id"] == "234567B"

def test_get_student_by_id():
    client = get_test_client()
    
    # Create a tutor first
    tutor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@university.edu"
    }
    tutor_response = client.post("/tutors/", json=tutor_data)
    assert tutor_response.status_code == 200
    tutor_id = tutor_response.json()["id"]
    
    # Create a student
    student_data = {
        "student_id": "123456A",
        "first_name": "John",
        "last_name": "Doe",
        "dob": "2000-01-01",
        "personal_tutor_id": tutor_id
    }
    client.post("/students/", json=student_data)
    
    # Get student by ID
    response = client.get("/students/123456A")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "123456A"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

def test_get_student_grades():
    client = get_test_client()
    
    # Create a tutor
    tutor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@university.edu"
    }
    tutor_response = client.post("/tutors/", json=tutor_data)
    assert tutor_response.status_code == 200
    tutor_id = tutor_response.json()["id"]
    
    # Create a module
    module_data = {
        "title": "Mathematics",
        "module_tutor_id": tutor_id
    }
    module_response = client.post("/modules/", json=module_data)
    assert module_response.status_code == 200
    module_id = module_response.json()["id"]
    
    # Create a student
    student_data = {
        "student_id": "123456A",
        "first_name": "John",
        "last_name": "Doe",
        "dob": "2000-01-01",
        "personal_tutor_id": tutor_id
    }
    client.post("/students/", json=student_data)
    
    # Create a grade
    grade_data = {
        "student_id": "123456A",
        "module_id": module_id,
        "score": 0.75
    }
    client.post("/grades/", json=grade_data)
    
    # Get student grades
    response = client.get("/students/123456A/grades")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["score"] == 0.75
    assert data[0]["student_id"] == "123456A"
    assert data[0]["module_id"] == module_id 