import pytest
from tests.test_client import get_test_client
from tests.test_db import get_test_db, init_test_db
from models import Module, Tutor

@pytest.fixture(autouse=True)
def init_db():
    init_test_db()

@pytest.fixture
def client():
    return get_test_client()

@pytest.fixture
def db():
    return next(get_test_db())

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

def test_create_module(client, sample_tutor):
    response = client.post(
        "/modules/",
        json={
            "title": "Test Module",
            "module_tutor_id": sample_tutor.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Module"
    assert data["module_tutor_id"] == sample_tutor.id

def test_get_module(client, db, sample_tutor):
    # Create a module first
    module = Module(
        title="Test Module",
        module_tutor_id=sample_tutor.id
    )
    db.add(module)
    db.commit()

    # Test getting the module
    response = client.get(f"/modules/{module.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Module"
    assert data["module_tutor_id"] == sample_tutor.id

def test_get_all_modules(client, db, sample_tutor):
    # Create multiple modules
    modules = [
        Module(title="Module 1", module_tutor_id=sample_tutor.id),
        Module(title="Module 2", module_tutor_id=sample_tutor.id)
    ]
    for module in modules:
        db.add(module)
    db.commit()

    # Test getting all modules
    response = client.get("/modules/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    module_titles = [m["title"] for m in data]
    assert "Module 1" in module_titles
    assert "Module 2" in module_titles 