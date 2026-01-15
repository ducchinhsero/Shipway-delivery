/**
 * Centralized Auth Store
 * Quản lý trạng thái authentication
 */

const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth:token',
  USER_DATA: 'auth:user',
  IS_AUTHENTICATED: 'auth:isAuthenticated'
};

class AuthStore {
  constructor() {
    this.token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN) || null;
    this.user = this.parseUserData();
    this.isAuthenticated = !!this.token;
  }

  /**
   * Get user data from localStorage
   */
  parseUserData() {
    const userData = localStorage.getItem(STORAGE_KEYS.USER_DATA);
    return userData ? JSON.parse(userData) : null;
  }

  /**
   * Set auth token
   */
  setToken(token) {
    this.token = token;
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
    this.isAuthenticated = !!token;
  }

  /**
   * Get auth token
   */
  getToken() {
    return this.token;
  }

  /**
   * Set user data
   */
  setUser(user) {
    this.user = user;
    localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
  }

  /**
   * Get user data
   */
  getUser() {
    return this.user;
  }

  /**
   * Clear auth data (logout)
   */
  clear() {
    this.token = null;
    this.user = null;
    this.isAuthenticated = false;
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER_DATA);
  }

  /**
   * Check if user is authenticated
   */
  isAuth() {
    return this.isAuthenticated && !!this.token;
  }

  /**
   * Get user role
   */
  getUserRole() {
    return this.user?.role || null;
  }

  /**
   * Check if user has specific role
   */
  hasRole(role) {
    return this.user?.role === role;
  }
}

// Export singleton instance
export const authStore = new AuthStore();
