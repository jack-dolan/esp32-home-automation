import uuid

def test_create_device(client, mock_db):
    """Test creating a new device."""
    device_data = {
        "name": "Test Thermostat",
        "type": "thermostat",
        "location": "Test Room"
    }
    
    response = client.post("/api/v1/devices/", json=device_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert "device" in result
    assert result["device"]["name"] == device_data["name"]
    assert result["device"]["type"] == device_data["type"]
    assert result["device"]["location"] == device_data["location"]
    assert "id" in result["device"]

def test_get_devices(client, mock_db):
    """Test retrieving all devices."""
    # First create a device
    device_data = {
        "name": "Test Thermostat",
        "type": "thermostat",
        "location": "Test Room"
    }
    create_response = client.post("/api/v1/devices/", json=device_data)
    
    # Then get all devices
    response = client.get("/api/v1/devices/")
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert "devices" in result
    assert len(result["devices"]) >= 1

def test_get_device_by_id(client, mock_db):
    """Test retrieving a specific device by ID."""
    # First create a device
    device_data = {
        "name": "Test Thermostat",
        "type": "thermostat",
        "location": "Test Room"
    }
    create_response = client.post("/api/v1/devices/", json=device_data)
    device_id = create_response.json()["device"]["id"]
    
    # Then get the specific device
    response = client.get(f"/api/v1/devices/{device_id}")
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert result["device"]["id"] == device_id
    assert result["device"]["name"] == device_data["name"]

def test_device_not_found(client, mock_db):
    """Test the API returns 404 for non-existent devices."""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/devices/{non_existent_id}")
    assert response.status_code == 404

def test_control_device(client, mock_db):
    """Test sending a control command to a device."""
    # First create a device
    device_data = {
        "name": "Test Thermostat",
        "type": "thermostat",
        "location": "Test Room"
    }
    create_response = client.post("/api/v1/devices/", json=device_data)
    device_id = create_response.json()["device"]["id"]
    
    # Then send a control command
    command_data = {
        "action": "set_temperature",
        "params": {
            "temperature": 22.5
        }
    }
    
    response = client.post(f"/api/v1/devices/{device_id}/control", json=command_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert "command_id" in result
    assert result["status"] == "sent"