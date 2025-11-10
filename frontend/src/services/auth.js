import api from './api';

export const register = async (userData) => {
  const response = await api.post('/auth/register/', userData);
  const { access, refresh, user } = response.data;

  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
  localStorage.setItem('user', JSON.stringify(user));

  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post('/auth/login/', { username, password });
  const { access, refresh } = response.data;

  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);

  // Get user info
  const userResponse = await api.get('/auth/me/');
  localStorage.setItem('user', JSON.stringify(userResponse.data));

  return response.data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  window.location.href = '/login';
};

export const getAuthToken = () => {
  return localStorage.getItem('access_token');
};

export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};
