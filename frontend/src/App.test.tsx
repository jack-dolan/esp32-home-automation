import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

// // Mock react-router-dom components
// jest.mock('react-router-dom', () => ({
//   BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
//   Routes: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
//   Route: () => <div />,
//   Outlet: () => <div />
// }));

// Mock the components used in App
jest.mock('./pages/Dashboard', () => () => <div>Dashboard</div>);
jest.mock('./pages/Devices', () => () => <div>Devices</div>);
jest.mock('./pages/Settings', () => () => <div>Settings</div>);
jest.mock('./pages/Login', () => () => <div>Login</div>);
jest.mock('./components/Layout/MainLayout', () => () => <div>MainLayout</div>);

test('renders without crashing', () => {
  render(<App />);
  // The test passes if rendering doesn't throw an error
  expect(true).toBeTruthy();
});