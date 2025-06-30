// API utility functions for VitaPink BloodBank
const API_BASE_URL = 'http://localhost:5000';

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` })
  };
};

// Helper function to handle API responses
const handleResponse = async (response) => {
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || 'An error occurred');
  }
  
  return data;
};

// Authentication API calls
export const authAPI = {
  // Login user
  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    
    return handleResponse(response);
  },

  // Register user
  register: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    
    return handleResponse(response);
  },

  // Get user profile
  getProfile: async () => {
    const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    
    return handleResponse(response);
  },

  // Refresh token
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${refreshToken}`
      }
    });
    
    return handleResponse(response);
  },

  // Logout user
  logout: async () => {
    const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    
    // Clear local storage regardless of API response
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    return handleResponse(response);
  }
};

// User management API calls
export const userAPI = {
  // Update user profile
  updateProfile: async (profileData) => {
    const response = await fetch(`${API_BASE_URL}/api/users/profile`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData)
    });
    
    return handleResponse(response);
  },

  // Change password
  changePassword: async (passwordData) => {
    const response = await fetch(`${API_BASE_URL}/api/users/change-password`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(passwordData)
    });
    
    return handleResponse(response);
  },

  // Update eligibility status
  updateEligibility: async (eligibilityData) => {
    const response = await fetch(`${API_BASE_URL}/api/users/eligibility`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(eligibilityData)
    });
    
    return handleResponse(response);
  },

  // Deactivate account
  deactivateAccount: async () => {
    const response = await fetch(`${API_BASE_URL}/api/users/deactivate`, {
      method: 'PUT',
      headers: getAuthHeaders()
    });
    
    return handleResponse(response);
  },

  // Update active status for donation
  updateActiveStatus: async (activeData) => {
    const response = await fetch(`${API_BASE_URL}/api/users/active-status`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(activeData)
    });
    
    return handleResponse(response);
  }
};

// General API calls
export const generalAPI = {
  // Health check
  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(response);
  },

  // Get API info
  getApiInfo: async () => {
    const response = await fetch(`${API_BASE_URL}/`);
    return handleResponse(response);
  }
};

// Helper functions for auth state management
export const authUtils = {
  // Check if user is logged in
  isLoggedIn: () => {
    return !!localStorage.getItem('access_token');
  },

  // Get current user from localStorage
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Clear all auth data
  clearAuthData: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  // Store auth data
  storeAuthData: (data) => {
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }
    if (data.refresh_token) {
      localStorage.setItem('refresh_token', data.refresh_token);
    }
    if (data.user) {
      localStorage.setItem('user', JSON.stringify(data.user));
    }
  }
}; 