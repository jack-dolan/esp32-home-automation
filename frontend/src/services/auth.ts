import api from './api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface AuthResponse {
  token: string;
  user: {
    id: string;
    username: string;
  };
}

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  const response = await api.post('/auth/login', credentials);
  const { token, user } = response.data;
  
  // Store token in localStorage
  localStorage.setItem('token', token);
  
  return { token, user };
};

export const logout = (): void => {
  localStorage.removeItem('token');
};

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('token');
};