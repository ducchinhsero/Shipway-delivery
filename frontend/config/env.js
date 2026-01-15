// Determine environment based on hostname
const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';

// API Configuration
export const API_CONFIG = {
  // Backend API URL - Auto-detect based on environment
  BASE_URL: isProduction 
    ? 'https://apishipway.lpwanmapper.com/api/v1'  // Production
    : 'http://localhost:8000/api/v1',              // Development
  
  // Environment
  ENV: isProduction ? 'production' : 'development',
  
  // Timeout settings
  TIMEOUT: 30000, // 30 seconds
  
  // Endpoints
  ENDPOINTS: {
    // Auth
    SEND_OTP: '/auth/send-otp',
    VERIFY_OTP: '/auth/verify-otp',
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    RESET_PASSWORD: '/auth/reset-password',
    GET_ME: '/auth/me',
    
    // Users
    GET_PROFILE: '/user/profile',
    UPDATE_PROFILE: '/user/profile',
    GET_USERS: '/user',
    UPDATE_DRIVER_INFO: '/user/driver/info',
    
    // Subscription & Credits
    GET_SUBSCRIPTION: '/subscription/plan',
    UPDATE_SUBSCRIPTION: '/subscription/plan',
    GET_CREDIT: '/subscription/credit',
    UPDATE_CREDIT: '/subscription/credit'
  }
};

// Storage keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'shipway_token',
  USER_DATA: 'shipway_user',
  REMEMBER_ME: 'shipway_remember'
};

export default API_CONFIG;

