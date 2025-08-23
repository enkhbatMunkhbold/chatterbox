// API Configuration
export const API_BASE_URL = 'http://localhost:5000';

// Helper function to make API calls
export const apiCall = (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  return fetch(url, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
};
