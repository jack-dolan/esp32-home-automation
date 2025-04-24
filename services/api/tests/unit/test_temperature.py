from datetime import datetime

def test_create_temperature_reading(client, mock_db):
    """Test creating a new temperature reading."""
    # First create a device
    device_data = {
        "name": "Test Temperature Sensor",
        "type": "temperature",
        "location": "Test Room"
    }
    create_device_response = client.post("/api/v1/devices/", json=device_data)
    device_id = create_device_response.json()["device"]["id"]
    
    # Then create a temperature reading
    reading_data = {
        "device_id": device_id,
        "temperature": 22.5,
        "humidity": 45.0
    }
    
    response = client.post("/api/v1/temperature/", json=reading_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert "readings" in result
    assert len(result["readings"]) == 1
    assert result["readings"][0]["temperature"] == reading_data["temperature"]

def test_get_temperature_readings(client, mock_db):
    """Test retrieving temperature readings for a device."""
    # First create a device
    device_data = {
        "name": "Test Temperature Sensor",
        "type": "temperature",
        "location": "Test Room"
    }
    create_device_response = client.post("/api/v1/devices/", json=device_data)
    device_id = create_device_response.json()["device"]["id"]
    
    # Create some temperature readings
    for temp in [21.0, 21.5, 22.0]:
        reading_data = {
            "device_id": device_id,
            "temperature": temp,
            "humidity": 45.0
        }
        client.post("/api/v1/temperature/", json=reading_data)
    
    # Then get the readings
    response = client.get(f"/api/v1/temperature/{device_id}")
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] is True
    assert "readings" in result
    assert len(result["readings"]) == 3