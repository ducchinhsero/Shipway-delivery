/**
 * Event Bus for Micro-Frontend Communication
 * Services communicate through CustomEvents, không import trực tiếp
 */

class EventBus {
  constructor() {
    this.events = new Map();
  }

  /**
   * Subscribe to an event
   * @param {string} eventName - Event name
   * @param {Function} callback - Callback function
   * @returns {Function} Unsubscribe function
   */
  on(eventName, callback) {
    const handler = (e) => callback(e.detail);
    
    if (!this.events.has(eventName)) {
      this.events.set(eventName, []);
    }
    
    this.events.get(eventName).push({ callback, handler });
    document.addEventListener(eventName, handler);

    // Return unsubscribe function
    return () => {
      this.off(eventName, callback);
    };
  }

  /**
   * Unsubscribe from an event
   * @param {string} eventName - Event name
   * @param {Function} callback - Callback function
   */
  off(eventName, callback) {
    if (!this.events.has(eventName)) return;

    const listeners = this.events.get(eventName);
    const index = listeners.findIndex(l => l.callback === callback);
    
    if (index > -1) {
      const { handler } = listeners[index];
      document.removeEventListener(eventName, handler);
      listeners.splice(index, 1);
    }
  }

  /**
   * Emit an event
   * @param {string} eventName - Event name
   * @param {any} data - Event data
   */
  emit(eventName, data) {
    const event = new CustomEvent(eventName, {
      detail: data,
      bubbles: true,
      cancelable: true
    });
    document.dispatchEvent(event);
  }

  /**
   * Subscribe to event once
   * @param {string} eventName - Event name
   * @param {Function} callback - Callback function
   * @returns {Function} Unsubscribe function
   */
  once(eventName, callback) {
    const unsubscribe = this.on(eventName, (data) => {
      callback(data);
      unsubscribe();
    });
    return unsubscribe;
  }
}

// Export singleton instance
export const eventBus = new EventBus();

// Auth Events
export const AUTH_EVENTS = {
  LOGIN_SUCCESS: 'auth:login:success',
  LOGIN_FAILED: 'auth:login:failed',
  REGISTER_SUCCESS: 'auth:register:success',
  REGISTER_FAILED: 'auth:register:failed',
  LOGOUT: 'auth:logout',
  TOKEN_EXPIRED: 'auth:token:expired',
  USER_UPDATED: 'auth:user:updated'
};
