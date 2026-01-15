/* =========================================================
   ONBOARDING - Main Script
   Integrated with real auth system
========================================================= */

import { authStore } from '../shared/auth-store.js';

/* =========================================================
   INIT APP
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  updateHeaderByAuth();
  setupActiveMenu();
});

/* =========================================================
   AUTH STATE - Using Real Auth System
========================================================= */
function updateHeaderByAuth() {
  const nav = document.querySelector(".main-nav ul");
  if (!nav) return;

  // Check if user is logged in (using real auth)
  if (!authStore.isAuthenticated()) {
    // Not logged in - show login/register buttons (already in HTML)
    return;
  }

  // User is logged in - show dashboard and logout
  const user = authStore.getUser();
  const dashboardUrl = user.role === 'driver' 
    ? '../driver/dashboard/index.html'
    : '../user/dashboard/index.html';

  nav.innerHTML = `
    <li><a href="#top" class="active">Trang chủ</a></li>
    <li><a href="#about">Về chúng tôi</a></li>
    <li><a href="${dashboardUrl}" class="btn-primary">Dashboard</a></li>
    <li><button class="btn-outline" id="logoutBtn">Đăng xuất</button></li>
  `;

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
  }
}

function logout() {
  // Use real auth logout
  authStore.logout();
  window.location.reload();
}

/* =========================================================
   ACTIVE MENU
========================================================= */
function setupActiveMenu() {
  const links = document.querySelectorAll(".main-nav a");
  
  links.forEach(link => {
    if (link.href === window.location.href) {
      link.classList.add("active");
    }
  });
}
