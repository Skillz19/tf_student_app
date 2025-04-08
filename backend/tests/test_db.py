from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base

# Create test database engine
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() 