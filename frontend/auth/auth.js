/**
 * Auth Service - Business Logic
 * Xử lý login, register, OTP, reset password
 * Không import service khác, chỉ import shared API
 */

import * as api from '../shared/api.js';
import { authStore } from '../shared/auth-store.js';
import { eventBus, AUTH_EVENTS } from '../shared/event-bus.js';

/**
 * Login user with phone and password
 */
export const loginUser = async (phone, password) => {
  try {
    const response = await api.login(phone, password);

    // Save token and user data to store
    if (response.token) {
      authStore.setToken(response.token);
      authStore.setUser(response.user);
    }

    // Emit success event for other services
    eventBus.emit(AUTH_EVENTS.LOGIN_SUCCESS, {
      user: response.user,
      token: response.token
    });

    return response;
  } catch (error) {
    // Emit failed event
    eventBus.emit(AUTH_EVENTS.LOGIN_FAILED, {
      error: error.message
    });
    throw error;
  }
};

/**
 * Register new user
 */
export const registerUser = async ({ phone, name, password, role = 'user', otp }) => {
  try {
    const response = await api.register({
      phone,
      name,
      password,
      role,
      otp
    });

    // Save token and user data to store
    if (response.token) {
      authStore.setToken(response.token);
      authStore.setUser(response.user);
    }

    // Emit success event
    eventBus.emit(AUTH_EVENTS.REGISTER_SUCCESS, {
      user: response.user,
      token: response.token
    });

    return response;
  } catch (error) {
    // Emit failed event
    eventBus.emit(AUTH_EVENTS.REGISTER_FAILED, {
      error: error.message
    });
    throw error;
  }
};

/**
 * Send OTP to phone number
 */
export const sendOtp = async (phone, opts = {}) => {
  try {
    const { purpose = 'register' } = opts;
    
    const response = await api.sendOTP(phone, purpose);

    // Log OTP to console for development
    if (response.otp) {
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('📱 MÃ OTP ĐÃ ĐƯỢC GỬI');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`   Số điện thoại: ${phone}`);
      console.log(`   🔐 Mã OTP: ${response.otp}`);
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    }

    return response;
  } catch (error) {
    throw error;
  }
};

/**
 * Verify OTP
 */
export const verifyOtp = async (phone, otp, purpose = 'register') => {
  try {
    const response = await api.verifyOTP(phone, otp, purpose);
    return response;
  } catch (error) {
    throw error;
  }
};

/**
 * Reset password
 */
export const resetPassword = async (phone, otp, newPassword) => {
  try {
    const response = await api.resetPassword(phone, otp, newPassword);
    return response;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout user
 */
export const logout = () => {
  authStore.clear();
  eventBus.emit(AUTH_EVENTS.LOGOUT, {});
};

/**
 * Get current user
 */
export const getCurrentUser = () => {
  return authStore.getUser();
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return authStore.isAuth();
};
