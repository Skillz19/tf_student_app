import pytest
from tests.test_client import get_test_client
from tests.test_db import get_test_db, init_test_db
from models import Tutor

@pytest.fixture
def client():
    return get_test_client()

@pytest.fixture
def db():
    return next(get_test_db())

@pytest.fixture(autouse=True)
def init_db():
    init_test_db()

def test_create_tutor(client):
    response = client.post(
        "/tutors/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "title": "Dr."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["title"] == "Dr."

def test_get_tutor(client, db):
    # Create a tutor first
    tutor = Tutor(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        title="Dr."
    )
    db.add(tutor)
    db.commit()

    # Test getting the tutor
    response = client.get(f"/tutors/{tutor.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["title"] == "Dr."

def test_get_all_tutors(client, db):
    # Create multiple tutors
    tutors = [
        Tutor(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            title="Dr."
        ),
        Tutor(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            title="Prof."
        )
    ]
    for tutor in tutors:
        db.add(tutor)
    db.commit()

    # Test getting all tutors
    response = client.get("/tutors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    tutor_emails = [t["email"] for t in data]
    assert "john.doe@example.com" in tutor_emails
    assert "jane.smith@example.com" in tutor_emails 