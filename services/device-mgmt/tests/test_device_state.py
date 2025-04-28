import pytest
from fastapi.testclient import TestClient
import uuid

from app.main import app
from app.db.database import MockDatabaseService, db_service

client = TestClient(app)

# Test API key
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

def test_thermostat_state_update(mock_db):
    """Test updating a thermostat state."""
    # First register a device
    device_data = {
        "name": "Living Room Thermostat",
        "type": "thermostat",
        "location": "Living Room",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "hardware_version": "v1.0",
        "firmware_version": "v1.2.3"
    }
    
    register_response = client.post("/devices/register", json=device_data, headers=HEADERS)
    device_id = register_response.json()["device"]["id"]
    
    # Then update its state
    state_data = {
        "state": {
            "current_temperature": 22.5,
            "target_temperature": 23.0,
            "mode": "heat",
            "is_heating": True,
            "humidity": 45.0
        }
    }
    
    response = client.put(f"/states/{device_id}", json=state_data, headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert result["state"]["device_id"] == device_id
    assert result["state"]["type"] == "thermostat"
    assert result["state"]["state"]["current_temperature"] == 22.5
    assert result["state"]["state"]["target_temperature"] == 23.0

def test_get_device_state(mock_db):
    """Test getting a device state."""
    # First register a device and set its state
    device_data = {
        "name": "Kitchen Thermostat",
        "type": "thermostat",
        "location": "Kitchen",
        "mac_address": "BB:CC:DD:EE:FF:AA",
        "hardware_version": "v1.0",
        "firmware_version": "v1.2.3"
    }
    
    register_response = client.post("/devices/register", json=device_data, headers=HEADERS)
    device_id = register_response.json()["device"]["id"]
    
    # Update its state
    state_data = {
        "state": {
            "current_temperature": 21.0,
            "target_temperature": 22.0,
            "mode": "cool",
            "is_cooling": True
        }
    }
    
    client.put(f"/states/{device_id}", json=state_data, headers=HEADERS)
    
    # Then get the state
    response = client.get(f"/states/{device_id}", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert result["state"]["device_id"] == device_id
    assert result["state"]["state"]["current_temperature"] == 21.0
    assert result["state"]["state"]["mode"] == "cool"