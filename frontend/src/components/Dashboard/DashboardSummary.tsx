import React from 'react';
import { Device } from '../../services/deviceService';

interface DashboardSummaryProps {
  devices: Device[];
}

const DashboardSummary: React.FC<DashboardSummaryProps> = ({ devices }) => {
  return (
    <div className="dashboard-summary">
      <h2>System Summary</h2>
      <div className="stats">
        <div className="stat-item">
          <h3>Total Devices</h3>
          <p>{devices.length}</p>
        </div>
        <div className="stat-item">
          <h3>Online Devices</h3>
          <p>{devices.filter(device => device.status === 'online').length}</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardSummary;