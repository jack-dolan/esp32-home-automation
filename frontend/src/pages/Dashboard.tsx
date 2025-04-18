import React, { useEffect, useState } from 'react';
import DashboardSummary from '../components/Dashboard/DashboardSummary';
import TemperatureChart from '../components/Temperature/TemperatureChart';
import { getDevices, Device } from '../services/deviceService';

const Dashboard: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const data = await getDevices();
        setDevices(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching devices:', error);
        setLoading(false);
      }
    };

    fetchDevices();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Home Automation Dashboard</h1>
      <DashboardSummary devices={devices} />
      <div className="dashboard-charts">
        <TemperatureChart />
      </div>
    </div>
  );
};

export default Dashboard;