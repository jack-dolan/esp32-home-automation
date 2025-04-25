import boto3
from datetime import datetime
import logging
import os
from typing import List, Optional

from app.models.device import Device, DEVICE_STATUSES

class MockDatabaseService:
    """Mock implementation for local development"""
    def __init__(self):
        self.devices = []
        logging.info("Using mock database service for device management")
    
    async def get_devices(self) -> List[Device]:
        return self.devices
    
    async def get_device(self, device_id: str) -> Optional[Device]:
        for device in self.devices:
            if device.id == device_id:
                return device
        return None
    
    async def get_device_by_mac(self, mac_address: str) -> Optional[Device]:
        for device in self.devices:
            if device.mac_address == mac_address:
                return device
        return None
    
    async def create_device(self, device_data: dict) -> Device:
        device = Device(**device_data)
        self.devices.append(device)
        return device
    
    async def update_device(self, device_id: str, device_data: dict) -> Optional[Device]:
        for i, device in enumerate(self.devices):
            if device.id == device_id:
                updated_device = Device(**{**device.dict(), **device_data})
                self.devices[i] = updated_device
                return updated_device
        return None
    
    async def delete_device(self, device_id: str) -> bool:
        initial_count = len(self.devices)
        self.devices = [d for d in self.devices if d.id != device_id]
        return len(self.devices) < initial_count

class DynamoDBService:
    """AWS DynamoDB implementation for prod"""
    def __init__(self, table_name: str = "Devices"):
        self.table_name = table_name
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_REGION", "us-east-1"))
            self.table = self.dynamodb.Table(self.table_name)
            logging.info(f"Using AWS DynamoDB service for device management: {self.table_name}")
        except Exception as e:
            logging.error(f"Error connecting to DynamoDB: {e}")
            raise
    
    async def get_devices(self) -> List[Device]:
        response = self.table.scan()
        return [Device(**item) for item in response.get('Items', [])]
    
    async def get_device(self, device_id: str) -> Optional[Device]:
        response = self.table.get_item(Key={'id': device_id})
        item = response.get('Item')
        return Device(**item) if item else None
    
    async def get_device_by_mac(self, mac_address: str) -> Optional[Device]:
        # This is not efficient for DynamoDB but works for small datasets
        # For production, we'll use a global secondary index on mac_address I hope :)
        response = self.table.scan(
            FilterExpression="mac_address = :mac",
            ExpressionAttributeValues={":mac": mac_address}
        )
        items = response.get('Items', [])
        return Device(**items[0]) if items else None
    
    async def create_device(self, device_data: dict) -> Device:
        device = Device(**device_data)
        self.table.put_item(Item=device.dict())
        return device
    
    async def update_device(self, device_id: str, device_data: dict) -> Optional[Device]:
        # Get current device
        device = await self.get_device(device_id)
        if not device:
            return None
        
        # Create update expression
        update_expression = "set "
        expression_attribute_values = {}
        
        for key, value in device_data.items():
            if key != 'id':
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
        
        # Remove trailing comma and space
        update_expression = update_expression[:-2]
        
        if expression_attribute_values:
            self.table.update_item(
                Key={'id': device_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        
        # Return updated device
        return await self.get_device(device_id)
    
    async def delete_device(self, device_id: str) -> bool:
        try:
            self.table.delete_item(Key={'id': device_id})
            return True
        except Exception as e:
            logging.error(f"Error deleting device {device_id}: {e}")
            return False

# Create the appropriate database service based on environment
use_mock_db = os.getenv("USE_MOCK_DB", "true").lower() == "true"
db_service = MockDatabaseService() if use_mock_db else DynamoDBService()