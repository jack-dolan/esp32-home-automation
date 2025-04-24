import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the router components to avoid routing issues
jest.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Routes: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Route: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Outlet: () => <div data-testid="outlet"></div>
}));

// Mock the page components
jest.mock('./pages/Dashboard', () => () => <div>Dashboard</div>);
jest.mock('./pages/Devices', () => () => <div>Devices</div>);
jest.mock('./pages/Settings', () => () => <div>Settings</div>);
jest.mock('./pages/Login', () => () => <div>Login</div>);
jest.mock('./components/Layout/MainLayout', () => ({ children }: { children: React.ReactNode }) => <div>MainLayout {children}</div>);

test('renders app without crashing', () => {
  render(<App />);
  // just check if the app renders without crashing
  expect(document.body).toBeInTheDocument();
});