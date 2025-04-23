import boto3
from datetime import datetime, timedelta
from app.core.config import settings
import os
import logging

class MockDynamoDBService:
    """Mock implementation for local development"""
    def __init__(self):
        self.devices = []
        self.temperature_readings = []
        logging.info("Using Mock DynamoDB Service")
    
    async def get_devices(self):
        return self.devices
    
    async def get_device(self, device_id):
        for device in self.devices:
            if device.get('id') == device_id:
                return device
        return None
    
    async def create_device(self, device_data):
        self.devices.append(device_data)
        return device_data
    
    async def update_device(self, device_id, device_data):
        for i, device in enumerate(self.devices):
            if device.get('id') == device_id:
                self.devices[i].update(device_data)
                return self.devices[i]
        return None
    
    async def delete_device(self, device_id):
        self.devices = [d for d in self.devices if d.get('id') != device_id]
        return {"success": True}
    
    async def get_temperature_readings(self, device_id, hours=24):
        return [r for r in self.temperature_readings if r.get('device_id') == device_id]
    
    async def create_temperature_reading(self, reading_data):
        self.temperature_readings.append(reading_data)
        return reading_data

class DynamoDBService:
    def __init__(self):
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
            self.devices_table = self.dynamodb.Table(settings.DYNAMODB_TABLE_DEVICES)
            self.temperature_table = self.dynamodb.Table(settings.DYNAMODB_TABLE_TEMPERATURES)
            logging.info("Using AWS DynamoDB Service")
        except Exception as e:
            logging.error(f"Error connecting to DynamoDB: {e}")
            raise
    
    # Device methods
    async def get_devices(self):
        response = self.devices_table.scan()
        return response.get('Items', [])
    
    async def get_device(self, device_id):
        response = self.devices_table.get_item(Key={'id': device_id})
        return response.get('Item')
    
    async def create_device(self, device_data):
        self.devices_table.put_item(Item=device_data)
        return device_data
    
    async def update_device(self, device_id, device_data):
        update_expression = "set "
        expression_attribute_values = {}
        
        for key, value in device_data.items():
            if key != 'id':
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
        
        # Remove trailing comma and space
        update_expression = update_expression[:-2]
        
        self.devices_table.update_item(
            Key={'id': device_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        # Return updated item
        return await self.get_device(device_id)
    
    async def delete_device(self, device_id):
        self.devices_table.delete_item(Key={'id': device_id})
        return {"success": True}
    
    # Temperature methods
    async def get_temperature_readings(self, device_id, hours=24):
        start_time = datetime.now() - timedelta(hours=hours)
        start_timestamp = int(start_time.timestamp())
        
        response = self.temperature_table.query(
            KeyConditionExpression="device_id = :device_id AND #ts >= :start_time",
            ExpressionAttributeNames={"#ts": "timestamp"},
            ExpressionAttributeValues={
                ":device_id": device_id,
                ":start_time": start_timestamp
            }
        )
        
        return response.get('Items', [])
    
    async def create_temperature_reading(self, reading_data):
        # Convert datetime to timestamp for DynamoDB
        if isinstance(reading_data['timestamp'], datetime):
            reading_data['timestamp'] = int(reading_data['timestamp'].timestamp())
        
        self.temperature_table.put_item(Item=reading_data)
        return reading_data

# Determine which service to use based on environment
use_mock = settings.USE_MOCK_DB
db_service = MockDynamoDBService() if use_mock else DynamoDBService()