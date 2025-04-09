import pytest
from ..test_client import get_test_client
from ..test_db import init_test_db

@pytest.fixture(autouse=True)
def setup_database():
    init_test_db()
    yield

def test_create_module():
    client = get_test_client()
    
    # Create a tutor first (since module requires a tutor)
    tutor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@university.edu"
    }
    tutor_response = client.post("/tutors/", json=tutor_data)
    assert tutor_response.status_code == 200
    tutor_id = tutor_response.json()["id"]
    
    # Test data
    module_data = {
        "title": "Mathematics",
        "module_tutor_id": tutor_id
    }
    
    # Create module
    response = client.post("/modules/", json=module_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == module_data["title"]
    assert data["module_tutor_id"] == module_data["module_tutor_id"]
    assert "id" in data

def test_get_all_modules():
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
    
    # Create multiple modules
    modules = [
        {
            "title": "Mathematics",
            "module_tutor_id": tutor_id
        },
        {
            "title": "Physics",
            "module_tutor_id": tutor_id
        }
    ]
    
    for module in modules:
        client.post("/modules/", json=module)
    
    # Get all modules
    response = client.get("/modules/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Mathematics"
    assert data[1]["title"] == "Physics"

def test_get_module_by_id():
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
    
    # Create a module
    module_data = {
        "title": "Mathematics",
        "module_tutor_id": tutor_id
    }
    module_response = client.post("/modules/", json=module_data)
    assert module_response.status_code == 200
    module_id = module_response.json()["id"]
    
    # Get module by ID
    response = client.get(f"/modules/{module_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == module_id
    assert data["title"] == "Mathematics"
    assert data["module_tutor_id"] == tutor_id

def test_get_module_grades():
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
    
    # Get module grades
    response = client.get(f"/grades/module/{module_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["score"] == 0.75
    assert data[0]["student_id"] == "123456A"
    assert data[0]["module_id"] == module_id 