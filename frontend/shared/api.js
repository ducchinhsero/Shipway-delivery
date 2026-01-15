/**
 * Shared API Service
 * Centralized API communication
 */

import { authStore } from './auth-store.js';

const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api/v1',
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/auth/login',
      REGISTER: '/auth/register',
      SEND_OTP: '/auth/send-otp',
      VERIFY_OTP: '/auth/verify-otp',
      RESET_PASSWORD: '/auth/reset-password'
    }
  }
};

/**
 * Make HTTP request to backend API
 */
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  // Add auth token if available
  const token = authStore.getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    method: options.method || 'GET',
    headers,
    ...options
  };

  // Add body if present
  if (options.body) {
    config.body = JSON.stringify(options.body);
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      const error = new Error(data.message || 'Request failed');
      error.statusCode = response.status;
      throw error;
    }

    return data;
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};

/**
 * Login API
 */
export const login = async (phone, password) => {
  return await apiRequest(API_CONFIG.ENDPOINTS.AUTH.LOGIN, {
    method: 'POST',
    body: { phone, password }
  });
};

/**
 * Register API
 */
export const register = async (data) => {
  return await apiRequest(API_CONFIG.ENDPOINTS.AUTH.REGISTER, {
    method: 'POST',
    body: data
  });
};

/**
 * Send OTP API
 */
export const sendOTP = async (phone, purpose = 'register') => {
  return await apiRequest(API_CONFIG.ENDPOINTS.AUTH.SEND_OTP, {
    method: 'POST',
    body: { phone, purpose }
  });
};

/**
 * Verify OTP API
 */
export const verifyOTP = async (phone, otp, purpose = 'register') => {
  return await apiRequest(API_CONFIG.ENDPOINTS.AUTH.VERIFY_OTP, {
    method: 'POST',
    body: { phone, otp, purpose }
  });
};

/**
 * Reset Password API
 */
export const resetPassword = async (phone, otp, newPassword) => {
  return await apiRequest(API_CONFIG.ENDPOINTS.AUTH.RESET_PASSWORD, {
    method: 'POST',
    body: { phone, otp, newPassword }
  });
};

export { API_CONFIG };
