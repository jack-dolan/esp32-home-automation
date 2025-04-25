import pytest
from fastapi.testclient import TestClient
import uuid

from app.main import app
from app.db.database import MockDatabaseService, db_service

client = TestClient(app)

# Test API key, it's not real I promise, github
TEST_API_KEY = "dev_api_key_12345"
HEADERS = {"X-API-Key": TEST_API_KEY}

@pytest.fixture
def mock_db():
    """Make sure we're using a clean mock database for tests."""
    # Save original service
    original_service = db_service
    
    # Replace with a hot/fresh mock service
    mock_service = MockDatabaseService()
    import app.db.database
    app.db.database.db_service = mock_service
    
    # Make the mock service available to tests
    yield mock_service
    
    # Restore original service
    app.db.database.db_service = original_service

def test_register_device(mock_db):
    """Test registering a new device."""
    device_data = {
        "name": "Living Room Thermostat",
        "type": "thermostat",
        "location": "Living Room",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "hardware_version": "v1.0",
        "firmware_version": "v1.2.3"
    }
    
    response = client.post("/devices/register", json=device_data, headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert "device" in result
    assert result["device"]["name"] == device_data["name"]
    assert result["device"]["mac_address"] == device_data["mac_address"]
    assert result["device"]["status"] == "provisioning"
    assert "api_key" in result["device"]

def test_register_existing_device(mock_db):
    """Test that registering the same device twice returns the existing registration."""
    device_data = {
        "name": "Bedroom Thermostat",
        "type": "thermostat",
        "location": "Bedroom",
        "mac_address": "11:22:33:44:55:66",
        "hardware_version": "v1.0",
        "firmware_version": "v1.2.3"
    }
    
    # Register device first time
    response1 = client.post("/devices/register", json=device_data, headers=HEADERS)
    device_id = response1.json()["device"]["id"]
    
    # Register same device again
    response2 = client.post("/devices/register", json=device_data, headers=HEADERS)
    assert response2.status_code == 200
    
    result = response2.json()
    assert result["success"] is True
    assert result["message"] == "Device already registered"
    assert result["device"]["id"] == device_id

def test_activate_device(mock_db):
    """Test activating a provisioned device."""
    # First register a device
    device_data = {
        "name": "Kitchen Thermostat",
        "type": "thermostat",
        "location": "Kitchen",
        "mac_address": "AA:BB:CC:11:22:33",
        "hardware_version": "v1.0",
        "firmware_version": "v1.2.3"
    }
    
    register_response = client.post("/devices/register", json=device_data, headers=HEADERS)
    device_id = register_response.json()["device"]["id"]
    
    # Then activate it
    response = client.put(f"/devices/{device_id}/activate", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert result["device"]["status"] == "online"

def test_deregister_device(mock_db):
    """Test removing a device from the registry."""
    # First register a device
    device_data = {
        "name": "Garage Sensor",
        "type": "temperature",
        "location": "Garage",
        "mac_address": "FF:EE:DD:CC:BB:AA",
        "hardware_version": "v1.0",
        "firmware_version": "v1.0.0"
    }
    
    register_response = client.post("/devices/register", json=device_data, headers=HEADERS)
    device_id = register_response.json()["device"]["id"]
    
    # Then deregister it
    response = client.delete(f"/devices/{device_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify it's gone
    get_response = client.get(f"/devices/{device_id}", headers=HEADERS)
    assert get_response.status_code == 404