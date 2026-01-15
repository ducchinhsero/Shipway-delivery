/**
 * Auth Controller - UI Logic
 * Xử lý DOM events, form validation, UI updates
 */

import {
  loginUser,
  registerUser,
  sendOtp,
  verifyOtp,
  resetPassword,
  logout,
  getCurrentUser,
  isAuthenticated
} from './auth.js';

import { eventBus, AUTH_EVENTS } from '../shared/event-bus.js';

/**
 * Initialize Auth Service
 */
export function initAuthService() {
  initLogin();
  initRegister();
  initResetPassword();
  setupEventListeners();
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
  // Listen for login success from other services
  eventBus.on(AUTH_EVENTS.LOGIN_SUCCESS, (data) => {
    console.log('User logged in:', data.user);
  });

  // Listen for logout from other services
  eventBus.on(AUTH_EVENTS.LOGOUT, () => {
    console.log('User logged out');
    redirectToLogin();
  });

  // Listen for token expired
  eventBus.on(AUTH_EVENTS.TOKEN_EXPIRED, () => {
    console.log('Token expired, please login again');
    logout();
    redirectToLogin();
  });
}

/* ================= LOGIN ================= */

function initLogin() {
  const form = document.getElementById('loginForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    form.classList.add('submitted');

    const msg = document.getElementById('loginMessage');
    clearMessage(msg);

    if (!form.checkValidity()) {
      showMessage(msg, 'Vui lòng nhập đầy đủ thông tin', 'error');
      form.querySelector(':invalid').focus();
      return;
    }

    const phone = document.getElementById('loginPhone').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    const countryCode = document.getElementById('loginCountry')?.value || '+84';
    const fullPhone = phone.startsWith('+') ? phone : `${countryCode}${phone}`;

    // Show loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Đang xử lý...';
    submitBtn.disabled = true;

    try {
      const response = await loginUser(fullPhone, password);
      showMessage(msg, response.message || 'Đăng nhập thành công', 'success');

      // Redirect based on role
      setTimeout(() => {
        const user = response.user;
        if (user.role === 'admin') {
          window.location.href = '/admin/dashboard.html';
        } else if (user.role === 'driver') {
          window.location.href = '/driver/dashboard.html';
        } else {
          window.location.href = '/user/dashboard.html';
        }
      }, 1000);
    } catch (err) {
      showMessage(msg, err.message || 'Đăng nhập thất bại', 'error');
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });

  // Handle forgot password link
  const forgotLink = document.getElementById('forgotLink');
  if (forgotLink) {
    forgotLink.addEventListener('click', (e) => {
      e.preventDefault();
      showResetPassword();
    });
  }
}

/* ================= REGISTER ================= */

