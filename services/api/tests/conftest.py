import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.dynamodb import MockDynamoDBService, db_service

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_db():
    """Ensure we're using the mock database for tests."""
    # Save original service
    original_service = db_service
    
    # Replace with a fresh mock service
    mock_service = MockDynamoDBService()
    import app.db.dynamodb
    app.db.dynamodb.db_service = mock_service
    
    # Make the mock service available to tests
    yield mock_service
    
    # Restore original service
    app.db.dynamodb.db_service = original_service