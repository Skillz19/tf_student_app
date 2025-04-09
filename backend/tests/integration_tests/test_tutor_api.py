import pytest
from ..test_client import get_test_client
from ..test_db import init_test_db

@pytest.fixture(autouse=True)
def setup_database():
    init_test_db()
    yield

def test_create_tutor():
    client = get_test_client()
    
    # Test data
    tutor_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@university.edu"
    }
    
    # Create tutor
    response = client.post("/tutors/", json=tutor_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == tutor_data["first_name"]
    assert data["last_name"] == tutor_data["last_name"]
    assert data["email"] == tutor_data["email"]
    assert "id" in data

def test_get_all_tutors():
    client = get_test_client()
    
    # Create multiple tutors
    tutors = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@university.edu"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@university.edu"
        }
    ]
    
    for tutor in tutors:
        client.post("/tutors/", json=tutor)
    
    # Get all tutors
    response = client.get("/tutors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["first_name"] == "John"
    assert data[1]["first_name"] == "Jane"

def test_get_tutor_by_id():
    client = get_test_client()
    
    # Create a tutor
    tutor_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@university.edu"
    }
    response = client.post("/tutors/", json=tutor_data)
    assert response.status_code == 200
    tutor_id = response.json()["id"]
    
    # Get tutor by ID
    response = client.get(f"/tutors/{tutor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@university.edu" 