function initRegister() {
  const form = document.getElementById('registerForm');
  if (!form) return;

  const phone = document.getElementById('regPhone');
  const otpInput = document.getElementById('regOtpInput');
  const sendOtpBtn = document.getElementById('sendOtpBtn');
  const otpSection = document.getElementById('otpSection');
  const msg = document.getElementById('registerMessage');

  let otpSent = false;

  sendOtpBtn.addEventListener('click', async () => {
    clearMessage(msg);

    if (!phone.value.trim()) {
      showMessage(msg, 'Vui lòng nhập số điện thoại', 'error');
      phone.focus();
      return;
    }

    // Show loading
    const originalText = sendOtpBtn.textContent;
    sendOtpBtn.textContent = 'Đang gửi...';
    sendOtpBtn.disabled = true;

    try {
      const countryCode = document.getElementById('regCountry')?.value || '+84';
      const fullPhone = phone.value.trim().startsWith('+')
        ? phone.value.trim()
        : `${countryCode}${phone.value.trim()}`;

      await sendOtp(fullPhone, { purpose: 'register' });
      otpSent = true;
      phone.disabled = true;
      otpSection.classList.remove('hidden');
      sendOtpBtn.textContent = 'Gửi lại mã';
      showMessage(msg, 'Mã OTP đã được gửi', 'success');
    } catch (err) {
      showMessage(msg, err.message || 'Gửi OTP thất bại', 'error');
      sendOtpBtn.textContent = originalText;
      sendOtpBtn.disabled = false;
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    form.classList.add('submitted');

    clearMessage(msg);

    if (!form.checkValidity()) {
      showMessage(msg, 'Vui lòng nhập đầy đủ thông tin', 'error');
      form.querySelector(':invalid').focus();
      return;
    }

    if (!otpSent) {
      showMessage(msg, 'Vui lòng gửi mã OTP trước', 'error');
      return;
    }

    const phoneValue = phone.value.trim();
    const countryCode = document.getElementById('regCountry')?.value || '+84';
    const fullPhone = phoneValue.startsWith('+') ? phoneValue : `${countryCode}${phoneValue}`;
    const name = document.getElementById('regName').value.trim();
    const password = document.getElementById('regPassword').value.trim();
    const otp = otpInput.value.trim();
    const role = document.querySelector('input[name="role"]:checked')?.value || 'user';

    // Show loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Đang xử lý...';
    submitBtn.disabled = true;

    try {
      const response = await registerUser({
        phone: fullPhone,
        name,
        password,
        otp,
        role
      });

      showMessage(msg, response.message || 'Đăng ký thành công', 'success');

      setTimeout(() => {
        window.location.href = '/user/dashboard.html';
      }, 1000);
    } catch (err) {
      showMessage(msg, err.message || 'Đăng ký thất bại', 'error');
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

/* ================= RESET PASSWORD ================= */

function initResetPassword() {
  const form = document.getElementById('resetForm');
  if (!form) return;

  const phone = document.getElementById('resetPhone');
  const otpInput = document.getElementById('resetOtpInput');
  const sendOtpBtn = document.getElementById('resetSendOtpBtn');
  const otpSection = document.getElementById('resetOtpSection');
  const msg = document.getElementById('resetMessage');

  let otpSent = false;

  sendOtpBtn.addEventListener('click', async () => {
    clearMessage(msg);

    if (!phone.value.trim()) {
      showMessage(msg, 'Vui lòng nhập số điện thoại', 'error');
      phone.focus();
      return;
    }

    const originalText = sendOtpBtn.textContent;
    sendOtpBtn.textContent = 'Đang gửi...';
    sendOtpBtn.disabled = true;

    try {
      const countryCode = document.getElementById('resetCountry')?.value || '+84';
      const fullPhone = phone.value.trim().startsWith('+')
        ? phone.value.trim()
        : `${countryCode}${phone.value.trim()}`;

      await sendOtp(fullPhone, { purpose: 'reset-password' });
      otpSent = true;
      phone.disabled = true;
      otpSection.classList.remove('hidden');
      sendOtpBtn.textContent = 'Gửi lại mã';
      showMessage(msg, 'Mã OTP đã được gửi', 'success');
    } catch (err) {
      showMessage(msg, err.message || 'Gửi OTP thất bại', 'error');
      sendOtpBtn.textContent = originalText;
      sendOtpBtn.disabled = false;
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    form.classList.add('submitted');

    clearMessage(msg);

    if (!form.checkValidity()) {
      showMessage(msg, 'Vui lòng nhập đầy đủ thông tin', 'error');
      form.querySelector(':invalid').focus();
      return;
    }

    if (!otpSent) {
      showMessage(msg, 'Vui lòng gửi mã OTP trước', 'error');
      return;
    }

    const phoneValue = phone.value.trim();
    const countryCode = document.getElementById('resetCountry')?.value || '+84';
    const fullPhone = phoneValue.startsWith('+') ? phoneValue : `${countryCode}${phoneValue}`;
    const otp = otpInput.value.trim();
    const newPassword = document.getElementById('resetPassword').value.trim();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Đang xử lý...';
    submitBtn.disabled = true;

    try {
      const response = await resetPassword(fullPhone, otp, newPassword);
      showMessage(msg, response.message || 'Đặt lại mật khẩu thành công', 'success');

      setTimeout(() => {
        showLogin();
      }, 1000);
    } catch (err) {
      showMessage(msg, err.message || 'Đặt lại mật khẩu thất bại', 'error');
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

/* ================= UI HELPERS ================= */

/**
 * Show message in form
 */
function showMessage(element, message, type = 'info') {
  if (!element) return;
  element.textContent = message;
  element.className = `form-message ${type}`;
}

/**
 * Clear message
 */
function clearMessage(element) {
  if (!element) return;
  element.textContent = '';
  element.className = 'form-message';
}

/**
 * Show login view
 */
function showLogin() {
  const loginView = document.getElementById('loginView');
  const registerView = document.getElementById('registerView');
  const resetView = document.getElementById('resetView');

  if (loginView) loginView.classList.remove('hidden');
  if (registerView) registerView.classList.add('hidden');
  if (resetView) resetView.classList.add('hidden');
}

/**
 * Show register view
 */
function showRegister() {
  const loginView = document.getElementById('loginView');
  const registerView = document.getElementById('registerView');
  const resetView = document.getElementById('resetView');

  if (loginView) loginView.classList.add('hidden');
  if (registerView) registerView.classList.remove('hidden');
  if (resetView) resetView.classList.add('hidden');
}

/**
 * Show reset password view
 */
function showResetPassword() {
  const loginView = document.getElementById('loginView');
  const registerView = document.getElementById('registerView');
  const resetView = document.getElementById('resetView');

  if (loginView) loginView.classList.add('hidden');
  if (registerView) registerView.classList.add('hidden');
  if (resetView) resetView.classList.remove('hidden');
}

/**
 * Redirect to login
 */
function redirectToLogin() {
  window.location.href = '/';
}

// Export functions for global use
window.showRegister = showRegister;
window.showLogin = showLogin;
window.showResetPassword = showResetPassword;
