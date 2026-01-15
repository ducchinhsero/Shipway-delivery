/**
 * Authentication Guard - Protect pages from unauthorized access
 * Usage: Include this script FIRST in any protected page
 */

import { authStore } from './auth-store.js';

class AuthGuard {
  constructor() {
    this.authStore = authStore;
  }

  /**
   * Check if user is authenticated
   * Redirect to login if not authenticated
   */
  requireAuth(redirectUrl = '../auth/index.html') {
    if (!this.authStore.isAuthenticated()) {
      console.warn('[AuthGuard] User not authenticated, redirecting to login');
      window.location.href = redirectUrl;
      return false;
    }
    return true;
  }

  /**
   * Check if user has required role
   * @param {string|string[]} allowedRoles - Single role or array of roles
   * @param {string} redirectUrl - Where to redirect if unauthorized
   */
  requireRole(allowedRoles, redirectUrl = '../auth/index.html') {
    if (!this.requireAuth(redirectUrl)) {
      return false;
    }

    const user = this.authStore.getUser();
    const roles = Array.isArray(allowedRoles) ? allowedRoles : [allowedRoles];

    if (!roles.includes(user.role)) {
      console.warn(`[AuthGuard] User role "${user.role}" not in allowed roles:`, roles);
      alert('Bạn không có quyền truy cập trang này');
      window.location.href = redirectUrl;
      return false;
    }

    return true;
  }

  /**
   * Get current user info
   */
  getCurrentUser() {
    return this.authStore.getUser();
  }

  /**
   * Check if user is a specific role
   */
  isUser() {
    const user = this.authStore.getUser();
    return user && user.role === 'user';
  }

  isDriver() {
    const user = this.authStore.getUser();
    return user && user.role === 'driver';
  }

  isAdmin() {
    const user = this.authStore.getUser();
    return user && user.role === 'admin';
  }

  /**
   * Logout and redirect
   */
  logout(redirectUrl = '../auth/index.html') {
    this.authStore.logout();
    window.location.href = redirectUrl;
  }
}

// Export singleton instance
export const authGuard = new AuthGuard();

// Auto-protect pages that include this script with data-protected attribute
document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  
  // Check if page requires authentication
  if (body.hasAttribute('data-protected')) {
    const requiredRole = body.getAttribute('data-required-role');
    
    if (requiredRole) {
      authGuard.requireRole(requiredRole);
    } else {
      authGuard.requireAuth();
    }
    
    console.log('[AuthGuard] Page protected, user:', authGuard.getCurrentUser());
  }
});
