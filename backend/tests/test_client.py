from fastapi.testclient import TestClient
from main import app
from tests.test_db import get_test_db
from database import get_db

# Override the database dependency to use the test database
app.dependency_overrides[get_db] = get_test_db

def get_test_client():
    return TestClient(app) 