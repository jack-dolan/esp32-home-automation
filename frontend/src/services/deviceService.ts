import api from './api';

export interface Device {
  id: string;
  name: string;
  type: 'temperature' | 'thermostat' | 'blind';
  status: 'online' | 'offline';
  lastReading?: number;
  lastUpdated: string;
}

export const getDevices = async (): Promise<Device[]> => {
  const response = await api.get('/devices');
  return response.data;
};

export const getDeviceById = async (id: string): Promise<Device> => {
  const response = await api.get(`/devices/${id}`);
  return response.data;
};

export const controlDevice = async (id: string, action: string, value?: any) => {
  const response = await api.post(`/devices/${id}/control`, { action, value });
  return response.data;
};