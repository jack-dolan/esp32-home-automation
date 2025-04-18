import React from 'react';
import { Device, controlDevice } from '../../services/deviceService';

interface DeviceControlPanelProps {
  device: Device;
}

const DeviceControlPanel: React.FC<DeviceControlPanelProps> = ({ device }) => {
  const handleToggle = async () => {
    try {
      await controlDevice(device.id, 'toggle');
      // In a real app, you would update the device state here
    } catch (error) {
      console.error('Error controlling device:', error);
    }
  };

  return (
    <div className="device-control-panel">
      <h3>{device.name}</h3>
      <p>Status: {device.status}</p>
      <button onClick={handleToggle}>Toggle Device</button>
    </div>
  );
};

export default DeviceControlPanel;